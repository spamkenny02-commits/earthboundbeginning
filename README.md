# EarthBound Beginnings SNES — traduction française

## Version actuelle : V55 (menus de transport)

V55 traduit **16 lignes de destination** dans quatre contextes de guichet, avec tarifs et noms de ville conservés, ainsi que deux phrases d'achat du billet. Les lignes sont alignées sur 128 pixels. La traduction reste partielle.

- [Patch V55 avec accents](patches/EarthBound_Beginnings_FR_v55_accents.ips)
- [Patch V55 ASCII](patches/EarthBound_Beginnings_FR_v55_ascii.ips)
- [Rapport V55](RAPPORT_V55.md)
- [Sources et tests](tools/v55/README_V55.md)
- [Essais Snes9x et captures](tests/emulation_v55/RAPPORT_EMULATION_V55.md)
- [Avancement estimé : environ 80 %](AVANCEMENT.md), estimation qualitative du travail restant.

Appliquer **un seul IPS V55 directement à la ROM originale USA 1.2**. 430 tests locaux réussis, 212 captures du parcours de référence identiques à V54 et 40 comparaisons de réponses de transport réussies. Les essais contrôlés ne valident pas tous les accès naturels ni les voyages. Aucune ROM distribuée.

## Version précédente : V54 (premier lot de menus)

V54 traduit **169 occurrences de libellés dans 85 blocs de menus** : 81 blocs Oui/Non, deux menus Déposer/Retirer, Soigner/Dormir et Petite/Moyenne/Grande pour les pizzas. Les curseurs, réponses et annulations sont comparés à V53 dans l'émulateur. La traduction reste partielle ; les menus de transport et d'autres écrans restent à examiner.

- [Patch V54 avec accents](patches/EarthBound_Beginnings_FR_v54_accents.ips)
- [Patch V54 ASCII](patches/EarthBound_Beginnings_FR_v54_ascii.ips)
- [Rapport V54](RAPPORT_V54.md)
- [Sources et tests](tools/v54/README_V54.md)
- [Essais Snes9x et captures](tests/emulation_v54/RAPPORT_EMULATION_V54.md)

Appliquer **un seul IPS V54 directement à la ROM originale USA 1.2**. 407 tests locaux réussis. Les 212 captures du parcours normal sont identiques à V53. Pour 14 scénarios contrôlés dans chaque variante, les images après sélection sont identiques à celles de V53. Cela ne valide pas tous les déclenchements naturels des 85 blocs. Aucune ROM distribuée.

## Version précédente : V53 (traduction partielle)

V53 traite **les trois dialogues protégés restants par leurs entrées de personnage** : maison hantée, adieux et ascenseur. Elle traduit aussi le préfixe de confirmation d'achat « Objet: ». La table des personnages est vérifiée par dix références du moteur. Les anciennes entrées intérieures restent intactes ; certains chemins secondaires peuvent encore afficher l'anglais. Les menus restent pour la suite.

- [Patch V53 avec accents](patches/EarthBound_Beginnings_FR_v53_accents.ips)
- [Patch V53 ASCII](patches/EarthBound_Beginnings_FR_v53_ascii.ips)
- [Rapport V53](RAPPORT_V53.md)
- [Sources et tests](tools/v53/README_V53.md)
- [Essais Snes9x et captures](tests/emulation_v53/RAPPORT_EMULATION_V53.md)

Appliquer **un seul IPS V53 directement à la ROM originale USA 1.2**. 386 tests locaux réussis. Les 212 captures du parcours normal sont identiques à V52 ; quatre lectures contrôlées par variante vérifient les ajouts. Déclenchements naturels et embranchements complets restent à vérifier. Aucune ROM distribuée.

## Version précédente : V52 (traduction partielle)

V52 ajoute **16 fragments dans six contextes** : scène du club d'Ellay, appel du père, commande de pizza et réponses de paiement. « Amour et paix, ouais! » passe en français tout en conservant ses anciennes entrées intérieures. Le décompte inclut deux onomatopées. Les menus restent pour la suite.

- [Patch V52 avec accents](patches/EarthBound_Beginnings_FR_v52_accents.ips)
- [Patch V52 ASCII](patches/EarthBound_Beginnings_FR_v52_ascii.ips)
- [Rapport V52](RAPPORT_V52.md)
- [Sources et tests](tools/v52/README_V52.md)
- [Essais Snes9x et captures](tests/emulation_v52/RAPPORT_EMULATION_V52.md)

Appliquer **un seul IPS V52 directement à la ROM originale USA 1.2**. 357 tests locaux réussis. Les 212 captures du parcours normal sont identiques à V51 ; 17 lectures contrôlées par variante vérifient les ajouts. Trois des quatre fragments reportés par V51 restent protégés. Déclenchements naturels et embranchements complets restent à vérifier. Aucune ROM distribuée.

## Version précédente : V51 (traduction partielle)

V51 traduit **24 fragments auparavant protégés, dans 21 contextes** : trésor, fantômes, indices, montagne, pizza et descriptions d'objets. Des sauts vers des copies françaises conservent les anciennes entrées intérieures. Quatre des 28 fragments examinés restent reportés. Les menus restent pour la suite.

- [Patch V51 avec accents](patches/EarthBound_Beginnings_FR_v51_accents.ips)
- [Patch V51 ASCII](patches/EarthBound_Beginnings_FR_v51_ascii.ips)
- [Rapport V51](RAPPORT_V51.md)
- [Sources et tests](tools/v51/README_V51.md)
- [Essais Snes9x et captures](tests/emulation_v51/RAPPORT_EMULATION_V51.md)

Appliquer **un seul IPS V51 directement à la ROM originale USA 1.2**. 335 tests locaux réussis. Les 212 captures du parcours normal sont identiques à V50 ; 26 lectures contrôlées sont effectuées dans chaque variante. Les déclenchements naturels et les parcours entrant à l'intérieur des anciens textes restent à vérifier. Aucune ROM distribuée.

