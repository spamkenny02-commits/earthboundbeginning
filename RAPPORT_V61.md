# V61 — fragments courts et huées

V61 corrige **deux fragments lexicaux courts** : l’article anglais devant le nom d’objet dans une confirmation (`34FADF`) est supprimé, et « to » devient « à » dans une formule de destinataire (`37BE28`). Trois huées temporisées deviennent **« Bouhouuuu! »**. Cela représente **20 fragments de glyphes modifiés dans cinq contextes**, pas 20 nouveaux dialogues.

Toutes les écritures gardent exactement leur taille. Les espaces de remplissage permettent de supprimer l’article sans imposer de genre au nom d’objet. Les sorties dynamiques, les pauses entre lettres, les commandes, leurs opérandes et toutes les adresses restent inchangés. Aucune allocation ni copie supplémentaire. Le générique V60 et les sprites restent identiques.

**564 tests passent**, dont dix V61. Les **212 captures de référence sont identiques à V60**. Vingt lectures contrôlées comparent les cinq cas dans les deux versions et profils : les dix comparaisons ne changent que les pixels de texte. Les deux planches ont été relues. Les lectures passent par un wrapper temporaire ; elles ne prouvent pas l’accès depuis les personnages ni le déroulement complet des scènes. Les variables ne sont pas initialisées comme dans leur scène d’origine : le destinataire « 2 » des captures est un résultat de ce contexte de test. [Captures et méthode](tests/emulation_v61/RAPPORT_EMULATION_V61.md).

## Audit des anciennes entrées

Le nouvel audit suit **648 graines, 3 335 débuts de script et 4 364 références de commandes**. Il examine **4 681 segments hors menus**. Dans ce graphe, aucune référence analysée n’entre dans les plages de texte conservées après les déplacements V51–V53 et V56–V59. Ce résultat ne couvre pas les appelants assembleur ou calculés.

Deux routines, `37C079` et `37C100`, sont incomplètement lues : le code `1A 21` n’est pas défini par le parseur. Elles restent explicitement dans la liste de vérification. Les 292 segments inchangés candidats incluent des noms, onomatopées, diagnostics et modèles hérités. Un contrôle de mots anglais fréquents ne signale aucun segment modifié, mais ce filtre ne prouve pas à lui seul la langue ou la traduction complète d’un texte.

Le lot est sauvegardé séparément sur `work/v61-textes`, puis publié sur main. L’objectif de **100 % des textes visibles reste à certifier** après les branches calculées, les deux routines ci-dessus, un parcours complet et le générique en situation réelle. Les menus restent pour la phase suivante.

[Sources, tests et audit](tools/v61/README_V61.md) — [Travail restant](RESTANT_TEXTES.md).

Appliquer un seul IPS V61 directement à la ROM originale USA 1.2. Aucune ROM, sauvegarde ou bibliothèque d’émulation n’est distribuée.
