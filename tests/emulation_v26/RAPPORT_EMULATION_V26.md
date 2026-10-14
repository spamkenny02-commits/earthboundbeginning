# Essais Snes9x V26

Parcours V18 Work rejoué depuis une nouvelle partie dans les deux profils V26: 339 commandes accents, 337 ASCII, 25 803 images simulées par profil. Snes9x 1.63, sans triche ni modification RAM. Les écrans de titre, introduction, après combat, état restauré et menu correspondent aux références V18. Les historiques, captures et empreintes sont conservés.

Le parcours ne couvre pas les 175 nouveaux segments dans leurs zones, ni la sauvegarde native. La restauration d'état est vérifiée par son écran, sans nouvelle comparaison indépendante de la WRAM.

Rejouer depuis la racine du dépôt (Python, numpy, Pillow et cœur Snes9x libretro requis):

```sh
python3 tests/emulation_v26/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/resultats'
```
