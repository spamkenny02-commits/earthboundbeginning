#!/usr/bin/env python3
"""Suffixes PSI natifs autorisés ; commandes de jeu interdites dans le texte FR."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'traduction'))
from integrer import encode_fr
for profile in [True,False]:
    assert encode_fr('[8B][8C][8D][8E][AB][AC][AD][AE]',profile)==bytes.fromhex('8B 8C 8D 8E AB AC AD AE')
    for command in ['[02]','[1C 0F]','[08 00 00 C0 00]']:
        try:encode_fr(command,profile)
        except ValueError:pass
        else:raise AssertionError('Commande acceptée dans un texte français')
print('Suffixes PSI préservés ; injection de commandes rejetée pour les deux variantes.')
