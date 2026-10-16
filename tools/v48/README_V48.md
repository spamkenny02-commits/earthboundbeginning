# Construction V48

40 scripts principaux, quatre routines grammaticales privées, 66 occurrences lexicales traduites et deux corrections de contexte `Anyone` → `Chacun`. Voir le [rapport](../../RAPPORT_V48.md) pour le détail et les limites.

```sh
python tools/v48/build_v48.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v48/run_regressions.py
python -m unittest discover -s tools/v48 -p test_v48_offline.py -v
```

ROM USA 1.2 requise : 4 194 304 octets, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`. Les IPS sont autonomes depuis cet original. Aucune ROM fournie.

- `translations_v48.json` : traductions par segment.
- `v48_dialogues_fr.json` : instantanés sources, appels et références préservées, corrections de contexte.
- `validation_v48.json` : empreintes, implantations et opérandes réécrits.
- `build_v48.py` : validation des sources, réserves, allocation par premier espace suffisant, relocalisation des commandes et contrôles de différences.

Les routines privées `07E5F3`, `07E5FE`, `07E6C5`, `07E6D1` gèrent `il`, `elle`, `Monsieur`, `Madame` uniquement pour les nouvelles copies concernées. Les sources et leurs autres appels ne changent pas. Les copies françaises V44 `07E602` et V45 `07E74E` sont réutilisées à leurs adresses publiées.

272 tests locaux réussis, dont 25 V48. La CI V48 exécute huit tests sans ROM. La reconstruction des ROM et les comparaisons de commandes utilisent également le lecteur IPS indépendant des tests V38. Le cas d'épuisement, la réutilisation d'une réserve partiellement remplie, les frontières contiguës et le rejet d'un alias textuel intérieur ont des tests dédiés.
