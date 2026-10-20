# V78 — pronoms et contextes français, checkpoint à 119 textes

Trois sources partagées nouvellement traduites : you → toi (387B2B), you all → vous (387B2F), you two → vous (387B37). Compteur dédoublonné : 119 textes distincts et 157 plages sources, cible 150. Les trois corrections françaises et deux redirections de possessif ne gonflent pas ce compteur. V77 reste publiée sur main ; même lot V78 en cours.

Le PNJ586, champ9, pointe vers 33FA7D. Sa branche 33FBDD mène à 320B30 puis 33FC0E, au préfixe copié 32FCA0 et à 33FC4C, seul appel du sélecteur 387B19. Le préfixe est corrigé en « Fiston se nomme comme » : « Mon fils se nomme aussi you » mélangeait les langues. Le premier essai corrigé rejetait le point seul à la ligne ; le préfixe a été raccourci, et son saut avancé de deux octets dans le même bloc. Aucun remplissage visible avant le pronom. Les retours des variantes plurielles suivent immédiatement « vous » ; les trois octets suivants sont une queue nulle inaccessible, sans pointeur intérieur qualifié ou brut.

Le PNJ1157, champ9, pointe vers 263B90, avec appels des branches 369D9B et 369E9E. Leurs deux appels de Your/nom's (369DD2, 369EA3) sont redirigés vers le retour vide existant 38B550. « L'amour de Maria, notre aïeule » porte déjà le possessif en français ; l'insertion anglaise était redondante. Les deux initiales de L'amour passent en majuscule. Le helper original 387AA2–387AB8 reste intact, aucune réécriture globale ni nouvelle réserve.

Huit enregistrements IPS supplémentaires, total 377 au-dessus de V77. Total alloué inchangé : 3 431 octets. Commandes vérifiées, hormis les deux opérandes d'appels autorisés, qui sont normalisés dans le contrôle ; retours abrégés analysés à leur nouvelle fin. Sprites, banque25, table PNJ et créneau privé restent inchangés. Toutes les écritures exactes et les chemins typés sont enregistrés dans v78_fixtures.json/context_grammar et contrôlés par les tests.

18 tests V78 avec ROM privée, reconstruction déterministe des IPS/fixtures vérifiée. Nouvelles preuves : 56 paires V77/V78, douze différences confinées au texte, 12 256 images échantillonnées, six cas par profil. Les 56 captures finales ont été relues en accents et ASCII. Les captures précédentes sont vérifiées contre leurs snapshots 81/99/114/116.

L'entrée complète du PNJ586 est forcée avec le flag00B8, lu dans son premier test 06 B8 00 ; sa branche nominale est également appelée directement. Le sélecteur singulier fonctionne avec Ninten seul. Les variantes plurielles sont appelées directement, suivies de la ponctuation/pause originale 33FC51 pour rendre le texte observable ; elles ne prouvent pas une sélection naturelle avec deux/trois personnages. Les deux branches de Maria sont forcées depuis le même état privé post-repos, sans progression naturelle ni acquisition de mélodie certifiée. Aucune écriture WRAM directe. Seuls PNG, rapports sémantiques, outils et IPS sont publics.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
|---|---|---|
| Accents | 1a347b1a7482110a31b62db50aa92f806f53501308c11a522162e67d6e4b5c59 | 32cc2fdf3b0494aec14056a73c73fa6df148260e23456c8cb7c8e54438d93f74 |
| ASCII | 2841b44127f8b46b06c4c2572d048ef6b7c8000ba004256bd2dc437d8c8582e5 | 89d5c0e1856cc5600f9ea716eabc7efa8acd7a35903e305fa833cde75dd48cb6 |

Suite : articles des trois dispatchs 38B551/38B56C/38B587 par contexte, limites du coursier, services à plusieurs personnages, anciennes branches et parcours naturels, puis menus. Les 31 sources avant 150 ne constituent pas un inventaire exhaustif. Le stockage local a retrouvé des écritures après suppression de caches Python et des seuls history.json des essais current_v78_help/reference_v78_help déjà remplacés ; sources, captures retenues, états et dépendances privées sont conservés. Aucune dépendance durable ne bloque la suite.
