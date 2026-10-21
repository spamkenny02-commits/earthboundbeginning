# V78 — checkpoint à 137 textes, cible 400

**État actuel, 21 octobre 2026 : 137/400 sources distinctes, 175 plages comptées.** Huit nouvelles sources depuis le checkpoint129 : cinq commandes d'objets et trois fragments d'aide des clés. Deux fragments du message natif de PV sont corrigés sans nouvelle source comptée : une copie avait déjà été traduite en V43. Même lot, sans petite release.

Les commandes natives d'objets deviennent « Util. / Aval. / Donne / Jette / Aide » dans leurs cinq cases de six octets, sans modification du lecteur ni de son pas. « Mange » et « Mang. » ont été remplacés par « Aval. » après constat de troncature. L'aide de la Machine à clés et celle de la clé du casier sont traduites. Récupération du Papier froissé PNJ606 et nouvelle tentative PNJ608 après consommation d'un biscuit : parcours à la manette après préparation native D1. Rapport et preuves : `RAPPORT_V78_COMMANDES_CHECKPOINT.md`, `tests/emulation_v78_actions`.

**Reprise concrète :** casier PNJ609/Bracelet claquant (le placement précédent a rencontré un casier vide ; ne pas le déclarer validé), autres flags des casiers et trajets naturels. Puis poursuivre les menus et autres aides accessibles, avant la fin/générique et la relecture intégrale. Les huit sources nouvelles sont listées dans le rapport et le registre `tools/v78/batch_ledger.json`. Il manque 263 sources à la cible du lot ; aucun inventaire exhaustif des restes du jeu n'est établi.

**Validation du checkpoint137 : 28 tests V78 réussis avec ROM privée ; 132 paires V77/V78, 60 changements textuels, 34 084 images échantillonnées.** Deux profils relus, 26 captures clés. Commit local intermédiaire conservé ; checkpoint Git, sans publication du lot400 incomplet.

## Historique à 129 sources — qualification initiale des casiers

**État actuel, 21 octobre 2026 : 129/400 sources distinctes, 167 plages.** Neuf sources des casiers de l'école sont nouvellement traduites. Les variantes accents/ASCII, les six PNJ partageant le texte et les captures ne sont pas comptés en double. Même lot V78 ; aucune petite release.

Interaction ordinaire « Voir » puis utilisation de la Machine à clés sur PNJ608/champ13 → `38E2C2`, après téléportation native D1 et passage à la manette par la porte existante. Ouverture, objet reçu (Fusée-jouet en kit), clé tordue, casier vide et sac plein contrôlés dans les deux profils. 108 paires V77/V78, 28 changements limités au texte, 27 436 images échantillonnées. Les racines des casiers ne sont pas appelées directement par la sonde ; le trajet initial naturel reste non certifié. Rapport : `RAPPORT_V78_CASIERS_CHECKPOINT.md`.

**Reprise concrète :** autres contenus des PNJ606/609 et reprise après libération d'une place au sac (zéro nouvelle source pour le texte partagé) ; qualifier ensuite le lecteur natif des commandes d'objets `38E834` et traduire les libellés encore anglais. Menus, fin, générique et relecture intégrale restent ouverts. Il reste 271 sources à la cible du lot ; ce nombre ne constitue pas un inventaire du jeu restant.

## Historique à 120 sources — état antérieur à la qualification des casiers

**Checkpoint à plusieurs personnages, 21 octobre 2026 :** Ninten dépose la fiole ID70, Ana la récupère ; les inventaires finaux sont relus dans les deux profils. Deux et trois personnages sont réellement présents via commandes natives de préparation ; le sélecteur choisit respectivement `387B37` et `387B2F`, et affiche « vous ». Les entrées de scènes restent forcées. 56 nouvelles paires V77/V78, huit changements textuels, 11 728 images échantillonnées ; **24 tests V78 réussis avec ROM privée**. Aucun texte nouvellement traduit dans ce checkpoint de validation ; les IPS sont identiques au précédent.

Rapport : `RAPPORT_V78_PARTY_CHECKPOINT.md`. Suivi de la recherche d'oublis et de la relecture : `tools/v78/review_coverage.json` ; menus, fin, générique et relecture intégrale restent ouverts.

**Prochain reste concret avant les menus :** qualifier l'usage de la Machine à clés IDAC avec PNJ608/champ13 → `38E2C2`, puis les textes anglais `06FA0C/06FA2E/06FA68/06FA93/06FAB4`. Les liens existent, mais l'accès en jeu n'est pas encore prouvé ; ne pas traduire cet héritage pour remplir 400. Les flags `0459` et `037F` contrôlent les branches. L'ancienne copie `32F120` n'est pas atteinte par les 47 racines du graphe typé actuel de `34B490` ; son seul pointeur brut est `34B745`, hors de ce graphe. Elle reste conservée, sans déclaration globale de dormance. Éviter de refaire ce seul audit sans nouvelle preuve d'appel calculé.

