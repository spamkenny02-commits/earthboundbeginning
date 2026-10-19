# V67 — quantités en boutique et inventaire plein

## Traduction

Le sélecteur de quantité du service d'achat affichait encore **Just one / Multiple**. Il devient **Un seul / En lot** dans les profils accents et ASCII. Deux fragments à taille constante : `37BBB0–37BBB8` et `37BBBB–37BBC3`, contexte `37BBAE`. Les espaces restants sont conservés comme remplissage. Aucun pointeur, commande ou stockage nouveau ; les enregistrements V66, la banque 25 et l'empreinte des sprites sont préservés. Les menus d'action généraux restent pour la phase suivante.

## Essais et preuves

Sept scénarios par profil, soit **14 essais V67, 86 captures relues et 18 476 images échantillonnées** :

| Scénario | Résultat relu à l'écran |
| --- | --- |
| Achat « Un seul » | Fiole à 20 $, poche 20 → 0 $, confirmation française |
| Achat « En lot », quantité 1 | Même coût et confirmation ; la saisie numérique est atteinte |
| Achat « En lot », quantité 2 | Refus « Tu n'as pas assez pour tout payer », poche inchangée à 20 $ |
| Achat avec inventaire plein | Refus « Tu portes trop de choses », sans paiement |
| Dépôt avec inventaire plein | 14 cases visibles : carte + 13 Badges Franklin ; la carte sélectionnée est refusée au dépôt |
| Retrait sur réserve vide | « Je ne garde aucun objet à toi » |
| Soins acceptés | Coût 10 $, poche 20 → 10 $, PV 18 → 30, « Te voilà guéri » |

Les montants et PV sont constatés à l'écran, sans lecture dédiée des champs mémoire. L'essai d'inventaire plein au stockage **n'est pas** un retrait vers un inventaire plein : seule la présentation de l'inventaire et le refus d'un objet protégé sont validés.

Les 14 mêmes scénarios sont rejoués avec V66 : **86 paires de captures**, dont six diffèrent uniquement dans la fenêtre de texte `(104,8,248,98)`, au sélecteur de quantité. Les 80 autres paires sont identiques en RGB. Les fichiers PNG, leurs empreintes et les transitions de curseur sont contrôlés hors émulateur. Huit tests V67 s'ajoutent aux suites antérieures.

Les 575 tests historiques V62, les 4 V63, 6 V64, 8 V65 et 7 V66 repassent, ainsi que les 8 V67 : **608 tests réussis**, avec la ROM privée fournie aux suites qui l'exigent. Le contrôle sans ROM exécute cinq tests V67 et ignore explicitement les trois tests privés.

## Méthode contrôlée, pas d'accès naturel revendiqué

Comme en V65/V66, un pointeur temporaire `368B51` appelle un wrapper à `330FC0`. Il appelle les racines complètes `365592`, `34B490` ou `24D4A0`, puis les touches utilisent le vrai moteur.

Nouveauté explicite : deux scénarios préparent l'inventaire par **treize commandes natives `1D 00 01 01`** avant l'appel du service. La convention `1D 00 personnage objet` est décrite par `EBTEXT_GIVE_ITEM_TO_CHARACTER` dans la source primaire Herringway/ebsrc (`include/textmacros.asm`, `src/text/ccs/give_item_to_character.asm`). Le rendu confirme l'ajout de treize objets 01, nommés Badge Franklin. La fixture tient dans les 64 octets réservés (52 octets de préparation + 5 d'appel + 1 retour = 58 octets). Les deux plages écrites sont déclarées dans chaque résultat et tous les autres octets sont vérifiés identiques au patch testé. Aucun hook assembleur, écriture directe en WRAM ou ajout d'objet dans l'IPS distribué.

Les anciens chemins privés ont disparu. La ROM et le cœur retrouvés ont les mêmes SHA256 qu'en V66. Les états V41 ne sont plus disponibles ; les états V33 retrouvés sont différents, leurs empreintes sont enregistrées dans les résultats. Leur point de départ est relu dans l'émulateur : Ninten seul à la maison, carte bancaire, 20 $, PV 18. Les références V66 sont **rejouées avec ces mêmes états**, et non comparées à des captures produites avec un autre état.

Source primaire consultée à la révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62` : [macro](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/include/textmacros.asm) et [handler natif](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/src/text/ccs/give_item_to_character.asm). La source explique la convention ; l'inventaire et le refus sont confirmés dans le remake par les captures, pas supposés depuis le seul code d'EarthBound.

## Sauvegarde et limites

Checkpoint : `work/v67-quantity`, `3e9c380fe117780c612a71753ac04b106e67971c`. ROM, cœur, états et dumps mémoire restent privés. Les captures et les traces de pointeurs ne contiennent pas ces fichiers.

Restent notamment : retrait d'un objet vers un inventaire plein, réserve pleine, plusieurs personnages, arrivée et transferts des coursiers, autres commerçants et accès naturels. **Aucun taux de couverture globale ni 100 % des textes n'est certifié.**

Exemples : [quantités](tests/emulation_v67/accents/shop_single/page_03.png), [refus de quantité](tests/emulation_v67/accents/shop_bulk_no_money/page_05.png), [inventaire plein](tests/emulation_v67/accents/storage_full_inventory/page_03.png), [soins](tests/emulation_v67/accents/doctor_accept/page_04.png).
