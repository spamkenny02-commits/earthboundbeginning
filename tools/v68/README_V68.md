# V68 — audit du retrait sur inventaire plein

Patch de jeu : **V67 inchangé**, pas d'IPS V68. Lire `RAPPORT_V68.md`.

```sh
EARTHBOUND_ROM=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v68 -v
python tools/v68/verify_display.py
```

Cinq tests hors ROM et un test de reconstruction des fixtures nécessitant la ROM privée. Sans `EARTHBOUND_ROM`, ce dernier est explicitement ignoré. Pillow est nécessaire pour recalculer les empreintes RGB.

```sh
python tests/emulation_v68/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out SORTIE_PRIVEE --profile accents
python tests/emulation_v68/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out SORTIE_PRIVEE --profile ascii
python tools/v68/collect_evidence.py --source SORTIE_PRIVEE --sheets REVUE_PRIVEE
```

Le probe génère trois fixtures successives, toutes basées sur les IPS V67 publiés. Les états sont chaînés après sortie du service ; leurs empreintes sont publiées, pas leur contenu. Les deux dernières phases commencent avec une touche A supplémentaire pour atteindre l'action de la carte depuis l'inventaire devenu multiple. La séquence ne doit pas être raccourcie sur la base de l'ancien état à un seul objet.

Préparation : ajout de treize objets 70, dépôt d'un objet par la manette. Blocage : ajout d'un objet 70, tentative de retrait. Récupération : suppression d'un objet 70 pour libérer une case, puis retrait par la manette et contrôle de la réserve vide. Les suppressions/ajouts sont des commandes natives dans la fixture, jamais des modifications directes de WRAM ni du patch distribué. Ne pas présenter ces préparations comme des actions naturelles.

Ne publier que les PNG et JSON importés par le collecteur. Les sorties brutes peuvent contenir états et journaux privés. Les tests vérifient l'absence d'extensions ROM/cœur/état/dump dans le dossier de preuves publié, les liens d'empreintes entre phases et les deux seules écritures autorisées dans chaque fixture.