## Historique avant le passage de la cible à 400


**21 octobre 2026 — checkpoint coursier, 120/150 sources distinctes, 158 plages.** Le même lot V78 continue ; V77 reste sur main. Une source visible adaptée : `35CFFF`, « @No: *pssst psst pssst* » → « @Num.: *pssst psst pssst* ». C'est une abréviation de numéro, pas une réponse Non. Registre exact : `tools/v78/batch_ledger.json`.

Limite de trois objets vérifiée avec quatre objets disponibles : Fiole/sagesse/vitalité en réserve, vitesse conservée au sac, frais 18 $. Réserve pleine chez le coursier : refus français, quatre objets et 20 $ conservés, 36 objets relus sur quatre pages. Téléphone et inspection forcés ; sortie de la maison à la manette et arrivée native. Pour le second cas, dix insertions natives remplissent artificiellement la réserve après l'appel. Aucun parcours complet naturel certifié.

152 paires V77/V78, quatre différences textuelles seulement, 46 620 images échantillonnées ; 26 captures clés relues dans les deux profils. Rapport : `RAPPORT_V78_COURSIER_CHECKPOINT.md`. Les anciennes preuves restent des snapshots historiques.

**Suite :** configurations à plusieurs personnages, ancienne copie `32F120`/helper `38B587` et autres dialogues accessibles à qualifier ; puis menus et parcours naturels. La limite effective de trois est prouvée, mais le message intérieur `064240` n'a pas été atteint ; ne pas le déclarer validé à l'écran. Il manque 30 sources à la cible, sans inventaire exhaustif prouvé ; ne pas remplir ce nombre avec du débogage ou des textes dormants.

## Historique avant le checkpoint coursier à 120 sources


**21 octobre 2026 — reprise validée des corrections Minnie/contenant.** Environnement et travail local récupérés. Six écritures, 383 enregistrements ajoutés à V77 ; aucune allocation ni source nouvelle. Compteur inchangé : **119/150**, 157 plages sources. Voir [RAPPORT_V78_ARTICLES_CHECKPOINT.md](../../RAPPORT_V78_ARTICLES_CHECKPOINT.md).

48 paires V77/V78, huit changements limités au texte, 10 148 images échantillonnées. Dans les deux profils, la fiole ID70 est présente dans le sac page03, absente page08, dans la réserve page11, puis revenue au sac page19. Entrée PNJ204 forcée avec préparation native ; aucun parcours naturel certifié. « Le Fiole » est corrigé.

Prochain reste : limites du coursier, services avec plusieurs personnages, contexte ancien `32F120`/helper `38B587` conservé à qualifier, dialogues et parcours naturels ; puis menus. Il manque 31 sources à la cible, sans inventaire exhaustif prouvé. Continuer le même lot ; ces corrections françaises ajoutent zéro au compteur.

## Historique antérieur à cette reprise

context_grammar_stage.py ajoute trois sources partagées (you/toi, you all/vous, you two/vous) et trois corrections de français, non comptées comme traductions nouvelles. Deux insertions possessives dans Maria sont redirigées vers un retour vide existant ; le helper original est conservé. Le préfixe du fils est raccourci avec son saut déplacé dans le même bloc. Aucune allocation ; total 377 enregistrements ajoutés aux IPS V77, 119 sources / 157 plages sources.

18 tests V78 avec ROM privée, reconstruction déterministe ; nouvelles preuves tests/emulation_v78_grammar : 56 paires, douze changements textuels, 12 256 images échantillonnées. Six cas par profil. Les variantes plurielles sont explicitement artificielles ; entrée PNJ586 forcée avec flag00B8, branches Maria forcées. Aucune progression naturelle certifiée. Les snapshots 81/99/114/116 restent reconstruits pour leurs anciennes preuves. Rapport actuel : RAPPORT_V78_GRAMMAIRE_CHECKPOINT.md ; suite : articles par appelant et services restants, puis menus.

## Historique du checkpoint à 116 textes

État actuel : 116 sources distinctes, 154 plages sources traitées. scoped_help_stage.py ajoute deux copies contextuelles après item_help_stage.py ; les originaux et alias intérieurs restent intacts. Aide ID6E : champ 1560E5 → 330CA8. Médical : retour du pont précédent 329025 → 32FC98. 272 octets protégés supplémentaires, 369 enregistrements ajoutés aux IPS V77.

