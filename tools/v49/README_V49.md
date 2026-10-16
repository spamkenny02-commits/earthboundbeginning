# Construction V49

207 fragments lexicaux et quatre ajustements non lexicaux, dédoublonnés dans 84 contextes. Les traductions sont réinsérées dans les plages anglaises existantes ; aucun déplacement de script ou de commande. Voir le [rapport](../../RAPPORT_V49.md).

```sh
python tools/v49/build_v49.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v49/run_regressions.py
python -m unittest discover -s tools/v49 -p test_v49_offline.py -v
```

ROM originale USA 1.2 requise : 4 194 304 octets, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

- `contexts_v49.json` : entrées auditées et exclusions.
- `translations_v49.json` : traductions proposées, associées au fragment anglais exact. Certaines propositions sont reportées par le contrôle d'adresse intérieure ; ce fichier n'est pas le décompte des intégrations.
- `v49_fixtures.json` : plages réellement modifiées, instantanés des contextes et segments reportés.
- `validation_v49.json` : décompte réel et empreintes des IPS et ROM cibles.

La capacité et la segmentation sont vérifiées sur les deux variantes V48. Une cible de pointeur littéral à l'intérieur d'une plage interdit son édition. Les segments communs à plusieurs contextes sont écrits une fois. Le texte français déjà présent et les commandes sont préservés ; les espaces de complément conservent les longueurs.

292 tests locaux, dont 20 V49. La CI exécute les huit tests sans ROM. Les tests avec ROM nécessitent l'original privé ; les essais Snes9x nécessitent également le cœur et les états privés indiqués dans le rapport d'émulation.
