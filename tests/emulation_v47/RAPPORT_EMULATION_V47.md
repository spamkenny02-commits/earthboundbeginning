# Essais Snes9x V47

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` rejoue les historiques de manette V18 sur les deux ROM V47 exactes. Il ne modifie ni la ROM appliquée, ni la WRAM. 339 commandes avec accents et 337 en ASCII, jusqu'à la frame 25803. Titre, introduction, combat, après-combat, restauration et menu passent. Les 109 captures avec accents et 103 ASCII sont toutes identiques pixel par pixel aux captures V46. Les changements historiques par rapport à V18 restent VICTOIRE et l'EXP. Voir `results.json` et `comparison_v46.json`.

## Affichage contrôlé

`display_probe.py` charge la sauvegarde après combat et ouvre normalement l'objet carte bancaire. Pour chaque cas, seul son opérande de description à `368B51` est remplacé par l'adresse de la nouvelle copie. Aucune écriture WRAM de test. **Ce sont des essais d'affichage avec routage ROM, pas les événements naturels.**

Huit scripts, chacun dans les deux variantes, sans arrêt du cœur :

| Source | Contrôle | Capture avec accents |
| --- | --- | --- |
| 366E26 | Respiration sifflante | [Capture](proofs/366E26_accents.png) |
| 366E39 | Quinte de toux | [Capture](proofs/366E39_accents.png) |
| 366E5B | Reprise du souffle | [Capture](proofs/366E5B_accents.png) |
| 36804C | Distraction | [Capture](proofs/36804C_accents.png) |
| 3603C7 | Accord pour le zoo, nom dynamique et clé | [Page 1](proofs/3603C7_page1_accents.png), [page 2](proofs/3603C7_page2_accents.png), [page 3](proofs/3603C7_page3_accents.png) |
| 34B686 | Aucun objet en dépôt | [Capture](proofs/34B686_accents.png) |
| 373CD8 | Prix trop élevé | [Capture](proofs/373CD8_accents.png) |
| 38227C | Plafond bancaire | [Capture](proofs/38227C_accents.png) |

Les mêmes captures ASCII sont dans `proofs/`, avec le suffixe `_ascii.png`. `display_results.json` contient les empreintes des ROM exactes et de test, destinations, captures et codes de sortie. Les captures ont été relues visuellement : accents corrects, lignes lisibles et contenu complet. Le quatrième écran du zoo montre la fermeture du dialogue ; il figure dans le journal, sans être une preuve de texte.

L'accès naturel à ces huit scènes et les 13 autres scripts ne sont pas validés ici. Les essais contrôlés n'attestent pas des effets de jeu des objets, du dépôt ou de l'asthme.

```sh
python tests/emulation_v47/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v47/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

Les états privés `accents/after_combat.state` et `ascii/after_combat.state` sont requis pour l'essai contrôlé. Aucune ROM, sauvegarde ni bibliothèque d'émulation n'est publiée.
