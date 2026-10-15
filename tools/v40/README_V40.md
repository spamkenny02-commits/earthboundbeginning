# V40 — messages de combat et dialogues de Giygas

Base : V39 (`fb0774a`). 80 scripts encore anglais sont relocalisés : messages de combat, états, utilisation d'objets et répliques de Giygas. Les menus sont laissés pour une passe ultérieure.

Le lot contient 270 fragments de texte : **156 traductions nouvelles**, 11 raccords grammaticaux anglais supprimés et 103 noms, signes ou marqueurs conservés. Aucun texte déjà français n'est recompté.

Les 95 références entrantes sont contrôlées sur les deux ROM V39 : 36 champs de la table des actions de combat (`368211–369549`, enregistrements de 12 octets, champ texte à +4), et 59 opérandes reconnus dans leurs commandes fermées. Le constructeur raccorde 88 références externes et 7 sauts entre les copies, dont les alias `3677EC` et `367DC8`. Les octets des scripts sources restent intacts.

Les copies utilisent sept sous-réserves nulles, non ciblées et sans collision IPS, entre `32A460` et `32E891`. Les autres réserves déclarées restent disponibles. Consulter le manifeste pour les limites exactes de chaque copie.

```sh
python tools/v40/build_v40.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python -m unittest discover -s tools/v40 -p 'test_v40*.py' -v
ROM_PATH='/chemin/original.sfc' python tools/v40/run_regressions.py
```

Le dernier appel exécute les suites dans des processus distincts pour éviter les constantes globales modifiées par les anciens constructeurs. Les contrôles de recompression V36/V37 dépendant de CoilSnake sont exclus ; leurs contrôles hors ligne et la conservation exacte de leurs enregistrements restent vérifiés.

Traductions : `translations_v40.json`. Octets sources et preuves de référence : `v40_dialogues_fr.json`. Empreintes et implantations : `validation_v40.json`.

Le parcours Snes9x de régression ne couvre pas les déclencheurs des 80 nouvelles scènes. Leurs affichages narratifs ou de combat restent à vérifier. Aucune ROM ni état n'est distribué.
