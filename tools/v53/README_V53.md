# Reconstruction et contrôles V53

`candidates_v53.json` décrit trois champs NPC et un court préfixe de confirmation. Les références primaires de CoilSnake y sont épinglées. Le constructeur vérifie les dix références moteur avant d'utiliser le schéma de table, puis les enregistrements et destinations des trois personnages. Il ne cherche pas une commande au voisinage d'une occurrence littérale.

```sh
python tools/v53/build_v53.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v53/run_regressions.py
python -m unittest discover -s tools/v53 -p test_v53_offline.py -v
```

386 tests locaux, dont 29 V53 (16 hors ROM et 13 avec ROM). La CI exécute les 16 contrôles hors ROM. `ROM_PATH` doit être absolu car les suites historiques changent de dossier.

Les copies NPC conservent les cibles absolues et refusent une branche pointant à l'intérieur d'un script à redimensionner. Les fins exclusives restent des destinations originales. La seule différence antérieure acceptée dans les sources est l'opérande V35 explicitement déclaré et revérifié. Le préfixe marchand utilise un saut aller/retour, indépendant des copies NPC.

`v53_fixtures.json` conserve les octets des dix références moteur, des enregistrements NPC, des sources par variante et des autres occurrences préservées. Les sources originales ne sont pas écrasées. Voir [RAPPORT_V53.md](../../RAPPORT_V53.md).
