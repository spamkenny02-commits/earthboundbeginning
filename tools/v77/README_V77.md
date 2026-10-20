# Reproduire V77

Treize fragments anglais et une correction française : mineur, billet/char et chameau. Treize remplacements fixes plus deux enregistrements de pont pour Non, onze octets de réserve protégée. Voir `RAPPORT_V77.md` pour les preuves et leurs limites.

```sh
python tools/v77/build_v77.py --rom "$EARTHBOUND_ROM" --out patches
python -m unittest discover -s tools/v77 -v
python tools/v77/verify_display.py
python tools/v77/audit_remaining.py --rom "$EARTHBOUND_ROM"
```

Pillow est requis. Sans `EARTHBOUND_ROM`, trois tests privés sont explicitement ignorés et cinq restent publics. Régressions ciblées utilisées : V76 avec `EARTHBOUND_ROM`, V65 avec `ROM_PATH`. L'audit actualise seulement le périmètre direct historique V73, pas une couverture complète.

Les essais exigent ROM, cœur et états privés `STATES/{accents,ascii}/accept/handoff.state`. Exécuter chaque profil en V77 et en V76 dans des sorties privées distinctes, puis collecter :

```sh
python tests/emulation_v77/probe.py --rom "$EARTHBOUND_ROM" --core "$EARTHBOUND_CORE" --states-dir "$STATES" --out "$DESERT_OUTPUT" --profile accents --version 77
python tools/v77/collect_evidence.py --current "$DESERT_CURRENT" --reference "$DESERT_REFERENCE" --sheets "$DESERT_SHEETS"
```

Le collecteur vérifie les mêmes états, préparations, appels et entrées manette, copie seulement les PNG et supprime les anciennes captures générées non déclarées. 48 paires et 10 500 images échantillonnées sont retenues. La relecture humaine reste nécessaire. Billet/char et prix sont des branches appelées directement ; achat, location et vol ne sont pas certifiés.
