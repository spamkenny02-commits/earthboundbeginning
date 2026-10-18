# V62 — audit étendu, patch V61 inchangé

```sh
ROM_PATH=/chemin/absolu/original.sfc python tools/v62/run_regressions.py
python -m unittest discover -s tools/v62 -p test_v62_offline.py -v
python tools/v62/audit_aliases_v62.py --rom /chemin/original.sfc --out /chemin/audit_accents.json
python tools/v62/audit_aliases_v62.py --rom /chemin/original.sfc --profile ascii --out /chemin/audit_ascii.json
```

Le fichier d’entrée est la ROM originale USA 1.2, vérifiée par son SHA-256. Le script applique en mémoire le patch V61 et vérifie son empreinte. Aucun fichier ROM n’est produit par l’audit. Les deux JSON enregistrés sont reproductibles et testés sur ROM.

## Preuve de `1A 21`

`opcode_proof.py` vérifie treize ancrages, dans la source et chaque profil :

- Le choix du handler `1A` à `018AD4` conduit à `C17B56`.
- Le hook à `017B56` appelle `F8BF0E`.
- Ce dispatch multiplie l’indice de sous-commande par quatre et lit la table `F8BDD0`.
- L’entrée d’indice `21`, à `38BE54`, désigne `F7B94D`.
- Le corps complet à `37B94D` lit les deux registres, compare leur mot bas puis leur mot haut, produit 0/1 et écrit le registre de travail. Il n’appelle pas le lecteur d’arguments de script et ne déplace pas le pointeur de texte.
- Les bridges, getters et setter sont vérifiés, ainsi que le calcul de la fenêtre active utilisé pour lire les registres lors du test.

Le contrat est donc une longueur totale de **deux octets**, sans paramètre ni pointeur de texte. Les usages adjacents de `1B 02` sont lus à leur vraie frontière. La sous-commande voisine `1A 22` reste inconnue et refusée.

Le [désassemblage primaire d’EarthBound](https://github.com/Herringway/ebsrc/tree/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62), commit épinglé, explique les conventions de dispatch et de registres : `src/text/display_text.asm`, `src/text/ccs/tree_1A.asm`, `src/text/get_argument_memory.asm`, `src/text/get_working_memory.asm` et `src/text/set_working_memory.asm`. Le hook et le corps `1A 21` sont propres à cette ROM : leur preuve vient de ses octets, pas d’une commande supposée dans le moteur original. Les liens des fichiers figurent dans les résultats de preuve.

`parser_v62.py` charge une instance indépendante du parseur historique et ajoute uniquement ce contrat dans sa propre table. Les modules historiques et `atelier/outils/commandes.json` restent intacts. Les tests confirment que l’ancien parseur refuse encore `1A 21` et que le nouveau lit exactement la commande suivante.

## Émulateur

```sh
python tests/emulation_v62/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/essais --profile accents
python tests/emulation_v62/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/essais --profile ascii
```

Un script temporaire à `330FC0`, appelé via l’action de carte bancaire à `368B51`, initialise les deux registres puis exécute le vrai `1A 21`. Deux callbacks temporaires à `330E00` et `330E20` retournent les constantes 32 bits via `06/08`. Le moteur original `1A 0C`, avec les flags `81`, range ces retours dans le registre de travail. Les quatre plages de test doivent être libres ou correspondre au seul opérande redirigé ; tous les autres octets restent identiques. Les treize ancrages moteur sont revérifiés dans chaque fixture.

Après l’opération, le test lit les registres de travail et d’argument de la fenêtre active et exige le résultat attendu. Il vérifie aussi visuellement le marqueur « suite lue. » placé après `1A 21`. Aucune écriture directe de WRAM par l’outil. Ces callbacks initialisent néanmoins des registres du moteur : c’est un test synthétique, pas une scène naturelle. Les données brutes de WRAM et les fixtures ROM restent hors du dépôt ; seuls les résultats numériques utiles et les captures sont conservés.

## Portée

Les deux routines initialement bloquées et leurs continuations ne contiennent aucun nouveau texte. L’audit obtient zéro racine non lue pour ses graines connues ; il ne couvre pas tous les pointeurs calculés ou appelants assembleur. Les 292 candidats hérités/noms/onomatopées/diagnostics restent à qualifier. Les décomptes de graphe ne constituent pas un taux de traduction du jeu.

V62 ne reconstruit pas de patch : **les IPS V61 sont ceux à utiliser**. Les tests historiques, y compris ceux des anciens parseurs, restent exécutés. Les suites graphiques V36/V37 nécessitant CoilSnake sont exclues ; leurs tests hors ROM sont inclus.
