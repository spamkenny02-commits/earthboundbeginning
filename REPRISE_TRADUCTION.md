# Reprise — services V64 en cours

État au 18 octobre 2026, avant les reprises horaires demandées jusqu'au 19 octobre à 10 h (Europe/Paris).

## État Git

Main validée : V63, `9febeb8c59007af0f4c4a1b2a28068a35002c598`. V64 est un **checkpoint de travail**, pas encore validée ni publiée sur main. Ne pas annoncer V64 terminée avant les essais et contrôles ci-dessous. Ne pas laisser ce fichier figé : le mettre à jour après chaque lot.

Le lot actuel a trouvé quatre fragments bancaires anglais et construit deux IPS autonomes V64 à partir de V61 (V62/V63 n'ont pas d'IPS). Aucun pointeur, aucune commande et aucun sprite modifiés ; quatre plages textuelles de taille fixe seulement. Les vérifications du constructeur passent. Le dépôt contient `tools/v64/build_v64.py`, les fixtures/manifeste et `tools/v64/session.py` (contrôleur d'émulateur, lecture de WRAM uniquement, redirection facultative de l'action carte bancaire).

## Découverte importante

Les graines V62 écartent de nombreuses racines NPC originales sous 330000. L'ATM utilise encore `0680A6` (champ 9) et `0680C2` (champ 13), notamment NPC 61, 406, 488, 716, 937, etc. Il ne faut pas conclure à 100 % sur le seul graphe V62.

- `0680B0–0680C0` : Please insert your ATM card → Mets ta carte.
- `38247B–382486` : Balance → Solde.
- `3824A7–3824D0` : Please enter the amount of your deposit → Saisis le montant de ton dépôt.
- `3824D2–3824DD` : Balance → Solde.

Le champ 9 de l'ATM teste la carte puis rejoint `062D30`, qui saute vers `382113`. Le menu et la plupart des réponses bancaires étaient déjà français ; seuls les quatre fragments ci-dessus ont été changés. Le champ 13 saute vers `35CE10`. Ne pas semer toutes les occurrences littérales sans validation : données héritées ou graphiques possibles.

## Dépendances privées disponibles dans cet espace

Racine : `/workspace/scratch/a52b6a3f0578`.

- ROM : `upload/EarthBound Beginnings (USA) 1.2(2).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- Cœur : `/workspace/scratch/96ddda3e7189/emutest/snes9x_libretro.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.
- États : `emulation_v41/{accents,ascii}/after_combat.state`.
- Runner : `tests/emulation_v18_work/libretro_runner.py`.
- Sources assembleur : `v62_analysis/ebsrc`, révision Herringway/ebsrc `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`.

Ne jamais publier ROM, cœur, états ou dumps mémoire. Si l'espace a été réinitialisé, récupérer le checkpoint de travail depuis Git et signaler les validations d'émulateur impossibles sans dépendances. Ne pas écraser de modifications locales.

## Explorations privées effectuées (non encore publiées comme validation)

Les fichiers à la racine scratch permettent de reprendre : `explore_controlled_services.py`, `explore_atm.py`, `dump_bank.py`, `v64_bank_dump.txt`, `v64_bank_graph.json`, dossiers `v64_controlled`, `v64_atm`, `v64_explore`.

Le téléphone de la maison n'a PAS été validé naturellement : Parler produit Biiip et Voir R.A.S. La route des anciennes captures V41 n'était pas une vraie conversation. Ne pas la compter comme un service testé.

Des entrées forcées vers les scripts complets suivants sont opérationnelles via la seule redirection temporaire de l'action carte bancaire `368B51` (4 octets), puis manette normale. **Cela teste les branches du service, pas son accès naturel sur la carte.** Aucun wrapper/callback, aucune écriture directe en WRAM.

- Téléphone gratuit : `35C597`. Après le texte « décroche », A ouvre Papa/Maman ; A choisit Papa. A suivants : présentation, prochain niveau, EXP, menu Sauver/Rien merci ; Sauver mène aux réponses de sommeil puis Suite/Dodo. Tester aussi Maman et annulation.
- Boutique : `365592` (NPC 90). Entrée → Bonjour ; A → question ; A → liste ; A → quantité ; A → achat de la Fiole de sérum à 20 $. L'écran montre la somme 20 → 0 et « Merci bien ». Tester refus d'achat d'un objet à 148 $ et annulation. Le script choisit son enseigne selon des flags ; ne pas prétendre visiter naturellement cette boutique.
- Stockage : `34B490` (NPC 1002). A → Déposer/Retirer. Déposer, A → question ; A → inventaire ; A sur carte bancaire → « Ne dépose pas cet objet ». Tester aussi Retirer sans objet stocké.
- Banque : `0680A6` avec carte en inventaire. Entrée → bienvenue ; A → Retrait/Dépôt ; Right,A → solde ; A → consigne dépôt ; A → nombre. Le curseur initial est sur les unités : Up,A dépose 1 $. A → merci ; A → ferme. Écran V64 relu : solde en français, compte 0 → 1 et poche 20 → 19. Tester Retrait compte nul, dépôt insuffisant (Left puis Up trois fois = 30 $), dépôt nul/annulation, retrait après un dépôt.
- Invitation à insérer la carte : accès contrôlé au texte `0680B0` si nécessaire pour vérifier le rendu. L'état initial a une carte non jetable ; ne pas prétendre avoir testé naturellement la condition sans carte.

## À faire pour terminer V64

1. Transformer ces explorations en probe reproductible `tests/emulation_v64/probe.py`, dans les deux profils, avec captures nommées et lecture de curseurs via `tools/v64/session.py`.
2. Vérifier les confirmations/refus téléphone, banque, boutique, stockage ; relire les captures. Documenter explicitement l'entrée forcée.
3. Ajouter les contrôles utiles : IPS autonome V61 + quatre plages autorisées, commandes/pointeurs/sprites identiques, analyse complète du graphe ATM depuis ses deux champs NPC. Chercher d'autres mots anglais dans ce graphe ; ne pas confondre paramètres de commande et texte.
4. Envisager une comparaison V61/V64 des mêmes écrans bancaires : seuls les rectangles de texte doivent changer. Les explorations `v64_controlled` ont utilisé V61 ; `v64_atm` utilise V64.
5. Rapports V64, README et RESTANT_TEXTES à mettre à jour. Après validation : checkpoint Git puis publication main sans force push. Le manifeste V64 existe mais le rapport principal recommande encore V61 tant que ce lot n'est pas fini.
6. Continuer ensuite les autres services et branches avec plusieurs personnages/inventaires pleins/vides. Textes d'abord, menus ensuite. Ne pas chiffrer une couverture globale sans dénominateur fiable.

## Publication Git

Le push shell n'a pas d'identifiants. Utiliser les outils GitHub create_blob (base64), create_tree avec base_tree_sha, create_commit puis create_branch pour le checkpoint ; update_ref main avec expected_sha et force=false après validation. Vérifier les hashes blobs/arbre local et distant. Les publications API créent un SHA de commit différent du local : fetch puis aligner la branche locale uniquement si arbre identique et état propre, en conservant une branche d'archive locale. Main est explicitement autorisée.
