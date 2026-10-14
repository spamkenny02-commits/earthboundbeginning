# V23 — constructeur portable

Depuis la racine du dépôt:

```sh
python3 tools/v23/build_v23.py --rom '/chemin/original.sfc' --out build_v23
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v23 -p test_v23.py -v
```

Appliquer un seul IPS V23 à la ROM originale USA 1.2. Conserver les sources V19, le catalogue V18 Work et les IPS V22 nécessaires à la construction. Lire `RAPPORT_V23.md` pour les limites.
