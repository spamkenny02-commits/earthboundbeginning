# V62 — levée des deux blocages du parseur

Les deux routines d’inventaire `37C079` et `37C100`, bloquées en V61 sur `1A 21`, sont désormais lues entièrement. La commande compare les registres de travail et d’argument sur **32 bits**, écrit 1 s’ils sont égaux et 0 sinon, et ne consomme **aucun opérande** après ses deux octets.

La preuve suit le dispatch du moteur, son hook et sa table jusqu’au corps de la comparaison, avec **13 ancrages d’octets** vérifiés dans la ROM originale et les deux profils V61. Le parseur étendu reste isolé : le schéma historique n’est pas modifié.

**575 tests locaux passent**, dont onze propres à V62. **Douze essais Snes9x** vérifient les résultats et les registres par lecture de WRAM : égalité et différence sur un octet, égalité 32 bits, différence du mot haut seul, différence du mot bas seul et égalité de zéro, dans les deux profils. Le marqueur de texte suivant la commande s’affiche dans chaque cas. L’initialisation utilise des callbacks temporaires de test, sans écriture directe de WRAM par l’outil. Il ne s’agit pas d’un parcours naturel de l’inventaire.

## Résultat de l’audit

Dans chaque profil, l’audit suit **648 graines, 3 341 débuts de script et 4 375 références de commandes**. Il ne reste **aucune racine non analysée dans ce graphe**. Par rapport à V61, six débuts et onze références supplémentaires sont lus ; ils n’exposent aucun nouveau segment de texte.

Le corpus reste de **4 681 segments hors menus**, avec **292 candidats inchangés** à qualifier. Aucune référence analysée ne rentre dans les anciennes plages de texte conservées vérifiées par l’audit. Ces résultats n’incluent pas les appelants assembleur ou calculés et ne prouvent pas l’accès naturel de chaque branche.

**Le patch de jeu reste V61, inchangé.** Aucun nouvel IPS n’est créé, aucun texte supplémentaire n’est annoncé comme traduit et aucune routine moteur n’est modifiée. V62 est une étape d’analyse et de validation, sauvegardée séparément sur `work/v62-audit` avant la publication sur main.

L’objectif de 100 % des textes visibles reste à certifier par les accès calculés, la qualification des modèles hérités et une relecture en situation, dont une fin de partie complète. Les menus restent pour la suite.

[Sources et reproduction](tools/v62/README_V62.md) — [Essais et captures](tests/emulation_v62/RAPPORT_EMULATION_V62.md) — [Travail restant](RESTANT_TEXTES.md).
