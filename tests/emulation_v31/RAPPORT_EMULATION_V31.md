# Essais Snes9x V31

## Parcours normal

Snes9x 1.63, 339 commandes accents et 337 ASCII, 25 803 images simulées par profil. Les cinq écrans de référence (titre, introduction, après combat, état restauré et menu) correspondent au parcours V18 Work. Captures et empreintes conservées ; commandes sources dans `tests/emulation_v18_work/*_history.json`.

Ce parcours ne valide pas les 16 dialogues dans leurs scènes. La restauration d'état est contrôlée par l'écran, sans nouvelle comparaison indépendante de WRAM. La sauvegarde native et boy/girl avec Ana ne sont pas testés ici.

```sh
python3 tests/emulation_v31/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/replay'
```

## Affichage natif par point d'entrée temporaire

Six essais supplémentaires, trois scripts dans deux profils, sont exécutés avec une ROM de test temporaire dérivée de V31. Le remplacement temporaire de cinq octets à `07C588` redirige le message «personne à qui parler» vers une copie V31. Le patch livré ne contient pas cette modification. Aucun octet de RAM n'est écrit.

Les captures inspectées montrent :

- Le dialogue COMBAT (`33BFA5`), dont «ÉNORME coup qui aurait dû te mettre K.O.?», avec le retour à la ligne et les accents.
- La publicité du médecin (`37D313`), dont «Pas cher, rapide et beau», avec continuation sur la page suivante.
- L'invitation à chanter (`35001E`) et ses deux choix «Oui / Non».

Les deux réserves de destination sont ainsi lues par le moteur natif, dans les deux profils. Ces observations portent sur les pages capturées et l'affichage des choix ; elles ne certifient pas les chemins après sélection. Pour l'invitation à chanter, le point d'entrée de test commence après la condition de disponibilité du personnage, qui n'est donc pas validée. Les déclencheurs narratifs originaux, les anciennes entrées secondaires et les autres dialogues doivent encore être testés en partie normale.

Captures et empreintes : `probes/`. Le script conserve l'empreinte de V31 et celle de la ROM de test, la destination et les octets exacts du point d'entrée temporaire.

```sh
python3 tests/emulation_v31/probe.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --replay-out '/chemin/replay' --out '/chemin/probes'
```

Python, numpy, Pillow et cœur Snes9x libretro requis. Aucun fichier ROM ou sauvegarde inclus.
