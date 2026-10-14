# Essais Snes9x V30

Le parcours enregistré V18 Work est rejoué depuis une nouvelle partie sur les IPS V30, dans les deux profils. Snes9x 1.63 : 339 commandes accents, 337 commandes ASCII, 25 803 images simulées par profil. Les cinq captures comparées (titre, introduction, après combat, état restauré et menu) correspondent aux empreintes des références V18. Les captures et `results.json` sont conservés ici ; les commandes sources sont dans `tests/emulation_v18_work/*_history.json`.

Ce parcours ne valide pas les 121 fragments ajoutés dans leurs scènes, ni les trois dialogues boy/girl corrigés en V29. Il ne valide ni Ana en tête, ni la sélection après KO, ni la présentation des phrases complètes. La restauration d'état est contrôlée par l'écran, sans comparaison indépendante de la WRAM. Aucun test de sauvegarde native ajouté.

```sh
python3 tests/emulation_v30/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/resultats'
```

Python, numpy, Pillow et cœur Snes9x libretro requis. Aucune ROM ni sauvegarde incluse.
