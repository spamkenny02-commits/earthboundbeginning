# V45 — fermeture des dépendances d'inventaire

20 nouvelles occurrences de fragments (18 anglais distincts), six messages et sept sous-routines privées. Les six ajustements non lexicaux et les choix de menus conservés sont exclus du compteur.

```sh
python tools/v45/build_v45.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python tools/v45/run_regressions.py
python -m unittest discover -s tools/v45 -p test_v45_offline.py -v
```

`translations_v45.json` contient les traductions. `v45_dialogues_fr.json` conserve `original_hex` et `baseline_hex` : leurs seules différences autorisées sont les deux opérandes prouvés déjà raccordés en V44 dans le dialogue de sélection d'objet. Le champ `source_pointer_updates_preserved` documente ces différences. Toute modification textuelle ou de commande hors opérande est rejetée.

`validation_v45.json` indique les implantations, les empreintes et les références. Les copies sont allouées sans confondre fin exclusive et début du script suivant. Les sous-routines de groupe, y compris le retour vide partagé, restent privées ; les références anglaises existantes ne sont pas globalement redirigées.

207 tests locaux, dont 26 V45. Les six tests hors ROM sont exécutés par GitHub. Le test de commande Équiper utilise un seul octet d'inventaire de fixture ; les dialogues d'inventaire et de fuite utilisent un routage de description explicite. Consulter [le rapport Snes9x](../../tests/emulation_v45/RAPPORT_EMULATION_V45.md) et [le rapport V45](../../RAPPORT_V45.md) pour les limites.
