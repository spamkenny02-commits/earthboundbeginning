# V32 — suite des dialogues complets

Depuis la racine du dépôt :

```sh
python3 tools/v32/build_v32.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v32 -p 'test_v32*.py' -v
python3 -m unittest discover -s tools/v32 -p test_v32_offline.py -v
```

Les listes françaises sont dans `dialogues_fr.json`, dans l'ordre des fragments du script source. Conserver les espaces explicites aux frontières des noms, objets et montants. Les textes peuvent grandir ; aucun espace de remplissage n'est ajouté aux copies. Le constructeur conserve les commandes et recalcule les références internes seulement aux frontières connues.

La source et les IPS V31 sont contrôlés par empreinte. Les scripts anciens et leurs alias sont conservés ; seules les entrées principales extérieures aux scripts sélectionnés sont redirigées. Les réserves doivent être nulles dans la source et les deux profils, sans référence HiROM littérale ni écriture IPS. La dernière partie de la deuxième réserve V31 est réutilisée à partir de `24D660`, après ses dernières copies.

Les 13 tests couvrent aussi explicitement les anciennes copies V31, leurs pointeurs d'entrée et les routines boy/girl. [Rapport et limites](../../RAPPORT_V32.md). Appliquer un seul IPS V32 directement à la ROM originale USA 1.2.
