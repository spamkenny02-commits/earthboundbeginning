# V24 — plages de texte avec provenance de script

Depuis la racine du dépôt:

```sh
python3 tools/v24/audit_v24.py --rom '/chemin/original.sfc' --out build_v24/audit.json
python3 tools/v24/build_v24.py --rom '/chemin/original.sfc' --out build_v24
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v24 -p test_v24.py -v
```

Les IDs TSV sont les offsets des premiers octets de texte; ne pas ajouter 1. Conserver les outils V19, le décodeur `traduction/preparer_v17.py`, le catalogue complet et les IPS V23. Le constructeur préserve les espaces source autour des commandes. Consulter `RAPPORT_V24.md` pour les limites. Appliquer un seul IPS autonome V24 directement à la ROM originale USA 1.2.
