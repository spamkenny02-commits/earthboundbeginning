# Régression Snes9x V39

Le parcours normal de référence V18 Work est rejoué avec Snes9x 1.63 dans les profils accents et ASCII : 339 et 337 commandes, jusqu'à l'image 25 803. Dans les deux profils, les empreintes du titre, de l'introduction, de l'après-combat, de la restauration d'état et du menu concordent avec les références.

Les seules différences avec V18 sont `battle_step_30` et `battle_step_31`, les deux images de la bannière VICTOIRE attendues depuis V36. Les deux processus se terminent sans erreur.

Ce parcours ne possède pas les objets du nouveau lot : le rendu des 22 descriptions V39 par leurs déclencheurs normaux n'est pas validé. Le script `replay.py` permet de reproduire la régression avec une ROM source et un coeur locaux. Aucune ROM, état, capture temporaire ou coeur n'est inclus.
