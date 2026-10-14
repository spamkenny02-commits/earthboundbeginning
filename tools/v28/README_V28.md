# V28 — reconstruction et validation

Base : V27 publiée sur main. **49 nouvelles plages** dans 49 scripts, dont des scripts à branchements et commandes hors du décodeur V27 des scripts complets.

Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s tools/v28 -p test_v28_offline.py -v
ROM_PATH='/chemin/ROM_originale.sfc' python3 -m unittest discover -s tools/v28 -p test_v28_rom.py -v
python3 tools/v28/build_v28.py --rom '/chemin/ROM_originale.sfc' --out build_v28
```

La ROM USA 1.2 sans en-tête est requise pour les contrôles complets. Le constructeur vérifie son empreinte, les préfixes de scripts et commandes, les pointeurs littéraux, l'encodage, les collisions, le roundtrip et la régression V27. Les tests hors ROM ne sont pas des tests d'émulateur.

Les IPS V28 sont **autonomes** : appliquer une seule variante à la ROM originale, jamais par-dessus V27. Aucune ROM n'est distribuée.
