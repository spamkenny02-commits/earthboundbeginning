# Essais Snes9x V35

## Parcours normal

Le parcours V18 Work a été rejoué avec Snes9x 1.63 sur les deux IPS V35 autonomes : 339 commandes pour le profil accents et 337 pour le profil ASCII, jusqu'à l'image 25 803. Les captures du titre, de l'introduction, de l'après-combat, de l'état restauré et du menu sont identiques aux références dans les deux profils. Les deux processus se terminent avec le code 0.

Ce parcours confirme le démarrage et la régression précoce. Il ne traverse pas les 31 scripts V35 depuis leurs déclencheurs normaux.

## Affichage ciblé

Dix sondes ont visé cinq copies, dans les deux profils : trésor du chien (`33C5A2`), maison hantée (`364FBE`), canari et choix Oui/Non (`371E94`), question du singe (`3770CF`) et texte conditionnel du vampire (`38535C`). Les captures des quatre premières montrent le moteur natif, les retours et les accents sans débordement observé. La sonde `38535C` revient au jeu sans afficher la branche attendue; elle n'est donc pas comptée comme validation visuelle de ce texte.

Le script remplace temporairement cinq octets à `07C588` pour rediriger le message « personne à qui parler ». Cette modification n'est jamais écrite dans les IPS. Il s'agit d'un point d'entrée artificiel, pas d'un déclenchement narratif ou conditionnel normal.

Les captures ont été relues. Les ROM de test, états, WRAM et cœur ne sont pas conservés; seuls les scripts, résultats JSON et PNG le sont.

```sh
python3 tests/emulation_v35/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/replay'
python3 tests/emulation_v35/probe.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --replay-out '/chemin/replay' --out '/chemin/probes'
```
