# Essais Snes9x V51

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` applique les IPS V51 exacts, sans retouche supplémentaire de ROM ou de WRAM : 339 commandes avec accents, 337 ASCII, jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V50. Les trois différences connues avec V18 sont celles des messages de combat déjà traduits. Voir `results.json` et `comparison_v50.json`.

## Lectures contrôlées

`display_probe.py` charge l'état privé V41 après combat et passe par l'action de la carte bancaire. Seuls les quatre octets de l'opérande de description `368B51` sont modifiés dans chaque ROM de test ; aucune WRAM n'est retouchée. La ROM temporaire est supprimée après l'essai.

Les 24 nouveaux débuts de texte sont ciblés individuellement. Deux lectures supplémentaires commencent au début des descriptions complètes `3565F7` (boisson énergétique) et `35806B` (sachet de sucre). Chaque fixture charge un état frais. Les pressions A peuvent sélectionner la première réponse ou lancer les effets de la scène d'origine ; ce n'est pas une validation de ces effets depuis leur contexte naturel. Certains noms dépendent d'un état que la carte bancaire ne prépare pas : « you » dans le fragment sur le fils ne valide pas le prénom en situation réelle.

Le retour est visible après « Un regain de forces quand la fatigue te prend. », avec « À boire pour récupérer environ 80 PV. », puis fermeture de la fenêtre. La description du sucre reprend sur « Une bonne association renforce les soins reçus. ». Les phrases, accents et retours à la ligne des 24 nouveaux fragments sont relus dans les deux variantes. Des lignes précédentes peuvent rester visibles pendant le défilement.

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Chaque planche contient les 24 premières pages et quatre captures des deux descriptions complètes, avec des vignettes natives 256 × 224. `display_results.json` conserve les empreintes, destinations et captures de chaque essai.

La livraison garde une réponse ultérieure en anglais dans la branche d'argent insuffisant ; les choix Yes/No restent à traiter avec les menus. Les points d'entrée internes préservés ne sont pas tous exécutés par ces essais. Déclenchements naturels et embranchements complets restent à vérifier.

```sh
python tests/emulation_v51/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v51/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

États privés requis : `accents/after_combat.state` et `ascii/after_combat.state`. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est publiée.