## Version précédente : V50 (traduction partielle)

V50 ajoute **46 fragments dans 29 contextes** et quatre petites routines privées pour « sa tête » et « son niveau max. ». Les 21 protections V49 sont auditées et conservées ; sept autres segments sont reportés. Les menus restent pour la suite.

- [Patch V50 avec accents](patches/EarthBound_Beginnings_FR_v50_accents.ips)
- [Patch V50 ASCII](patches/EarthBound_Beginnings_FR_v50_ascii.ips)
- [Rapport V50](RAPPORT_V50.md)
- [Sources, audit et tests](tools/v50/README_V50.md)
- [Essais Snes9x et captures](tests/emulation_v50/RAPPORT_EMULATION_V50.md)

Appliquer **un seul IPS V50 directement à la ROM originale USA 1.2**. 317 tests locaux réussis. Les 212 captures du parcours normal sont identiques à V49 ; treize cas d'affichage sont relus dans les deux variantes avec des fixtures contrôlées. Déclenchements naturels et embranchements restent à vérifier. Aucune ROM distribuée.

## Version précédente : V49 (traduction partielle)

V49 traduit **207 fragments lexicaux et quatre liaisons ou ponctuations dans 84 contextes** déjà partiellement français : Magicant, indices, école, appels, objets et chalet. Les segments communs sont dédoublonnés. Vingt et un segments visés par une adresse intérieure restent à examiner ; les menus restent pour la suite.

- [Patch V49 avec accents](patches/EarthBound_Beginnings_FR_v49_accents.ips)
- [Patch V49 ASCII](patches/EarthBound_Beginnings_FR_v49_ascii.ips)
- [Rapport V49](RAPPORT_V49.md)
- [Sources et tests](tools/v49/README_V49.md)
- [Essais Snes9x et captures](tests/emulation_v49/RAPPORT_EMULATION_V49.md)

Appliquer **un seul IPS V49 directement à la ROM originale USA 1.2**. 292 tests locaux réussis. Le parcours normal conserve les 212 captures V48 ; treize contextes sont relus par appel contrôlé dans les deux variantes. Les déclenchements naturels et embranchements restent à vérifier. Aucune ROM distribuée.

## Version précédente : V48 (traduction partielle)

V48 ajoute **66 fragments traduits dans 40 scripts et quatre routines privées**, plus deux corrections « Chacun ». Les phrases communes des descriptions d'objets passent en français : équipement, PV récupérés et usage unique ou répété. Les menus restent pour la suite.

- [Patch V48 avec accents](patches/EarthBound_Beginnings_FR_v48_accents.ips)
- [Patch V48 ASCII](patches/EarthBound_Beginnings_FR_v48_ascii.ips)
- [Rapport V48](RAPPORT_V48.md)
- [Sources et tests](tools/v48/README_V48.md)
- [Essais Snes9x et captures](tests/emulation_v48/RAPPORT_EMULATION_V48.md)

Appliquer **un seul IPS V48 directement à la ROM originale USA 1.2**. 272 tests locaux réussis. Le parcours normal conserve les 212 captures V47 ; huit messages et cinq contextes de descriptions sont relus par appel contrôlé dans les deux variantes. L'accès naturel aux scènes reste à vérifier. Aucune ROM distribuée.

## Version précédente : V47 (traduction partielle)

V47 ajoute **34 fragments traduits dans 21 scripts** : services, zoo, asthme, distraction et utilisation d'objets. Les menus restent pour la suite.

- [Patch V47 avec accents](patches/EarthBound_Beginnings_FR_v47_accents.ips)
- [Patch V47 ASCII](patches/EarthBound_Beginnings_FR_v47_ascii.ips)
- [Rapport V47](RAPPORT_V47.md)
- [Sources et tests](tools/v47/README_V47.md)
- [Essais Snes9x et captures](tests/emulation_v47/RAPPORT_EMULATION_V47.md)

Appliquer **un seul IPS V47 directement à la ROM originale USA 1.2**. 247 tests locaux réussis. Le parcours normal conserve les 212 captures V46 ; huit scripts sont relus par appel contrôlé dans les deux variantes. Leur accès naturel et les 13 autres scripts restent à vérifier. Aucune ROM distribuée.

## Version précédente : V46 (traduction partielle)

V46 traduit **deux messages de consommation** et corrige **sept contextes français** encore liés aux noms de groupes anglais. L'audit du lot préparatoire a retrouvé 98 sources déjà modifiées et deux brouillons identiques : ces 100 entrées ne sont pas comptées comme nouvelles intégrations.

- [Patch V46 avec accents](patches/EarthBound_Beginnings_FR_v46_accents.ips)
- [Patch V46 ASCII](patches/EarthBound_Beginnings_FR_v46_ascii.ips)
- [Rapport V46](RAPPORT_V46.md)
- [Sources et tests](tools/v46/README_V46.md)
- [Essais Snes9x](tests/emulation_v46/RAPPORT_EMULATION_V46.md)

Appliquer **un seul IPS V46 directement à la ROM originale USA 1.2**. 229 tests locaux réussis. Le menu Eat affiche le nouveau texte avec un pain de fixture ; l'EXP est relue dans le parcours normal. Les scènes tardives et les groupes multiples restent à vérifier. Les menus restent pour la suite. Aucune ROM distribuée.

## Version précédente : V45 (traduction partielle)

V45 ajoute **20 fragments français dans six messages et sept sous-routines privées** : inventaire plein, abandon d'objet, fuite et variations d'attaque/défense. Les raccords V44 déjà présents dans le dialogue de sélection sont conservés dans les nouvelles copies.

