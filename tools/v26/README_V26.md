# V26 — reconstruction et tests

Depuis la racine du dépôt:

```sh
python3 tools/v26/build_v26.py --rom '/chemin/original.sfc' --out build_v26
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v26 -p test_v26.py -v
python3 -m unittest discover -s tools/v26 -p test_v26_offline.py -v
```

Les IDs TSV pointent vers le premier octet de texte. Conserver les helpers V19, le décodeur V17, le catalogue complet et les IPS V25. Appliquer un seul IPS autonome V26 directement à la ROM originale USA 1.2. Voir `RAPPORT_V26.md` pour les limites.
