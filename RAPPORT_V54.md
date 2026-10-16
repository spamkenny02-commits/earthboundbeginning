# V54 — premier lot de menus

169 occurrences de libellés traduites dans 85 blocs de choix. Il s'agit de répétitions de neuf libellés anglais, pas de 169 nouveaux dialogues. Deux occurrences de « Oui », déjà françaises, sont recopiées sans être comptées comme nouvelles. La traduction reste partielle.

| Blocs | Avant | Après | Occurrences nouvellement traduites |
| --- | --- | --- | --- |
| 79 | Yes / No | Oui / Non | 158 |
| 2 | Oui / No | Oui / Non | 2 |
| 2 | Store / Take out | Déposer / Retirer | 4 |
| 1 | Heal / Sleep | Soigner / Dormir | 2 |
| 1 | Small / Medium / Large | Petite / Moyenne / Grande | 3 |

## Repérage et intégration

`discover_menus.py` parcourt les commandes depuis des entrées de personnages du remake et les descriptions d'actions actuelles de V53. Il suit les destinations de scripts et reconnaît les définitions `19 02 <libellé> 02` sur des frontières analysées. Les références de table des personnages utilisent le schéma établi en V53. Un résultat du parcours de commandes ne prouve pas qu'un personnage ou événement soit naturellement rencontré en jeu.

Le constructeur revalide chaque groupe dans ses contextes complets, ses libellés exacts et les deux variantes V53. Les 85 blocs retenus sont vérifiés dans 87 contextes qui peuvent se recouvrir. La routine de choix partagée à `07DD4F`, utilisée notamment par les confirmations de services, fait partie du lot.

« Non » occupe un octet de plus que « No ». Pour garder les adresses intérieures, un saut long de cinq octets rejoint une copie des définitions françaises. La copie revient à l'adresse originale immédiatement après les définitions. Les commandes de sélection, de cancellation et de branchement restent ainsi à leur adresse originale. L'ordre des options est conservé ; aucun appel ni nouvelle entrée de pile de retour n'est créé.

Le constructeur refuse une cible littérale dans les quatre octets après le début du bloc. Tous les octets après les cinq premiers restent identiques à V53 ; aucune occurrence de pointeur intérieur n'est réécrite. Une entrée secondaire directement dans cette partie conservée pourra encore afficher d'anciens libellés. Le dictionnaire partagé, la table NPC et les commandes de branchement ne changent pas.

Les copies utilisent des plages nulles des banques de traduction 25/32, sans cible littérale intérieure et sans enregistrement IPS antérieur. Les 170 nouveaux enregistrements s'ajoutent à ceux de V53. Les anciens enregistrements restent dans les IPS ; les cinq octets des entrées retenues sont volontairement remplacés dans le résultat.

## Vérification

407 tests locaux passent, dont 21 nouveaux (11 hors ROM et 10 avec ROM). Ils couvrent la reconstruction exacte, l'inventaire, l'ordre des options, le nombre de choix, les réserves, les collisions, débordements et entrées protégées, le trajet aller/retour et les commandes des 87 contextes. Les suites sont listées dans `tools/v54/run_regressions.py` ; les anciens tests graphiques V36/V37 nécessitant CoilSnake ne sont pas inclus.

Les 212 captures du parcours normal Snes9x sont identiques à V53. Quatorze scénarios contrôlés sont exécutés dans V53 puis V54, avec accents et en ASCII : Oui, Non et B sur la maison hantée ; dépôt et retrait ; second menu de stockage ; deux options de repos ; trois tailles de pizza et annulation ; refus de paiement et d'achat. Les 28 images obtenues après sélection en V54 sont identiques pixel par pixel aux résultats V53 correspondants. Les libellés et les déplacements du curseur sont relus visuellement. Voir [rapport et planches](tests/emulation_v54/RAPPORT_EMULATION_V54.md).

Ces essais ne parcourent pas naturellement les 85 blocs ni toutes leurs conséquences de jeu. Ils confirment les résultats visibles dans l'état de test choisi, pas l'état complet du jeu après une transaction ou un repos.

## Suite

Les menus de transport, tarifs alignés et certains écrans restent à examiner. Les choix déjà entièrement français sont laissés en place. Les menus de débogage et des services hérités non retenus sont inventoriés sans être comptés comme traductions ; voir `discovery_audit_v54.json`. Ce lot ne prétend pas terminer tous les menus ou tous les textes du jeu.

## Application

Appliquer un seul IPS V54 à la ROM originale USA 1.2 de 4 Mio, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

[Patch avec accents](patches/EarthBound_Beginnings_FR_v54_accents.ips) · [Patch ASCII](patches/EarthBound_Beginnings_FR_v54_ascii.ips) · [Empreintes exactes](tools/v54/validation_v54.json).

Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.
