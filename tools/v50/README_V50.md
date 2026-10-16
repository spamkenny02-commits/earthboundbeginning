# Construction V50

46 fragments dans 29 contextes, plus quatre copies privées de possessifs. Les commandes principales conservent leurs positions ; deux appels grammaticaux sont explicitement redirigés. Voir le [rapport](../../RAPPORT_V50.md).

```sh
python tools/v50/build_v50.py --rom /chemin/original.sfc
python tools/v50/audit_references.py --rom /chemin/original.sfc
ROM_PATH=/chemin/original.sfc python tools/v50/run_regressions.py
python -m unittest discover -s tools/v50 -p test_v50_offline.py -v
```

Original USA 1.2 requis : 4 194 304 octets, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

- `translations_v50.json` et `contexts_v50.json` : propositions et contextes audités. Leur taille n'est pas un décompte d'intégrations.
- `v50_fixtures.json` : plages réellement intégrées, sept reports et quatre routines privées.
- `validation_v50.json` : implantations et empreintes.
- `audit_references_v49.json` : les 21 protections V49, leurs 93 sites et les candidats d'analyse non acceptés.

`audit_references.py` reproduit ce relevé avec l'original privé et les IPS V49. Les champs `legacy_window_candidate` sont des résultats heuristiques historiques ; ils ne constituent pas une preuve de pointeur et ne sont pas une liste d'autorisations. Chaque entrée conserve `accepted_for_text_edit: false`.

Les sources `07E660` / `07E66B` sont copiées avec « sa » pour le contexte `3479FF`. `35C758` / `35C764` sont copiées avec « son » pour `35C6FC`. Les branches de genre sont conservées, les autres appelants ne changent pas, et les copies sont placées dans une réserve nulle protégée des écritures précédentes.

317 tests locaux, dont 25 V50 ; dix tests V50 sans ROM en CI. Les 21 protections V49 et les sept reports V50 restent à qualifier avant édition. Les menus ne sont pas inclus dans ce lot.