- [Patch V45 avec accents](patches/EarthBound_Beginnings_FR_v45_accents.ips)
- [Patch V45 ASCII](patches/EarthBound_Beginnings_FR_v45_ascii.ips)
- [Rapport V45](RAPPORT_V45.md)
- [Sources et tests](tools/v45/README_V45.md)
- [Essais Snes9x et captures](tests/emulation_v45/RAPPORT_EMULATION_V45.md)

Appliquer **un seul IPS V45 directement à la ROM originale USA 1.2**. 207 tests locaux réussis et parcours normal Snes9x conforme. Les dialogues d'inventaire et de fuite sont relus par routage contrôlé ; les notifications de statistiques restent à vérifier dans leur scène. Les menus restent pour la suite. Aucune ROM distribuée.

## Version précédente : V44 (traduction partielle)

V44 ajoute **93 fragments français dans 46 scripts de messages et six routines grammaticales privées** : combat, inventaire, services, Laura et Pippi. Elle corrige aussi **14 pointeurs V43** touchés par une collision entre la fin d'un script et l'entrée du suivant. Les menus restent pour la suite.

- [Patch V44 avec accents](patches/EarthBound_Beginnings_FR_v44_accents.ips)
- [Patch V44 ASCII](patches/EarthBound_Beginnings_FR_v44_ascii.ips)
- [Rapport V44 et corrections](RAPPORT_V44.md)
- [Traductions, constructeur et tests](tools/v44/README_V44.md)
- [Essais Snes9x et captures](tests/emulation_v44/RAPPORT_EMULATION_V44.md)

Appliquer **un seul IPS V44 directement à la ROM originale USA 1.2**. 181 tests locaux réussis. Le parcours normal Snes9x est conforme dans les deux profils ; dix messages sont relus dans chaque profil avec un routage de combat contrôlé. Leur accès naturel et les scènes tardives restent à vérifier. Aucune ROM distribuée.

## Version précédente : V43 (traduction partielle)

V43 ajoute **102 occurrences de fragments français dans 56 scripts** : combat, objets, réponses de services, variations de statistiques et souvenirs de Maria. Les menus restent pour la suite.

- [Patch V43 avec accents](patches/EarthBound_Beginnings_FR_v43_accents.ips)
- [Patch V43 ASCII](patches/EarthBound_Beginnings_FR_v43_ascii.ips)
- [Rapport V43](RAPPORT_V43.md)
- [Traductions, constructeur et tests](tools/v43/README_V43.md)
- [Essais Snes9x et limites](tests/emulation_v43/RAPPORT_EMULATION_V43.md)

Appliquer **un seul IPS V43 directement à la ROM originale USA 1.2**. 158 tests locaux réussis et parcours Snes9x conforme dans les deux profils. Deux opérandes antérieurs sont actualisés après preuve ; les autres octets antérieurs et le dictionnaire partagé sont préservés. Le nouveau message de « Voir » est relu sur la première lampe dans les deux profils ; les 55 autres scripts restent à vérifier dans leurs scènes. Aucune ROM distribuée.

## Version précédente : V42 (traduction partielle)

V42 traduit **187 occurrences de fragments dans 100 scripts d'actions hérités**, dont le message d'utilisation de la carte bancaire. Les copies françaises développent les tokens anglais sans modifier le dictionnaire partagé. Les dix références littérales non prouvées et les scripts sources restent intacts.

- [Patch V42 avec accents](patches/EarthBound_Beginnings_FR_v42_accents.ips)
- [Patch V42 ASCII](patches/EarthBound_Beginnings_FR_v42_ascii.ips)
- [Rapport V42](RAPPORT_V42.md)
- [Sources, dictionnaire utilisé et tests](tools/v42/README_V42.md)
- [Carte bancaire et Parer : preuves Snes9x](tests/emulation_v42/RAPPORT_EMULATION_V42.md)

Appliquer **un seul IPS V42 directement à la ROM originale USA 1.2**. 141 tests locaux réussis et parcours Snes9x conforme dans les deux profils. Carte bancaire et Parer sont relus par leurs commandes normales dans les deux profils ; l'accès et le rendu des 98 autres scripts restent à vérifier. Les menus restent pour la suite. Aucune ROM distribuée.

## Version précédente : V41 (traduction partielle)

V41 ajoute **197 occurrences de fragments français dans 108 scripts** : services, transports, hôtels, banque, objets et passages de l'épilogue. Ces occurrences correspondent à 125 fragments anglais distincts. Les choix Yes/No et les menus sont laissés pour leur passe dédiée.

- [Patch V41 avec accents](patches/EarthBound_Beginnings_FR_v41_accents.ips)
- [Patch V41 ASCII](patches/EarthBound_Beginnings_FR_v41_ascii.ips)
- [Rapport V41](RAPPORT_V41.md)
- [Traductions, constructeur et tests](tools/v41/README_V41.md)
- [Régression Snes9x et limites](tests/emulation_v41/RAPPORT_EMULATION_V41.md)

Appliquer **un seul IPS V41 directement à la ROM originale USA 1.2**. 124 tests locaux réussis et parcours Snes9x conforme dans les deux profils. Neuf opérandes antérieurs sont actualisés après preuve ; tous les autres octets antérieurs restent protégés. Les nouvelles scènes restent à vérifier dans leur contexte réel. Aucune ROM distribuée.

## Version précédente : V40 (traduction partielle)

V40 traduit **156 fragments nouveaux dans 80 scripts** : messages de combat, états, utilisation d'objets et répliques de Giygas. Les 11 raccords grammaticaux retirés et les 103 fragments neutres conservés ne sont pas ajoutés à ce compteur. Les menus restent pour une passe ultérieure.

