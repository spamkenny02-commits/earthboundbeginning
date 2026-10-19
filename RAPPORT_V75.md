# V75 — canari et mélodie

## Traductions

Sept fragments anglais sont traduits dans la conversation du canari et ses branches :

- `3861E4–386213` : « Oh ! Ce canari est le petit de Laura. »
- `386215–386233` : « Vas-tu le lui rendre ? »
- Deux paires Oui/Non : question du petit et confirmation de la mélodie.
- `386380–386397` : « Le chant a du pouvoir. »

La racine complète `3861D3` est référencée par le champ 9 du PNJ 291, opérande `203504`. Ce pointeur reste inchangé. La branche de mélodie `32CC90`, déjà française en V74 sauf ses choix, est atteinte par un test de flag dans cette racine. La réponse sur le chant est `38636E`. Les fragments français préexistants ne sont pas remplacés.

Cinq remplacements à taille fixe et deux couples saut/définition ajoutent neuf enregistrements aux IPS V74. Pour « Non », cinq octets de définition d'origine deviennent un saut vers onze octets protégés :

| Définition | Copie | Retour |
| --- | --- | --- |
| `38623A` | `3302D4` | `38623F` |
| `32CCEA` | `330408` | `32CCEF` |

Les 22 octets alloués sont dans la réserve protégée, hors sprites, anciens IPS, pointeurs connus et créneau privé de test. Après dépliage des ponts, les commandes natives des sélecteurs sont identiques à V74. Les commandes de la réponse sur le chant, le pointeur PNJ, les sprites, la banque 25 et le créneau privé sont également inchangés.

## Essais retenus

Cinq scénarios par profil, accents et ASCII :

| Scénario | Entrée contrôlée | Résultat relu |
| --- | --- | --- |
| Sans petit canari | `3861D3` | Beau temps, « Mais quelle importance? », sortie |
| Petit, Oui | `3861D3`, don natif A8 | Présentation, Oui/Non, « Où est-elle passée ? », sortie |
| Petit, Non | `3861D3`, don natif A8 | Présentation, Oui/Non, réponse sur la vie, sortie |
| Mélodie, Oui | `32CC90` directement | Souvenir de Laura, Oui/Non, vérité et pouvoir du chant, sortie |
| Mélodie, Non | `32CC90` directement | Souvenir de Laura, Oui/Non, « Oh non, c'est embêtant. », sortie |

42 captures V75 relues et comparées à 42 captures V74 avec les mêmes états, préparations et entrées manette. 18 différences, toutes limitées à la fenêtre textuelle `(104,8,248,98)`. 9 364 images échantillonnées côté V75. Les traces distinguent les réponses : `386254` pour le Oui au petit, `252D4D` pour son refus, `38637F` pour le Oui à la mélodie et `38639D` pour son refus. Les PNG, empreintes et transitions sont dans `tests/emulation_v75/`.

Les premiers essais privés `explore_v75` et `reference_v74_canary` sélectionnaient encore Oui dans les cas nommés Non. Ils sont exclus. Les preuves publiées viennent exclusivement de `validated_v75` et `reference_v74_canary_final`, avec les séquences corrigées : après la présentation, une seule touche A ouvre la question, puis Droite+A choisit Non. Les captures superflues des essais initiaux ne sont pas conservées dans Git.

24 tests ciblés réussis avec ROM privée : V75 (8), régression V74 (8), stockage protégé V65 (8). Le contrôle public exécute cinq tests, en ignorant explicitement les trois qui nécessitent la ROM ; Pillow est nécessaire. Les IPS reconstruits ont les mêmes empreintes que ceux testés.

## Limites importantes

Tous les accès initiaux sont forcés par une fixture privée de carte bancaire. Les cas avec petit reçoivent l'objet A8 par commande native `1D 00 01 A8`, sans écriture directe WRAM. Les choix et réponses sont ensuite exécutés normalement par le moteur. Les cas de mélodie appellent une branche intérieure directement : aucun flag de progression n'est préparé ni prouvé, et aucun apprentissage réel de mélodie n'est certifié. Les cas du petit ne prouvent pas sa restitution à Laura ni une modification finale de l'inventaire.

État initial privé : référence post-repos V71, Ninten seul, 30 PV, 10 PP, 20 $, carte bancaire. ROM originale vérifiée SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`. Cœur SNES9x SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`. Les empreintes des états figurent dans les résultats, jamais leurs contenus. Aucune ROM, cœur, sauvegarde ni dump mémoire n'est publié.

## Patchs et suite

Appliquer un seul IPS V75 directement à la ROM originale USA 1.2.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
| --- | --- | --- |
| Accents | `dde8bc2d611da323d39af14015c176bfe927cc78144cb9bfcdc97a31618a9537` | `3b90bbe8c5dfd202634dc8bfcdd21928b9dc112ebfa4edd791aad05e782c31f5` |
| ASCII | `770e235d3eea71d4772c2026621e762ec7ca318507c234de9131292cfde2c3fc` | `09181c7acdc8058b88bb51840a9d53352acc0920d9a1ce5fef4fdc8ddfe7b44e` |

Checkpoint initial local `f744b5a` / `work/v75-canary-local`. Lot validé destiné à `work/v75-canary-validated`, puis `main`, sans force push. Prochain candidat concret : Pippi `386B63`/PNJ 319, puis mines `3738F8`/210 et autres racines historiques V73 non traitées. Le canari `3861D3` et la revente `387221` sont désormais traités dans ce relevé historique ; il ne prouve pas une couverture exhaustive. Services restants, menus, générique et parcours naturel complet restent à valider. Aucun pourcentage global ni 100 % certifié.
