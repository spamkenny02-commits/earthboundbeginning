# Reproduire V75

Le constructeur étend les IPS V74 : cinq plages fixes et deux définitions Non protégées. Aucun pointeur PNJ ni commande métier n'est modifié. Voir `RAPPORT_V75.md` pour les limites des essais.

```sh
python tools/v75/build_v75.py --rom "$EARTHBOUND_ROM" --out patches
python -m unittest discover -s tools/v75 -v
python tools/v75/verify_display.py
```

Pillow est requis. Sans `EARTHBOUND_ROM`, les trois tests privés sont explicitement ignorés ; cinq tests restent publics. Régressions ciblées : `tools/v74` avec `EARTHBOUND_ROM`, `tools/v65` avec `ROM_PATH`.

Le probe nécessite les dépendances privées et les états post-repos `RESALE_STATES/{accents,ascii}/accept/handoff.state`. Pour chaque profil, exécuter V75 et référence V74 dans des sorties privées différentes :

```sh
python tests/emulation_v75/probe.py --rom "$EARTHBOUND_ROM" --core "$EARTHBOUND_CORE" --states-dir "$RESALE_STATES" --out "$CANARY_OUTPUT" --profile accents --version 75
python tools/v75/collect_evidence.py --current "$CANARY_CURRENT" --reference "$CANARY_REFERENCE" --sheets "$CANARY_SHEETS"
```

Le collecteur exige les mêmes états, préparations, entrées et nombres d'images ; il copie seulement les PNG et retire les anciennes captures générées devenues inutiles dans `tests/emulation_v75`. La comparaison automatisée ne remplace pas la relecture humaine. Les preuves retenues comportent 42 paires et 9 364 images échantillonnées V75.

Le probe distingue trois appels d'entrée complète du PNJ et deux appels directs de branche mélodie. Les dons natifs A8 sont déclarés ; aucun flag ou inventaire n'est écrit directement. Ces essais ne prouvent ni accès naturel, ni retour du petit, ni apprentissage réel de la mélodie. Les premières sorties exploratoires aux refus mal sélectionnés sont exclues.
