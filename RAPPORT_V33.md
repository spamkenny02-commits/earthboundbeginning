# V33 — commerces, hébergements et dialogues secondaires

Base : V32. **58 scripts et messages révisés**, comprenant **153 fragments**, dont **64 encore anglais dans V32**. Les autres fragments reprennent ou révisent le français existant, ou conservent des éléments non linguistiques. Ces nombres ne désignent pas 153 nouveaux dialogues.

La série complète notamment les messages de vente, inventaires pleins, équipement, fonds insuffisants, hébergements, indices et petits dialogues à Snowman, Magicant et ailleurs. Elle comprend les plans de vol A/B/C, le solde bancaire, le chocolat chaud, les indications de Spookane, les rumeurs sur le robot du mont Itoi et la continuation du trésor du chien. Les noms propres et jeux cités restent conservés ; les phrases qui les entourent sont françaises. Le symbole dollar du solde bancaire passe après le montant, dans les fragments de texte, sans changer la commande numérique.

## Continuation depuis V31

La branche de la copie V31 du dialogue du chien à `2929EA` vise encore la continuation originale `33C628` dans V32. Elle est désormais redirigée vers sa nouvelle copie française `258DC0`. Le pointeur supplémentaire est accepté seulement parce qu'il est identifié comme opérande de commande dans une copie relocalisée connue. Une adresse littérale supplémentaire ailleurs demeure bloquante.

Les plages originales des scripts V31 et V32 sont protégées et restent intactes. Les anciennes entrées secondaires restent donc disponibles, avec leurs textes antérieurs. Les copies antérieures sont conservées, à l'exception de cet opérande de continuation explicitement redirigé ; les routines et trois appels boy/girl sont inchangés.

## Allocation et contrôles

Les réserves `[258DC0,259400)`, `[25C210,25C820)`, `[32B620,32BC20)`, `[228820,228D60)` et `[32D530,32DA20)` sont nulles dans la source et les deux profils V32, sans référence HiROM littérale entrante ni écriture IPS antérieure. Les copies occupent 6 034 octets hors alignement. 80 références d'entrée sont réécrites ; les scripts originaux et leurs 97 références littérales vers des entrées intérieures sont préservés. Les adresses reconstruites ou calculées indirectement ne font pas l'objet d'une preuve exhaustive.

**14 tests réussis** : provenance et fixtures, encodage, fermeture des copies, commandes, frontières de branchement, opérandes des IPS publiés, allocation, application IPS indépendante, comparaison exhaustive hors écritures déclarées, préservation des versions précédentes, refus d'une adresse inconnue, d'un débordement ou d'une branche dans du texte remplacé. Un test dédié vérifie le raccord de la continuation V31.

Le [parcours Snes9x et les essais d'affichage](tests/emulation_v33/RAPPORT_EMULATION_V33.md) couvrent les deux profils. Les cinq copies inspectées par point d'entrée temporaire ne remplacent pas la vérification des déclencheurs narratifs, des parcours de vente et des anciennes entrées secondaires dans une partie normale.

[Sources françaises](tools/v33/dialogues_fr.json) · [Destinations et empreintes](tools/v33/validation_v33.json) · [Construction et tests](tools/v33/README_V33.md).

Appliquer un seul IPS V33 directement à la ROM originale USA 1.2. Aucune ROM ni sauvegarde distribuée.
