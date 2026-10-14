# EarthBound Beginnings FR — V23

Lot du 14 octobre 2026, depuis V22 publiée sur main (`dd96b3d`).

## Résultats

- **120 nouveaux segments** français intégrés dans deux IPS autonomes: accents et ASCII.
- Hôtels et tarifs, commerces, soins, banque, canari, service Escargo Express et indices du journal.
- 10 tests V23 et 10 tests V22 réussis, sans tests ignorés.
- Source anglaise, suffixes de commande, frontières, encodage, longueurs et références HiROM littérales contrôlés sur la ROM originale USA 1.2; aucun pointeur littéral intérieur dans les nouvelles plages.
- Absence de collision, conservation de V22 et de tous les octets hors des 120 ajouts; aller-retour indépendant des deux IPS.
- Snes9x 1.63: parcours du début du jeu conforme aux cinq écrans de référence dans les deux profils, 339 commandes accents et 337 ASCII, 25 803 images simulées par profil.
- **737 ajouts depuis V18 Work**: V19 119, V20 160, V21 153, V22 185, V23 120. Ces nombres comptent les segments modifiés, pas les scripts complets ni les phrases uniques.

Les formulations sont parfois abrégées pour les emplacements fixes. Les nouveaux segments restent à vérifier visuellement dans leurs zones. Le parcours émulateur contrôle le début du jeu; il ne constitue pas un parcours complet.

## Utilisation et reconstruction

Appliquer un seul IPS V23 directement à la ROM originale USA 1.2 sans en-tête, sans préinstaller V22. SHA-256 source: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v23/build_v23.py --rom '/chemin/original.sfc' --out build_v23
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v23 -p test_v23.py -v
```

Sources éditables, manifeste, empreintes et exclusions dans `tools/v23/`. Captures, historique et outil de rejeu dans `tests/emulation_v23/`. Aucun fichier ROM distribué.

## Suite et limites

Le sous-catalogue de 913 segments utilisé depuis V18 Work ne laisse plus que **21 candidats présélectionnés non intégrés**, documentés dans `exclusions_v23.json`: rires inchangés, diagnostics de transaction, texte de développement et deux fragments ambigus. Ce n'est pas le compte de textes restant à traduire dans le jeu. La suite nécessite un audit du catalogue plus large et des autres formats.

Les pointeurs indirects, les textes compressés, les scripts multisegments partiels, la sauvegarde native et les graphismes anglais (dont YOU WON) restent à traiter.
