# V56 — priorité aux textes

22 zones de texte sont reprises, soit 24 fragments : une séquence de rire comporte trois fragments séparés par des délais. Le lot comprend aussi les deux anciennes copies du message « But nothing happened. », un chuchotement, un autre rire et une suppression d'article nécessaire à la grammaire française. Ce sont des occurrences, pas 24 dialogues distincts.

Les textes sont copiés dans des réserves nulles vérifiées. Un saut de cinq octets rejoint chaque copie, puis revient avant la commande suivante. Les anciennes entrées intérieures et les délais sont conservés. Aucun menu n'est modifié. Les tests vérifient également les définitions et copies des menus V54/V55.

Reconstruction et contrôles :

```sh
python tools/v56/build_v56.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v56/run_regressions.py
python -m unittest discover -s tools/v56 -p test_v56_offline.py -v
```

`audit_texts.py` produit une liste conservatrice de textes non modifiés, hors libellés de menus, à partir d'entrées de personnages et d'actions de la V55. La liste contient aussi de l'héritage EarthBound et du débogage. Elle manque certains accès calculés et certains textes déjà déplacés ou modifiés. La présence dans la liste ne prouve pas un accès naturel, et l'absence ne prouve pas une traduction complète. Le test naturel de Télépathie a ainsi trouvé une réponse anglaise que l'audit n'avait pas remontée.

`natural_telepathy.py` reproduit le même usage normal de Télépathie dans V55/V56 sans modification de ROM ou WRAM. `display_probe.py` utilise une redirection temporaire de l'objet carte bancaire pour lire les autres textes ; `--temporal-check` échantillonne les messages éphémères. Ces essais contrôlés ne valident pas les conditions naturelles de chaque scène, les objets utilisés ou les effets des réparations.