- [Patch V40 avec accents](patches/EarthBound_Beginnings_FR_v40_accents.ips)
- [Patch V40 ASCII](patches/EarthBound_Beginnings_FR_v40_ascii.ips)
- [Rapport V40](RAPPORT_V40.md)
- [Traductions, constructeur et tests](tools/v40/README_V40.md)
- [Régression Snes9x et limites](tests/emulation_v40/RAPPORT_EMULATION_V40.md)

Appliquer **un seul IPS V40 directement à la ROM originale USA 1.2**. 109 tests locaux réussis, références et anciens IPS préservés, parcours Snes9x conforme dans les deux profils. Les nouveaux textes dans leurs scènes réelles restent à vérifier. Aucune ROM distribuée.

## Version précédente : V39 (traduction partielle)

V39 traduit **22 descriptions d'objets**, soit **32 fragments réellement nouveaux** : armes, protections, tickets et soins. Les 44 références de table et d'affichage sont raccordées aux copies françaises ; les scripts sources et les modifications V38 restent intacts.

- [Patch V39 avec accents](patches/EarthBound_Beginnings_FR_v39_accents.ips)
- [Patch V39 ASCII](patches/EarthBound_Beginnings_FR_v39_ascii.ips)
- [Rapport V39](RAPPORT_V39.md)
- [Traductions, constructeur et tests](tools/v39/README_V39.md)
- [Régression Snes9x et limites](tests/emulation_v39/RAPPORT_EMULATION_V39.md)

Appliquer **un seul IPS V39 directement à la ROM originale USA 1.2**. 94 tests locaux réussis et parcours normal Snes9x conforme dans les deux profils. Les 22 descriptions ont été relues dans chaque profil via Objets → Help!, avec un inventaire de test contrôlé : retours à la ligne, accents et noms dynamiques lisibles. L'acquisition naturelle des objets n'est pas couverte ; des messages annexes restent anglais. Aucune ROM distribuée.

## Version précédente : V38 (traduction partielle)

V38 relocalise et traduit **114 descriptions d'ennemis réellement nouvelles**, soit 126 fragments. Les 114 entrées de table et 17 alias de saut sont raccordés aux copies françaises; les anciens scripts et les seize redirections vides sont conservés.

- [Patch V38 avec accents](patches/EarthBound_Beginnings_FR_v38_accents.ips)
- [Patch V38 ASCII](patches/EarthBound_Beginnings_FR_v38_ascii.ips)
- [Rapport V38 et sécurité binaire](RAPPORT_V38.md)
- [Traductions, constructeur, manifeste et tests](tools/v38/README_V38.md)
- [Essais Snes9x](tests/emulation_v38/RAPPORT_EMULATION_V38.md)

Appliquer **un seul IPS V38 directement à la ROM originale USA 1.2**. 89 tests V38 à V29 et boy/girl sont réussis. Le parcours Snes9x ne présente aucune régression. Le premier combat normal permet de sélectionner « Voir », mais n'affiche que le nom de la lampe; le rendu réel des nouvelles descriptions reste donc à obtenir. Aucune ROM distribuée.

## Version précédente : V37 (traduction partielle)

V37 remplace le graphisme compressé **« SMAAAASH!! »** par **« COUP CRIT! »**. Les vingt tuiles dédiées sont recompressées dans la réserve V36; aucun dialogue ancien n'est recompté.

- [Patch V37 avec accents](patches/EarthBound_Beginnings_FR_v37_accents.ips)
- [Patch V37 ASCII](patches/EarthBound_Beginnings_FR_v37_ascii.ips)
- [Rapport V37 et sécurité binaire](RAPPORT_V37.md)
- [Constructeur, manifeste et aperçu](tools/v37/README_V37.md)
- [Essais et recherche du déclenchement normal](tests/emulation_v37/RAPPORT_EMULATION_V37.md)

Appliquer **un seul IPS V37 directement à la ROM originale USA 1.2**. 74 tests V37 à V29 et boy/girl sont réussis. Le parcours Snes9x ne présente aucune régression; le déclenchement naturel d'un coup critique reste à obtenir. La tentative `HP` → `PV`, incorrecte à cause de tuiles partagées, a été exclue. Aucune ROM distribuée.

## Version précédente : V36 (traduction partielle)

V36 remplace le graphisme compressé de victoire **« YOU WON! »** par **« VICTOIRE »**. Les 16 tuiles sont recompressées et relocalisées dans une réserve vérifiée ; aucun ancien fragment de dialogue n'est recompté.

- [Patch V36 avec accents](patches/EarthBound_Beginnings_FR_v36_accents.ips)
- [Patch V36 ASCII](patches/EarthBound_Beginnings_FR_v36_ascii.ips)
- [Rapport V36 et sécurité binaire](RAPPORT_V36.md)
- [Constructeur, manifeste et aperçu](tools/v36/README_V36.md)
- [Validation du combat normal sous Snes9x](tests/emulation_v36/RAPPORT_EMULATION_V36.md)

Appliquer **un seul IPS V36 directement à la ROM originale USA 1.2**. 64 tests V36/V35/V34/V33/V29/boy-girl sont réussis. Le premier combat affiche la bannière française dans les deux profils par son déclenchement normal. Aucune ROM distribuée.

## Version précédente : V35 (traduction partielle)

V35 corrige un angle mort des anciens remplacements IPS : **32 fragments anglais réellement nouveaux dans 31 scripts**, dont les choix « Non », deux textes longs, « Maison hantée », plusieurs raccords dynamiques et une indication du labyrinthe des singes. Les copies relocalisées contiennent 141 fragments : 32 nouveaux, 99 déjà français et 10 noms, cris ou signes conservés.

- [Patch V35 avec accents](patches/EarthBound_Beginnings_FR_v35_accents.ips)
- [Patch V35 ASCII](patches/EarthBound_Beginnings_FR_v35_ascii.ips)
- [Rapport V35 et limites](RAPPORT_V35.md)
- [Traductions réellement nouvelles](tools/v35/translations_v35.json)
- [Constructeur, manifeste et tests](tools/v35/README_V35.md)
- [Essais Snes9x](tests/emulation_v35/RAPPORT_EMULATION_V35.md)

