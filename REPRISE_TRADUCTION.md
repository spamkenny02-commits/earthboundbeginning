# Reprise — V74, revente validée

V74 est le patch actuel : service complet `387221`, PNJ 87 champ 9, opérande `202778` inchangé. Neuf fragments anglais traduits, deux formulations françaises améliorées. Quatre définitions « Non » en stockage protégé (44 octets), 15 enregistrements ajoutés. Voir `RAPPORT_V74.md` et `tools/v74/README_V74.md`.

Quatre scénarios par profil, 56 captures relues et comparées V73/V74, 30 différences textuelles seulement, 12 044 images échantillonnées ; 24 tests ciblés V74/V73/V65 réussis. Vente d'une Fiole : offre 29 $, portefeuille 20 → 49 $, inventaire final carte seule. Refus de l'offre : dialogue et argent vérifiés, inventaire non rouvert. Carte protégée et sortie vérifiées. Entrée forcée par carte bancaire ; don préparatoire natif déclaré, aucune écriture directe WRAM. Branche équipée seulement contrôlée statiquement. Pas d'accès naturel certifié.

**Prochaine priorité : canari `3861D3`/PNJ 291**, puis Pippi `386B63`/319 et autres lignes de `tools/v73/custom_npc_roots_v73.json`, sauf `387221` désormais traité. Ne pas refaire les audits acquis sans raison. Menus `Use/Eat/Give/Drop/Help!` encore anglais ; autres personnages, limites de coursier et parcours naturel complet restent à vérifier. Aucun 100 %.

Sauvegardes locales initiales `a6cd3ef`, `61fbc28`, branches `work/v74-resale-local`, `work/v74-resale-polish-local`. Checkpoint validé : `work/v74-resale-validated`. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v74`, référence `/workspace/scratch/98c4eaa3ef23/reference_v73_resale`. Les deux répertoires `v74_explore` et `v74_sale_explore` sont exploratoires.

Dépendances **actuelles V74** : l'ancien répertoire `60defd300f2e` et les états V33 ne sont plus disponibles. ROM récupérée auprès du fichier utilisateur et vérifiée : `/workspace/scratch/98c4eaa3ef23/private_v74/EarthBound Beginnings (USA) 1.2(1).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`. Cœur : `/workspace/scratch/c267dac1e2c1/emulator/snes9x_libretro_standard.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`. États utilisés : `/workspace/scratch/98c4eaa3ef23/reference_v71_lodging/{accents,ascii}/accept/handoff.state` (post-repos : Ninten, 30 PV, 10 PP, 20 $, carte). Leurs empreintes figurent dans les résultats V74. Ne jamais les présenter comme les états V33. Ne rien publier de ces dépendances. Les paragraphes suivants sont historiques, y compris les anciens chemins.

## Historique V73

V73 est le patch actuel : huit plages du service `37899B` (PNJ 898, opérande `205D53`) traduites, dont Oui/Non. Sept remplacements fixes et un pont de définition de « Non » : saut de cinq octets à `378A32` vers onze octets protégés à `330200`, retour à `378A37`. Les commandes dépliées, branches, scripts de repos, sprites, banque 25 et pointeur PNJ sont préservés. Voir `RAPPORT_V73.md` et `tools/v73/README_V73.md`.

Trois essais dans chaque profil : refus, acceptation et conversation après repos depuis l'état privé de l'acceptation. L'entrée complète est forcée par carte bancaire ; aucun flag ni PV préparé par l'outil. Le jeu exécute le repos et le changement de pièce ; PV observés 18 → 30, PP 10 inchangés. Pas de preuve de rencontre naturelle du PNJ. 40 captures relues, 40 comparaisons dont 18 changements uniquement textuels, 9 296 images échantillonnées et 20 tests ciblés réussis. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v73`, référence `/workspace/scratch/98c4eaa3ef23/reference_v71_lodging`. L'exploration `v73_explore` est privée.

