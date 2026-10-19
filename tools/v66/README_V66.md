# V66 — sélecteur Escargo et fins d'appel

Lire `RAPPORT_V66.md` pour les résultats et limites. V66 prolonge V65 et ne change que deux fragments à taille fixe. Appliquer un seul IPS V66 à la ROM originale USA 1.2, jamais sur une ROM déjà patchée.

```sh
python tools/v66/build_v66.py --rom SOURCE.sfc
EARTHBOUND_ROM=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v66 -v
python tools/v66/verify_display.py
```

Sans `EARTHBOUND_ROM`, les trois tests nécessitant la ROM sont explicitement ignorés, les quatre tests hors ROM restent exécutables. Pillow est nécessaire au vérificateur visuel.

```sh
python tests/emulation_v66/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile accents
python tests/emulation_v66/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile ascii
```

`--version 65 --case mom_pickup` (accents) et `--version 65 --case mom_delivery` (ASCII), dans deux sorties distinctes, reproduisent les références. Le probe réutilise `tools/v65/service_session.py`, dont les vérifications de ROM source, IPS, ROM cible, réserve temporaire et ancrages moteur s'appliquent aussi à V66. Les seules modifications de la fixture sont le pointeur `368B51` et le wrapper `330FC0`. Tous deux sont absents des IPS.

Chaque page reçoit 180 images de stabilisation ; les touches sont pressées deux images puis relâchées douze images. Les curseurs de texte sont échantillonnés image par image : ce n'est pas une preuve d'exhaustivité des glyphes/branches. Les fichiers publiés contiennent les captures, leurs empreintes et les transitions observées, pas les états mémoire ni les ROM temporaires.
