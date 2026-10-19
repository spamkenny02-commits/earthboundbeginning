# V70 — livraison Escargo Express

Le coursier réellement arrivé après une commande téléphonique affichait encore « I'm from Escargo Express!! », les frais et ses réponses en anglais. V70 traduit **24 plages textuelles** des scripts `0642A3`, `0643A7`, `06442F`, `06445F`, `0644A0`, `0644E3` et `064600`. Les deux IPS intègrent V67 et s'appliquent directement à la ROM originale USA 1.2, jamais à une ROM déjà patchée.

Les remplacements sont à taille constante, sans réécriture de pointeur ni allocation. Les commandes natives, sprites et banque 25 restent identiques à V67. Le reconstructeur vérifie la décompression anglaise avant chaque remplacement ; les codes de dictionnaire sont du texte et ne doivent pas découper les plages en fragments littéraux.

## Validation de l'affichage et des effets

Douze essais retenus, six scénarios dans les profils accents et ASCII :

| Scénario | Résultat observé |
| --- | --- |
| Trois objets distincts | Fiole, capsule de sagesse et capsule de vitalité reçues ; poche de 20 à 2 $ |
| Sans argent | Refus en français, aucun objet reçu |
| Refus de paiement puis retour accepté | Objets non reçus, « Rappelle-nous » |
| Retour refusé puis réponse à la nouvelle question | « Que faire ? », « Tu es sans argent ? », puis objets reçus selon les choix du probe |
| Deux cases libres pour trois objets | « Trop chargé », deux objets reçus, frais de 18 $ |
| Une case libre pour deux objets | « Trop chargé », une Fiole reçue, frais de 18 $ |

Les frais de 18 $ sont ceux de la livraison complète, pas de chaque objet. Le retour effectif du reliquat dans la réserve après livraison partielle n'est pas encore relu. L'inventaire plein de Badges révèle aussi un défaut d'affichage préexistant du menu superposé, identique dans V67 et V70 ; les menus restent à traiter.

**338 captures principales et 338 références V67** sont comparées à entrées manette et préparations identiques ; 92 paires changent, uniquement dans la fenêtre de texte `(104,8,248,98)`. Les 116 captures du coursier et des inventaires finaux ont été relues visuellement dans les deux profils. Les autres captures documentent la commande téléphonique. Les traces totalisent **112 364 images échantillonnées** pour les essais principaux.

La préparation d'inventaire/réserve et d'argent utilise des commandes natives dans une fixture privée. L'appel complet `35C597` est forcé via un wrapper à `330FC0` et une redirection à `368B51`. **Le script du coursier n'est jamais appelé par le test** : après la commande par la manette, une attente de 600 images laisse le mécanisme de livraison normal déclencher son arrivée chez Ninten. Cela prouve cette arrivée et ses branches dans cette configuration, pas un parcours naturel préalable jusqu'au téléphone. Aucun accès direct en écriture à la WRAM, aucun callback assembleur de test.

Un essai à zéro case libre n'a pas atteint le dialogue attendu. Il est exclu des résultats et des captures publiés ; « Sac plein. Rappelle-nous. » est traduit et contrôlé statiquement, mais son affichage n'est pas certifié. Ne pas réutiliser cette tentative comme preuve.

## Reproduction et sauvegardes

Les 575 tests historiques du runner V62, les 45 tests V63–V69 et les cinq tests V70 passent avec la ROM privée fournie : **625 tests réussis**. La vérification RGB des 338 paires passe également. Ces suites contrôlent chaque version historique contre sa propre base ; elles ne remplacent pas un parcours complet du jeu sur V70.

Voir [les outils V70](tools/v70/README_V70.md), [les résultats accents](tests/emulation_v70/results_accents.json), [ASCII](tests/emulation_v70/results_ascii.json) et [les comparaisons](tests/emulation_v70/comparison_v67.json). Cinq tests V70 vérifient les IPS, scénarios, préparations strictes, traces, commandes, sprites et empreintes des fixtures ; `verify_display.py` vérifie chaque PNG et chaque différence RGB. Le test privé est explicitement ignoré sans ROM.

Checkpoint initial local `7f5cca444e00d59eec019d94268e84c559146ffa`, distant `work/v70-courier` : `80752c2d8a885c370cec00d659282b85e3cc0e78`. Ce checkpoint précède les preuves et la correction du périmètre des essais. Le lot validé est sauvegardé séparément avant publication sur main.

Empreintes IPS SHA-256 : accents `79b78c5218611b0e2d4fcd9816857aaed1042add24800ef74493a415b1426dad` ; ASCII `341e0647fe18eb1f423dab36319007059c58ce7fd8b9961f9319c6158dfe8b8b`.

Restent notamment le coursier de dépôt, le reliquat des livraisons partielles, le sac entièrement plein, plusieurs personnages, autres enseignes et hôtels, puis les menus d'action anglais et la relecture d'un parcours complet. Aucun pourcentage exhaustif ni achèvement global n'est certifié. ROM, cœur, états et dumps restent privés.
