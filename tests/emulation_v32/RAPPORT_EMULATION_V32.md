# Essais Snes9x V32

## Parcours normal

Snes9x 1.63 : 339 commandes accents et 337 ASCII, 25 803 images simulées par profil. Les cinq écrans de référence (titre, introduction, après combat, état restauré et menu) correspondent au parcours V18 Work. Captures et empreintes conservées ; commandes sources dans `tests/emulation_v18_work/*_history.json`.

Ce parcours ne valide pas les 16 dialogues dans leurs scènes. La restauration d'état est contrôlée par l'écran, sans nouvelle comparaison indépendante de WRAM. La sauvegarde native et boy/girl avec Ana ne sont pas testés ici.

```sh
python3 tests/emulation_v32/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/replay'
```

## Affichage natif par point d'entrée temporaire

Huit essais supplémentaires : quatre copies dans les deux profils. La ROM de test dérive de V32 ; cinq octets à `07C588` remplacent temporairement le message «personne à qui parler» par un saut vers la copie sélectionnée. Cette modification ne figure pas dans les IPS livrés. Aucun octet de RAM n'est écrit.

Les captures inspectées montrent l'hébergement chez Jack (`33C945`), la demande de chanson de Mary (`3483DC`), l'appel maternel à un compagnon (`35E2C2`) et le début du dialogue de Lloyd (`379FD3`). Les quatre plages de destination sont lues dans le moteur natif. Les accents, retours à la ligne et continuation des pages inspectées fonctionnent. Les variables de noms apparaissent dans le contexte artificiel de l'équipe chargée, qui ne reproduit pas l'identité de l'appelant narratif réel.

Pour Lloyd, le point d'entrée commence au premier marqueur de texte, après la condition narrative et les opérations d'inventaire ; seules les premières pages sont capturées avant les déplacements de personnages. Ces opérations ne sont donc pas validées par cet essai. Les scènes originales, le recrutement, les récompenses, les choix du maire et les anciennes entrées secondaires restent à tester en partie normale.

Captures et empreintes dans `probes/`. Les résultats distinguent l'empreinte V32 de celle de chaque ROM de test et consignent les destinations et octets temporaires.

```sh
python3 tests/emulation_v32/probe.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --replay-out '/chemin/replay' --out '/chemin/probes'
```

Python, numpy, Pillow et cœur Snes9x libretro requis. Aucune ROM ni sauvegarde incluse.
