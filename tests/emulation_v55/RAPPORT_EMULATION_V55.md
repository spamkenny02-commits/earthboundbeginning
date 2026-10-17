# Contrôles Snes9x V55

Le parcours de référence rejoue 339 commandes dans la variante accents et 337 dans la variante ASCII jusqu'à l'image 25803. Les 212 captures sont identiques à la V54 reproduite localement. Snes9x 1.63 termine sans erreur.

Les transports sont contrôlés dans quatre contextes : `33F0CF`, `355558`, `363D16`, `3781AA`. Les identifiants podunk/merry/reindeer/snowman du script servent seulement à classer les essais ; ils ne prouvent pas la localisation géographique des guichets.

Pour chaque contexte, quatre positions du curseur et une annulation sont essayées. La V54 et la V55, chacune avec et sans accents, représentent 80 exécutions. Deux lectures supplémentaires montrent l'introduction du billet dans la V55. Les quatre planches transport et les deux captures de l'introduction sont conservées dans `proofs/`.

Le routage contrôlé modifie uniquement les quatre octets de l'adresse d'action de la carte bancaire en `368B51`. Trois essais par version/profil forcent temporairement le saut conditionnel vers Youngtown ; les autres octets et la WRAM restent inchangés. Ces modifications ne sont pas incluses dans les IPS publiés. Les ROM temporaires sont supprimées après les essais.

La comparaison porte sur les réponses après choix ou annulation. La nouvelle question de `3781AA` remplace l'anglais ; pour les huit images concernées, seuls les pixels du rectangle `(106,16,243,29)` peuvent différer. Tous les autres pixels, dont les tarifs et Oui/Non, doivent être identiques à la V54. Le script `compare_results.py` impose cette limite.

Les essais s'arrêtent à la confirmation du tarif. Ils ne valident ni l'achat effectif, ni le voyage, ni les conditions naturelles d'accès aux scènes ou à Youngtown. Les images du parcours de référence ne couvrent pas toute la partie. Aucun cœur d'émulation, état de sauvegarde ou fichier ROM n'est distribué.

Résultat : **40 comparaisons réussies**. 32 réponses sont identiques pixel par pixel ; huit diffèrent uniquement dans la zone de la question traduite. Les 82 exécutions se terminent sans erreur. Les six planches ont été relues visuellement dans les deux variantes.
