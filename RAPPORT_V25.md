# EarthBound Beginnings FR — V25

Lot du 14 octobre 2026, depuis V24 consolidée publiée sur main (`fe79072`).

## Résultats

- **165 nouvelles plages intégrées dans 86 scripts**, deux IPS autonomes accents/ASCII.
- École, soins et médecins, inventions, appels familiaux et livraisons, scènes d'EVE et de Maria.
- 97 plages suivent des commandes ou d'autres marqueurs plutôt qu'un simple @.
- 12 tests V25 sur ROM, 4 tests V25 sans ROM et 12 tests de régression V24 réussis: **28 tests locaux**, sans tests ignorés.
- Décodage français indépendant, aller-retour IPS, absence de collision et conservation des enregistrements V24 et des octets hors des nouvelles plages dans chaque profil.
- Snes9x 1.63: parcours du début du jeu conforme dans les deux profils aux cinq écrans de référence, 339 commandes accents et 337 ASCII, 25 803 images simulées par profil.
- **1 115 ajouts depuis V18 Work** (119 + 160 + 153 + 185 + 120 + 213 + 165). Les compteurs sont des plages modifiées, pas des scripts complets ni des phrases uniques.

L'audit complet hérité de V24 vérifie la correspondance des scripts à la ROM originale, les références de début conservées en V24, les commandes inchangées et l'absence de pointeur littéral dans les nouvelles plages. 617 candidats sont audités sur V24; 165 sont intégrés ici et 452 restent à relire. Ce n'est pas le nombre de textes restant dans le jeu.

## Exclusion repérée lors de la relecture

Les fragments `352FD5` et `352FED` d'une phrase d'école sont conservés en anglais. La commande `[08 05 7B F8 00]` appelle la routine `387B05`, qui imprime encore `boy` ou `girl` en anglais. Traduire le début seulement produirait une phrase hybride. Ces deux fragments ont été retirés avant la construction finale; une traduction coordonnée de cette routine reste à faire. Voir `exclusions_v25.json`.

## Utilisation et reconstruction

Appliquer un seul IPS V25 directement à la ROM originale USA 1.2 sans en-tête, sans préinstaller V24. SHA-256 source: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v25/audit_v25.py --rom '/chemin/original.sfc' --out build_v25/audit.json
python3 tools/v25/build_v25.py --rom '/chemin/original.sfc' --out build_v25
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v25 -p test_v25.py -v
python3 -m unittest discover -s tools/v25 -p test_v25_offline.py -v
```

Sources, manifestes et empreintes dans `tools/v25/`. Les IDs sont les premiers octets de texte (ne pas ajouter 1). Les commandes et leurs positions ne sont pas déplacées; les espaces source aux frontières sont conservés et les emplacements complétés par des espaces. Aucun fichier ROM distribué.

## Limites

Le parcours Snes9x couvre le début du jeu, pas les 165 nouvelles plages dans leurs scènes. L'affichage, les espacements et la cohérence des scripts partiellement traduits restent à contrôler en jeu. Les 23 traductions archivées en V24 restent conservées pour audit du layout. Les pointeurs indirects, textes compressés, sauvegarde native et graphismes anglais (dont YOU WON) restent à traiter. Aucune traduction complète du jeu n'est revendiquée.
