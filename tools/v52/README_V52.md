# Reconstruction et contrôles V52

`candidates_v52.json` contient quinze segments et leurs traductions. Le constructeur calcule les copies à partir des deux ROM V51, valide les frontières de texte et génère les fixtures, IPS et empreintes. Les fragments séparés par une attente `10` sont copiés ensemble ; aucun autre opcode interne n'est accepté.

```sh
python tools/v52/build_v52.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v52/run_regressions.py
python -m unittest discover -s tools/v52 -p test_v52_offline.py -v
```

357 tests locaux, dont 22 V52 (onze hors ROM et onze avec ROM). La CI exécute les onze contrôles hors ROM. `ROM_PATH` doit être absolu car les suites historiques changent de dossier.

`already_french_spans` distingue le préfixe conservé des nouveaux fragments. Les tests vérifient explicitement sa copie, la conservation du suffixe source et des neuf opérandes de l'appelant. Le contrôle logique suit les nouveaux sauts pour comparer les commandes ; il ne simule pas les branches du moteur. Les fichiers JSON et IPS générés sont nécessaires aux tests hors ROM. Voir [RAPPORT_V52.md](../../RAPPORT_V52.md).
