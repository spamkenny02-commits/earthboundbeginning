# V25 — reconstruction et tests

Depuis la racine du dépôt:

```sh
python3 tools/v25/build_v25.py --rom '/chemin/original.sfc' --out build_v25
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v25 -p test_v25.py -v
python3 -m unittest discover -s tools/v25 -p test_v25_offline.py -v
```

Les IDs TSV pointent vers le premier octet de texte, sans @. Conserver les helpers V19, le décodeur de layout V17, le catalogue complet et les IPS V24 consolidés. Appliquer un seul IPS autonome V25 directement à la ROM originale USA 1.2. Voir `RAPPORT_V25.md` pour les exclusions et limites.
