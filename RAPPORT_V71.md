# V71 — coursier de dépôt Escargo

Le coursier de dépôt arrivé après un appel Escargo affichait encore « Hello, this is Escargo Express! », les frais et les choix d'objets en anglais. V71 traduit **32 plages textuelles** de son graphe `063EB0–064295`, ainsi que les refus d'objet protégé `064633`. Les IPS comprennent V70 et s'appliquent directement à la ROM originale USA 1.2.

Les remplacements sont de même taille, sans allocation ni réécriture de pointeur. Le reconstructeur vérifie les frontières textuelles et l'anglais décompressé avant remplacement. Commandes, sprites et banque 25 restent identiques à V70. Les articles anglais « the / and the » de la confirmation deviennent des espaces et « et », sans modifier les noms d'objets.

## Essais retenus et portée

Six scénarios sont joués dans les profils accents et ASCII, avec références V70 aux mêmes touches et préparations :

| Scénario | Preuve retenue |
| --- | --- |
| Dépôt de trois objets distincts | Fiole, capsule de sagesse et capsule de vitalité sélectionnées, liste confirmée, remerciement ; inventaire final réduit à la carte bancaire et poche de 20 à 2 $ |
| Dépôt d'une Fiole | Sélection, refus d'ajouter un autre objet, confirmation et remerciement relus ; inventaire final non certifié |
| Paiement refusé | « Ah. Rappelle. », retour au menu ; pas de preuve dédiée d'inventaire final |
| Poche vide | « Sans $. Rappelle-nous. » ; arrêt sur ce refus |
| Carte bancaire sélectionnée | « Garde-le. Autre objet ? » ; arrêt pendant l'échange |
| Confirmation de trois objets refusée | « On recommence ? », retour à la sélection ; arrêt pendant l'échange |

La préparation privée accorde trois objets par commandes natives et dépense 20 $ dans le cas sans argent. Un wrapper temporaire appelle le **téléphone complet `35C597`**. Le choix Maman puis Déposer se fait à la manette. Après 600 images d'attente, **le mécanisme normal du jeu fait arriver le coursier** chez Ninten : aucune entrée du coursier n'est appelée par l'outil. L'accès initial au téléphone et l'inventaire préparé ne sont donc pas naturels. Aucune écriture directe en WRAM ni callback assembleur de test.

La fin des dialogues ne se cale pas toujours au même nombre de touches entre les deux langues. Des tentatives d'attente supplémentaire puis de fermeture A/B ont laissé certains essais au menu ou à « À qui ? » au lieu d'un inventaire. Ces tentatives restent privées et ne sont pas les preuves publiées. Les séquences publiques s'arrêtent aux écrans utiles ; seul le dépôt de trois objets comprend un inventaire final correctement atteint dans les deux versions. Ne pas confondre retrait de l'inventaire et relecture du contenu de la réserve : la réouverture de celle-ci après le passage du coursier reste à faire.

Les réponses de réserve pleine, de limite de trois objets et la variante de présentation sont également traduites et contrôlées statiquement. Leur présence dans le graphe ne certifie pas leur affichage en jeu. Le coursier de livraison validé en V70 reste intégré sans modification.

## Reproduction et sauvegardes

Douze essais principaux, **218 captures et 218 références V70**, dont 108 paires changent uniquement dans la fenêtre de texte `(104,8,248,98)`. Les **134 captures de coursier/inventaire** ont été relues visuellement dans les deux profils. Les traces principales totalisent **88 664 images échantillonnées**. Les quatre tests V71 passent avec la ROM privée, ainsi que les 21 tests ciblés V65, V67 et V70 : **25 tests réussis**. La suite historique complète n'a pas été relancée dans ce lot ; les 625 tests du rapport V70 restent un résultat historique, pas un nouveau résultat V71. Sans ROM, le test privé V71 est explicitement ignoré.

Voir [les outils V71](tools/v71/README_V71.md), [les résultats accents](tests/emulation_v71/results_accents.json), [ASCII](tests/emulation_v71/results_ascii.json) et [les comparaisons V70](tests/emulation_v71/comparison_v70.json). Les tests vérifient les 32 records ajoutés, les préparations déclarées, les touches, les traces actives, les commandes, les sprites et les empreintes des fixtures. La vérification d'affichage relit les PNG et les différences RGB ; elle ne remplace pas la relecture humaine des dialogues.

Checkpoint initial local `013572a195040ddbfd10acb8bd6b6fb2e5d5245a`, distant `work/v71-pickup` : `158efc7a433e7207195be2a4f63c7f7e2b1f8615`. Il précède les preuves d'émulateur. Le lot validé est conservé séparément sous `work/v71-pickup-validated` avant publication sur main.

Empreintes IPS SHA-256 : accents `0290365376b20e6b77bd4bce12839f7378bd34c0431f36fad3dee19b852ed0a6` ; ASCII `4969ab315e6df24d9d4ef3bb47caac7f67c755d855d4c236c9f64402e20bdb68`.

Prochain reste concret : relire la réserve après le dépôt et le reliquat après livraison partielle ; puis sacs/réserve pleins côté coursier, autres personnages, hôtels et enseignes. Les menus Use/Eat/Give/Drop/Help! restent anglais. La relecture d'un parcours complet est encore nécessaire : aucun 100 % certifié. ROM, cœur, états et dumps mémoire ne sont pas distribués.
