# Essais Snes9x V49

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` rejoue les historiques V18 sur les ROM V49 exactes, sans modification de ROM ni de WRAM. 339 commandes avec accents et 337 en ASCII, jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V48. Titre, introduction, combat, après-combat, restauration et menu restent conformes. Les différences historiques par rapport à V18 restent VICTOIRE et l'EXP. Voir `results.json` et `comparison_v48.json`.

## Lectures contrôlées

`display_probe.py` utilise la carte bancaire depuis l'état après combat. Chaque ROM de test change uniquement son opérande de description à `368B51`, sans écriture WRAM de test. Pour `34B70F`, la destination `34B722` entre directement au texte de la question, après la garde d'inventaire : la fixture ne prouve ni la présence d'objets stockés ni le fonctionnement du retrait.

Treize contextes, dans chaque variante :

| Contexte | Lecture |
| --- | --- |
| 33B970 | Moineau et question sur l'avantage au combat |
| 33F560 | Habitants moroses de Spookane |
| 34B70F, entrée 34B722 | Question de retrait d'objet |
| 355A80 | Badge Franklin, Rayon PK gamma |
| 355F89 | Pistolet paralysant, restriction à Lloyd |
| 355FF0 | Fusil à air, restriction à Lloyd |
| 3561C5 | Avertissement du boomerang |
| 356D6E | Insecticide et types d'insectes |
| 35B03F | Indice pour trouver Lloyd |
| 35B10B | Indice des explosifs de Sweet Little Factory |
| 35EAA7 | Refus d'un indice gratuit |
| 364C61 | Question sur l'objet à donner |
| 36A2F3 | Demande de rester au chalet |

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Chaque vignette conserve la capture de 256 × 224 pixels, étiquetée par contexte et page. Les retours à la ligne, accents et noms dynamiques sont relus visuellement. Certaines captures répètent une ligne lors du défilement normal. Une réponse par défaut au tutoriel est passée pour afficher son premier écran d'explication ; les branches complètes ne sont pas validées. Les réponses Yes/No restent anglaises pour la passe des menus. Le boomerang garde des commandes d'attente : les captures portent sur l'avertissement affiché, pas sur toutes ses pages possibles.

`display_results.json` consigne les empreintes des ROM de base et de test, les destinations, captures et codes de sortie. **Ces lectures ne sont pas des parcours naturels** et n'attestent pas des effets de jeu, des embranchements ou des 84 contextes du lot. Les 21 segments protégés restent anglais et ne sont pas couverts par une déclaration de traduction complète.

```sh
python tests/emulation_v49/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v49/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

Les états privés `accents/after_combat.state` et `ascii/after_combat.state` sont requis pour l'essai contrôlé. Aucune ROM, sauvegarde ni bibliothèque d'émulation n'est publiée.
