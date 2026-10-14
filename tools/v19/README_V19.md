# EarthBound Beginnings FR — V19 (119 segments)

Cette version autonome se base sur **V18 Work publiée** et ajoute **119 segments** français dans les deux variantes IPS. Appliquer **un seul IPS V19** directement à la ROM originale **USA 1.2, sans en-tête** ; ne pas appliquer d'autres IPS auparavant.

ROM attendue : SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

Contenu : `translations_v19.tsv` (source éditable), `v19_dialogues_fr.json` (manifeste), `build_v19.py` (constructeur), `test_v19.py` (11 tests unitaires), `test_v19_integration.py` (4 tests ROM), `RAPPORT_V19.md` (rapport), `validation_v19.json` et les deux patchs autonomes. Aucun fichier ROM commercial.

```sh
python3 tools/v19/build_v19.py --repo . --rom '/chemin/ROM_USA_1.2.sfc' --out build_v19
REPO_ROOT="$PWD" V19_OUT="$PWD/build_v19" ROM_PATH='/chemin/ROM_USA_1.2.sfc' python3 -m unittest discover -s tools/v19 -p 'test_v19*.py' -v
```

**Statut :** tests binaires sur ROM originale réussis ; émulation V19 et contrôle visuel non effectués. Voir `RAPPORT_V19.md` pour les limites et deux exclusions de sécurité liées aux pointeurs.
