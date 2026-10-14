# V30 — reconstruction et tests

Depuis la racine du dépôt :

```sh
python3 tools/v30/audit_v30.py --rom '/chemin/original.sfc' --out '/chemin/audit.json'
python3 tools/v30/build_v30.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' V30_OUT=patches python3 -m unittest discover -s tools/v30 -p 'test_v30*.py' -v
```

Sans ROM, la CI exécute :

```sh
python3 -m unittest discover -s tools/v30 -p test_v30_offline.py -v
```

Les deux IPS sont autonomes et s'appliquent directement à la ROM originale USA 1.2, jamais par-dessus V29. Le constructeur vérifie l'empreinte de la source et de V29. La nouvelle série est limitée aux fragments source encore intacts, non occupés et sans pointeur intérieur, dans des scripts référencés dont les commandes et pointeurs d'entrée sont préservés.

L'audit accepte désormais les fragments d'au moins trois caractères, pour intégrer les «Yes» et autres réponses brèves auparavant exclues. Aucun critère structurel n'est assoupli. Les cris de singes, noms propres et onomatopées sans traduction nécessaire restent intacts. Le possessif anglais attaché au nom dans la phrase du dragon devient une proposition française avec un espace explicite, testé au niveau de la frontière dynamique.

[Rapport, périmètre et limites](../../RAPPORT_V30.md). Sources françaises dans `translations_v30.tsv`, provenance complète des scripts dans `v30_dialogues_fr.json`.
