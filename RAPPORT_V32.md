# V32 — Mary, Pippi, Lloyd et les livraisons

Base : V31. **16 scripts révisés et relocalisés**, comprenant **140 fragments**, dont **63 encore anglais dans V31**. Les autres reprennent ou révisent le français existant, ou conservent ponctuation, espaces et onomatopées. Ces nombres ne représentent pas 140 nouveaux dialogues.

Les nouvelles copies complètent l'accueil téléphonique factice, l'hébergement chez Jack, l'appel du faux parent, la clôture à protéger, l'indice de la maison hantée, l'adresse des Rosemary, la chanson de Mary, ses cauchemars, l'amitié à Magicant, l'accès au toit de l'école, l'appel à Escargo Express, l'appel maternel à un compagnon, l'échec de livraison Mach Pizza, la récompense du maire après Pippi, les fragments du cristal et l'arrivée de Lloyd avec la fusée-bouteille.

Les noms, objets et montants dynamiques restent des commandes. Les fragments autour de ces éléments sont révisés ensemble. Le maire propose «Oui / Non», sans abréviation ; les scripts narratifs et leurs commandes de progression restent conservés dans les copies.

## Réserves et références

Les copies utilisent `[24D660,24DB80)`, `[25B560,25BE20)`, `[263690,263E80)` et `[32D0E0,32D520)`. La première plage prolonge l'allocation V31 dans sa partie encore libre. Toutes les plages sont vérifiées nulles dans la source et V31, sans référence HiROM littérale entrante et sans écriture IPS antérieure. Les copies occupent 5 655 octets hors alignement.

21 références extérieures aux entrées principales sont redirigées. Les appels et branches internes vers des scripts sélectionnés sont recalculés aux frontières vérifiées. Les anciens scripts et leurs 39 références littérales vers des entrées intérieures restent intacts ; ces anciennes entrées secondaires peuvent donc encore afficher les fragments V31. Les adresses assemblées ou calculées indirectement ne sont pas vérifiées exhaustivement.

## Contrôles

**13 tests V32 réussis** : provenance sur la ROM originale USA 1.2, source et fixtures, références d'entrée, réserves, fermeture des copies, commandes et opérandes des IPS publiés, encodage des deux profils, absence de chevauchement, application IPS indépendante et masque exhaustif des modifications. Les branches dans un texte remplacé, débordements, références supplémentaires et commandes modifiées sont refusés.

Un contrôle dédié confirme la conservation des scripts anciens et copies V31, de leurs références redirigées et des routines boy/girl de V29. Les enregistrements V31 restent inclus dans les IPS autonomes ; seules les nouvelles références d'entrée déclarées sont réécrites.

[Parcours Snes9x et essais d'affichage](tests/emulation_v32/RAPPORT_EMULATION_V32.md). Les essais d'affichage utilisent un point d'entrée temporaire absent des patches livrés. Ils ne remplacent pas la validation des déclencheurs narratifs, des branches de progression et des anciennes entrées secondaires dans une partie normale.

[Sources françaises](tools/v32/dialogues_fr.json) · [Destinations et empreintes](tools/v32/validation_v32.json) · [Construction et tests](tools/v32/README_V32.md).

Appliquer un seul IPS V32 directement à la ROM originale USA 1.2. Aucune ROM ni sauvegarde distribuée.
