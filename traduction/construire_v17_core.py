#!/usr/bin/env python3
"""V17: construire deux IPS autonomes depuis V16, ROM originale et traductions.

Préconditions: Python 3; depuis la racine du dépôt; manifeste audité V17
(v17_candidats_controles.json) et sauvegarde V17 des traductions disponibles.
Ce script ne distribue jamais de ROM et refuse les ambiguïtés de décodage.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'traduction'))
from construire_v11 import ROM_SHA, encode, apply_ips, parse_ips
from construire_v14 import spans_for_entry

ROM_SIZE = 4 * 1024 * 1024
SPLIT = re.compile(r'(\[[0-9A-Fa-f ]+\]|\n|@)')


def merge_sources(candidates, translations):
    """Rapproche par ID, jamais par index; exclut les brouillons et les absents."""
    if candidates.get('base') != 'v16' or translations.get('base') != 'v16':
        raise ValueError('Base V16 requise')
    refs = {e['id']: e for e in candidates['entries']}
    if len(refs) != len(candidates['entries']):
        raise ValueError('IDs candidats dupliqués')
    items = translations['entries']
    if len({e['id'] for e in items}) != len(items):
        raise ValueError('IDs de traductions dupliqués')
    merged = []
    for t in items:
        ident = t['id']
        if ident not in refs or t.get('status') not in ('traduit_non_integre', 'integre_v17'):
            raise ValueError('Traduction hors audit / statut invalide : ' + ident)
        c = refs[ident]
        if not c.get('pointer_refs_declared'):
            raise ValueError('Aucun pointeur déclaré : ' + ident)
        merged.append({'id': ident, 'english': c['english'],
                       'translations': t['translations'],
                       'pointer_refs': c['pointer_refs_declared']})
    return merged


def derive_mask(source, start, english):
    """Détermine le masque des retours 00 / 03 00 à partir de la ROM.

    Ne choisit pas arbitrairement si plusieurs reconstructions correspondent.
    """
    choices = {(start, 0)}
    newline_index = 0
    for part in filter(None, SPLIT.split(english)):
        nxt = set()
        if part == '\n':
            for pos, mask in choices:
                for raw, short in ((b'\x00', True), (b'\x03\x00', False)):
                    if source[pos:pos + len(raw)] == raw:
                        nxt.add((pos + len(raw), mask | ((1 << newline_index) if short else 0)))
            newline_index += 1
        else:
            if part == '@':
                raw = b'\x70'
            elif part.startswith('[') and part.endswith(']'):
                raw = bytes.fromhex(part[1:-1])
            else:
                if any(not 32 <= ord(ch) <= 122 or ch in '[]' for ch in part):
                    raise ValueError('Caractère anglais non encodable')
                raw = bytes(ord(ch) + 48 for ch in part)
            if not raw:
                raise ValueError('Commande vide')
            nxt = {(pos + len(raw), mask) for pos, mask in choices
                   if source[pos:pos + len(raw)] == raw}
        choices = nxt
        if not choices:
            raise ValueError(f'Source ROM différente au script {start:06X}')
    if len(choices) != 1:
        raise ValueError(f'Layout ambigu au script {start:06X}: {len(choices)} variantes')
    return next(iter(choices))[1]


def literal_refs(source, targets):
    """Retourne les références HiROM 24 bits avec octet de poids fort nul."""
    found = {t: [] for t in targets}
    for at in range(len(source) - 3):
        if source[at + 3] == 0 and 0xC0 <= source[at + 2] <= 0xFF:
            target = int.from_bytes(source[at:at + 4], 'little') - 0xC00000
            if target in found:
                found[target].append(at)
    return found


def validate_and_spans(source, entries):
    if len(source) != ROM_SIZE or hashlib.sha256(source).hexdigest() != ROM_SHA:
        raise ValueError('ROM USA 1.2 originale 4 Mio, SHA-256 requis')
    if not entries or len({e['id'] for e in entries}) != len(entries):
        raise ValueError('Aucune entrée ou doublons')
    spans, ranges, refs_to_check = [], [], {}
    for e in entries:
        start = int(e['id'], 16)
        e['newline_one_byte_mask'] = derive_mask(source, start, e['english'])
        at, raw, edits = spans_for_entry(e)
        if source[at:at + len(raw)] != raw:
            raise ValueError('Script source modifié : ' + e['id'])
        ranges.append((at, at + len(raw), e['id']))
        if not edits:
            continue
        if not e['pointer_refs']:
            raise ValueError('Pointeurs absents : ' + e['id'])
        for p in e['pointer_refs']:
            ptr_at = int(p, 16)
            if source[ptr_at:ptr_at + 4] != (0xC00000 + at).to_bytes(4, 'little'):
                raise ValueError('Référence HiROM incorrecte : ' + e['id'] + ' / ' + p)
        for pos, english, fr, ident in edits:
            for profile in (True, False):
                if len(encode(fr, profile)) > len(english):
                    raise ValueError('Texte trop long : ' + ident)
        spans.extend(edits)
        refs_to_check[at] = e['id']
    ranges.sort()
    for a, b in zip(ranges, ranges[1:]):
        if a[1] > b[0]:
            raise ValueError('Scripts chevauchants : ' + a[2] + ' / ' + b[2])
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if a[0] + len(a[1]) > b[0]:
            raise ValueError('Segments chevauchants : ' + a[3] + ' / ' + b[3])
    interiors = {pos + j for pos, english, _, _ in spans for j in range(1, len(english))}
    targets = interiors | set(refs_to_check)
    refs = literal_refs(source, targets)
    for target in interiors:
        if refs[target]:
            raise ValueError(f'Pointeur intérieur dangereux vers {target:06X}, depuis {refs[target][0]:06X}')
    for start, ident in refs_to_check.items():
        if not refs[start]:
            raise ValueError('Aucun pointeur littéral : ' + ident)
    return spans, refs


