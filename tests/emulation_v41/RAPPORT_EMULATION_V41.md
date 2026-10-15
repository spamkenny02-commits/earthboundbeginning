# Régression Snes9x V41

Le parcours normal de référence V18 Work est rejoué sous Snes9x 1.63 dans les profils accents et ASCII : 339 et 337 commandes, jusqu'à l'image 25 803. Les empreintes du titre, de l'introduction, de l'après-combat, de la restauration d'état et du menu concordent avec les références.

Les seules différences avec V18 sont `battle_step_30` et `battle_step_31`, les deux images de la bannière VICTOIRE attendues depuis V36. Les deux processus se terminent sans erreur.

Ce parcours ne valide pas les déclencheurs ni la mise en page des 108 nouvelles scènes V41. Aucun point d'entrée artificiel n'a été utilisé.

Un second essai charge l'état normal après le combat V40 et utilise la carte bancaire naturellement présente dans l'inventaire : A → droite → A → A → A. Aucun objet n'est injecté et aucun octet ROM ou WRAM n'est modifié par la sonde. La fenêtre affiche « To use this, go to a cash machine and insert the card. » dans les deux profils. Ce texte antérieur n'appartient pas au lot V41 et reste à analyser ; cette sonde ne constitue pas une validation des nouvelles copies.

`replay.py` reproduit la régression. `item_use_probe.py` reproduit l'essai supplémentaire avec `--rom`, `--core`, `--states-dir` et `--out`. Les résultats et empreintes sont dans `results.json` et `item_use_results.json`. Les ROM, états, captures temporaires et coeurs restent locaux.
