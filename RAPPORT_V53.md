# V53 — trois dialogues protégés raccordés aux personnages

Quatre fragments passent en français : maison hantée de Spookane, adieux, ascenseur et préfixe de confirmation d'achat. Ce petit lot résout les trois protections reportées par V52 sur les chemins des personnages. La traduction reste partielle ; il ne modifie pas les menus.

## Table des personnages vérifiée

La table active est à `2021A8`, avec des enregistrements de 17 octets et deux champs texte aux offsets 9 et 13. Son adresse SNES `E021A8` est confirmée dans dix références du moteur, dont le chargement des personnages, « parler », « examiner » et l'utilisation d'objets dans le décor. Le constructeur vérifie les structures ASM à chargements immédiats et stockages successifs, ou les références longues indexées, puis leur destination exacte, dans l'original et les deux variantes V52.

Le schéma et les emplacements de référence proviennent de CoilSnake au commit `346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a`, déjà utilisé par l'atelier : [structure NPC](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/assets/structures/eb.yml), [références moteur](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/modules/eb/ExpandedTablesModule.py), [format des pointeurs ASM](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/util/eb/pointer.py). L'adresse active est lue dans cette ROM ; l'ancienne adresse de table n'est pas utilisée.

| Dialogue | Début exact | Personnage, index à partir de zéro | Champ réécrit |
| --- | --- | --- | --- |
| Maison hantée | `33F3EE` | 878 | `205BFF` |
| Adieux | `3609EB` | 102 | `202877` |
| Ascenseur | `350000` | 857 | `205A9A` |

L'ascenseur avait auparavant été associé au candidat `34FFED`. Le champ de personnage désigne le vrai début `350000`, où les deux commandes conditionnelles précédant « Going up! » sont entières. Ce début est utilisé pour la copie. L'autre occurrence littérale vers `350000` à `15DA77` est conservée sans réinterprétation ; un éventuel trajet par elle reste à vérifier et pourra encore lire l'original anglais.

## Conservation du comportement

Trois copies françaises privées gardent toutes les commandes et leurs destinations absolues ; seuls les champs texte des trois personnages changent. Les scripts sources et toutes leurs entrées intérieures restent entièrement identiques à V52. Les branches vers les fins exclusives `33F442` et `360A1A` continuent de viser les commandes originales, sans confusion avec une copie voisine.

La suite des adieux contient déjà la réparation V35 `360A16 → 16F920`, correspondant à l'ancienne destination `360A5B`. Elle est vérifiée dans le rapport V35 et dans la commande originale, puis conservée dans la copie. Toute autre différence de source non déclarée est refusée.

Le préfixe `@The ` de `354DB2` devient `@Objet: ` par un saut vers une copie, puis revient à `354DB7` pour l'affichage dynamique de l'objet. Le contexte complet affiche « Objet: Arme ultime, hein? » dans la fixture de sélection. Le reste de cette confirmation est déjà français.

Les quatre copies sont placées dans des plages nulles des banques de traduction 25/32, non couvertes par les IPS antérieurs et sans cible littérale intérieure. Huit enregistrements IPS s'ajoutent à V52 ; le dictionnaire partagé et le moteur restent inchangés.

## Vérification

386 tests locaux réussis, dont 29 nouveaux (16 hors ROM, 13 avec ROM) : reconstruction IPS, dix références moteur distinctes, refus des mauvaises structures et destinations, champs de table, commandes et sources conservées, branches de fin exclusive, continuation V35, réserves et écritures limitées aux plages déclarées. Les suites sont listées dans `tools/v53/run_regressions.py` ; les anciens tests graphiques V36/V37 nécessitant CoilSnake ne sont pas inclus.

Les 212 captures du parcours normal Snes9x restent identiques à V52. Quatre appels contrôlés par variante lisent les destinations publiées dans les trois champs de personnage et la confirmation d'achat complète. Voir [le rapport d'émulation et les captures](tests/emulation_v53/RAPPORT_EMULATION_V53.md). Cela ne prouve pas l'accès naturel à chaque personnage, les branches de l'ascenseur, la fin du jeu ou une transaction réelle.

Ces protections sont traitées pour les entrées indiquées ; cela n'implique pas que tous les textes du jeu soient traduits. Les menus, des routines héritées, graphismes et chemins secondaires restent à vérifier.

## Application

Appliquer un seul IPS V53 à la ROM originale USA 1.2 de 4 Mio, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

[Patch avec accents](patches/EarthBound_Beginnings_FR_v53_accents.ips) · [Patch ASCII](patches/EarthBound_Beginnings_FR_v53_ascii.ips) · [Empreintes exactes](tools/v53/validation_v53.json).

Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.
