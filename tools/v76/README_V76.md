# Reproduire V76

V76 ajoute six remplacements fixes aux IPS V75, sans allocation ni modification de commandes.

```sh
python tools/v76/build_v76.py --rom "$EARTHBOUND_ROM" --out patches
python -m unittest discover -s tools/v76 -v
python tools/v76/verify_display.py
```

Pillow est requis. Sans `EARTHBOUND_ROM`, les deux tests privés sont ignorés et cinq tests restent publics. Régressions ciblées utilisées : V75 avec `EARTHBOUND_ROM`, V65 avec `ROM_PATH`.

Le probe nécessite la ROM, le cœur et les états privés `STATES/{accents,ascii}/accept/handoff.state`. Exécuter V76 et V75 dans des sorties privées séparées pour chaque profil, puis :

```sh
python tests/emulation_v76/probe.py --rom "$EARTHBOUND_ROM" --core "$EARTHBOUND_CORE" --states-dir "$STATES" --out "$PIPPI_OUTPUT" --profile accents --version 76
python tools/v76/collect_evidence.py --current "$PIPPI_CURRENT" --reference "$PIPPI_REFERENCE" --sheets "$PIPPI_SHEETS"
```

Le collecteur exige les mêmes appels, états et entrées manette, copie uniquement les PNG et refuse toute différence hors fenêtre textuelle. Il supprime les anciennes captures générées non déclarées. La relecture humaine reste nécessaire. Les trois cas portant une racine intérieure ne constituent pas des accès naturels.
