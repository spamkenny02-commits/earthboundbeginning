# Construire et vérifier V29

Depuis la racine du dépôt :

```sh
python3 tools/v29/build_v29.py --rom '/chemin/original.sfc' --out '/chemin/patches'
python3 -m unittest discover -s tools/v29 -p test_v29_offline.py -v
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v29 -p 'test_v29*.py' -v
```

Le constructeur refuse une source différente, une V28 différente, une réserve occupée, des références supplémentaires ou des textes appelants modifiés. Les tests hors ROM vérifient les IPS publiés et interprètent les octets des deux routines. Les tests ROM utilisent une application IPS indépendante et comparent tous les octets hors plages autorisées.

Les deux routines, trois destinations et cinq fragments français sont déclarés dans `build_v29.py`. [Rapport et limites](../../RAPPORT_V29.md).
