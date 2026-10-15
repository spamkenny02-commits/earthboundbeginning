# Régression Snes9x V40

Le parcours normal de référence V18 Work est rejoué avec Snes9x 1.63 dans les profils accents et ASCII : 339 et 337 commandes, jusqu'à l'image 25 803. Les empreintes du titre, de l'introduction, de l'après-combat, de la restauration d'état et du menu concordent avec les références.

Les seules différences avec V18 sont `battle_step_30` et `battle_step_31`, les deux images de la bannière VICTOIRE attendues depuis V36. Les deux processus se terminent sans erreur.

Ce parcours vérifie le démarrage, l'exploration et le premier combat ; **il ne valide pas le rendu des nouvelles répliques de Giygas, des actions et des états du lot V40 dans leurs scènes réelles**. Aucun point d'entrée artificiel n'a été utilisé pour ce contrôle. Les 44 cas d'affichage V39 concernent des textes antérieurs et ne sont pas ajoutés à cette couverture.

Reproduire avec `replay.py --rom ... --core ... --out ...`. Les empreintes des ROM et les résultats sont conservés dans `results.json`. Aucune ROM, aucun état ni coeur n'est publié.