**Prochaine priorité concrète : `387221`, champ 9 du PNJ 87, service de retour d'objets encore anglais.** Lire ensuite `tools/v73/custom_npc_roots_v73.json` : 181 racines directes de `[36BB00,3F0000)` examinées, 11 candidats après V73. Autres pistes : `3861D3`/PNJ 291 (canari), `386B63`/319 (Pippi), `3738F8`/210 (mines), dialogues et sélecteurs. Ce relevé n'est pas une fermeture récursive ni une preuve d'accès naturel/classification linguistique. L'ancien filtre NPC `330000–36BB00` et copies connues omettait ces racines ; ne plus conclure à l'exhaustivité à partir de son graphe sans erreur.

Checkpoint initial distant `work/v73-lodging` : `460ed6283742df76ecc2e0bf42ec1a9b88990976` ; checkpoint validé `work/v73-lodging-validated`. Éviter de refaire les audits V68–V72 sans changement qui le justifie. Réserve pleine/limite de trois côté coursier et autres personnages restent à valider, puis menus généraux, noms tronqués et parcours complet. Aucun 100 % certifié. Les paragraphes suivants sont historiques.

V72 est un audit sans nouvel IPS : **V71 reste le patch actuel**. Voir `RAPPORT_V72.md` et `tools/v72/README_V72.md`. Après dépôt, la réserve contient bien Fiole + sagesse + vitalité. Après livraison de deux objets sur trois, vitalité reste seule ; après livraison d'un sur deux, sagesse reste seule. Ces trois cas sont vérifiés dans les deux profils à partir d'états privés sauvegardés après le départ du coursier : six chaînes, 12 sessions, 174 captures contrôlées, 36 captures clés relues et 10 tests ciblés réussis.

La phase suivante recharge exactement l'état de passage et appelle `34B490`. Après dépôt, aucune opération intermédiaire ; après livraison partielle, retrait natif d'un Badge Franklin de l'inventaire pour libérer une case, sans toucher à la réserve ni au reliquat. Le téléphone initial et l'accès au stockage sont forcés ; le coursier arrive par le mécanisme normal. Les empreintes de passage sont publiées, pas les états. Les six touches d'accès après livraison partielle sont nécessaires ; avec un sac plein, même le bon accès refuse d'ouvrir la réserve. Ne pas compter ces premiers essais comme une lecture de reliquat.

Sorties privées retenues : `/workspace/scratch/98c4eaa3ef23/validated_v72_free_slot`. Les sorties `v72_explore` et `validated_v72` sont exploratoires et non publiées. Checkpoint validé : `work/v72-courier-storage`. Ne pas refaire ces trois contrôles sans nouvelle modification qui les justifie.

Prochain lot concret : branches de coursier sur réserve pleine et limite de trois objets, ou autres enseignes/hôtels pour chercher le prochain anglais réellement affiché. Les cas à plusieurs personnages restent non vérifiés. Ensuite menus d'action et libellés longs tronqués dans certaines listes à deux colonnes ; parcours naturel complet et générique restent nécessaires. Aucun 100 % certifié. Les paragraphes suivants sont historiques.

V71 est le patch actuel : 32 plages traduites en place, commandes, sprites et banque 25 préservés. Voir `RAPPORT_V71.md` et `tools/v71/README_V71.md`. Le wrapper privé accorde trois objets puis appelle le téléphone complet `35C597` ; Maman puis Déposer sont choisis à la manette. Après 600 images, le mécanisme normal du jeu fait arriver le coursier, jamais appelé directement par le test. Le téléphone initial reste artificiel.

Six scénarios dans chaque profil : dépôt de trois objets avec inventaire final, confirmation d'un dépôt simple, paiement refusé, argent nul, carte protégée et confirmation refusée/reprise. Seul le premier certifie l'inventaire final (carte seule) et les frais (20 → 2 $). Les autres s'arrêtent aux dialogues utiles ou au menu. La réserve n'a pas encore été rouverte après le coursier : c'est le prochain lot concret, avec le reliquat des livraisons partielles. Réserve pleine, limite de trois et variante de présentation : traductions statiquement contrôlées, affichage non certifié.