Appliquer **un seul IPS V35 directement à la ROM originale USA 1.2**. 53 tests V35/V34/V33/V29/boy-girl et le parcours Snes9x de référence dans les deux profils sont réussis. Quatre nouvelles copies sont affichées par un point d'entrée temporaire; leurs déclencheurs narratifs normaux restent à vérifier. Aucune ROM distribuée.

## Version précédente : V34 (traduction partielle)

V34 nettoie **87 fragments anglais résiduels dans 62 scripts** : raccords autour des noms et objets dynamiques, messages de vente et d'utilisation, réponses courtes et dialogues mixtes. Les cris, noms propres et le langage fictif des singes restent volontairement inchangés et ne sont pas comptés.

- [Patch V34 avec accents](patches/EarthBound_Beginnings_FR_v34_accents.ips)
- [Patch V34 ASCII](patches/EarthBound_Beginnings_FR_v34_ascii.ips)
- [Rapport V34 et limites](RAPPORT_V34.md)
- [Traductions éditables](tools/v34/translations_v34.tsv)
- [Constructeur et tests](tools/v34/README_V34.md)
- [Essais Snes9x](tests/emulation_v34/RAPPORT_EMULATION_V34.md)

Appliquer **un seul IPS V34 directement à la ROM originale USA 1.2**. 16 tests V34, 34 contrôles de régression V33/V29/boy-girl et un parcours Snes9x dans les deux profils sont réussis. Cinq scripts sont inspectés par point d'entrée temporaire ; leurs déclencheurs normaux restent à vérifier. Aucune ROM distribuée.

## Version précédente : V33 (traduction partielle)

V33 révise et relocalise **58 dialogues et messages** : commerces, hébergements, indices et échanges secondaires. Les copies comprennent 153 fragments, dont 64 encore anglais dans V32. La continuation du dialogue du chien est aussi raccordée depuis la copie V31.

- [Patch V33 avec accents](patches/EarthBound_Beginnings_FR_v33_accents.ips)
- [Patch V33 ASCII](patches/EarthBound_Beginnings_FR_v33_ascii.ips)
- [Rapport V33 et limites](RAPPORT_V33.md)
- [Sources françaises](tools/v33/dialogues_fr.json)
- [Constructeur et tests](tools/v33/README_V33.md)
- [Essais Snes9x et affichage natif](tests/emulation_v33/RAPPORT_EMULATION_V33.md)

Appliquer **un seul IPS V33 directement à la ROM originale USA 1.2**. 14 tests réussis, parcours Snes9x du début conforme dans les deux variantes et cinq copies inspectées par point d'entrée temporaire. Les parcours narratifs et de vente restent à vérifier. Aucune ROM distribuée.

## Version précédente : V32 (traduction partielle)

V32 révise et relocalise **16 autres dialogues**, notamment Mary, Pippi, Lloyd et les livraisons. Les copies comprennent 140 fragments, dont 63 encore anglais dans V31. Les copies V31 et les corrections boy/girl sont conservées.

- [Patch V32 avec accents](patches/EarthBound_Beginnings_FR_v32_accents.ips)
- [Patch V32 ASCII](patches/EarthBound_Beginnings_FR_v32_ascii.ips)
- [Rapport V32 et limites](RAPPORT_V32.md)
- [Sources françaises](tools/v32/dialogues_fr.json)
- [Constructeur et tests](tools/v32/README_V32.md)
- [Essais Snes9x et affichage natif](tests/emulation_v32/RAPPORT_EMULATION_V32.md)

Appliquer **un seul IPS V32 directement à la ROM originale USA 1.2**. 13 tests réussis, parcours Snes9x du début conforme dans les deux variantes et quatre copies contrôlées par point d’entrée temporaire. Les déclencheurs narratifs et les anciennes entrées secondaires restent à vérifier. Aucune ROM distribuée.

## Version précédente : V31 (traduction partielle)

V31 révise et relocalise **16 dialogues complets** : conseils, COMBAT, trésor du chien, asthme, guitariste, appel maternel, médecin et autres échanges. Les copies françaises comprennent 132 fragments, dont 26 encore anglais dans V30. Les choix «Oui / Non» tiennent désormais sans abréviation dans les scripts concernés.

- [Patch V31 avec accents](patches/EarthBound_Beginnings_FR_v31_accents.ips)
- [Patch V31 ASCII](patches/EarthBound_Beginnings_FR_v31_ascii.ips)
- [Rapport V31 et limites](RAPPORT_V31.md)
- [Sources françaises](tools/v31/dialogues_fr.json)
- [Constructeur et tests](tools/v31/README_V31.md)
- [Essais Snes9x et affichage natif](tests/emulation_v31/RAPPORT_EMULATION_V31.md)

Appliquer **un seul IPS V31 directement à la ROM originale USA 1.2**. 12 tests réussis ; parcours Snes9x du début conforme dans les deux variantes et trois dialogues contrôlés par point d'entrée temporaire. Les scènes narratives et les anciennes entrées secondaires restent à vérifier. Aucune ROM distribuée.

## Version précédente : V30 (traduction partielle)

V30 ajoute **121 fragments français** : 95 dans les dialogues et interfaces du jeu, et 26 dans la boutique de test. Réponses courtes, appels téléphoniques, dépôt bancaire et réveil du dragon. Les corrections boy/girl de V29 sont conservées.