16 tests V78 réussissent avec EARTHBOUND_ROM. Les tests hors ROM vérifient aussi les 36 nouvelles paires de tests/emulation_v78_scoped. Six changements textuels seulement, quatre cas par profil, 7 912 images échantillonnées. Appels artificiels, navigation naturelle et effets non certifiés. Chaque preuve antérieure est reconstruite depuis son snapshot 81/99/114. Voir RAPPORT_V78_COPIES_CHECKPOINT.md et REPRISE_TRADUCTION.md pour les limites et la suite du même lot. V77 reste publiée sur main.

## Historique du checkpoint à 114 textes

État actuel : 114 sources distinctes, 152 plages. item_help_stage.py ajoute 15 traductions en place, sans allocation. Ses 82 objets sont reliés aux stocks de wrappers PNJ personnalisés ; huit listes de stocks et les aides sélectionnées sont relues en émulateur. Les helpers d'aide partagés sont inclus par un chemin d'appels typés, et comptés une fois.

Nouvelles preuves : tests/emulation_v78_help, 164 paires dont 46 changements textuels et 36 456 images échantillonnées. python3 tools/v78/verify_help.py les vérifie. 14 tests V78 passent avec EARTHBOUND_ROM ; sans ROM, 8 passent et 6 sont ignorés. Le constructeur et update_ledger.py régénèrent les compteurs.

Les captures médicales et trains conservent respectivement les snapshots de 81 et 99 textes, reconstruits pour leurs contrôles. Elles ne sont pas présentées comme des captures du nouveau patch. La bouteille d'eau reste anglaise à 05473C, garde-fou sur 054743. L'aide A5 de la pharmacie à 20 $ est distincte de l'objet70 à 58 $. Voir RAPPORT_V78_AIDES_CHECKPOINT.md et REPRISE_TRADUCTION.md pour les limites et la reprise. Les paragraphes suivants décrivent le checkpoint précédent.

## Historique du checkpoint à 99 textes

V77 reste publiée. V78 compte 99 sources distinctes dans 137 plages, cible 150 ; registre exact dans batch_ledger.json et REPRISE_TRADUCTION.md. Les variantes contextuelles de Sell, Oui/Non répétés et profils sont dédoublonnés.

build_v78.py construit successivement le groupe PNJ, medical_stage.py puis remaining_stage.py. Le dernier module copie cinq scripts superposés à des sprites dans la banque25 sans en modifier un octet. Ses cinq redirections sont gardées par un inventaire exhaustif de leurs pointeurs explicites. Les mots, commandes et définitions de choix restent entiers dans les copies. Les quatre devis du train sont parcourus depuis leur script parent ; les appels directs sans contexte sont exclus des preuves.

Construction privée : python3 tools/v78/build_v78.py --rom CHEMIN_PRIVE --out patches
Registre : python3 tools/v78/update_ledger.py
Tests : python3 -m unittest discover -s tools/v78 -v
Tests complets : définir EARTHBOUND_ROM au chemin privé.
Vérifications RGB : python3 tools/v78/verify_display.py et python3 tools/v78/verify_remaining.py

Les 146 paires médicales certifient exactement le checkpoint de 81 textes. Les 166 paires de tests/emulation_v78_remaining certifient le checkpoint actuel : 66 changements textuels, 37 060 images échantillonnées. Tests complets : 12 V78 réussis ; hors ROM, 7 réussis et 5 ignorés. Les captures médicales sont vérifiées contre leur ancien IPS reconstruit, les captures restantes contre l'IPS final.

Les probes utilisent ServiceSession, avec préparations natives flag0339, flag0376 et don AB explicitement déclarées. Aucune écriture WRAM directe. Les devis et refus sont validés, aucun voyage certifié ; les branches de retrait/remise ne prouvent pas de transfert bancaire. Hôtel : salutation seulement. Youngtown : phrase affichée, animation suivante hors contexte ; Papa et Crois en nous statiques. Les menus généraux restent pour la phase suivante.

collect_evidence.py --remaining enregistre les PNG et rapports dans tests/emulation_v78_remaining ; les dépendances et sorties binaires privées restent hors dépôt. La fenêtre des devis du train est limitée à y126, les autres à y98. Les séquences corrigées et les sorties retenues sont indiquées dans REPRISE_TRADUCTION.md.

audit_active_text.py ajoute les mots courts omis (Buy/Sell/Welcome/Bye/Care/Daddy/Believe). Ses 237 candidats incluent des données héritées et des aides sans usage établi. Ne pas traduire pour atteindre artificiellement 150. L'alias médical 0911F0 reste à qualifier.