Sorties privées retenues : `/workspace/scratch/98c4eaa3ef23/validated_v71_accepted` et `/workspace/scratch/98c4eaa3ef23/reference_v70_pickup_accepted`. Les tentatives sans suffixe, `_stable` et `_final` contiennent des navigations finales non fiables et ne sont pas les preuves publiées. Ne pas les compter. Le probe public se limite aux séquences acceptées ; la fermeture A/B et des A supplémentaires peuvent laisser le menu actif ou sélectionner Parler au lieu des objets. Garder des sorties distinctes lors d'explorations.

Checkpoint initial local `013572a195040ddbfd10acb8bd6b6fb2e5d5245a`, distant `work/v71-pickup` : `158efc7a433e7207195be2a4f63c7f7e2b1f8615`. Checkpoint validé : `work/v71-pickup-validated`. Les paragraphes suivants sont historiques. Menus d'action encore anglais et parcours complet restant : pas de 100 % certifié.

V70 est le patch actuel : 24 plages du coursier traduites en place, sans allocation ni changement des commandes. Voir `RAPPORT_V70.md` et `tools/v70/README_V70.md`. Douze essais valides, 338 comparaisons V67/V70 dont 92 changements uniquement textuels ; 116 captures de coursier/inventaire relues. Les autres preuves V69 ci-dessous restent historiques.

Le téléphone complet `35C597` est appelé par une fixture privée ; après commande à la manette et attente de 600 images, le coursier arrive par le mécanisme du jeu, sans appel forcé à sa racine `0642A3`. Six cas dans chaque profil : trois objets, sans argent, refus de paiement/retour accepté, retour refusé/nouvelle réponse, deux places libres, une place libre. Frais 18 $ au total, pas par objet. Préparations natives déclarées, aucune écriture directe WRAM.

Prochain reste concret : coursier de dépôt, ou vérifier le reliquat après livraison partielle, puis sac totalement plein et autres personnages. Le cas exploratoire `no_room` n'a pas atteint le dialogue attendu et est exclu des preuves ; ne pas le compter. Le probe public conserve seulement les six cas valides. Les sorties privées principales sont `/workspace/scratch/98c4eaa3ef23/validated_v70`, références `/workspace/scratch/98c4eaa3ef23/reference_v67_courier`. La tentative exclue reste uniquement dans les sorties privées.

Checkpoint initial distant `work/v70-courier` : `80752c2d8a885c370cec00d659282b85e3cc0e78` ; checkpoint validé `work/v70-courier-validated`. Le code de décompression `b.spans_fr` reconnaît les commandes dictionnaire comme texte ; ne pas utiliser les seuls fragments littéraux du parseur pour conclure à l'absence d'anglais. Les menus Use/Eat/Give/Drop/Help! et certains chevauchements de fenêtres préexistants restent à traiter. 100 % non certifié.

V69 est un audit sans nouveau patch : les IPS V67 restent actuels. Voir `RAPPORT_V69.md`. Réserve pleine relue sur quatre pages, 10 + 10 + 10 + 6 = 36 Fioles ; dépôt refusé, retrait normal puis redépôt normal et nouveau refus. Six sessions, 50 captures, 10 676 images échantillonnées. Checkpoint `work/v69-full-storage` : `56bbfdd78971750717a258712ac1105b5fe4c716`.

Préparation privée en trois phases par commandes natives : 13 insertions de réserve `1D 18 70 00`, puis 13 autres, puis 10 et un don à Ninten avant le service. Pas d'écriture directe en WRAM ; états privés chaînés après retour à la carte. Les numéros « Réserve (1)… » désignent les pages, pas des quantités. Pour lire toutes les pages : cinq Bas+A depuis la première, puis A, puis A (le curseur reste sur la ligne de changement de page), enfin Bas avant de sélectionner l'objet. Les essais R ou cinq Bas répétés à chaque page étaient incorrects et ne sont pas des preuves. Les résultats publiés ne reprennent que la séquence correcte. Sorties privées `/workspace/scratch/98c4eaa3ef23/validated_v69`.

