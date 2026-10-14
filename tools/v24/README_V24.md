# V24 — textes multisegments (expérimental)

63 nouvelles traductions sont décrites dans `translations_v24.tsv` et `manifest_v24.json`. Le constructeur lit le catalogue d'extraction `atelier/extraction/dialogues.json`, vérifie le SHA-256 de la ROM originale et de l'IPS V23, contrôle les références HiROM du script parent, les collisions, l'encodage et les commandes, puis produit deux IPS autonomes.

```sh
python3 tools/v24/build_v24.py --rom '/chemin/ROM_originale.sfc' --out build_v24
ROM_PATH='/chemin/ROM_originale.sfc' python3 -m unittest discover -s tools/v24 -p test_v24.py -v
```

Voir `RAPPORT_V24.md` pour les limites et les tests réellement effectués. Ne jamais distribuer de ROM commerciale.