# V60 — générique textuel

**21 intitulés traduits**, avec **42 noms et mentions conservés** : équipe, production, réalisation, conception, musique, programmation, coordination, traduction et remerciements. Le champ du nom du joueur, tous les espacements et les types de ligne restent identiques.

Le bloc d’origine à `17FBE8` mesure 1 026 octets. Le français occupe **1 004 octets**, terminateur inclus, et tient à la même adresse. Aucun pointeur, code moteur, caractère graphique ou palette n’est modifié. La hauteur de **1 680 pixels** et ses trois constantes moteur sont inchangées. Les deux profils utilisent les mêmes intitulés en capitales sans accents, conformément à la police existante.

**554 tests passent**, dont 17 propres à V60. Les **212 captures de référence sont identiques à V59**. Les quatre comparaisons du générique sont des **reconstitutions statiques utilisant la police et les palettes de la ROM**, relues visuellement. Elles ne sont pas des captures d’un défilement en émulateur ; l’accès naturel et la fin de partie restent à vérifier. [Rapport de vérification et aperçus](tests/emulation_v60/RAPPORT_VERIFICATION_V60.md).

Un point de sauvegarde séparé, `work/v60-generique`, précède la publication finale. La V59 et son checkpoint restent disponibles.

L’objectif est **100 % des textes visibles**, avant les menus. Ce taux n’est pas atteint ou certifié par ce lot. Le générique textuel est traduit ; les anciens accès intérieurs, les réponses calculées et un parcours complet restent dans [le suivi des textes](RESTANT_TEXTES.md).

[Sources et reproduction](tools/v60/README_V60.md). Appliquer un seul IPS V60 directement à la ROM originale USA 1.2. Aucune ROM, sauvegarde ou bibliothèque d’émulation n’est distribuée.
