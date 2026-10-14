# EarthBound Beginnings FR — V22

Lot du 14 octobre 2026, depuis V21 publiée sur main (`fc3fe12`).

## Résultats

- **185 nouveaux segments** traduits et intégrés dans deux IPS autonomes: accents et ASCII.
- Dialogues de fin de jeu, commerces, Snowman, Youngtown, désert Yucca, canari et Téléportation.
- 10 tests V22 et 10 tests de régression V21 réussis, sans tests ignorés.
- Vérification sur la ROM originale USA 1.2: source anglaise, suffixes de commande, frontières, encodage, longueurs, pointeurs HiROM explicites et intérieurs, collisions.
- Conservation exacte des enregistrements V21 et des octets hors des 185 nouvelles plages; aller-retour indépendant des deux IPS.
- Essais Snes9x du début du jeu réussis dans les deux profils (voir `tests/emulation_v22/`).
- **617 ajouts depuis V18 Work**: V19 119, V20 160, V21 153, V22 185. Ces chiffres sont des segments modifiés, pas des scripts entiers ni des phrases uniques; des textes identiques apparaissent à plusieurs emplacements.

Les libellés de débogage et les fragments sans modification réelle ne sont pas inclus. Les formulations ont parfois été abrégées pour rester dans les emplacements fixes.

## Utilisation et reconstruction

Appliquer un seul IPS V22 directement à la ROM originale USA 1.2 sans en-tête; ne pas préinstaller V21. SHA-256 original: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v22/build_v22.py --rom '/chemin/original.sfc' --out build_v22
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v22 -p test_v22.py -v
```

Les traductions éditables sont dans `tools/v22/translations_v22.tsv`; manifeste et empreintes dans le même dossier. Aucun fichier ROM distribué.

## Limites et suite

Les nouveaux segments des zones ultérieures ne sont pas validés visuellement en jeu. Les pointeurs indirects, les textes compressés, la sauvegarde native et les graphismes anglais (dont YOU WON) restent à traiter. Les scripts multisegments peuvent rester partiellement anglais.

Après ce lot, 141 candidats du catalogue de 913 restent hors des plages déjà modifiées et passent la présélection conservatrice; ce n'est ni un compte de dialogues restants ni une preuve de traduction possible (ce groupe contient aussi des libellés techniques et des fragments identiques).
