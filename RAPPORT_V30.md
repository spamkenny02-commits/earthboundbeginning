# V30 — réponses courtes et fragments restants

Base : V29, incluant les routines françaises boy/girl. **121 nouveaux fragments**, dont **95 dans les dialogues et interfaces du jeu** et **26 dans les messages de la boutique de test**. Ils concernent 98 scripts référencés (76 hors boutique de test), avec 130 pointeurs littéraux d’entrée. Ces fragments ne correspondent pas à 121 dialogues complets.

La série traduit les réponses «Yes» encore compatibles, salutations, exclamations, appels téléphoniques, dépôt bancaire, indices, réactions de personnages et fragments du réveil du dragon. Exemple coordonné : «Le dragon sent [nom] et s'éveille.» Le fragment suivant le nom reçoit un espace français explicite à la place du possessif anglais. La banque affiche désormais «Retrait» et «Dépôt».

Les 26 messages de boutique de test sont comptés séparément car leur présence dans des scripts référencés ne démontre pas leur accessibilité lors d'une partie normale. Les réponses «No» trop courtes pour «Non» et les fragments exigeant une relocalisation restent à traiter. D'autres fragments anglais peuvent encore subsister dans les scripts concernés ; cette version ne prétend pas achever chacun de ces dialogues.

## Contrôles

Audit contre la ROM originale USA 1.2, empreinte vérifiée. Seuil minimal de trois caractères pour les textes courts, avec les mêmes contrôles de disposition binaire : scripts explicitement référencés, commandes préservées, pointeurs d'entrée intacts, aucune référence intérieure ni collision avec les écritures V29.

**16 tests V30 réussis** : manifeste et textes sources, références et limites des scripts, longueurs accents/ASCII, frontières dynamiques, commandes, absence de chevauchement, décodeur et application IPS indépendants, conservation de tous les enregistrements V29, comparaison exhaustive hors ajouts, refus d'une mauvaise source, d'une plage inconnue et d'un texte trop long. Les **12 tests V29** sont également réexécutés.

Les IPS autonomes contiennent chacun 121 enregistrements supplémentaires. Tous les octets antérieurs sont conservés, y compris les deux routines boy/girl et les trois appels corrigés. Les empreintes sont dans [validation_v30.json](tools/v30/validation_v30.json).

## Émulation et limites

[Parcours Snes9x du début du jeu](tests/emulation_v30/RAPPORT_EMULATION_V30.md). Ce parcours ne valide pas les nouvelles scènes ni la sélection native boy/girl avec Ana. Les textes restent dans des plages fixes, avec espaces de remplissage : la mise en page exacte des scènes doit encore être vérifiée.

Appliquer un seul IPS V30 directement à la ROM originale USA 1.2. Aucune ROM ni sauvegarde distribuée.
