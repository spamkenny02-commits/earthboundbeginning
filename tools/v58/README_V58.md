# Construction et validation V58

20 zones, 14 contextes, 33 fragments modifiés (32 avec du texte anglais et un espacement), un marqueur conservé. Les modèles sont hérités ; leurs accès naturels restent à établir.

```sh
python tools/v58/build_v58.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v58/run_regressions.py
python -m unittest discover -s tools/v58 -p test_v58_offline.py -v
```

Les IPS autonomes prolongent exactement V57. Les premières cinq unités d’octet de chaque zone deviennent un saut vers sa copie ; les entrées intérieures restent intactes. Les suffixes de direction incluent leur terminateur original `02`, qui retourne avant le saut de reprise ajouté après lui. Cela permet de traiter le suffixe minimal de cinq octets sans écraser son voisin.

Seuls les appels `08` à `07E66E`, ancrés par le parseur dans trois copies, sont redirigés vers les feuilles V50 `251E0C` (« sa ») ou `251E1C` (« son »). Leurs octets exacts sont vérifiés. Le contrôle des commandes normalise uniquement ces appels connus. Les commandes de nom `19 1F` sont autorisées dans la copie du dentifrice ; les autres commandes `19` sont refusées.

Le stockage vient de `tools/v57/safe_storage.py`, uniquement dans le remplissage original `328A70–331000`, hors données de sprites, enregistrements antérieurs et cibles explicites. Les empreintes finales des sprites sont comparées à V57.

```sh
python tests/emulation_v58/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/sortie --mode controlled
python tests/emulation_v58/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/parcours
```

Le probe redirige l’opérande d’action `368B51`, sans écriture de WRAM par le testeur. Pour les huit directions seulement, un wrapper temporaire à `330FC0` reproduit le préfixe français, appelle le suffixe puis attend. Son espace doit être nul. Toutes les autres différences de ROM sont refusées. Ce wrapper n’est jamais intégré aux IPS. L’option `--only` sélectionne une lecture. Le mode naturel hérité peut comparer les opérations de carte bancaire V57/V58 ; il n’est pas utilisé pour les preuves de ce lot.

Les résultats JSON et quatre planches sont dans `tests/emulation_v58`. Ils prouvent un rendu contrôlé, pas l’obtention des objets, leurs effets ni tous les embranchements naturels. Aucun taux global de couverture textuelle n’est certifié.
