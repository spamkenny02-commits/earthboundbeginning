# V43 — textes de combat et de services

56 scripts, 102 nouvelles occurrences (91 fragments anglais distincts). Les 12 ajustements de ponctuation et les 52 fragments neutres conservés sont exclus du compteur. Les textes du menu restent pour leur passe dédiée.

`translations_v43.json` contient les traductions. `v43_dialogues_fr.json` conserve les sources, les plages textuelles, le dictionnaire utilisé et les preuves des références. `validation_v43.json` indique les implantations, les empreintes des IPS et ROM cibles et les exceptions de pointeurs antérieurs.

```sh
python tools/v43/build_v43.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python -m unittest discover -s tools/v43 -p 'test_v43*.py' -v
ROM_PATH='/chemin/original.sfc' python tools/v43/run_regressions.py
```

Le constructeur accepte les scripts avec ou sans compression par dictionnaire. Il développe les tokens anglais uniquement dans les copies françaises et alloue les copies les plus longues en premier. Il vérifie les réserves, les sources et tous les opérandes redirigés. Les références intérieures non prouvées restent intactes. Les IPS sont autonomes sur la ROM originale USA 1.2.

Les suites locales totalisent 158 tests, dont 17 V43. Le workflow GitHub ne reçoit aucune ROM : ses cinq tests hors ROM vérifient les empreintes et reconstruisent les ajouts à partir des sources documentées.

Consulter [le rapport V43](../../RAPPORT_V43.md) et [les essais Snes9x](../../tests/emulation_v43/RAPPORT_EMULATION_V43.md). Les références binaires ne suffisent pas à établir l'accessibilité de chaque action en jeu ; les nouvelles scènes ne sont pas toutes validées visuellement.