- [Patch V30 avec accents](patches/EarthBound_Beginnings_FR_v30_accents.ips)
- [Patch V30 ASCII](patches/EarthBound_Beginnings_FR_v30_ascii.ips)
- [Rapport V30 et limites](RAPPORT_V30.md)
- [Traductions éditables](tools/v30/translations_v30.tsv)
- [Constructeur, audit et tests](tools/v30/README_V30.md)
- [Essais Snes9x](tests/emulation_v30/RAPPORT_EMULATION_V30.md)

Appliquer **un seul IPS V30 directement à la ROM originale USA 1.2**. 28 tests V29–V30 réussis ; parcours Snes9x du début conforme dans les deux profils. Les nouvelles scènes restent à vérifier en jeu. Aucune ROM distribuée.

## Version précédente : V29 (traduction partielle)

V29 corrige les trois dialogues utilisant boy/girl : **garçon/fille** et **un écolier/une écolière**, avec leurs phrases françaises accordées. Elle conserve la V28 et ses 1 515 ajouts depuis V18 Work.

- [Patch V29 avec accents](patches/EarthBound_Beginnings_FR_v29_accents.ips)
- [Patch V29 ASCII](patches/EarthBound_Beginnings_FR_v29_ascii.ips)
- [Rapport V29 et limites](RAPPORT_V29.md)
- [Constructeur et tests](tools/v29/README_V29.md)
- [Essais Snes9x](tests/emulation_v29/RAPPORT_EMULATION_V29.md)

Appliquer **un seul IPS V29 directement à la ROM originale USA 1.2**. 12 tests V29 et 4 tests V28 réussis ; parcours Snes9x du début conforme dans les deux profils. Les trois dialogues et la sélection native avec Ana restent à vérifier en jeu. Aucune ROM distribuée.

## Version précédente : V28 (traduction partielle)

V28 ajoute **49 plages françaises dans 49 scripts** à V27, pour **1 515 ajouts depuis V18 Work**.

- [Patch V28 avec accents](patches/EarthBound_Beginnings_FR_v28_accents.ips)
- [Patch V28 ASCII](patches/EarthBound_Beginnings_FR_v28_ascii.ips)
- [Rapport V28](RAPPORT_V28.md)
- [Traductions V28](tools/v28/translations_v28.tsv)
- [Constructeur et tests V28](tools/v28/README_V28.md)

Appliquer un seul IPS V28 **directement à la ROM originale USA 1.2**. Les nouvelles plages ont été vérifiées sur la ROM ; le roundtrip complet des IPS autonomes et les essais V28 en émulateur restent à faire. Aucune ROM distribuée.


## Version précédente : V27 (traduction partielle)

V27 ajoute **176 plages françaises dans 124 scripts**, pour **1 466 plages depuis V18 Work**. Les nouvelles zones couvrent notamment commerces, dialogues de retour, banque, panneaux et messages secondaires.

- [Patch V27 avec accents](patches/EarthBound_Beginnings_FR_v27_accents.ips)
- [Patch V27 ASCII](patches/EarthBound_Beginnings_FR_v27_ascii.ips)
- [Rapport V27 et limites](RAPPORT_V27.md)
- [Traductions éditables](tools/v27/translations_v27.tsv)
- [Constructeur, audit et tests](tools/v27/README_V27.md)

Appliquer **un seul IPS V27 directement à la ROM originale USA 1.2**. Les 176 plages et 124 scripts parents ont été vérifiés sur la ROM originale; les deux IPS ont passé les contrôles structurels et de régression synthétique. **Le roundtrip complet sur ROM et les essais V27 en émulateur restent à effectuer.** Aucune ROM distribuée.


## Version précédente : V26 (traduction partielle)

V26 ajoute **175 plages dans 105 scripts**: Snowman, commerces, char du désert, singes et Téléportation. Les ajouts V19–V26 représentent **1 290 plages depuis V18 Work**.

- [Patch V26 avec accents](patches/EarthBound_Beginnings_FR_v26_accents.ips)
- [Patch V26 ASCII](patches/EarthBound_Beginnings_FR_v26_ascii.ips)
- [Rapport V26 et limites](RAPPORT_V26.md)
- [Traductions éditables](tools/v26/translations_v26.tsv)
- [Audit, constructeur et tests](tools/v26/README_V26.md)
- [Essais Snes9x](tests/emulation_v26/RAPPORT_EMULATION_V26.md)

Appliquer **un seul IPS V26 directement à la ROM originale USA 1.2**. 28 tests locaux réussis; parcours Snes9x du début du jeu conforme dans les deux variantes. Les nouvelles scènes restent à vérifier en jeu. Aucun fichier ROM distribué.

L’[audit dédié boy/girl](tools/boy_girl/RAPPORT_BOY_GIRL.md) confirme trois appels partagés et documente les corrections coordonnées requises; 8 tests binaires réussis, essai natif des deux branches encore à faire.

## Version précédente : V25


V25 ajoute **165 plages dans 86 scripts**: école, soins, inventions, appels familiaux, livraisons et scènes d'EVE et Maria. Les ajouts V19–V25 représentent **1 115 plages depuis V18 Work**.

- [Patch V25 avec accents](patches/EarthBound_Beginnings_FR_v25_accents.ips)
- [Patch V25 ASCII](patches/EarthBound_Beginnings_FR_v25_ascii.ips)
- [Rapport V25 et limites](RAPPORT_V25.md)
- [Traductions éditables](tools/v25/translations_v25.tsv)
- [Audit, constructeur et tests](tools/v25/README_V25.md)
- [Essais Snes9x](tests/emulation_v25/RAPPORT_EMULATION_V25.md)

Appliquer **un seul IPS V25 directement à la ROM originale USA 1.2**. 28 tests locaux réussis; parcours Snes9x du début du jeu conforme dans les deux profils. Les nouvelles scènes restent à vérifier en jeu. Deux fragments dépendant encore de la routine anglaise boy/girl sont exclus. Aucun fichier ROM distribué.

## Version précédente : V24


