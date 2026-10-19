# V67 — reproduction du lot boutiques

Lire `RAPPORT_V67.md`. Appliquer un seul IPS V67 à la ROM originale USA 1.2, jamais sur une ROM déjà patchée.

```sh
python tools/v67/build_v67.py --rom SOURCE.sfc
EARTHBOUND_ROM=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v67 -v
python tools/v67/verify_display.py
```

Les cinq tests hors ROM restent utilisables sans dépendance privée ; les trois autres sont explicitement ignorés sans `EARTHBOUND_ROM`. Pillow est nécessaire à la vérification RGB.

```sh
python tests/emulation_v67/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out COURANT --profile accents
python tests/emulation_v67/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out COURANT --profile ascii
python tests/emulation_v67/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out REFERENCE --profile accents --version 66
python tests/emulation_v67/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out REFERENCE --profile ascii --version 66
python tools/v67/collect_evidence.py --current COURANT --reference REFERENCE --sheets REVUE_PRIVEE
```

Les deux états doivent être `ETATS_V33/{accents,ascii}/after_combat.state`. Ne jamais publier les sorties brutes : seuls les PNG et résultats filtrés par le collecteur sont destinés au dépôt. Le collecteur n'importe ni ROM, ni état, ni dump, ni journal brut.

La session vérifie source, patch, ROM cible, ancrages moteur et portée exacte des deux écritures privées. Les préparations sont optionnelles, limitées à 13 objets et à des IDs 1–255 ; le wrapper complet doit tenir dans 64 octets. Les deux cas d'inventaire plein donnent les objets par le moteur, pas par mutation directe de WRAM. Cette méthode artificielle ne prouve pas l'accès naturel au service. La banque 25 n'est pas utilisée comme réserve.
