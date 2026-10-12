# Traduction française v07 — Podunk et atelier CSV

**718 entrées intégrées**, soit 44 dialogues supplémentaires par rapport à la v06. Le nouveau lot couvre les habitants de Podunk, les panneaux de la ville, le cimetière, Pippi, l'adjoint du maire, l'accès au zoo, le Village des Canaris et deux descriptions d'objets. Les commandes et conditions du scénario restent en place. Les cinq champs et le dialogue trop longs déjà exclus en v06 restent anglais.

## Outil de traduction

`traduction/atelier.py` exporte 1 124 fragments de champs et de dialogues ordinaires dans un CSV UTF-8 éditable. L'import dispose d'un mode de vérification sans écriture. Il conserve les originaux et refuse les identifiants inconnus ou répétés, les caractères non représentables, les commandes injectées et les suffixes PSI modifiés. Un import incomplet est permis pour ne modifier que quelques lignes.

La commande `construire` produit les deux variantes et lance le vérificateur indépendant. Le CSV de sortie indique les entrées intégrées ou exclues. Les noms de fichiers portent désormais une version explicite, au lieu de rester fixés à v06. Le guide et les commandes Windows sont inclus dans le kit.

L'import CSV valide les textes, pas leur capacité réelle dans la ROM : cette vérification intervient lors de la reconstruction. Les formats comprimés, les routines déplacées, les appels français du téléphone et l'introduction restent éditables dans leurs JSON. L'outil n'est pas encore une interface graphique et son CSV n'est pas un export exhaustif de tous les textes anglais.

## Contrôles et essais

Les deux profils passent la vérification indépendante des 718 entrées, l'application IPS, les checksums et la protection des pointeurs et terminaisons partagées. Le profil accents vérifie 80 glyphes dans cinq polices. Les 173 fragments concernés conservent leurs positions.

Le test CSV vérifie l'aller-retour sans modification, l'import partiel et six refus. Il confirme qu'une erreur en fin de CSV ne laisse pas les modifications du début écrites dans les sources. Les tests d'encodage et d'appels du téléphone passent également.

Avec le cœur snes9x2010 `fe690dd321fa5a46b5234a2bde089d2518c62b0e`, les deux ROM finales sont rejouées depuis une nouvelle partie jusqu'au premier combat, sa victoire et le retour à la maison.

Quatre nouveaux dialogues sont également testés dans chaque variante par entrée directe : Abbott (`360871`), le panneau de l'hôtel (`37D046`), les remerciements de la mère de Pippi avec le nom variable (`36115F`) et le garde (`360AD5`). L'essai détourne six octets de « À qui ? » dans une ROM de test distincte ; les métadonnées gardent les empreintes de la ROM finale et de la ROM de test. Les captures confirment le français, les accents, le nom variable et les retours à la ligne. Les espaces conservant les positions fixes peuvent être visibles.

Ces huit essais isolés ne valident pas les trajets dans Podunk, les conditions de quête, les récompenses ni les branches non parcourues. Aucun cœur, ROM, état instantané ou SRAM n'est distribué. Le son et une partie complète ne sont pas validés. Les graphismes anglais restent à traduire.

## Suite

Tester Podunk par le parcours normal, traduire les dialogues longs du maire et de Pippi, poursuivre le cimetière et le zoo, puis intégrer les graphismes anglais. Le kit v07 contient les patchs, les sources, le CSV éditable, les rapports et les captures de ces essais.