V68 est un **audit sans nouveau patch** : les IPS V67 restent actuels et inchangés. Voir `RAPPORT_V68.md` et `tools/v68/README_V68.md`. Retrait sur inventaire plein refusé en français, puis récupération après libération d'une case, avec réserve d'une Fiole encore intacte après le refus puis vide après récupération. Six sessions, 50 captures relues, 10 564 images échantillonnées. Checkpoint `work/v68-storage-audit` : `171a0c75eb39658da9a8db61df24a307c751c33b`.

Le probe V68 chaîne trois états privés après sortie du service. Préparations natives : 13 ajouts de Fiole (ID 70), dépôt normal d'une Fiole ; ajout d'une Fiole pour bloquer le retrait ; suppression d'une Fiole pour libérer une case, puis récupération normale. Ce ne sont pas des préparations naturelles. Les deux dernières phases exigent six touches de déclenchement, pas cinq : sinon l'essai reste au menu d'action et ne prouve rien. Les empreintes des états de passage, pas leurs contenus, sont conservées dans les résultats. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v68` ; exploration antérieure `v68_explore` non exhaustive. Aucun nouvel accès naturel certifié.

V67 est le patch actuel : `37BBB0` et `37BBBB`, « Just one / Multiple » → « Un seul / En lot », à taille constante. Voir `RAPPORT_V67.md`. 14 essais principaux, 86 captures relues, 18 476 images échantillonnées, 86 comparaisons V66/V67 dont six sélecteurs changent seulement dans la fenêtre de texte. Checkpoint `work/v67-quantity` : `3e9c380fe117780c612a71753ac04b106e67971c`.

Les préparations d'inventaire sont **artificielles et déclarées** : treize commandes natives `1D 00 01 01` ajoutent des Badges Franklin avant le service. Elles restent dans la fixture privée, jamais dans l'IPS. L'inventaire de 14 cases et le refus d'achat sont visibles ; le retrait vers un inventaire plein reste non testé. L'achat en lot de 1, le refus de 2 faute d'argent, le stockage vide et les soins acceptés sont contrôlés dans les deux profils. Aucun nouvel accès naturel certifié.

L'ancien dépôt local V38 `/workspace/scratch/60defd300f2e/earthboundbeginning` a une archive modifiée et reste intact. Le travail courant est dans `/workspace/scratch/98c4eaa3ef23/earthboundbeginning`, copie propre issue de main V66. Les chemins de dépendances ci-dessous sont mis à jour ; les anciens états V41 n'ont pas été retrouvés, les références V66 ont été rejouées avec les états V33.

V66 ajoute deux traductions à taille fixe : sélecteur Escargo `063734` / `06373E`, « Pick-up / Delivery » → « Déposer / Retirer ». Voir `RAPPORT_V66.md` et `tools/v66/README_V66.md`. Douze essais principaux, 178 captures relues, 36 204 images échantillonnées et 48 comparaisons avec V65 (deux paires changent, seulement le sélecteur). Checkpoint `work/v66-services` : `e3c3ec3aef576884747a5d817c907fe07884d0a2`.

Les fins d'appel Papa sans sauvegarde (gratuit/payant), le refus du téléphone sans argent, le refus bancaire de 2 $ sur compte de 1 $, Maman puis les deux choix Escargo sont maintenant contrôlés dans les deux profils. Les appels sont forcés comme en V65 : pas de nouvel accès naturel prouvé. Escargo demande un coursier au dépôt et indique une réserve vide au retrait ; son arrivée et les transferts restent à tester. Attention : ouvrir le sélecteur avec A en page 19, puis Droite+A en page 20 pour choisir réellement Retirer. L'ancienne exploration anticipait Droite et n'est pas une preuve de retrait.

