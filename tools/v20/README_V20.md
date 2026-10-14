# V20 française — patchs IPS autonomes

V20 ajoute **160 segments** français à la V19 locale validée. Les deux patchs IPS finaux se trouvent dans `patches/` et s'appliquent **directement** à la ROM originale USA 1.2 sans en-tête (SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`). N'appliquez pas V18 ou V19 avant V20.

La ROM commerciale n'est pas incluse. La base publiée sur GitHub est V18 Work ; les sources et patchs V19 nécessaires sont fournis localement dans ce paquet pour permettre une reconstruction reproductible de V20.

Depuis la racine du paquet :

```sh
python3 tools/v20/build_v20.py --rom '/chemin/ROM_USA_1.2.sfc' --out build_v20
ROM_PATH='/chemin/ROM_USA_1.2.sfc' V20_OUT="$PWD/build_v20" python3 -m unittest discover -s tools/v20 -p test_v20.py -v
```

Sources éditables : `tools/v20/translations_v20.tsv`. Métadonnées : `tools/v20/v20_dialogues_fr.json`. Vérifications : `tools/v20/test_v20.py`, `tools/v20/validation_v20.json` et `RAPPORT_V20.md`.

**État : validée structurellement sur ROM originale, non testée sous émulateur, non publiée sur GitHub.**
