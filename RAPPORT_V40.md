# V40 — messages de combat et dialogues de Giygas

Base publiée et vérifiée : V39, commit `fb0774a6b97e83415029821ea3a11d402afdf235`.

## Traductions intégrées

**80 scripts encore anglais sont révisés**, comprenant les répliques de Giygas, les messages d'états et d'actions de combat, les tentatives de fuite et des messages d'utilisation d'objets. Les menus ne sont pas modifiés par ce lot.

Les copies comprennent 270 fragments : **156 traductions nouvelles**, 11 raccords grammaticaux anglais supprimés, et 103 noms, signes ou marqueurs conservés. Les fragments retirés ne sont pas ajoutés au compteur des nouvelles traductions. Aucun texte déjà français n'est recompté.

Sur les 85 scripts candidats, cinq restent inchangés : `35CC29` et `367694` appellent des routines possessives anglaises partagées, `367700` et `3680C9` comportent des références dont la structure demande une analyse supplémentaire, et `35CD0C` contient le cri neutre ZAP.

## Références et conservation binaire

Les sources sont vérifiées sur la ROM USA 1.2 par SHA-256, puis comparées aux deux ROM V39. Les 95 références entrantes sont identifiées : 36 champs de la table des actions de combat et 59 opérandes de commandes reconnues et fermées.

Le constructeur raccorde **88 références externes et 7 sauts entre les copies**. Les deux alias intérieurs `3677EC` et `367DC8` sont raccordés à leurs frontières conservées, sans saut au milieu du texte redimensionné. Les scripts sources restent intacts.

Les copies utilisent sept sous-réserves nulles, non référencées et sans chevauchement avec les IPS V39, entre `32A460` et `32E891`. Les IPS autonomes ajoutent chacun 168 enregistrements : 80 copies et 88 réécritures de références externes. Les sept redirections internes se trouvent dans les copies.

Tous les enregistrements antérieurs sont conservés. L'application indépendante des IPS depuis la ROM originale produit les mêmes ROM que l'application des seules additions à V39. Les différences exhaustives ne montrent aucune écriture hors des plages déclarées. Les implantations accents et ASCII sont identiques.

## Contrôles

**109 tests locaux réussis**, dont 15 tests V40, 15 V39, 14 V38, 4 V37 hors ligne, 4 V36 hors ligne, 11 V35, 12 V34, 14 V33, 12 V29 et 8 boy/girl. Les tests de recompression V36/V37 dépendant de CoilSnake ne sont pas réexécutés ; leurs contrôles hors ligne et la conservation exacte de leurs IPS sont vérifiés.

Les tests V40 couvrent les octets sources, les preuves de référence, les réserves, l'application IPS indépendante, le décodage français indépendant, les commandes conservées, les alias, les sauts, les profils et tous les octets hors du lot.

Le parcours normal Snes9x 1.63 est conforme dans les deux profils jusqu'à l'image 25 803 : titre, introduction, premier combat remporté, après-combat, restauration d'état et menu. Les deux différences avec V18 sont les bannières VICTOIRE attendues depuis V36.

**Limite : les déclencheurs et l'affichage des nouvelles scènes V40 ne sont pas validés par ce parcours du début du jeu.** Les dialogues finaux de Giygas, les actions et les états concernés restent à vérifier dans leurs situations réelles. Les essais V39 sur les descriptions d'objets restent documentés séparément et ne sont pas comptés comme des essais des nouveaux textes V40.

## Fichiers

- [Traductions, constructeur et méthode](tools/v40/README_V40.md)
- [Manifeste binaire et empreintes](tools/v40/validation_v40.json)
- [IPS accents](patches/EarthBound_Beginnings_FR_v40_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v40_ascii.ips)
- [Rapport Snes9x](tests/emulation_v40/RAPPORT_EMULATION_V40.md)

Aucune ROM, aucun état d'émulateur ni coeur n'est publié.