V24 élargit l'audit au catalogue complet et ajoute **213 plages de texte dans 124 scripts**, dont des fragments après commandes dynamiques. Les ajouts V19–V24 représentent **950 plages depuis V18 Work**.

- [Patch V24 avec accents](patches/EarthBound_Beginnings_FR_v24_accents.ips)
- [Patch V24 ASCII](patches/EarthBound_Beginnings_FR_v24_ascii.ips)
- [Rapport V24 et limites](RAPPORT_V24.md)
- [Traductions éditables](tools/v24/translations_v24.tsv)
- [Audit, constructeur et tests](tools/v24/README_V24.md)
- [Essais Snes9x](tests/emulation_v24/RAPPORT_EMULATION_V24.md)

Appliquer **un seul IPS V24 directement à la ROM originale USA 1.2**. 26 tests V23–V24 et CI locale réussis; parcours Snes9x du début du jeu conforme dans les deux profils. Les nouvelles plages dans leurs scènes restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V23


V23 ajoute **120 nouveaux segments** à V22: hôtels, commerces, soins, banque, canari et indices du journal. Les ajouts V19–V23 représentent **737 segments depuis V18 Work**.

- [Patch V23 avec accents](patches/EarthBound_Beginnings_FR_v23_accents.ips)
- [Patch V23 ASCII](patches/EarthBound_Beginnings_FR_v23_ascii.ips)
- [Rapport V23 et limites](RAPPORT_V23.md)
- [Traductions éditables](tools/v23/translations_v23.tsv)
- [Constructeur et tests](tools/v23/README_V23.md)
- [Essais Snes9x](tests/emulation_v23/RAPPORT_EMULATION_V23.md)

Appliquer **un seul IPS V23 directement à la ROM originale USA 1.2**. 20 tests V22–V23 réussis; parcours Snes9x du début du jeu conforme dans les deux profils. Les nouveaux segments dans leurs zones restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V22


V22 ajoute **185 nouveaux segments** à V21: dialogues de fin de jeu, commerces, Snowman, Youngtown et désert Yucca. Les ajouts V19–V22 représentent **617 segments depuis V18 Work**.

- [Patch V22 avec accents](patches/EarthBound_Beginnings_FR_v22_accents.ips)
- [Patch V22 ASCII](patches/EarthBound_Beginnings_FR_v22_ascii.ips)
- [Rapport V22 et limites](RAPPORT_V22.md)
- [Traductions éditables](tools/v22/translations_v22.tsv)
- [Constructeur et tests](tools/v22/README_V22.md)
- [Essais Snes9x et outil de rejeu](tests/emulation_v22/RAPPORT_EMULATION_V22.md)

Appliquer **un seul IPS V22 directement à la ROM originale USA 1.2**. 20 tests V21–V22 réussis; essais Snes9x du début du jeu réussis dans les deux profils. Les nouveaux segments dans leurs zones restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V21 Work


V21 ajoute **153 nouveaux segments** à V20 et conserve les **119 ajouts V19** et les **160 ajouts V20**: **432 ajouts depuis V18 Work**.

- [Patch V21 avec accents](patches/EarthBound_Beginnings_FR_v21_accents.ips)
- [Patch V21 ASCII](patches/EarthBound_Beginnings_FR_v21_ascii.ips)
- [Rapport V21 et limites](RAPPORT_V21.md)
- [Traductions éditables](tools/v21/translations_v21.tsv)
- [Constructeur et tests](tools/v21/README_V21.md)
- [Essais Snes9x](tests/emulation_v21/RAPPORT_EMULATION_V21.md)

Appliquer **un seul IPS V21 à la ROM originale USA 1.2**, sans préinstaller les anciennes versions. 45 tests V18–V21 réussis; essais Snes9x du début du jeu réussis dans les deux profils. Les nouveaux dialogues dans les zones ultérieures restent à vérifier en jeu. Aucune ROM distribuée.

## Version précédente : V18 Work


La V18 Work autonome reprend la V17 publiée et ajoute **168 segments** : 16 dans le premier lot V18, puis 152 dans la reprise Work. Les 70 segments de `traduction/v18_brouillons_01.json` sont un lot distinct non intégré et ne sont pas ajoutés à ce compteur.

- [Patch V18 Work avec accents](patches/EarthBound_Beginnings_FR_v18_work_accents.ips)
- [Patch V18 Work sans accents](patches/EarthBound_Beginnings_FR_v18_work_ascii.ips)
- [Rapport et instructions](tools/v18_work/README_WORK.md)
- [Constructeur portable](tools/v18_work/sources/build_work.py), [tests](tools/v18_work/sources/test_work.py), [résultats binaires](tools/v18_work/validation_work.json)
- [16 premières traductions](tools/v18_work/v18_dialogues_fr.json), [152 traductions Work](tools/v18_work/v18_work_dialogues_fr.json)

**Appliquer un seul IPS V18 Work directement à la ROM originale USA 1.2**, sans préinstaller V17 ou V18. Aucune ROM n'est distribuée.

Contrôles exécutés : reconstruction des deux variantes, décodage indépendant des 152 nouveaux textes, absence de collisions, conservation de la base et de tous les octets hors du nouveau lot, **10 tests réussis**. **Premiers essais Snes9x réussis dans les deux variantes** : nouveau jeu, introduction, exploration, premier combat remporté et restauration d'état. [Rapport et limites de couverture](tests/emulation_v18_work/RAPPORT_EMULATION_V18.md). La sauvegarde native et les 168 nouveaux segments dans leurs zones restent à tester; il s'agit d'une version de développement.

```sh
python3 tools/v18_work/sources/build_work.py "/chemin/ROM_originale.sfc"
ROM_PATH="/chemin/ROM_originale.sfc" python3 -m unittest discover -s tools/v18_work/sources -p test_work.py -v
```