V65 est terminée pour le lot décrit dans `RAPPORT_V65.md` et `tools/v65/README_V65.md`. Consulter le dernier état Git et ne pas écraser les modifications d'une autre exécution. V62/V63 n'ont pas d'IPS. Priorité utilisateur : 100 % des textes visibles, services et accès calculés, puis menus. Main est autorisée ; sauvegarder chaque gros lot.

## Ce qui est validé

V64 reste la base : quatre plages bancaires traduites. V65 corrige deux confirmations « The Fiole de sérum » au dépôt et à la récupération. L'auxiliaire partagé `38B587` est inchangé ; une copie privée conserve sa classification/dispatch et retourne sans article anglais. La phrase de dépôt devient « Cet objet sera bien au chaud. ».

Attention au stockage historique : le pointeur de récupération `259B27` est dans une ancienne copie qui chevauche des sprites. Ne pas le modifier directement. V65 relocalise les sept scripts de banque 25 du graphe de `34B490` dans neuf blocs de remplissage protégé : 338 octets sources + 10 octets de sauts + 27 octets d'auxiliaire = 375 octets. Banque 25, auxiliaire original et sprites restent identiques à V64. Voir fixtures, reconstructeur et tests V65. `330FC0–331000` est exclu de l'allocation pour conserver le créneau des probes.

593 tests passent (575 historiques + 4 V63 + 6 V64 + 8 V65). Six essais V65, 84 captures relues, 40 comparaisons V64/V65 limitées au texte. Checkpoint final du code : `work/v65-storage-safe`, `a3081132ab378f643d36ebfaa1e6e230e179b6e6`.

Les accès ont été **forcés** par un wrapper temporaire à `330FC0`, appelé par la redirection de quatre octets à `368B51`. Le wrapper enchaîne uniquement `08 pointeur` vers les scripts complets puis `02`. Les touches activent ensuite le vrai moteur ; aucune écriture directe en WRAM ni callback assembleur. Ce n'est pas une visite naturelle sur la carte.

Le cycle bancaire fait trois appels du distributeur : dépôt de 1 $, retrait de 1 $, puis refus sur compte redevenu nul. La poche revient de 19 à 20 $. Le stockage enchaîne achat puis service : dépôt confirmé, réserve contenant une Fiole, récupération confirmée, puis réserve vide. Les effets sont vérifiés à l'écran, pas par lecture dédiée des champs mémoire d'argent/inventaire.

## Prochain lot utile

1. Tester les plafonds et annulations supplémentaires ; retrait positif validé en V65, refus au-delà du solde en V66. L'ancienne réouverture via le menu principal n'était pas fiable et ne doit pas être utilisée comme preuve.
2. Vérifier plusieurs personnages et objets variés. Le retrait bloqué par inventaire plein est contrôlé en V68, la réserve pleine en V69, pour Ninten seul ; ne pas étendre ces preuves à d'autres configurations. Les préparations par commandes natives doivent rester explicitement déclarées et hors des IPS publiés.
3. Tester d'autres enseignes, hôtels, autres téléphones et effets des coursiers. Les fins d'appel Maman/Papa sans sauvegarde sont relues en V66 ; les soins acceptés en V67. Ne pas étendre cette preuve aux autres configurations.
4. Examiner les autres anciennes racines NPC sous `330000` que V62 exclut. V64 a trouvé le distributeur ainsi : 17 NPC pointent vers `0680A6`/`0680C2`. Élargir prudemment les graines avec leur provenance réelle ; certaines entrées sont héritées/dormantes. Une occurrence littérale de pointeur peut être une donnée graphique.
5. Piste du soigneur classée : NPC 149, racine `24D4A0`, « you have » est un faux positif. Les octets `15 0D` traversent les commandes `1A 15` et `0D 00` et ne sont pas un fragment textuel. La branche de refus est relue dans les deux profils ; ce contexte n'est pas modifié par V65.

