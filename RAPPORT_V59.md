# V59 — boutiques, consignes et livraisons

**61 fragments traduits dans 59 zones et 39 contextes** : commandes et remerciements de boutique, refus pour argent ou inventaire insuffisant, choix du porteur, confirmations de stockage/livraison et réponses téléphoniques d’Escargo Express. Certains services sont hérités d’EarthBound ; leur présence dans le graphe de commandes ne prouve pas leur accès naturel dans le portage.

Les noms et sorties d’objets restent dynamiques, notamment la liste de trois objets. Le court « and » est copié avec la commande complète de sortie de l’objet suivant ; elle reste inchangée. Aucune référence extérieure, table de menus ou routine partagée n’est modifiée. L’entrée conservée à `063C8D` peut toujours lire l’ancienne copie : son accessibilité reste à établir.

**537 tests réussis** (511 historiques et 26 V59). Les **212 captures de référence sont identiques à V58**. Les **118 lectures isolées** terminent sans erreur ; huit planches ont été relues dans les deux profils. Les essais isolent les entrées et leurs copies avec un retour temporaire et une pause ; ils ne valident pas une commande réelle, un paiement ou une livraison. [Captures et méthode](tests/emulation_v59/RAPPORT_EMULATION_V59.md).

Un premier point de sauvegarde a été publié sur `work/v59-textes` avant la finalisation des preuves. Les copies sont limitées au remplissage protégé de V57 ; les sprites restent identiques à V58.

L’audit conservateur passe de 373 à **312 fragments candidats inchangés**, dont des onomatopées, noms, textes hérités et débogage. Ce nombre n’est pas un décompte de dialogues actifs ni une base de pourcentage. Les accès calculés et anciennes entrées intérieures restent à vérifier. L’objectif demandé est désormais **100 % des textes**, sans déclaration prématurée de couverture ; les menus restent pour ensuite.

[Reproduction](tools/v59/README_V59.md) — [Textes restant à examiner](RESTANT_TEXTES.md).

Appliquer un seul IPS V59 directement à la ROM originale USA 1.2. Aucune ROM, sauvegarde ou bibliothèque d’émulation n’est distribuée.
