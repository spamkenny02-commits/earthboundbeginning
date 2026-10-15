# V33 — reconstruction et contrôles

Depuis la racine du dépôt :

```sh
python3 tools/v33/build_v33.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v33 -p 'test_v33*.py' -v
python3 -m unittest discover -s tools/v33 -p test_v33_offline.py -v
```

Les listes françaises `dialogues_fr.json` suivent les fragments du script source. Les espaces autour des noms, objets et montants dynamiques sont explicites. Les copies peuvent grandir ; aucun espace de remplissage n'est ajouté. Les commandes et leurs frontières sont conservées, hormis les opérandes de pointeurs déclarés et remappés.

Les références entrantes incluent désormais les appels prouvés par le parseur dans les copies V31/V32 connues. Le constructeur exige le jeu exact de références, identique dans les deux profils. Les références vers les entrées principales présentes dans les anciens scripts protégés ne sont pas réécrites. Seule leur copie active est raccordée lorsque son opérande est prouvé. Les scripts anciens et alias restent intacts.

Les IPS V32, la ROM source, les réserves nulles, les écritures précédentes et les références HiROM sont contrôlés avant construction. Les fixtures `v33_dialogues_fr.json` contiennent les plages originales protégées et la provenance des appels antérieurs vérifiés. Les 14 tests couvrent aussi V31/V32 et boy/girl. [Rapport et limites](../../RAPPORT_V33.md).
