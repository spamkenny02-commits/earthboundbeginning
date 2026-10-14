# EarthBound Beginnings FR — V27

Lot du 14 octobre 2026, depuis V26 publiée sur `main` (commit `8d4f3d8235f3be1e4208138dd850d8290bf35b0f`).

## Résultats

- **176 nouvelles plages de texte français dans 124 scripts**, deux IPS autonomes (accents et ASCII) reconstruits en ajoutant les nouvelles plages à tous les enregistrements de V26.
- Scènes de retour, commerces et équipements, hôtels et banque, panneaux directionnels, appels téléphoniques et répliques secondaires.
- **1 466 ajouts depuis V18 Work** (1 290 publiés jusqu'à V26 + 176 V27). Il s'agit de plages distinctes modifiées, pas de dialogues complets ni de phrases uniques. Les répétitions à plusieurs adresses sont comptées séparément.
- 180 traductions ont franchi les premiers filtres; **4 ont été écartées** parce que des enregistrements IPS antérieurs recouvrent leurs références littérales. 91 autres propositions du premier lot ont été écartées car des pointeurs littéraux visent l'intérieur de leurs plages. Aucun brouillon n'est compté.

## Contrôles effectivement exécutés

- ROM originale USA 1.2 (4 Mio) vérifiée localement, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- **176/176** plages anglaises vérifiées sur la ROM par empreinte des octets; **124/124** scripts parents complets vérifiés de la même manière, y compris les commandes.
- **181 références littérales HiROM** dans ces 124 scripts: concordance exacte entre les références extraites et celles relevées directement dans la ROM; aucune référence littérale interne aux 176 plages retenues.
- Les deux IPS V26 publiés ont été lus intégralement; conservation de leurs enregistrements, absence de collision avec les 176 plages, longueurs et glyphes vérifiés dans les deux profils.
- Aller-retour IPS **sur mémoire synthétique** pour les deux profils, conservation de tous les octets hors des ajouts et absence de régression des enregistrements V26. Ceci n'est **pas** un roundtrip sur la ROM complète.
- Les traductions de `tools/v27/translations_v27.tsv` correspondent au manifeste `v27_dialogues_fr.json`; commandes et espaces aux frontières conservés sans déplacement des adresses.

| Profil | Enregistrements V26 | Ajouts V27 | Total | SHA-256 IPS V27 |
|---|---:|---:|---:|---|
| Accents | 5 373 | 176 | 5 549 | `b48cbe0373f36408d545f8b0ad82e664725d0cf7877fb11c72668135593a27c6` |
| ASCII | 5 268 | 176 | 5 444 | `298d3bb4c54b6f1db62e835e952a095b99f69aec80296d92b022092dbbe9011a` |

## Limites de validation

Le roundtrip **intégral** des IPS V27 sur la ROM originale n'a pas été exécuté dans un environnement réunissant le dépôt et la ROM. Les tests Python V27 sur ROM et les essais V27 en émulateur **ne sont pas effectués**. Le parcours du début de V26 ne constitue pas une validation des nouvelles scènes V27. L'audit de sécurité se limite aux pointeurs HiROM littéraux et aux commandes reconnues; pointeurs indirects, textes compressés, graphismes anglais et rendu de dialogues partiellement traduits restent à vérifier.

## Reconstruction et utilisation

Appliquer **un seul IPS V27 directement à la ROM originale USA 1.2**, sans superposer V26. Aucun fichier ROM commercial n'est distribué. Pour reconstruire et vérifier complètement sur une ROM personnelle :

```sh
python3 tools/v27/audit_v27.py --rom '/chemin/original.sfc' --out build_v27/audit.json
python3 tools/v27/build_v27.py --rom '/chemin/original.sfc' --out build_v27
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v27 -p test_v27.py -v
python3 -m unittest discover -s tools/v27 -p test_v27_offline.py -v
```

La publication inclut les deux IPS autonomes, les sources, le manifeste, les tests et les empreintes. Les validations intégrales non réalisées doivent rester explicitement marquées comme telles jusqu'à exécution.
