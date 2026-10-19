# Reprise — après audit V68 du stockage

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
2. Vérifier réserve pleine et plusieurs personnages. Le retrait bloqué par inventaire plein puis la récupération après libération d'une case sont contrôlés en V68 pour Ninten seul ; ne pas étendre cette preuve à d'autres configurations. L'état de départ n'a que la carte bancaire. Les préparations par commandes natives doivent rester explicitement déclarées et hors des IPS publiés.
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
