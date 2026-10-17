# Contrôles Snes9x V56

**451 tests locaux réussis**, dont 21 propres à la V56. Les 212 images du parcours de référence sont identiques à la V55, après 339 commandes avec accents et 337 en ASCII, jusqu'à l'image 25803.

## Télépathie par le menu normal

Quatre exécutions comparent V55/V56 dans les deux variantes, depuis la sauvegarde après le combat de référence. La ROM appliquée est celle du patch publié, sans modification de routage ni de WRAM. Le menu PSI permet d'utiliser Télépathie normalement.

Avant : « Ninten tried / Telepathy π! / But nothing happened. » Après : « Ninten lance / Telepathy π! / Mais rien ne se passe. ». La comparaison confirme que tous les pixels hors du rectangle de texte `(104,16,244,65)` restent identiques. Les deux paires de captures sont relues visuellement. Le nom du PSI reste pour la phase des libellés de menus.

## Lectures contrôlées

24 cas par variante, soit 48 exécutions, lisent 21 zones isolées et les contextes complets du journal, du chuchotement et de la réparation. La ligne PSI est vérifiée par le parcours normal ci-dessus, qui initialise correctement le nom du pouvoir. Un essai forcé de cette ligne seule ne permettrait pas de vérifier les valeurs dynamiques.

Huit exécutions supplémentaires lisent les trois messages éphémères avec leur nom de personnage et le journal. Les échantillons sont pris aux images 15, 45, 50 et 105 après l'ouverture de l'action. Les messages « Ninten fouille la poubelle », « Ninten ouvre le coffre » et « Ninten ouvre le cercueil » sont visibles avant leur fermeture automatique. Le journal est parcouru jusqu'à la dernière phrase.

Dans ces 56 lectures contrôlées, seule l'adresse d'action de la carte bancaire en `368B51` change temporairement. Les IPS publiés et la WRAM ne sont pas modifiés pour le test. Les ROM temporaires sont supprimées après exécution. Snes9x 1.63 termine sans erreur pour les 60 essais d'affichage, auxquels s'ajoutent les deux relectures du parcours de référence.

Les planches des deux variantes ont été relues : aucune coupure ou sortie de fenêtre constatée dans les textes traités. Les valeurs d'objets affichées lors des réparations proviennent de la sauvegarde du test et ne prouvent pas le déclenchement d'une véritable réparation. La plupart des scènes restent des lectures forcées ; seule Télépathie est ici testée par son accès normal. Ces essais ne constituent pas une partie complète.

Aucun fichier ROM, cœur d'émulation ou état de sauvegarde n'est distribué.
