# EarthBound Beginnings FR — Rapport V17 (14 octobre 2026)

## Livraison

La V17 est **autonome** : appliquer un seul IPS directement sur la ROM USA 1.2 originale, sans installer V16.
Elle reprend les enregistrements IPS V09–V16 et ajoute **195 segments français réellement modifiés dans 117 scripts** (196 segments examinés ; 1 inchangé).
Trois scripts du lot de 120 restent exclus : `349CAB` (commande atypique), `34F3BE` et `34FB49` (non traduits).

- `patches/EarthBound_Beginnings_FR_v17_accents.ips` : 77 558 octets.
- `patches/EarthBound_Beginnings_FR_v17_ascii.ips` : 76 072 octets.
- Traductions : `traduction/v17_traductions_117.json`.
- Source anglaise auditée : `traduction/v17_candidats_controles.json`.
- Constructeur reproductible : `traduction/construire_v17.py` et `traduction/construire_v17_core.py`.
- Test IPS sans ROM : `tests/verifier_fusion_v17.py`.

## Vérifications effectivement réalisées

- ROM originale USA 1.2 : 4 194 304 octets, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- 117 scripts, 195/195 segments comparés octet par octet aux octets anglais originaux et contrôlés en longueur/encodage dans l'environnement local.
- 130 références HiROM littérales vers les débuts de scripts contrôlées ; aucun pointeur littéral intérieur détecté sur les 195 segments. Les pointeurs indirects ne sont pas prouvés.
- 21 tests locaux exécutés et réussis avant la fusion.
- Les véritables IPS V16 récupérés via l'API GitHub : **3 720 enregistrements (accents)** et **3 615 (ASCII)** ; les 195 nouveaux segments ne chevauchent aucun de leurs enregistrements, dans les deux profils.
- Les deux surcouches V17 de 5 885 octets ont été reproduites exactement à partir des traductions et des offsets validés (empreintes FNV-1a conformes à la sauvegarde locale).
- IPS autonomes produits par concaténation des enregistrements V16 intacts et des 195 nouveaux enregistrements, sans redistribuer la ROM.
- Tests de non-régression et roundtrip sur ROM neutre disponibles dans `tests/verifier_fusion_v17.py` ; le passage CI doit être consulté séparément.

## Limites

Pas de test d'émulateur ni de parcours de gameplay complet lors de cette livraison. Les textes compressés, les graphismes anglais et les références indirectes restent à examiner. Une vérification visuelle des dialogues longs reste nécessaire. Les patchs ont été construits et validés structurellement sans modifier la ROM commerciale distribuée ; **aucune ROM n'est incluse dans le dépôt**.

## Reproduire

```bash
python tests/verifier_fusion_v17.py
python traduction/construire_v17.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v17
```

Comparer les IPS reconstruits aux fichiers de `patches/` avant diffusion. Le constructeur vérifie la ROM source, les commandes, les références, les collisions et le roundtrip réel lorsque la ROM originale est fournie.
