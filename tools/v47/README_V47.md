# Construction V47

21 scripts, 34 occurrences lexicales traduites (28 textes anglais distincts), quatre ajustements non lexicaux. Les deux choix Yes/No sont conservés. Les patchs sont autonomes depuis la ROM originale USA 1.2 ; ne pas les empiler sur V46.

```sh
python tools/v47/build_v47.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v47/run_regressions.py
python -m unittest discover -s tools/v47 -p test_v47_offline.py -v
```

La ROM doit avoir l'empreinte SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c` et mesurer 4 194 304 octets. Elle n'est pas incluse.

`translations_v47.json` contient les traductions ; `v47_dialogues_fr.json` conserve les segments sources, appels prouvés et références non prouvées ; `validation_v47.json` consigne les implantations et empreintes. Le constructeur réutilise le parseur historique et la transformation V33 avec protection des frontières de scripts. Les tests appliquent aussi les IPS avec un lecteur indépendant et comparent les commandes et textes décodés.

247 tests locaux : 229 historiques et 18 V47. La CI V47 exécute les six tests sans ROM. Voir le [rapport général](../../RAPPORT_V47.md) pour les essais d'émulation et leurs limites.
