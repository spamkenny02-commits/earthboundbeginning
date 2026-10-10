# Tests de la première intégration

Premiers essais réalisés en v02 : menus de création de partie, introduction, maison, dialogue de la sœur et premier combat jusqu’à la victoire. Voir RAPPORT_V02.md pour le périmètre exact. Les contrôles binaires et de structure passent pour les deux variantes.

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

## Mise à jour v03

Vérifier le clavier MAJ/min/Au choix/Effacer, les goûts des fenêtres, les 23 noms d’ennemis et les nouveaux messages de combat. Le premier combat est documenté dans RAPPORT_V03.md ; poursuivre les attaques/dégâts, les textes résiduels d’expérience et les combats à plusieurs alliés.

## Mise à jour v04

Confirmés : attaque du héros et de la lampe, dégâts aux deux cibles, expérience sans caractère parasite, retour à la maison dans les deux variantes, « À qui ? », « R.A.S. » et dialogue sur l’oreiller vivant. Les boutiques, descriptions PSI, sauvegarde/chargement, autres combats et la fin de la séquence familiale restent à valider. Voir tests/rapport_emulation_v04.json.

## Mise à jour v05

Niveau 2, mélodie et premier appel familial observés ; sauvegarde SRAM et chargement après redémarrage confirmés pour les deux variantes finales. Poursuivre les messages financiers, les menus PSI, le stockage, les cadeaux, la défaite, les autres emplacements de sauvegarde et la relecture des espaces. Voir RAPPORT_V05.md et tests/rapport_emulation_v05.json.

## Mise à jour v06

Virements et formules du père observés dans un essai isolé ; les calculs et le parcours normal restent à vérifier. Nouvelle partie et lecture SRAM sur les deux ROM finales confirmées. Vérifier les groupes, le stockage, les PSI et les espacements. Voir RAPPORT_V06.md et tests/rapport_emulation_v06.json.
