# V66 — téléphone et Escargo Express

## Correction

La conversation complète avec Maman mène au service Escargo Express. Son sélecteur affichait encore **Pick-up / Delivery**, absent des fragments corrigés en V59. V66 le traduit en **Déposer / Retirer**, selon le sens du transfert vers/depuis le stockage. Il s'agit du choix de service dans la conversation ; les menus d'action principaux restent pour la phase suivante.

Deux fragments seulement : `063734–06373B` et `06373E–063746`, contexte analysé `063732`. Remplacement à taille constante, avec un espace final après « Retirer ». Deux enregistrements IPS ajoutés à V65 ; aucun pointeur, commande ou stockage nouveau. Les anciens enregistrements, la banque 25 et l'empreinte des sprites restent inchangés.

## Validation

- Sept tests V66 : portée exacte, séquences/traces, PNG, références, commandes, sprites/banque 25 et empreintes des ROM produites.
- Les 575 tests du runner historique V62, les 4 V63, 6 V64 et 8 V65 repassent : **600 tests réussis au total**, ROM privée fournie aux suites qui l'exigent.
- Douze essais principaux, six par profil : Maman puis demande de dépôt ; Maman puis retrait sur réserve vide ; Papa sans sauvegarde ; même appel payant ; téléphone payant sans argent après achat ; retrait de 2 $ après dépôt de 1 $.
- 36 204 images de moteur échantillonnées et **178 captures relues**, profils accents et ASCII. Les appels retenus vont jusqu'au raccrochage, sauf le distributeur qui revient à l'affichage du solde après le refus.
- Deux essais V65 de référence : dépôt en accents et retrait en ASCII, **48 comparaisons**. Deux paires diffèrent, uniquement dans la fenêtre de texte `(104,8,248,98)` : le sélecteur. Toutes les empreintes PNG/RGB sont recalculables avec les outils fournis.
- Papa « Rien, merci » rejoint « Bon vent ! », puis raccroche. L'appel payant fait passer la poche de 20 à 19 $. Après l'achat qui laisse 0 $, le téléphone refuse avec « Manque d'argent ». Le distributeur garde le compte à 1 $ après la tentative de retrait de 2 $. Ces effets sont lus à l'écran, sans lecture dédiée des champs mémoire d'argent.
- Escargo confirme l'envoi de quelqu'un pour le dépôt ; la branche retrait indique qu'aucun objet n'est en dépôt. L'arrivée du livreur et un transfert réel par coursier ne sont **pas** testés dans ce lot.

Une première exploration du retrait Escargo pressait Droite avant l'ouverture du sélecteur et choisissait donc le dépôt. Elle a été écartée ; le probe publié attend la page 19, puis choisit Droite+A en page 20. La réponse « aucun de tes objets n'est en dépôt » distingue bien la branche retenue.

## Limites et sauvegarde

Les racines `35C597` (gratuit), `35C53A` (payant), `365592` (boutique) et `0680A6` (banque) sont appelées par un **wrapper temporaire**, comme en V65. Ses deux écritures sont déclarées dans les résultats ; les choix suivants utilisent le vrai moteur et la manette, sans écriture directe en WRAM ni hook moteur. Ces essais ne prouvent pas un accès naturel sur la carte. Aucun wrapper ne figure dans les IPS publiés.

Checkpoint Git : `work/v66-services`, commit `e3c3ec3aef576884747a5d817c907fe07884d0a2`. Les ROM, cœur, états et dumps mémoire ne sont pas distribués. Restent les inventaires/réserves pleins, plusieurs personnages, l'arrivée des coursiers, d'autres services et les parcours naturels. **100 % des textes n'est pas certifié.**

Captures : [sélecteur accents](tests/emulation_v66/accents/mom_pickup/page_19.png), [retrait vide accents](tests/emulation_v66/accents/mom_delivery/page_20.png), [sélecteur ASCII](tests/emulation_v66/ascii/mom_pickup/page_19.png), [refus bancaire](tests/emulation_v66/accents/bank_overdraft/page_12.png). Résultats et traces : `tests/emulation_v66/results_{accents,ascii}.json`.
