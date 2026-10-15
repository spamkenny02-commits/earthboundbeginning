# Essai Snes9x V36

Le parcours de référence V18 Work a été rejoué intégralement avec Snes9x 1.63 (`1bcc369`) sur les deux IPS V36. Il s'agit du déclenchement narratif normal du premier combat contre la lampe, sans point d'entrée temporaire ni modification de sauvegarde.

Les profils accents et ASCII atteignent tous deux la bannière **« VICTOIRE »**. La relecture visuelle des captures `battle_step_30` et `battle_step_31` confirme huit lettres nettes, centrées dans la fenêtre et sans débordement. Ce sont les deux seules captures dont le rendu diffère de la référence V18 Work ; les écrans titre, introduction, restauration d'état, menu et retour après combat conservent leurs empreintes.

Le parcours compte 339 commandes pour le profil accents et 337 pour le profil ASCII, jusqu'à l'image 25 803. Le cœur termine avec le code 0 dans les deux cas. Les empreintes et résultats reproductibles sont consignés dans [`results.json`](results.json). Aucune ROM, sauvegarde d'état, mémoire vive ni copie du cœur n'est publiée.