Les menus d'action Use/Eat/Give/Drop/Help! restent pour la phase menus. 100 % des textes visibles n'est pas certifié.

## Dépendances privées de cet espace

Dépôt courant : `/workspace/scratch/98c4eaa3ef23/earthboundbeginning`.

- ROM : `/workspace/scratch/60defd300f2e/downloads/EarthBound Beginnings (USA) 1.2(1).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- Cœur : `/workspace/scratch/c267dac1e2c1/emulator/snes9x_libretro_standard.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.
- États V33 : `/workspace/scratch/60defd300f2e/emulation_v33/{accents,ascii}/after_combat.state`. SHA256 : accents `622aa30903aeffe159b1b748d8537776a7a2c092dda3ef70eeca26434acaf4a7`, ASCII `9364b593e11b3beeb993dfe8c63f161362f1a6e1c31402f332f5484ff9aa2ee0`.
- Runner : `tests/emulation_v18_work/libretro_runner.py` ; `--history-every 120` accélère l'échantillonnage sans perdre les commandes du journal final.
- Assembleur original : `v62_analysis/ebsrc`, Herringway/ebsrc révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`.

Ne jamais publier ROM, cœur, états ou dumps mémoire. Si le scratch est réinitialisé, récupérer main/checkpoints et poursuivre les analyses possibles sans inventer de validation d'émulateur.

## Reprise des outils

`tools/v65/service_session.py` hérite des opérations du runner V64 et ajoute le wrapper de services successifs. `tests/emulation_v65/probe.py` décrit les trois scénarios retenus. `--version 64 --case buy_store_retrieve` rejoue la référence ; utiliser une sortie distincte. Les cas V64 restent disponibles pour les essais simples.

Pour le stockage V65, ne pas précipiter les menus : après dépôt, A affiche Oui/Non ; Right+A (Non) revient à Déposer/Retirer ; Right+A (Retirer) affiche la question de récupération ; A ouvre la réserve, A choisit la Fiole, A choisit Ninten ; la confirmation suit. La séquence complète est dans le probe.

Entrées de service déjà explorées :
- `0680A6` : ATM complet, vérifie la carte ; `0680C2` est l'autre champ NPC. Dépôt : A (menu), Right+A (Dépôt), A (consigne), A (nombre), Up+A (1 $), A (merci). Les nombres démarrent sur les unités ; Left puis Up trois fois saisit 30 $.
- `35C597` : téléphone gratuit ; A ouvre Papa/Maman, Down+A choisit Maman. Papa propose la sauvegarde après présentation/niveau/EXP.
- `365592` : boutique (NPC 90), enseigne choisie selon les flags ; A puis A atteint les objets. Fiole de sérum à 20 $ disponible avec la somme initiale.
- `34B490` : stockage (NPC 1002), A ouvre Déposer/Retirer.

Le téléphone de la maison essayé dans `v64_explore` ne donnait que Biiip/R.A.S. ; ne pas le compter comme conversation naturelle réussie.

Sorties privées V65 : `/workspace/scratch/98c4eaa3ef23/validated_v65`, `reference_v64`, `explore`, `regressions_v65.log`. Les explorations intermédiaires ne sont pas toutes validées ; seuls les résultats publiés décrivent les séquences retenues. Les dépendances ROM/cœur/états restent aux chemins ci-dessus. Le dépôt contient les captures et références utiles, sans données privées.

## Publication

Le push shell n'a pas d'identifiants. Utiliser les outils GitHub create_blob (base64), create_tree avec base_tree_sha, create_commit puis create_branch pour le checkpoint ; update_ref main avec expected_sha et force=false après validation. Vérifier hashes blobs/arbre local/distant. Les publications API créent un SHA de commit différent du local : fetch puis aligner la branche locale seulement si arbre identique, en conservant une branche d'archive locale. Ne jamais force-pusher main.
