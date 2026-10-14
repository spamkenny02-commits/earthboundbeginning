# Construire V21

Depuis la racine du dépôt:

```sh
python3 tools/v21/build_v21.py --rom '/chemin/original.sfc' --out build_v21
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v21 -p test_v21.py -v
```

Lire `RAPPORT_V21.md` pour les limites. Les sources V19 et les IPS V20 doivent rester présents pour reconstruire cette version autonome.
