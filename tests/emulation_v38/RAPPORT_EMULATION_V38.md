# Essais Snes9x V38

Le parcours normal V18 Work a été rejoué avec Snes9x 1.63 dans les profils accents et ASCII : 339 et 337 commandes, jusqu'à l'image 25 803. Le titre, l'introduction, l'après-combat, la restauration d'état et le menu restent identiques aux références. Les seules différences avec V18 sont les deux images de la bannière « VICTOIRE », attendues depuis V36.

Une seconde passe a atteint le premier combat contre la lampe par le parcours normal, sans point d'entrée temporaire. Le menu de combat a été parcouru jusqu'à **« Voir »** dans les deux profils. Les captures relues montrent le curseur sur « Voir », puis uniquement le nom « La lampe hantée »; le tour du combat reprend ensuite. **Aucune des nouvelles descriptions V38 n'a donc été vue à l'écran et leur scène réelle n'est pas revendiquée comme validée.**

[`replay.py`](replay.py) reproduit le parcours de régression. [`description_probe.py`](description_probe.py) reproduit la tentative naturelle sur la lampe. Les ROM, états, captures temporaires, WRAM et coeur restent privés et ne sont pas publiés.
