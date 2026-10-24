# V78 — saisie du nom du joueur et générique

Une correction de français existant, **zéro nouvelle source anglaise**. Les traductions et relectures précédentes ne sont pas recomptées : historique249 sources distinctes/297 plages,137 publiées/112 en attente ; aucune conclusion sur un reste global inférieur à400.

## Invite tronquée corrigée

Le clavier natif affichait « Inscris ton nom, s'il te p » : l'ancienne traduction a30 caractères, tandis que le lecteur01EB54 demande26 octets à PRINT_STRING. L'invite devient « Inscris ton nom : », terminée par zéro, entièrement visible.

La garde vérifie le chargement immédiat du pointeur03FB2B et la constante26 par les octets `a92bfb850ea9c3008510a91a0020fc0e228b8fc0`. Les36 octets du champ et de son remplissage original sont seuls réécrits : l'ancien texte français avait déjà utilisé une partie des zéros d'origine. Le lecteur natif, les champs voisins et tous les autres octets de la ROM cible restent identiques au checkpoint précédent. Aucun pointeur déplacé, aucune allocation ni modification de police.

## Saisie native et affichage final

La préparation appelle le dialogue existant35CA21, qui ouvre le clavier par1F4103, puis l'entrée de fin38ECEB. Les touches saisissent A ou24 A et confirment dans les deux fenêtres natives du dialogue. Aucun nom n'est écrit directement en WRAM. Après le retour du dialogue, la fin appelle elle-même les crédits puis la boucle téléphonique : le probe ne saute pas directement au texte ou à l'image du générique.

Quatre cas par build : longueurs1 et24, profils accents et ASCII. Les32 PNG publics représentent16 paires avant/après : clavier vide, rempli, confirmation, puis une vue du générique. Les seules différences sont dans le bandeau de l'invite ; les vues de noms du générique sont identiques. Les captures retenues ont été relues visuellement.

Le nom complet est aussi contrôlé par ses masques de glyphes natifs, dans la même image que « JOUEUR », avec leur alignement vertical relatif observé de11 pixels. Une lettre A isolée ailleurs dans les crédits ne suffit donc pas à valider le cas court. Le cas long occupe192 pixels entre x32 et224, sans troncature. Les24 A sont bien ceux entrés au clavier, pas le nom du héros Ninten. La police vient de la ROM source privée ; seuls les résultats typés et PNG sont distribués.

Les anciennes preuves montrant JOUEUR avec un nom vide depuis un état précoce restent historiques et inchangées. Ce complément qualifie la chaîne **saisie native → fin forcée → nom rendu** pour les deux chaînes testées. Il ne prouve ni déclenchement naturel de l'appel demandant le nom, ni victoire finale, ni parcours de partie, ni toutes les combinaisons de caractères possibles.

Sources primaires locales : ebsrc révision68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62, `src/unknown/C1/C1BEFC.asm`, `src/text/enter_your_name_please.asm`, `src/ending/credits_scroll_frame.asm` et `include/structs.asm`. L'événement1F4103 sélectionne le registre de nom du joueur ; les crédits lisent earthbound_playername. Preuves : `tests/emulation_v78_player_name/coverage.json`.

## Contrôles et sauvegarde

84 tests V78 passent avec la ROM privée, dont le contrôle des limites du champ, le rejet d'un lecteur altéré, les différences de pixels et les noms complets sous JOUEUR. Reconstruction complète et IPS intégrés concordants ; inventaires dépendants actualisés. Une préparation intermédiaire a été arrêtée par la garde de checksum avant lancement de l'émulateur ; le build, les deux profils et leurs métadonnées ont ensuite été reconstruits et synchronisés séquentiellement avant les essais finaux.

| Profil | SHA256 IPS | SHA256 cible privée |
| --- | --- | --- |
| accents | `5438417ce3d21279db9b1d8b3aaa30c220c176d42885723304881ab96cc34b9b` | `76f4f91c686a5f8be12d4888b0b38fecda99c234696e65c5f521c79bf13ca1de` |
| ascii | `58eb6d9d9064dff348eb953d4fbb1b705bd75218f112e2e46bb2d865c16befa3` | `4646162343c04ddba12bd8fcabed1c3e00e6b904d58217ab60a5718b00f77804` |

Pas de release V78, pas de400 nouvelles traductions, pas de100% annoncé. Poursuivre les courts libellés, les autres assemblages de texte, la fidélité bilingue et les graphiques ; l'accès naturel aux scènes de fin reste ouvert. Le nom dynamique testé ne doit plus être repris comme « jamais affiché » ; ses limites naturelles et de jeu de caractères restent explicites. Aucun ROM, cœur, état ni dump mémoire distribué.
