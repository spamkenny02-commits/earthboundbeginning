# Essais Snes9x V52

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` applique les IPS V52 exacts, sans autre retouche de ROM ou de WRAM. 339 commandes avec accents et 337 ASCII jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V51. Les trois différences connues avec V18 concernent les messages de combat déjà traduits. Voir `results.json` et `comparison_v51.json`.

## Lectures contrôlées

`display_probe.py` charge l'état privé V41 après combat et utilise l'action de la carte bancaire. Seuls les quatre octets de l'opérande de description `368B51` sont redirigés ; aucune WRAM n'est retouchée. Chaque cas recharge un état frais et supprime sa ROM temporaire après l'essai.

Quinze entrées visent les segments V52. Deux autres visent `3517D7`, l'appelant du texte « Amour et paix », et `35E4E9`, la livraison déjà traduite en V51. Ce dernier cas suit les réponses jusqu'à la branche d'argent insuffisant, maintenant française. Il ne représente pas un test des conditions financières réelles dans la scène naturelle.

Les deux fragments regroupés à `350BEF` s'affichent, puis le dialogue reprend sur le prénom Ninten et la réplique française suivante. Le préfixe des amoureux et son suffixe français s'affichent depuis leur entrée directe et depuis l'appelant. Le père reprend sur les lignes françaises existantes. Les quinze segments sont relus dans les deux variantes : accents, prénom et retours à la ligne sans coupure visible. Les choix Yes/No et les tailles de pizza restent pour le lot des menus.

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Vingt vignettes natives 256 × 224 par planche : quinze premières pages et cinq contrôles d'appelant ou de continuation. `display_results.json` consigne les 17 cas par variante, empreintes et captures.

Les fixtures entrent directement dans des portions de scène. Elles ne prouvent pas les déclenchements naturels, les points d'entrée secondaires conservés, le combat du club, le recrutement, ni tous les embranchements. Aucun test de combat ou de recrutement n'est déclenché depuis la menace : la capture s'arrête avant validation de cette page.

```sh
python tests/emulation_v52/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v52/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

États privés requis : `accents/after_combat.state` et `ascii/after_combat.state`. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est publiée.
