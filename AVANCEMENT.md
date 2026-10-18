# Avancement estimé

Environ **80 %**, avec une fourchette indicative de **75 à 85 %**.

Cette estimation qualitative porte sur le travail restant pour une traduction utilisable et vérifiée : textes intégrés, menus et graphismes relus, puis validation d'un parcours naturel complet. Elle ne mesure pas le pourcentage des chaînes de la ROM traduites. Les copies anciennes, textes hérités, alias et scripts inutilisés empêchent de donner un dénominateur fiable ; additionner les lots successifs compterait certains textes plusieurs fois.

Les textes sont très avancés. Restent les menus et graphismes encore anglais, la relecture et les embranchements à parcourir dans le jeu. Les essais contrôlés ne prouvent pas tous les accès naturels aux scènes.

Priorité confirmée : **terminer les textes, puis reprendre les menus**. Le lot V56 suit cet ordre. Les derniers tests naturels de Télépathie ont trouvé un résidu absent de l’audit automatique ; cet inventaire n’est donc pas une preuve d’exhaustivité.

V57 : objectif demandé de **85 % du texte**, non certifié. Le précédent taux global ne mesure pas la couverture textuelle. Le lot ajoute 63 fragments modifiés dans 37 zones ; suite des contrôles dans `RESTANT_TEXTES.md`.

V58 : 33 fragments modifiés dans des modèles hérités d’objets et de recherche (32 fragments anglais et un espacement). 511 tests et 28 lectures contrôlées ; 212 captures identiques à V57. Les accès naturels restent à établir. Le taux de 85 % du texte reste non certifié.

V59 : 61 fragments de boutiques et livraisons traduits ; 537 tests, 118 lectures isolées, 212 captures identiques à V58. Un checkpoint Git précède la publication. Objectif utilisateur : 100 % des textes, puis menus ; aucun taux exhaustif certifié.

V60 : 21 intitulés du générique traduits, 42 noms/mentions inchangés, hauteur de 1 680 pixels conservée. 554 tests, 212 captures de référence identiques à V59 et reconstitution statique avec la police réelle. Checkpoint Git séparé. Une fin de partie complète et les accès restants empêchent encore de certifier 100 % des textes.

V61 : deux fragments courts et trois huées corrigés (20 fragments de glyphes, cinq contextes). 564 tests et 212 captures identiques à V60 ; dix comparaisons contrôlées changent uniquement le texte. Audit de 4 681 segments hors menus : aucun appel analysé vers les anciennes plages conservées, deux routines non lues et 292 candidats inchangés à qualifier. 100 % du jeu reste non certifié.

V62 (audit, patch V61 inchangé) : les deux routines bloquées sur 1A 21 sont analysées. Comparaison 32 bits sans opérande prouvée sur treize ancrages et douze essais Snes9x. 575 tests ; zéro racine non lue dans le graphe connu, six débuts et onze références supplémentaires, sans texte nouveau. Les accès calculés et la relecture naturelle empêchent encore de certifier 100 %.
