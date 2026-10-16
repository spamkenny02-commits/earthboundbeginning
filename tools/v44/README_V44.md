# V44 — dialogues et correction des entrées contiguës

93 nouvelles occurrences de fragments (85 anglais distincts), réparties entre 46 scripts de messages et six routines grammaticales privées. Les sept lettres de huées ajustées et les 13 ajustements non lexicaux sont exclus. Les 12 choix Yes/No restent inchangés.

```sh
python tools/v44/build_v44.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python tools/v44/run_regressions.py
python -m unittest discover -s tools/v44 -p test_v44_offline.py -v
```

`translations_v44.json` contient les traductions ; `v44_dialogues_fr.json` documente les sources, les références et les routines privées. `validation_v44.json` conserve les implantations et empreintes des deux profils, les 14 réparations V43 et les exceptions de pointeurs antérieurs.

Le placement par longueur conserve une correspondance pour les octets strictement intérieurs aux sources. **La fin exclusive d'un script ne doit jamais remplacer l'entrée du script source suivant.** Les tests contrôlent l'identité des entrées et reproduisent le cas de deux scripts contigus alloués dans l'ordre inverse.

Les réparations V43 sont dérivées de ses sources et de son implantation, confrontées au pointeur de la ROM d'origine et au pointeur effectif de la base V43. Les 14 changements ont une preuve de commande ou de champ de table. Les routines françaises restent privées : leurs anciennes références globales ne sont pas redirigées.

181 tests locaux, dont 23 V44 ; six tests hors ROM pour GitHub. Les limites de la validation visuelle figurent dans le [rapport Snes9x](../../tests/emulation_v44/RAPPORT_EMULATION_V44.md). Consulter aussi le [rapport de version](../../RAPPORT_V44.md).
