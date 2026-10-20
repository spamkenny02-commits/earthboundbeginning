# V77 — désert, mineur et chameau

Treize fragments anglais sont traduits : souvenir des mines, avertissement, messages de billet et de char, prix refusé, question du chameau, Oui/Non et relance après Non. Une formulation déjà française est corrigée au féminin : « Je les ai toutes ôtées sauf une... », en référence aux mines.

## Intégration

Treize plages fixes et un pont de définition Non ajoutent 15 enregistrements aux IPS V76. La définition de cinq octets `374357–37435C` devient un saut vers onze octets protégés à `328DBC`, puis revient à `37435C`. La question complète `374307` et la reprise intérieure `374351` utilisent la même définition. Leurs commandes, une fois le pont déplié, sont identiques à V76.

Les commandes des contextes `3738F8`, `373C34`, `373CD8` et `374409`, les sprites, la banque 25, le créneau privé de test et toute la table des 1 584 PNJ sont préservés. Le mineur reste le PNJ 210 et le chameau le PNJ 894 (champ 9, opérande `205D0F`). Le constructeur normalise la référence française selon le profil pour vérifier aussi l'ancien texte ASCII des mines.

## Validation en émulateur

Cinq scénarios dans chacun des deux profils :

| Scénario | Accès contrôlé | Observation |
| --- | --- | --- |
| Mineur | Entrée complète `3738F8` | Souvenir de guerre, mines et avertissement, puis proposition de vol et question d'itinéraire |
| Chameau Oui | Entrée complète `374307` | Choix Oui, trois pages de conseil, retour à la carte |
| Chameau Non puis Oui | Entrée complète `374307` | Refus, relance française, nouveau choix Oui, conseils et retour à la carte |
| Billet et char | Branche directe `373C34` | Libellé dynamique « Talon de billet », condition des dix billets, char et rire |
| Prix refusé | Branche directe `373CD8` | « Bon, c'est assez cher... Je te comprends. », puis sortie |

48 captures V77 relues, comparées à 48 captures V76 issues des mêmes états et entrées manette ; 28 différences, toutes dans la fenêtre textuelle `(104,8,248,98)`. 10 500 images échantillonnées côté V77. Les seuls PNG publiés sont les 96 captures déclarées. La trace du refus du chameau passe bien par `37440A`, puis celle du conseil par `374371` ; le cas Oui initial ne passe pas par le refus.

23 tests ciblés réussis avec la ROM privée : V77 (8), régression V76 (7), stockage protégé V65 (8). Hors ROM, cinq tests publics restent exécutés et trois sont explicitement ignorés. Les IPS se reconstruisent à l'identique.

Tous les accès initiaux sont forcés par la fixture privée de carte bancaire. Les trois premiers cas appellent les entrées complètes et laissent le moteur choisir les branches. Les deux derniers isolent des textes intérieurs : ils ne certifient ni achat réel de billet, ni coût débité, ni location de char, ni trajet en avion. Le service de vol n'est pas poursuivi au-delà de la question d'itinéraire. Aucune opération préparatoire d'inventaire ou de flag, aucune écriture WRAM directe. Aucun accès naturel de carte n'est certifié.

L'état privé est la référence V71 post-repos (Ninten seul, 30 PV, 10 PP, 20 $, carte bancaire). Les empreintes de la ROM originale, du cœur et des états sont dans les résultats. ROM, cœur, états et dumps restent privés.

## Patchs

Appliquer un seul IPS V77 directement à la ROM originale USA 1.2.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
| --- | --- | --- |
| Accents | `e365e74853f492096ff52d2d006addb508b9cc640b400dbd81b239f838fe751b` | `9bfad9ec558cc83bb3e329a4f5b3997b2da3101ab0610f26a6e066116fd62752` |
| ASCII | `cef07d5d3de773ccfb8dbe31bda97deb86343854fb2571be1b533c875d3f1ead` | `89354e541ef9ea1aba062e6b758493ab678deddf98361866026a1be38c4215f5` |

Checkpoint initial local `6e58b18`, branche `work/v77-desert-local` ; checkpoint validé prévu `work/v77-desert-validated`, puis publication sur `main` sans force push.

## Restes concrets

Le relevé direct des PNJ personnalisés a été actualisé après les corrections V74–V77 : 181 racines examinées, aucune erreur d'analyse et six candidats restants : `36EB50`, `376ABE`, `376BB7`, `377108`, `37D45C`, `380A2A`. Voir `tools/v77/custom_npc_roots_v77.json`. Ce relevé n'est pas récursif, ne classe pas parfaitement la langue et ne prouve pas les accès naturels ; six candidats ne signifie pas six derniers textes du jeu.

Prochaine priorité : maison hantée `36EB50`/PNJ 411, puis les trois singes `376ABE`/904, `376BB7`/905 et `377108`/908, avant panneau `37D45C` et fusée `380A2A`. Poursuivre ensuite les restes de services et accès calculés, les menus, puis le parcours naturel complet et le générique. Aucun 100 % certifié.
