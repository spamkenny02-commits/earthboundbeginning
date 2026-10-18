# V63 — observation des accès de texte en jeu

Le patch publié reste V61. Aucun nouvel IPS, aucune écriture dans le moteur ou la WRAM.

`tests/emulation_v63/probe.py` restaure une sauvegarde privée après le combat initial, puis exécute sept séquences de manette dans Snes9x. Il lit, après chaque image, le pointeur du cadre DISPLAY_TEXT courant. Les octets du moteur original et des deux profils V61 sont vérifiés avant la lecture : allocation à `014012`, initialisation à `01866D`. La pile commence à `96AA`, comporte dix cadres de 27 octets ; son index courant est à `97B8`. Le premier champ du cadre est le pointeur de script. Les cadres inactifs et les pointeurs hors ROM sont exclus.

Cette observation contourne la dépendance aux seules références statiques : elle voit le curseur même quand un appelant a calculé son adresse. Elle ne reconstruit pas la chaîne assembleur de l'appelant, et ne distingue pas à elle seule un appel calculé d'un appel direct omis dans les graines. Une image peut contenir plusieurs appels terminés avant l'échantillon : ce n'est pas une trace CPU exhaustive. Le curseur indique le prochain octet ; il peut désigner une commande ou la fin d'un script, et ne prouve pas la lecture d'un fragment anglais adjacent.

Sources locales vérifiées contre la ROM : désassemblage Herringway/ebsrc, révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`, fichiers `src/unknown/C1/C14012.asm`, `C14049.asm`, `C1866D.asm`, `src/text/display_text.asm`. Les adaptations du remake sont contrôlées par les ancres binaires, sans supposer que toutes ses routines sont identiques à EarthBound.

## Reproduction privée

Ne pas ajouter la ROM, le cœur, les états ou les dumps mémoire au dépôt.

```sh
python -m unittest discover -s tools/v63 -p 'test*.py'
python tests/emulation_v63/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile accents
python tests/emulation_v63/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile ascii
python tools/v63/summarize.py --rom SOURCE.sfc --results SORTIE/results_accents.json --out AUDIT_ACCENTS.json
python tools/v63/summarize.py --rom SOURCE.sfc --results SORTIE/results_ascii.json --out AUDIT_ASCII.json
```

Le répertoire des états doit contenir `accents/after_combat.state` et `ascii/after_combat.state`. `--case` permet de rejouer une seule séquence ; utiliser un répertoire distinct si l'on souhaite conserver le rapport global. Les JSON versionnés ne contiennent que les pointeurs observés, compteurs, commandes de manette, empreintes et captures. Les captures sont examinées visuellement ; aucune détection automatique de la langue n'est prétendue.
