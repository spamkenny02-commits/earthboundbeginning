# V70 — coursier de livraison

```sh
python tools/v70/build_v70.py --rom /chemin/original.sfc
EARTHBOUND_ROM=/chemin/original.sfc python -m unittest discover -s tools/v70 -v
python tools/v70/verify_display.py
python tests/emulation_v70/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v70 --profile accents
python tests/emulation_v70/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v67 --profile accents --version 67
```

Répéter les deux probes pour ASCII. Importer ensuite seulement les preuves partageables :

```sh
python tools/v70/collect_evidence.py --current /chemin/prive/v70 --reference /chemin/prive/v67
```

Les états attendus sont `{accents,ascii}/after_combat.state` V33, Ninten seul chez lui avec carte bancaire et 20 $. Leurs empreintes et celle du cœur figurent dans les résultats. Les scripts temporaires préparent la réserve avec `1D 18`, l'inventaire avec `1D 00` et, pour le refus, dépensent 20 $ avec `1D 09`. Maximum 14 opérations, wrapper de 64 octets ; aucune préparation dans l'IPS public.

L'unique entrée forcée est le téléphone complet `35C597`. L'arrivée du coursier est déclenchée ensuite par le jeu ; ne jamais décrire l'appel téléphonique initial comme naturel. Les séquences exactes et les six scénarios valides sont dans `tests/emulation_v70/probe.py`.

Attention : une seule case relancée avec `--case` remplace le JSON de résultats de la sortie choisie. Utiliser un répertoire distinct pour toute exploration. La tentative de sac totalement plein est exclue du probe public, car aucune preuve d'arrivée/dialogue exploitable n'a été obtenue. Voir `RAPPORT_V70.md` pour la portée et les limites.
