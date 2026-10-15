# V34 — reconstruction et tests

Depuis la racine du dépôt :

```sh
python3 tools/v34/audit_v34.py --rom '/chemin/original.sfc' --out '/chemin/audit.json'
python3 tools/v34/build_v34.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' V34_OUT=patches python3 -m unittest discover -s tools/v34 -p 'test_v34*.py' -v
```

Sans ROM, la CI exécute :

```sh
python3 -m unittest discover -s tools/v34 -p test_v34_offline.py -v
```

Les deux IPS sont autonomes et s'appliquent directement à la ROM originale USA 1.2, jamais par-dessus V33. Le constructeur vérifie l'empreinte de la source et de V33. Les 87 ajouts sont limités aux fragments source encore intacts, non occupés et sans pointeur intérieur, dans 62 scripts référencés dont les commandes et pointeurs d'entrée sont préservés.

Ce lot est un nettoyage en place : aucune relocalisation ni nouvelle réécriture de pointeur n'est effectuée en V34. Le langage des singes, les noms propres et les cris sans contenu linguistique restent volontairement intacts et ne sont pas comptés. Les tests préservent les espacements autour des noms, objets et montants dynamiques et contrôlent les encodages accents et ASCII.

[Rapport, périmètre et limites](../../RAPPORT_V34.md). Sources françaises dans `translations_v34.tsv`, provenance complète des scripts dans `v34_dialogues_fr.json`.
