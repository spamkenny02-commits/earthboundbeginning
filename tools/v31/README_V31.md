# V31 — dialogues complets relocalisés

Depuis la racine du dépôt :

```sh
python3 tools/v31/build_v31.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v31 -p 'test_v31*.py' -v
python3 -m unittest discover -s tools/v31 -p test_v31_offline.py -v
```

Éditer les listes françaises dans `dialogues_fr.json`. Chaque liste suit les fragments du script anglais ; les espaces autour des noms et objets dynamiques sont explicites. Les commandes, pauses, retours et marqueurs de dialogue sont conservés. Les textes peuvent grandir et aucun espace de remplissage n'est ajouté.

Le constructeur vérifie les empreintes de la ROM et des deux IPS V30, la disposition exacte des scripts sources, les commandes V30, les références d'entrée, les réserves nulles et leur absence de références HiROM littérales et d'écritures IPS. Les cibles internes sont recalculées seulement lorsqu'une frontière de commande ou de texte est connue. Une branche dans l'intérieur d'un texte remplacé bloque la construction.

Les scripts V30 et leurs alias intérieurs restent intacts. Seules les références aux entrées principales extérieures aux scripts sélectionnés sont redirigées. Les appels et branches dans les nouvelles copies sont ajustés vers les nouvelles frontières. Les anciennes entrées secondaires restent sur les anciennes données.

Les fixtures `v31_dialogues_fr.json` permettent les contrôles hors ROM. `validation_v31.json` consigne les destinations et les écritures de pointeurs. `layout_v31.py` vérifie les octets sans limite artificielle à 12 retours : sa limite passe à 64 retours, 8 000 caractères et 512 commandes. L'audit de candidats `audit_v31.py` reste utilisable pour la suite.

[Rapport et limites](../../RAPPORT_V31.md). Les patches sont autonomes et s'appliquent directement à la ROM originale USA 1.2.
