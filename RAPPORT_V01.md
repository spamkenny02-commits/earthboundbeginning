# Première traduction et intégration française

## Livrable

393 éléments intégrés : **317 champs textuels, 74 blocs de dialogue et 2 séquences de l'introduction**. Parmi les champs figurent 215 noms d'objets modifiés. Les traductions sont des premières versions adaptées aux contraintes de place, à relire et tester en jeu.

16 caractères ajoutés : é è ê ë à â î ï ô ù û ü ç É À Ç. Codes B0–BF, glyphes 96–111. Les 80 cellules correspondantes dans les cinq polices étaient entièrement FF avant modification. La largeur de chaque lettre de base est réutilisée. La petite police 8×8 compresse certaines majuscules pour faire tenir l'accent : sa lisibilité doit être contrôlée en jeu. Voir `docs/polices_fr_v01.png` (aperçu technique, pas une capture d'émulateur).

La ROM conserve sa taille de 4 Mio. Aucun pointeur n'a été déplacé. Les commandes de dialogue et leurs paramètres sont conservés. 10 blocs contenant des pointeurs intérieurs utilisent des espaces de remplissage dans chaque fragment de texte pour conserver les positions exactes ; la mise en page doit être vérifiée en jeu. Les autres dialogues sont raccourcis à leur adresse d'origine, avec remplissage nul après la terminaison.

Les champs de menu n'utilisent que la place réellement observée. La table des objets possède des champs de nom de 25 octets dans des enregistrements de 39 octets : seuls ces 25 octets sont modifiés. Cinq libellés restent anglais faute de place prouvée : No dans la confirmation de suppression, Beam, Sick, Cold et Sing. Leurs traductions françaises sont conservées dans le fichier éditable et consignées comme rejetées dans les rapports.

## Vérifications effectuées

- SHA-256 de la ROM source contrôlé ; le fichier original reste inchangé.
- Application IPS reproduite avec un second lecteur indépendant.
- Taille, en-tête HiROM et checksum vérifiés.
- Relecture des 393 intégrations et conservation de la séquence des commandes.
- Positions conservées dans les blocs à pointeurs intérieurs.
- Emplacements des 80 glyphes, données des glyphes et tables de largeurs vérifiés.
- Variante sans accents : données des polices strictement inchangées.
- Application avec retrait d'un en-tête copieur de 512 octets vérifiée.

Résultats détaillés : `patches/verification_integration.json` et `patches/rapport_accents.json`.

## Limites

**Le patch est partiel et expérimental. Aucun parcours en émulateur n'a été validé.** La majorité du scénario, les noms d'ennemis, les textes PSI, les crédits et les textes intégrés aux images restent à traduire. Les champs hérités peuvent ne pas être utilisés par le remake. La traduction finale pourra nécessiter une relocation pour retrouver une formulation plus naturelle et éviter les contraintes de longueur. Les espaces de remplissage et les largeurs des fenêtres demandent une vérification visuelle.

La comparaison avec la traduction française NES de Mother n'a pas été commencée.
