# V72 — réserve après coursier et reliquats

V72 est un audit du patch V71, sans nouvel IPS. Les trois cas reprennent les gestes utiles de V70/V71 pour établir un **nouvel état persistant de réserve**, pas pour refaire leurs contrôles déjà acquis.

```sh
python tests/emulation_v72/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v72 --profile accents
python tests/emulation_v72/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v72 --profile ascii
python tools/v72/collect_evidence.py --source /chemin/prive/v72 --sheets /chemin/prive/relecture
EARTHBOUND_ROM=/chemin/original.sfc python -m unittest discover -s tools/v72 -v
python tools/v72/verify_display.py
```

Les états initiaux sont les états V33 `{accents,ascii}/after_combat.state`, Ninten seul chez lui avec carte bancaire et 20 $. Le téléphone complet est forcé via un wrapper privé. La commande se fait à la manette ; le coursier arrive par le mécanisme normal du jeu après 600 images, sans appel forcé de sa racine. Les préparations initiales par commandes natives sont explicitement déclarées.

Chaque cas sauvegarde un état privé après le départ du coursier, **avant d'ouvrir l'inventaire final** des anciens probes. La phase suivante recharge cet état dans une fixture qui appelle le service de stockage complet `34B490`, sans modifier le contenu de la réserve. Les empreintes des états de passage sont chaînées dans les rapports, jamais leurs contenus.

Après dépôt de trois objets, aucune opération supplémentaire. Après livraison partielle, le sac est plein : la consultation commence par retirer **un Badge Franklin (ID 01) de l'inventaire de Ninten**, avec la commande native `1D 01 01 01`. Ce n'est pas un objet du reliquat (capsule de sagesse/vitalité), aucun objet n'est ajouté à la réserve et celle-ci n'est pas réinitialisée. Cette libération est une préparation artificielle déclarée, pas une action naturelle du joueur.

Le déclenchement du service demande cinq touches dans le cas du dépôt, six après les livraisons partielles. Puis A, Droite+A et A ouvrent la liste de réserve. Les premières explorations à cinq touches pour tous les cas restaient dans l'inventaire. À six touches mais sans libérer de case, le vrai refus français d'inventaire plein empêche d'ouvrir la liste. Ces sorties restent privées, exclues des preuves retenues.

Le test contrôle les écritures limitées au pointeur `368B51` et au wrapper `330FC0`, les empreintes ROM/IPS/fixtures, les commandes de préparation, les traces et les PNG. Aucun accès direct en écriture à la WRAM ni callback assembleur de test. Les ROM, cœur, états, historiques bruts et dumps mémoire ne sont jamais importés dans le dépôt. Sans ROM privée, le test concerné est explicitement ignoré.