## Version précédente : V17 (traduction partielle)

La **V17 autonome** reprend toutes les modifications V09–V16 et ajoute **195 segments français réellement modifiés dans 117 scripts**. Les trois scripts exclus du lot de 120 ne sont pas comptés. Depuis V09, les versions V10–V17 ajoutent **766 segments/blocs** cumulés (50 + 27 + 18 + 141 + 130 + 77 + 128 + 195).

- [Patch V17 avec accents](patches/EarthBound_Beginnings_FR_v17_accents.ips)
- [Patch V17 sans accents](patches/EarthBound_Beginnings_FR_v17_ascii.ips)
- [Rapport V17](RAPPORT_V17.md), [traductions](traduction/v17_traductions_117.json), [constructeur](traduction/construire_v17.py), [tests](tests/verifier_fusion_v17.py)
- [CI V17](https://github.com/spamkenny02-commits/earthboundbeginning/actions/workflows/verifier-v17.yml)

**Appliquer uniquement V17 directement à la ROM originale USA 1.2**, sans préinstaller V09 à V16.

```sh
python traduction/construire_v17.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v17
```

**Contrôles :** 117 scripts, 130 références HiROM vers leurs débuts, 195 remplacements, zéro collision avec les enregistrements IPS V16 dans les deux profils. Les contrôles binaires ne remplacent pas un parcours sous émulateur ; le jeu reste partiellement traduit.



## Archives de préparation V17

La [présélection historique](traduction/v17_priorites_non_verifiees.json), l'[outil de préparation](traduction/preparer_v17.py), les [tests synthétiques](tests/verifier_preparation_v17.py), leur CI et le [rapport archivé](RAPPORT_V17_PREPARATION.md) sont conservés. Cette préparation est antérieure aux IPS V17 publiés et à la V21 actuelle.

## Versions précédentes

Les rapports [V16](RAPPORT_V16.md), [V15](RAPPORT_V15.md), [V14](RAPPORT_V14.md), [V13](RAPPORT_V13.md), [V12](RAPPORT_V12.md), [V11](RAPPORT_V11.md) et [V10](RAPPORT_V10_ADDON.md) restent disponibles. Les anciens patchs sont archivés dans `patches/`.

## Historique V09 et atelier


Historique de l'intégration expérimentale v09 : **1 095 entrées intégrées et contrôlées**, introduction et 16 caractères accentués. Les quatre scènes bloquées de Podunk et le canari utilisent désormais des routines déplacées, avec `Oui / Non` et des phrases naturelles. Les tables de noms et de destinations extraites sont préparées. Un atelier CLI permet l’export et l’import CSV ainsi que la reconstruction vérifiée des deux variantes. Les deux variantes passent les contrôles binaires et les premiers essais depuis une nouvelle partie. Le téléphone est testé par une entrée isolée ; son parcours normal reste à vérifier. **La traduction reste partielle.**

La sauvegarde intégrale de la TBL, des textes extraits et du repérage graphique est dans `sauvegardes/atelier_extraction_graphismes_v02.zip`. Décompresser à la racine pour retrouver tout le dossier `atelier/` (les outils et rapports principaux sont également visibles directement).

Les traductions éditables sont dans `traduction/`. Les patchs IPS et leurs rapports sont dans `patches/`. Aucun fichier ROM n'est distribué.

ROM source attendue : EarthBound Beginnings (USA) 1.2.sfc, 4 Mio sans en-tête copieur.
SHA-256 : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

Avec Python 3 :

```sh
python traduction/integrer.py "ROM.sfc" --appliquer patches/EarthBound_Beginnings_FR_v09_accents.ips
```

Le résultat est écrit dans `build/EarthBound_Beginnings_FR.sfc`. La ROM source reste inchangée. Une variante `ascii.ips` est fournie pour comparer l'affichage sans les nouveaux glyphes accentués.

Pour reconstruire depuis les traductions, décompresser la sauvegarde puis :

```sh
python traduction/integrer.py "ROM.sfc"
```

Un libellé `No` trop court reste exclu et consigné dans le rapport. Certaines légendes utilisent des abréviations françaises. Les blocs à pointeurs intérieurs conservent leurs positions grâce à un remplissage par espaces. Les graphismes avec du texte anglais restent à modifier. Les noms d'objets hérités peuvent ne pas tous être utilisés par le remake.

Rapport actuel : [RAPPORT_V09.md](RAPPORT_V09.md). Étape précédente : [RAPPORT_V08.md](RAPPORT_V08.md). Historique : [RAPPORT_V01.md](RAPPORT_V01.md). Vérifications à effectuer : [TESTS_A_FAIRE.md](TESTS_A_FAIRE.md). Sous Windows, glisser la ROM originale sur `Appliquer_patch_FR.bat`.

Le kit courant est [EarthBound_Beginnings_FR_v09_atelier_patch.zip](distributions/EarthBound_Beginnings_FR_v09_atelier_patch.zip). Il contient les deux patchs et les sources nécessaires à leur intégration. Le moteur de déplacement vérifie la réserve et les références explicites ; voir RAPPORT_V09.md.

Guide de l’outil : [traduction/ATELIER.md](traduction/ATELIER.md). Le CSV couvre les champs et dialogues ordinaires préparés ; les autres formats restent éditables en JSON.

L’audit signale les fragments identiques à relire et refuse les rapports périmés. Le catalogue contient encore 2 043 blocs candidats non préparés : leur utilisation, leurs frontières et leur traduction restent à vérifier. Les graphismes et le générique ne sont pas finalisés.

Éditeur local : ouvrir `atelier_fr.html`, charger `traductions.csv`, puis utiliser `Importer_CSV_FR.bat` et `Reconstruire_FR.bat`. Les sources précédentes sont sauvegardées avant chaque import modifiant des fichiers.


