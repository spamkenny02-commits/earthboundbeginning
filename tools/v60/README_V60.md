# V60 — générique en place

```sh
python tools/v60/build_v60.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v60/run_regressions.py
python -m unittest discover -s tools/v60 -p test_v60_offline.py -v
python tools/v60/preview_staff.py --rom /chemin/original.sfc --out /chemin/apercus
```

21 intitulés remplacés et 42 noms/mentions inchangés. `staff_original.md` et `staff_fr.md` permettent la relecture. Le constructeur décode les commandes de ligne/police, espacement, nom du joueur et fin ; il refuse glyphes inconnus, lignes de plus de 32 cases, blocs non terminés, inventaire divergent ou débordement. Les styles et espacements sont comparés avant/après.

Le chargeur assembleur à `04F252` doit correspondre exactement à `a9e8fb8de7b4a9d7008de9b4`, qui désigne `D7FBE8`. Les constantes à `04F583`, `04F58C` et `04F66F` doivent valoir la hauteur décodée de 1 680 pixels. Les 1 004 octets français tiennent dans les 1 026 octets d’origine : un seul enregistrement IPS par profil. Les 22 octets après le nouveau terminateur restent inchangés et ne sont pas lus par le bloc terminé. Tous les enregistrements V59 sont conservés.

Les 17 tests couvrent reconstruction des IPS, empreintes, capacité, noms, champ joueur, hauteur, commandes, conservation des sprites et refus de sources/fixtures endommagées. Les tests historiques sont exécutés par processus séparés. Les suites graphiques V36/V37 exigeant CoilSnake restent exclues ; leurs tests hors ROM sont inclus.

## Format et police

Sources primaires épinglées à CoilSnake `346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a` :

- [StaffModule.py](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/modules/eb/StaffModule.py) : codes, taille des lignes, chargeur et constantes de hauteur.
- [eb_staff_chars.yml](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/assets/structures/eb_staff_chars.yml) : correspondance des caractères reprise dans `staff_chars.json`.
- [fonts.py](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/model/eb/fonts.py) : police 192 tuiles, 2 bpp, attribution des palettes.
- [exhal/compress.c](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/util/eb/exhal/compress.c) : format de décompression utilisé en lecture seule par l’aperçu.

Le constructeur ne dépend pas de CoilSnake, PyYAML ou Pillow. Pillow n’est requis que pour l’aperçu. Celui-ci relit la police compressée à `21453F`, via son chargeur `04F1A7`, et la palette à `21E914`. Il reconstitue les lignes centrées et place « NINTEN » comme exemple de nom du joueur. Les PNG portent explicitement la mention de reconstitution statique. Aucun défilement complet du générique dans l’émulateur n’est revendiqué.
