# Reprise — après V64 services

V64 est terminée pour le lot décrit dans `RAPPORT_V64.md` et `tools/v64/README_V64.md`. Consulter le dernier état Git et ne pas écraser les modifications d'une autre exécution. Les IPS actuels sont V64 ; V62/V63 n'ont pas d'IPS. Priorité utilisateur : 100 % des textes visibles, services et accès calculés, puis menus. Main est autorisée ; sauvegarder chaque gros lot.

## Ce qui est validé

Quatre plages bancaires traduites à taille fixe ; tous les enregistrements V61 conservés, aucune allocation, aucune commande/pointeur/sprite changé. 585 tests passent (575 historiques + 4 V63 + 6 V64). V64 : 26 essais contrôlés, 122 captures relues, 22 comparaisons V61/V64 limitées au texte. Le checkpoint du constructeur est `work/v64-services` : `76aa3ce617549fe2d26e87d8ff35e764081e081e`.

Les accès ont été **forcés** vers les scripts du service par une redirection temporaire de quatre octets à `368B51`, puis les touches activent le vrai moteur. Ce n'est pas une visite naturelle sur la carte. Deux cas isolés vérifient l'invite de carte et la consigne de retrait, sans certifier la condition sans carte ni un compte positif. Voir les cases `kind` dans les résultats.

## Prochain lot utile

1. Établir un retrait avec solde positif et vérifier les effets. L'essai de réouverture du distributeur après dépôt via une succession rapide de touches n'a pas réussi à rentrer dans le service : il affichait « À qui ? » et n'a PAS été retenu. Ne pas réutiliser ce chemin comme preuve. Un wrapper contrôlé appelant deux fois le script via `08 pointeur`, dans une zone vérifiée nulle, est une piste à documenter explicitement si nécessaire ; ne pas modifier la ROM publiée pour cela.
2. Acheter un objet stockable, le confier puis le reprendre ; vérifier stock plein, inventaire plein et refus. L'état de départ n'a que la carte bancaire, qui est refusée au stockage. Ne pas revendiquer les branches sans les avoir exécutées.
3. Tester d'autres enseignes, soins/hôtels, autres téléphones. Finir les conversations Maman/Papa et les refus de sauvegarde, plutôt que compter seulement le début d'appel.
4. Examiner les autres anciennes racines NPC sous `330000` que V62 exclut. V64 a trouvé le distributeur ainsi : 17 NPC pointent vers `0680A6`/`0680C2`. Élargir prudemment les graines avec leur provenance réelle ; certaines entrées sont héritées/dormantes. Une occurrence littérale de pointeur peut être une donnée graphique.
5. Piste à qualifier : NPC 149, racine `24D4A0` (soins), mélange français/anglais dans le décodage brut (« you have »). Vérifier les vraies frontières de texte/commandes avant toute modification. Ce n'est pas encore un défaut confirmé à l'écran.

Les menus d'action Use/Eat/Give/Drop/Help! restent pour la phase menus. 100 % des textes visibles n'est pas certifié.

## Dépendances privées de cet espace

Racine : `/workspace/scratch/a52b6a3f0578`, dépôt `earthboundbeginning`.

- ROM : `upload/EarthBound Beginnings (USA) 1.2(2).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- Cœur : `/workspace/scratch/96ddda3e7189/emutest/snes9x_libretro.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.
- États : `emulation_v41/{accents,ascii}/after_combat.state`.
- Runner : `tests/emulation_v18_work/libretro_runner.py` ; `--history-every 120` accélère l'échantillonnage sans perdre les commandes du journal final.
- Assembleur original : `v62_analysis/ebsrc`, Herringway/ebsrc révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`.

Ne jamais publier ROM, cœur, états ou dumps mémoire. Si le scratch est réinitialisé, récupérer main/checkpoints et poursuivre les analyses possibles sans inventer de validation d'émulateur.

## Reprise des outils

`tools/v64/session.py` fournit Session, send, tap, step (échantillonnage par image de la pile DISPLAY_TEXT), capture et close. `tests/emulation_v64/probe.py` décrit treize cas reproductibles. `--version 61` permet la comparaison antérieure ; `--case` rejoue un seul cas dans un répertoire distinct.

Entrées de service déjà explorées :
- `0680A6` : ATM complet, vérifie la carte ; `0680C2` est l'autre champ NPC. Dépôt : A (menu), Right+A (Dépôt), A (consigne), A (nombre), Up+A (1 $), A (merci). Les nombres démarrent sur les unités ; Left puis Up trois fois saisit 30 $.
- `35C597` : téléphone gratuit ; A ouvre Papa/Maman, Down+A choisit Maman. Papa propose la sauvegarde après présentation/niveau/EXP.
- `365592` : boutique (NPC 90), enseigne choisie selon les flags ; A puis A atteint les objets. Fiole de sérum à 20 $ disponible avec la somme initiale.
- `34B490` : stockage (NPC 1002), A ouvre Déposer/Retirer.

Le téléphone de la maison essayé dans `v64_explore` ne donnait que Biiip/R.A.S. ; ne pas le compter comme conversation naturelle réussie.

Sorties privées : `v64_probe`, `v64_withdraw`, `v64_prior`, `v64_controlled`, `v64_atm`, `v64_explore`. Les deux essais ratés de réouverture ATM sont dans `v64_probe/*/atm_deposit_then_withdraw` et `v64_chain_fixed` : exclus des résultats publiés. Le dépôt contient toutes les captures et les références utiles, sans données privées.

## Publication

Le push shell n'a pas d'identifiants. Utiliser les outils GitHub create_blob (base64), create_tree avec base_tree_sha, create_commit puis create_branch pour le checkpoint ; update_ref main avec expected_sha et force=false après validation. Vérifier hashes blobs/arbre local/distant. Les publications API créent un SHA de commit différent du local : fetch puis aligner la branche locale seulement si arbre identique, en conservant une branche d'archive locale. Ne jamais force-pusher main.
