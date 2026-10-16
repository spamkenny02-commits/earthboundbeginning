# Reconstruction et contrôles V54

`candidates_v54.json` sélectionne 85 blocs de définitions de menus. Le constructeur compare les octets et les frontières des libellés dans les contextes V53 complets ; les deux variantes doivent présenter les définitions attendues. Il génère les copies françaises, fixtures, IPS et empreintes.

```sh
python tools/v54/build_v54.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v54/run_regressions.py
python -m unittest discover -s tools/v54 -p test_v54_offline.py -v
python tools/v54/discover_menus.py --rom /chemin/original.sfc --out /chemin/inventaire.json
```

407 tests locaux, dont 21 V54 (11 hors ROM et 10 avec ROM). La CI exécute les 11 contrôles hors ROM. `ROM_PATH` doit être absolu car les suites historiques changent de dossier.

Les copies contiennent uniquement des définitions de deux ou trois options suivies d'un saut vers le sélecteur original. Le contrôle logique suit les nouveaux sauts et compare toutes les autres commandes. Les entrées intérieures et leurs sites de références restent inchangés ; les tests valident explicitement les deux profils, les 85 copies et les 87 contextes.

L'inventaire est une aide au repérage, pas une preuve de présence naturelle en jeu. `discovery_audit_v54.json` conserve les chemins des contextes retenus et les groupes non sélectionnés. Les listes de destinations avec contrôles de mise en page et les menus de débogage restent hors de ce lot. Les essais natifs vérifient 14 scénarios par variante et comparent leurs résultats avec V53. Voir [RAPPORT_V54.md](../../RAPPORT_V54.md).
