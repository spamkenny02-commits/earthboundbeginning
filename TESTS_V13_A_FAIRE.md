# Plan de tests en jeu — V13

Les contrôles binaires et les tests GitHub Actions sont réussis. **Cette liste est à exécuter dans un émulateur SNES** : aucune capture ou validation de gameplay V13 n'est encore disponible.

- [ ] Démarrer une nouvelle partie avec V13 accents et V13 ASCII ; vérifier les cinq polices, le nom du héros et le premier menu.
- [ ] Charger une sauvegarde V09/V12 si compatible ; confirmer l'absence de corruption et le bon fonctionnement du téléphone.
- [ ] Visiter Snowman, Magicant et Ellay ; contrôler les répliques des PNJ, le retour à la ligne et la fermeture des fenêtres.
- [ ] Ouvrir et fermer les boutiques ; tester acheter, vendre, inventaire plein, argent insuffisant et objet équipé.
- [ ] Vérifier les messages d'ascenseur, de gare, de chambre et de portes fermées.
- [ ] Déclencher un combat, examiner un ennemi, utiliser des objets et comparer les deux profils d'accents.
- [ ] Tester les événements avec commandes de script longues : piano, groupe musical, dialogues conditionnels, retour des personnages.
- [ ] Vérifier les caractères accentués et les éventuels débordements à l'écran, puis documenter chaque capture et état de sauvegarde.

**Critère de validation gameplay :** aucun blocage, aucun texte illisible, aucun débordement, aucune branche incorrecte et aucune régression V12 observés dans les scènes testées. Le succès des tests binaires ne suffit pas à cocher ces cases.
