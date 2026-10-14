# V29 — correction coordonnée boy/girl

Base : V28 publiée (`8c23172`), ROM originale USA 1.2. Les IPS autonomes accents et ASCII s'appliquent directement à cette ROM, sans empiler les versions.

La V29 corrige les trois appels identifiés par l'audit. Elle ajoute deux routines françaises dans une partie libre de la réserve déjà déclarée, redirige les trois appels et remplace cinq fragments de texte. Elle conserve tous les enregistrements IPS V28 et la routine anglaise originale, y compris sa branche intérieure.

| Dialogue | Sortie garçon | Sortie fille |
|---|---|---|
| Charmant | Oh, tu es adorable, brave garçon... | Oh, tu es adorable, brave fille... |
| Courage | Bravo, brave garçon! | Bravo, brave fille! |
| École | Tu es donc bien un écolier, pas vrai? | Tu es donc bien une écolière, pas vrai? |

Les fragments restent dans leurs plages fixes, avec des espaces de remplissage. La virgule, la pause `10 0F`, les commandes de dialogue et les retours sont conservés. La présentation exacte reste à inspecter dans ces scènes.

## Références et allocation

- Routine garçon/fille : `3FF990`, branche fille `3FF9A2`.
- Routine scolaire : `3FF9B0`, branche écolière `3FF9C6`.
- Réserve contrôlée : `[3FF990,3FF9E0)`, vide dans la source et dans les deux profils V28, sans enregistrement IPS ni pointeur littéral entrant.
- Appels `33FAA8` et `33FC1F` → `3FF990`; appel `352FE6` → `3FF9B0`.
- Original `387B05..387B19` conservé. Son alias intérieur `387B14` conserve sa référence originale.

Le sélecteur `19 10 01`, la comparaison `0B 02` et le branchement `1B 03` restent identiques. Seule la destination intérieure de la branche est recalculée. La V29 n'ajoute aucune nouvelle hypothèse sur la sélection d'équipe.

## Validation

12 tests V29 réussis : interprétation des octets publiés pour les IDs 1/2/3/4 dans les deux profils, branches et retours, appels scolaires séparés, allocation sans chevauchement, conservation des enregistrements V28, application IPS indépendante sur ROM, masque exhaustif des modifications, références entrantes, commandes intactes, rejet d'une réserve occupée et d'un appel inconnu. Les 4 tests V28, dont son roundtrip complet sur ROM, passent également.

Les essais Snes9x du début du jeu sont consignés dans [le rapport d'émulation](tests/emulation_v29/RAPPORT_EMULATION_V29.md). Ils ne couvrent pas les trois scènes boy/girl ni Ana en tête d'équipe. Le test des deux branches est un interpréteur des commandes de dialogue, pas une exécution native du sélecteur sous Snes9x. La sélection après KO et la disponibilité des personnages restent à tester en jeu.

Aucune ROM ni sauvegarde distribuée. Empreintes et références : [validation_v29.json](tools/v29/validation_v29.json).
