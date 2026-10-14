# EarthBound Beginnings FR — V26

Lot du 14 octobre 2026, depuis V25 publiée sur main (`18aa55f`).

## Résultats

- **175 nouvelles plages intégrées dans 105 scripts**, deux IPS autonomes accents/ASCII.
- Snowman, répliques de commerce et équipement, char du désert et billets, paroles des singes et Téléportation.
- 62 plages ne suivent pas un simple @; elles sont validées dans le layout complet de leur script.
- 12 tests V26 sur ROM, 4 tests sans ROM et 12 tests de régression V25 réussis: **28 tests locaux**, sans tests ignorés.
- Décodage français indépendant, aller-retour des IPS, absence de collision et conservation des anciennes modifications et des octets hors des nouvelles plages.
- Snes9x 1.63: parcours du début du jeu conforme aux cinq écrans de référence dans les deux variantes, 339 commandes accents et 337 ASCII, 25 803 images simulées par profil.
- **1 290 ajouts depuis V18 Work** (119 + 160 + 153 + 185 + 120 + 213 + 165 + 175). Ces chiffres comptent des plages modifiées, pas des scripts complets ni des phrases uniques.

Les noms propres et les sons des singes sont conservés; leurs répliques entre parenthèses sont traduites. Les mêmes messages de commerce peuvent exister à plusieurs offsets et sont comptés séparément. Les libellés du magasin de test, les fragments liés à boy/girl et les traductions archivées non auditées ne sont pas ajoutés au lot.

## Audit et reconstruction

L'audit vérifie les scripts contre la ROM originale, leurs références de début conservées en V25, les commandes inchangées et l'absence de pointeurs littéraux dans les nouvelles plages. 452 candidats passent la présélection sur V25; 175 sont intégrés ici et 277 restent à relire. Ce n'est pas le nombre total de textes restant dans le jeu.

Appliquer un seul IPS V26 directement à la ROM originale USA 1.2 sans en-tête, sans préinstaller V25. SHA-256 original: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v26/audit_v26.py --rom '/chemin/original.sfc' --out build_v26/audit.json
python3 tools/v26/build_v26.py --rom '/chemin/original.sfc' --out build_v26
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v26 -p test_v26.py -v
python3 -m unittest discover -s tools/v26 -p test_v26_offline.py -v
```

Sources, manifeste et empreintes dans `tools/v26/`. Les IDs sont les premiers octets de texte, sans @. Les commandes ne sont pas déplacées; les espaces aux frontières sont conservés et les emplacements complétés par des espaces. Aucun fichier ROM distribué.

## Limites

Le parcours Snes9x teste le début du jeu, pas les 175 nouvelles plages dans leurs scènes. L'affichage, les espacements et les scripts partiellement traduits doivent encore être contrôlés en jeu. La routine boy/girl, les 23 traductions archivées en V24, les pointeurs indirects, les textes compressés, la sauvegarde native et les graphismes anglais (dont YOU WON) restent à traiter.
