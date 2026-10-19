# V73 — hébergement du PNJ 898

```sh
python tools/v73/build_v73.py --rom /chemin/original.sfc
EARTHBOUND_ROM=/chemin/original.sfc python -m unittest discover -s tools/v73 -v
python tools/v73/verify_display.py
python tests/emulation_v73/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v73 --profile accents
python tests/emulation_v73/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v71 --profile accents --version 71
```

Répéter les deux probes pour ASCII, puis :

```sh
python tools/v73/collect_evidence.py --current /chemin/prive/v73 --reference /chemin/prive/v71 --sheets /chemin/prive/relecture
python tools/v73/audit_custom_npc_roots.py --rom /chemin/original.sfc
```

Le script complet `37899B` est référencé par le champ 9 du PNJ 898 (`205D53`). Il est appelé artificiellement par la carte bancaire via le wrapper privé `330FC0` et la redirection `368B51`. Ce n'est pas une visite naturelle au PNJ. Aucun don d'objet, aucune initialisation de flag ni écriture directe en WRAM. Le jeu exécute lui-même le repos et le changement de pièce ; l'état laissé après acceptation est sauvegardé et rechargé pour la conversation suivante. Seules les empreintes des états sont publiées.

Les états initiaux sont ceux de V33 `{accents,ascii}/after_combat.state`. Les choix exacts sont dans le probe : refus, acceptation puis retour. Après acceptation, attendre 600 images, afficher le menu pour lire les PV, puis le fermer en laissant 180 images entre A et B. Ne pas appliquer les anciennes fermetures sans attente à ce scénario.

Les sept plages fixes sont remplacées en place. Le choix « No » n'a que deux octets de texte ; « Non » en exige trois. Sa définition complète de cinq octets est remplacée par un saut vers onze octets de stockage protégé : `19 02 Non 02`, puis saut de retour à `378A37`. Le sélecteur, ses deux branches et le repos restent ceux du jeu. Les tests déplient ce pont et comparent les commandes natives à l'original ; les deux choix sont aussi vérifiés en émulateur.

L'allocation est calculée avec `safe_reserves` sur la ROM originale et les deux profils V71 : aucun ancien record IPS, pointeur référencé, sprite ou créneau de probe n'est utilisé. Banque 25 et `330FC0–331000` restent identiques. Aucun déplacement du script entier ou du pointeur PNJ.

Le relevé `custom_npc_roots_v73.json` examine uniquement les racines directes de PNJ dans `[36BB00,3F0000)`, omises par l'ancien filtre de racines. Il recense 181 racines et 11 candidats anglais après V73, sans fermeture récursive ni preuve d'accès naturel ou de classification linguistique complète. Prochaine priorité : `387221`, PNJ 87, service de retour d'objets. Ne pas confondre ces nombres avec un pourcentage du jeu.

Les ROM, cœur, états, historiques bruts et dumps mémoire restent privés. Le collecteur importe seulement les PNG et traces utiles.
