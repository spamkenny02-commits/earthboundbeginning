# V55 — menus de transport

16 lignes « Vers [ville] [tarif] $ » dans quatre contextes de guichet, dont trois destinations conditionnelles Youngtown. Deux fragments sont aussi traduits : « mais il te faut un billet. » et « Tu veux acheter un billet? ».

Les noms de ville, tarifs et ordre des choix sont conservés. Chaque ligne utilise une avance de 128 pixels selon la police du jeu. Les définitions sont copiées individuellement dans des réserves nulles vérifiées, puis reviennent avant la commande originale suivante. 36 enregistrements sont ajoutés à chaque IPS V54 ; les enregistrements précédents sont conservés. Les anciennes entrées intérieures, la table des personnages, le dictionnaire et la police partagée restent intacts.

La V55 a été reconstruite depuis la V54 publiée après perte des fichiers locaux de la session précédente. Les empreintes de cette reconstruction figurent dans `tools/v55/validation_v55.json`.

L'avancement global est estimé à environ 80 %, avec une fourchette de 75 à 85 %. Ce n'est pas une mesure du nombre de chaînes traduites : voir [AVANCEMENT.md](AVANCEMENT.md).

Les tests de structure et les captures contrôlées vérifient les choix et confirmations. Les conditions naturelles d'ouverture de Youngtown, l'achat effectif d'un billet, le trajet et un parcours complet du jeu restent à vérifier.

Validation locale : **430 tests réussis**, dont 23 propres à la V55. Les **212 captures du parcours de référence** sont identiques à la V54 (109 avec accents, 103 ASCII). Cette couverture ne constitue pas un parcours complet du jeu.

Affichage : **82 exécutions Snes9x**, 40 comparaisons de réponses réussies ; 32 images identiques à la V54 et huit dont seule la question traduite change. Voir [le rapport d’émulation](tests/emulation_v55/RAPPORT_EMULATION_V55.md).
