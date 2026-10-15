# Snes9x V43 — parcours et Voir

Le parcours normal de référence V18 est rejoué avec les IPS V43 finaux, sous Snes9x 1.63 : 339 commandes dans le profil accents, 337 dans le profil ASCII, jusqu'à l'image 25 803. Titre, introduction, après-combat, restauration d'état et menu restent conformes. Les seules différences avec V18 sont les deux captures VICTOIRE attendues. Les deux processus se terminent sans erreur ; empreintes et résultats dans `results.json`.

## Nouveau message d'examen — deux profils

Depuis l'état normal V41 `lamp_checkpoint`, la navigation de référence rejoint la première lampe. Droite → bas → droite sélectionne **Voir** ; A ouvre la cible, puis A confirme la lampe. Les captures sont prises toutes les dix images pour suivre l'action et son texte.

À la capture `check_text_35`, la phrase complète est lisible : **« Ninten examine La lampe hantée ! »**, sans débordement. Le profil ASCII donne « hantee ». Ce message provient du script V43 `361CA1`, appelé par l'action d'examen `2F8531`. Le sujet et le nom de cible sont produits par le jeu.

- [Voir — accents](check_accents.png)
- [Voir — ASCII](check_ascii.png)

Aucun patch de test, objet injecté ou octet WRAM écrit n'est utilisé. L'état est chargé dans le profil correspondant ; les ROM sont exactement celles produites par les IPS publiés.

## Reproduction et portée

`replay.py` prend `--rom`, `--core` et `--out`. `check_probe.py` prend aussi `--states-dir`, répertoire contenant les états normaux par profil. Le coeur, les ROM et les états restent locaux.

Un des 56 scripts nouveaux est ainsi relu dans les deux profils. Les 55 autres, dont Maria et les actions tardives, restent à vérifier dans leurs scènes réelles. Le parcours général n'est pas présenté comme une validation visuelle de ces textes. Le JSON voisin documente la sonde et les empreintes de ses captures.
