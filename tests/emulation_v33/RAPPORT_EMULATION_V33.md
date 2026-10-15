# Essais Snes9x V33

## Parcours normal

Snes9x 1.63 : 339 commandes accents et 337 ASCII, 25 803 images simulées par profil. Les cinq écrans de référence (titre, introduction, après combat, état restauré et menu) correspondent au parcours V18 Work. Captures et empreintes conservées ; commandes sources dans `tests/emulation_v18_work/*_history.json`.

Ce parcours ne valide pas les 58 nouveaux scripts et messages dans leurs scènes. La restauration d'état est contrôlée par l'écran, sans nouvelle comparaison indépendante de WRAM. La sauvegarde native et boy/girl avec Ana ne sont pas testés ici.

```sh
python3 tests/emulation_v33/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/replay'
```

## Affichage natif ciblé

Dix essais supplémentaires : cinq copies dans les deux profils. Une ROM temporaire dérivée de V33 remplace cinq octets à `07C588` pour rediriger le message «personne à qui parler» vers la copie choisie. Ce raccord n'est pas inclus dans les IPS livrés. Aucun octet de RAM n'est écrit.

Les captures inspectées montrent l'interdiction d'ouvrir la porte à Snowman (`33CAA1`), les fonds insuffisants pour une quantité d'objets (`34F5B6`), la rumeur du vieil homme des montagnes (`36411D`), l'enfant qui révise ses calculs (`37853B`) et le chocolat chaud avec guimauves (`382567`). Les cinq zones de destination sont ainsi lues par le moteur natif, dans les deux variantes ; les textes, accents et retours à la ligne des captures sont vérifiés.

Ces essais ne vérifient ni les transactions réelles ni les conditions narratives. Le raccord de la continuation du chien est contrôlé au niveau des commandes et pointeurs, sans nouvel essai natif de la réponse correspondante. Les anciennes entrées secondaires et les autres pages restent à tester.

Captures et empreintes dans `probes/`. Les résultats conservent l'empreinte V33, celle de chaque ROM de test, les destinations et les octets temporaires.

```sh
python3 tests/emulation_v33/probe.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --replay-out '/chemin/replay' --out '/chemin/probes'
```

Python, numpy, Pillow et cœur Snes9x libretro requis. Aucun fichier ROM ou sauvegarde inclus.
