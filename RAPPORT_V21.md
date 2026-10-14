# EarthBound Beginnings FR — V21 Work

Reprise du 14 octobre 2026 depuis l'archive V20 retrouvée. Aucune sauvegarde EarthBound V21 annoncée précédemment n'a été retrouvée; ses compteurs ne sont pas repris.

## Résultats

- 153 nouveaux segments intégrés sur ROM originale vérifiée, deux profils autonomes (accents et ASCII).
- 119 ajouts V19 et 160 ajouts V20 conservés: 432 ajouts depuis V18 Work.
- 10 tests V21, 10 tests V20, 15 tests V19 et 10 tests V18 Work réussis, sans tests ignorés. Les premières exécutions des tests hérités ont nécessité de corriger leurs chemins de sortie; les exécutions finales passent.
- Commandes, frontières, encodage, longueurs, références HiROM littérales, pointeurs intérieurs et collisions contrôlés.
- Enregistrements V20 conservés, aucun changement hors des plages V21; aller-retour IPS vérifié avec un interpréteur indépendant.
- Snes9x 1.63: 339 commandes accents, 337 commandes ASCII, 25 803 images simulées par profil. Titre, introduction, après combat, restauration d'état et menu identiques aux références V18.

Les textes couvrent les trains, Magicant, l'école, l'usine Duncan, le mont Itoi et les appels familiaux. Des formulations sont abrégées pour les emplacements fixes. Les scripts multisegments peuvent rester partiellement anglais.

## Limites

Le parcours Snes9x couvre le début du jeu. Les 153 nouveaux segments dans les zones ultérieures et la sauvegarde native ne sont pas testés. Les pointeurs indirects, les textes compressés et les graphismes anglais restent à traiter. Les deux pointeurs invalidés hérités de V18 restent exclus. Aucun graphisme VICTOIRE n'est ajouté.

## Utilisation

Appliquer un seul IPS V21 directement à la ROM originale USA 1.2 sans en-tête, sans préinstaller les anciennes versions. SHA-256 source: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v21/build_v21.py --rom '/chemin/original.sfc' --out build_v21
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v21 -p test_v21.py -v
```

Sources éditables: `tools/v21/translations_v21.tsv`. Métadonnées: `tools/v21/v21_dialogues_fr.json`. Résultats: `tools/v21/validation_v21.json`, `tests/emulation_v21/results.json`. Aucune ROM incluse.

## Publication

Le blocage initial de publication a été suivi d'une autorisation explicite de publier V21 sur main et de fusionner toutes les branches. Les branches v17-preparation, v17-preparation-audit et v17-preparation-ci sont désormais intégrées à l'historique de main. Les outils et la CI sont conservés; les anciens rapports sont identifiés comme historiques. Aucun fichier ROM n'est suivi par Git.
