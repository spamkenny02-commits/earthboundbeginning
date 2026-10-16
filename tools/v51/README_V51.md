# Reconstruction et contrôles V51

Les 28 candidats proviennent des segments reportés par V49/V50. `candidates_v51.json` contient leur texte français. Le constructeur régénère `v51_fixtures.json`, les réserves, les deux IPS et les empreintes ; il ne fait pas confiance aux anciens indicateurs `can_jump` des candidats, conservés pour traçabilité.

```sh
python tools/v51/build_v51.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v51/run_regressions.py
python -m unittest discover -s tools/v51 -p test_v51_offline.py -v
```

335 tests locaux, dont 18 V51 (neuf hors ROM et neuf avec ROM). La CI exécute les neuf contrôles hors ROM. Le chemin `ROM_PATH` doit être absolu car les suites historiques s'exécutent dans leur propre dossier.

Le constructeur valide les frontières dans les contextes V50 complets, refuse les adresses intérieures dans le préfixe réécrit et garde les queues sources. Les tests suivent explicitement les nouveaux sauts et comparent les autres commandes des contextes ; ils ne simulent pas les branches du moteur. Aucun pointeur extérieur n'est réécrit. Les méthodes heuristiques d'audit de V50 ne servent pas d'autorisation.

Les fichiers JSON générés et les IPS sont nécessaires aux contrôles hors ROM. Les scripts historiques sont conservés tels quels. Voir [RAPPORT_V51.md](../../RAPPORT_V51.md).
