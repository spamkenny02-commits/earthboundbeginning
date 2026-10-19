# Reproduire V74

`build_v74.py` étend V73 : neuf fragments anglais et deux formulations françaises, quatre ponts de sélecteurs en stockage protégé. Voir `RAPPORT_V74.md` pour les limites.

```sh
python tools/v74/build_v74.py --rom "$EARTHBOUND_ROM" --out patches
python -m unittest discover -s tools/v74 -v
python tools/v74/verify_display.py
```

Sans `EARTHBOUND_ROM`, trois tests privés sont explicitement ignorés ; les cinq tests publics restent exécutables. Pillow est requis pour la vérification des images. Les tests de régression utilisés sont `tools/v73` (avec `EARTHBOUND_ROM`) et `tools/v65` (avec `ROM_PATH`).

La preuve en émulateur nécessite la ROM originale, le cœur SNES9x et les états privés post-repos. Ne pas substituer silencieusement d'autres états ni publier ces dépendances. Exécuter pour chaque profil (`accents`, `ascii`), avec `--version 74` puis `--version 73` dans des sorties privées distinctes :

```sh
python tests/emulation_v74/probe.py --rom "$EARTHBOUND_ROM" --core "$EARTHBOUND_CORE" --states-dir "$RESALE_STATES" --out "$RESALE_OUTPUT" --profile accents --version 74
python tools/v74/collect_evidence.py --current "$RESALE_CURRENT" --reference "$RESALE_REFERENCE" --sheets "$RESALE_SHEETS"
```

Structure attendue : `RESALE_STATES/{accents,ascii}/accept/handoff.state`. Provenance exacte et empreintes dans les résultats. Le collecteur ne copie que les captures PNG dans Git, jamais les fixtures, états, dumps ou journaux privés. Il exige les mêmes entrées, préparations, états initiaux et nombres d'images, puis vérifie les différences hors fenêtre textuelle. Le collecteur automatise la comparaison, pas la relecture humaine.
