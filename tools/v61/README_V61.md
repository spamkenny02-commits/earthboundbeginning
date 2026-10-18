# V61 — corrections à taille constante et audit

```sh
python tools/v61/build_v61.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v61/run_regressions.py
python -m unittest discover -s tools/v61 -p test_v61_offline.py -v
python tools/v61/audit_aliases.py --rom /chemin/original.sfc --out /chemin/audit.json
```

Deux fragments lexicaux et trois huées corrigés : 20 fragments de glyphes dans cinq contextes. Chaque écriture a la taille de la séquence source et se situe sur une frontière de texte validée dans son contexte complet. Aucun pointeur, branchement, saut, réserve, dictionnaire ou police n’est modifié. Le constructeur refuse une source divergente et compare les commandes complètes avant/après. Les dix nouveaux tests couvrent tailles, empreintes, commandes, huées reconstituées, tables de personnages, sprites, générique et reconstruction exacte des IPS.

Les deux espaces après `@` remplacent le « A » anglais sans décaler les commandes suivantes. La préposition française remplit les quatre octets d’origine avec une espace terminale supplémentaire. Les huées gardent leurs neuf lettres et leur point d’exclamation, avec les mêmes pauses entre les glyphes.

## Affichage

```sh
python tests/emulation_v61/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/lectures --profile accents
python tests/emulation_v61/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/lectures --profile ascii
python tests/emulation_v61/compare_display.py --display /chemin/lectures --out /chemin/comparaison.json
python tests/emulation_v61/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/parcours
```

Les lectures redirigent uniquement l’action de la carte bancaire à `368B51` vers un wrapper placé dans les octets nuls à `330FC0`. Les scripts et commandes des patchs restent intacts. Le troisième cri est lu à partir de `3505D4`, sans reproduire tout le spectacle qui le précède. Un préfixe explicatif est ajouté pour lire la préposition de destinataire ; les variables de cette formule ne sont pas initialisées comme dans sa scène naturelle. Aucune intervention du testeur sur la WRAM. Le rendu et les pixels extérieurs au texte sont comparés, pas l’obtention naturelle des dialogues. Les reprises du parcours utilisent les IPS sans modification.

## Audit conservateur

`alias_audit_v61.json` contient le graphe issu des graines de personnages/actions reconnues, les références vers les plages originales conservées, les candidats inchangés et les routines non lues. Les graines et le format de commandes sont ceux déjà utilisés par les outils V53–V59 ; il ne s’agit pas d’une preuve d’accès naturel.

Les plages vérifiées sont celles de V51, V52, V53, V56, V57, V58 et V59 ; les blocs de menus V54/V55 sont hors de cet examen. Les cibles après les cinq octets du saut sont examinées, et toute entrée dans la source intégralement préservée d’une copie NPC V53 est recherchée. Aucune arête de ce graphe n’y entre. Les pointeurs calculés ou assembleur restent hors de portée. Les deux racines `37C079` et `37C100` échouent sur la sous-commande inconnue `1A 21` ; elles ne sont pas assimilées à des chemins traduits.

L’audit conserve les exclusions de forme (par exemple une table à plus de 64 cibles) et les erreurs de parse dans ses résultats. Son relevé de 4 681 segments n’est pas un dénominateur de couverture du jeu. Le filtre de mots anglais fréquents appliqué aux segments modifiés est une aide de recherche, pas une classification linguistique. Les 292 candidats inchangés restent à qualifier selon langue et accessibilité.
