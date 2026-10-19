# V73 — hébergement et racines personnalisées oubliées

Le script d'hébergement `37899B`, référencé par le champ 9 du PNJ 898, conservait son premier accueil et ses choix en anglais. V73 traduit **huit plages** : accueil, absence du père, argent, proposition de dormir, « Oui/Non » et interjection de refus. Les autres réponses françaises existantes sont conservées. Les IPS incluent V71 et s'appliquent directement à la ROM originale USA 1.2.

## Modification et sécurité

Sept remplacements sont à taille constante. La définition de « No » (`378A32–378A37`) ne permet pas d'écrire « Non » en place. Un saut de cinq octets mène donc à une définition française de six octets, suivie d'un saut vers `378A37` : onze octets alloués dans le remplissage protégé, à `330200`. Les choix et branches restent natifs. Après dépliage du pont, les commandes sont identiques à l'original. Le pointeur du PNJ, les scripts de repos, la banque 25, les sprites et le créneau de probe restent inchangés.

L'allocateur exclut les images de sprites, tous les records précédents, les cibles de pointeurs des deux profils et la zone `330FC0–331000`. Les neuf nouveaux records IPS sont testés, ainsi que les empreintes des ROM reconstruites. Aucun trou arbitraire en banque 25 n'est utilisé.

## Vérification en jeu

Trois essais dans chaque profil accents/ASCII, avec références V71 aux mêmes touches : refus de la nuit, acceptation et conversation suivante depuis l'état sauvegardé après repos. Le sélecteur affiche bien « Oui/Non ». Accepter déclenche la séquence normale du jeu et le changement de pièce ; les PV de Ninten passent visiblement de 18 à 30. Les PP restent à 10 : aucune preuve supplémentaire de récupération des PP n'est revendiquée. La conversation suivante affiche « Bonjour ! », atteignant la branche après repos sans flag préparé par l'outil.

L'entrée complète est **forcée par une fixture privée** depuis l'action de carte bancaire. Aucun appel direct de la routine de repos, aucune écriture de flag ou de WRAM. Le lien dans la configuration du PNJ est vérifié ; cela ne constitue pas une preuve de sa rencontre naturelle sur la carte. Ne pas présenter la première scène, déclenchée depuis la maison de Ninten, comme une visite à ce PNJ.

**40 captures principales et 40 références V71** sont comparées : 18 paires changent, uniquement dans la fenêtre de texte `(104,8,248,98)`. Les 40 captures principales ont été relues visuellement, y compris le menu, le repos, le statut et le retour. Les traces principales totalisent **9 296 images échantillonnées**. Huit tests V73 vérifient les records, le pont, l'allocation, les commandes, les traces, les fixtures, les captures et le relevé de racines. Les tests privés sont explicitement ignorés sans ROM.

## Reste concret découvert

L'ancien filtre des racines PNJ ne prenait directement que `330000–36BB00` et certaines copies connues. Cette racine personnalisée à `37899B` était donc omise malgré sa référence PNJ. Le nouveau relevé direct de `[36BB00,3F0000)` examine **181 racines** et conserve **11 candidats anglais après V73**, dont le service de retour d'objets `387221` (PNJ 87), le canari `3861D3` (PNJ 291), Pippi `386B63` (PNJ 319), les mines `3738F8` (PNJ 210) et plusieurs dialogues/sélecteurs. Voir [le relevé](tools/v73/custom_npc_roots_v73.json).

Ce relevé n'est pas récursif, son filtre de mots n'est pas une classification de langue et les références PNJ ne prouvent pas les placements actifs sur la carte. Il fournit des prochains lots précis, pas une certification de couverture. Priorité suivante : le service `387221`, puis les autres textes visibles candidats avant les menus généraux. Réserve pleine/limite de trois côté coursier, autres personnages, parcours naturel et générique restent également à valider. Aucun 100 % certifié.

## Reproduction et sauvegardes

Les huit tests V73 et les douze tests ciblés V65/V71 passent avec la ROM privée fournie : **20 tests ciblés réussis**. La suite historique complète n'est pas relancée dans ce lot. Le contrôle RGB des 40 paires passe aussi ; les résultats des anciennes suites restent ceux de leurs rapports respectifs.

Voir [les outils V73](tools/v73/README_V73.md), [résultats accents](tests/emulation_v73/results_accents.json), [ASCII](tests/emulation_v73/results_ascii.json) et [comparaisons](tests/emulation_v73/comparison_v71.json). Checkpoint initial local `c9440a1c9ab4ec467bb8d8391322b2dd9ef50ea8`, distant `work/v73-lodging` : `460ed6283742df76ecc2e0bf42ec1a9b88990976`. Le checkpoint validé est conservé sous `work/v73-lodging-validated` avant publication sur main. ROM, cœur, états et dumps ne sont pas distribués.

SHA-256 IPS : accents `849f17f6bb7c115be2ce671611da4bae557647c25e72572f1bda9141581e3459` ; ASCII `12594efae377c46a70bab92f38057468c55d4cc15e42b02e53936dd05310c310`.
