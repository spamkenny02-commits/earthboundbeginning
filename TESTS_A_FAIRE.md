# Tests de la première intégration

Aucun test en émulateur n'a été réalisé dans cette étape. Les contrôles binaires et de structure ont passé pour les deux variantes du patch.

À vérifier dans un émulateur SNES :

- Introduction : accents, centrage, défilement et passage au jeu.
- Nouvelle partie, choix du texte et du son, saisie des noms, chargement et suppression d'une sauvegarde.
- Maison : mère, père au téléphone, jumelles, poupée, musique et clé sur le collier du chien.
- Dialogues avec variables : le nom du héros, son plat préféré et les objets doivent s'afficher correctement.
- Stockage chez Minnie : menus Dépôt / Retirer et capacité de l'inventaire.
- Menus de combat, inventaire, noms d'objets et statuts ; le libellé Sing reste anglais dans ce patch.
- Victoire/défaite, reprise de partie, sauvegarde et retour au titre.
- Dialogue avec espaces de remplissage : vérifier qu'ils ne provoquent pas de ligne vide supplémentaire.

Comparaison : repartir chaque fois de la ROM anglaise d'origine, puis appliquer soit le patch accents, soit le patch ascii. Ne pas appliquer les deux patches l'un sur l'autre. La variante ascii permet d'isoler un éventuel problème de rendu des nouveaux glyphes.

Les enseignes, images anglaises, crédits et la majorité du scénario ne sont pas encore traduits par ce patch.
