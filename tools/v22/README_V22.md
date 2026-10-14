# V22 — constructeur portable

Depuis la racine du dépôt:

```sh
python3 tools/v22/build_v22.py --rom '/chemin/original.sfc' --out build_v22
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v22 -p test_v22.py -v
```

Appliquer un seul IPS autonome V22 à la ROM originale USA 1.2. Conserver les sources V19, le catalogue V18 Work et les IPS V21 nécessaires au constructeur. Consulter `RAPPORT_V22.md` pour les contrôles et limites.
