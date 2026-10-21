# Reprise — lot V78 en cours, cible 150 textes distincts

**21 octobre 2026 — reprise validée des corrections Minnie/contenant.** Environnement et travail local récupérés. Six écritures, 383 enregistrements ajoutés à V77 ; aucune allocation ni source nouvelle. Compteur inchangé : **119/150**, 157 plages sources. Voir [RAPPORT_V78_ARTICLES_CHECKPOINT.md](RAPPORT_V78_ARTICLES_CHECKPOINT.md).

48 paires V77/V78, huit changements limités au texte, 10 148 images échantillonnées. Dans les deux profils, la fiole ID70 est présente dans le sac page03, absente page08, dans la réserve page11, puis revenue au sac page19. Entrée PNJ204 forcée avec préparation native ; aucun parcours naturel certifié. « Le Fiole » est corrigé.

Prochain reste : limites du coursier, services avec plusieurs personnages, contexte ancien `32F120`/helper `38B587` conservé à qualifier, dialogues et parcours naturels ; puis menus. Il manque 31 sources à la cible, sans inventaire exhaustif prouvé. Continuer le même lot ; ces corrections françaises ajoutent zéro au compteur.

## Historique antérieur à cette reprise

**Blocage au 20 octobre 2026 : environnement local indisponible.** Le checkpoint distant reste à 119 textes. Des corrections Minnie/contenant supplémentaires étaient encore locales ; les récupérer avant toute réinitialisation. Voir [REPRISE_ENVIRONNEMENT_INDISPONIBLE.md](REPRISE_ENVIRONNEMENT_INDISPONIBLE.md) pour les écritures, les sondes et les validations interrompues. Aucun nouveau patch n'est validé par cette note.

**État actuel : 119 textes distincts / cible 150, 157 plages sources.** Même lot V78 sur `work/v78-batch150`, V77 reste publiée sur main. `context_grammar_stage.py` traduit trois sources partagées (table ci-dessous), sans nouvelle allocation ; huit enregistrements supplémentaires, total 377. Trois corrections françaises ne sont pas comptées comme de nouvelles traductions : préfixe du fils et deux majuscules après retrait du possessif redondant.

| Source nouvelle | Français | Offset |
|---|---|---|
| you | toi | 387B2B |
| you all | vous | 387B2F |
| you two | vous | 387B37 |

PNJ586 : racine `33FA7D`, chemin vers `32FCA0` puis `33FC4C` → unique appel de `387B19`. Le préfixe devient « Fiston se nomme comme » ; son saut est avancé de deux octets dans le même bloc pour éviter des espaces visibles et un point isolé à la ligne. Les helpers plurielles retournent juste après « vous », sans espaces avant le point ; leurs queues devenues inaccessibles sont nulles et n'ont aucune référence intérieure. PNJ1157 : racine `263B90` → `369D9B` / `369E9E` ; seules les deux insertions du possessif `387AA2` sont redirigées vers le retour vide existant `38B550`, car la phrase française dit déjà « notre aïeule ». Le helper original Your/nom's est intact.

18 tests V78 avec ROM privée ; reconstruction déterministe vérifiée. Preuves `tests/emulation_v78_grammar` : 56 paires V77/V78, douze changements textuels seulement, 12 256 images échantillonnées, six cas par profil relus. Le premier choix conditionnel de PNJ586 est `06 B8 00` : préparation native flag00B8. Les variantes plurielles sont des appels artificiels du helper puis de la ponctuation/pause `33FC51`, pas des parties à deux/trois personnages. Les branches de Maria sont forcées ; aucun parcours naturel ni écriture WRAM certifié. Les captures antérieures 81/99/114/116 gardent leurs snapshots.

**Prochain reste :** articles `38B52B–38B550`, dispatchs `38B551`, `38B56C`, `38B587`, à qualifier par appelant avant correction ; limites du coursier et plusieurs personnages ; anciennes branches et parcours naturels ; puis menus. Il manque 31 sources à la cible du lot, sans inventaire exhaustif déjà prouvé. Ne pas compter des corrections françaises, des noms propres ou des branches dormantes pour remplir la cible. Sorties privées retenues : `current_v78_grammar` / `reference_v78_grammar`. Rapport : `RAPPORT_V78_GRAMMAIRE_CHECKPOINT.md`.

## Historique du checkpoint à 116 textes

**État actuel : 116 textes distincts / cible 150, 154 plages sources.** V77 reste publiée sur main ; continuer le même lot V78 sur `work/v78-batch150`. Deux sources nouvelles, par copies contextuelles. La cible restante de 34 n'est pas un inventaire prouvé ; ne pas publier une release de deux textes.

L'aide de la bouteille d'eau ID6E est redirigée depuis son champ `1560E5` vers `330CA8`. La continuation médicale après « Dans ce cas, » est redirigée depuis le saut `329025` vers `32FC98`. `scoped_help_stage.py` copie les commandes et garde chaque mot entier ; 272 octets de remplissage protégés supplémentaires, total 3 431, 369 enregistrements ajoutés aux IPS V77. Les originaux restent intacts, notamment `054743`/occurrence `3C8B3F` et `0911F0`/occurrences `0047F0`, `00706A`. Aucun garde-fou global levé.

16 tests V78 réussis avec ROM privée. 36 nouvelles paires V77/V78, six changements limités aux fenêtres textuelles, 7 912 images échantillonnées ; 36 captures finales relues dans les deux profils. Cas : copie eau, original eau, continuation médicale via le saut précédent, original médical. Appels contrôlés via carte bancaire ; aucune écriture WRAM. Navigation naturelle dans Aide, diagnostic et consommation non certifiés. Les anciennes preuves 81/99/114 sont testées contre leurs snapshots, pas contre le nouvel IPS final.

**Suite concrète :** helpers possessifs/pronoms/articles `387AA2`, `387B19`, `38B532–38B54F` avec leurs appelants ; limites du coursier et services à plusieurs personnages ; autres références à l'ancienne aide eau (`05ABBA`, `37065F`) à qualifier avant redirection ; anciennes branches intérieures et parcours naturel. Puis menus et relecture. Le rôle des trois références brutes intérieures reste ouvert, mais ne bloque plus les deux chemins traduits : ne pas refaire leur audit pour le même appel. L'espace libre protégé est très fragmenté ; vérifier toute nouvelle allocation sans toucher aux sprites.

| Nouvelle source distincte | Français | Implantation source / copie |
|---|---|---|
| @When you drink it, your PP slightly increases. | @Bois pour gagner un peu de PP. | 05473C / via ID6E |
| @the best thing to do is to call home and hear your mom's voice. | @Passe un coup de fil à maman : sa voix te fera du bien. | 0911ED / via saut précédent |

Registre exact complet : `tools/v78/batch_ledger.json` ; la table historique de 114 sources ci-dessous, plus ces deux lignes, donne les 116. Rapport actuel : `RAPPORT_V78_COPIES_CHECKPOINT.md`. Sorties privées : `/workspace/scratch/98c4eaa3ef23/current_v78_scoped` et `reference_v78_scoped` ; publier seulement PNG, résultats, outils et IPS. Dépendances privées inchangées.

## Historique du checkpoint à 114 textes

**V77 reste publiée sur main. Continuer le même lot V78 avant publication.** Branche de checkpoint : `work/v78-batch150`. Compteur exact : **114 traductions distinctes / cible 150**, **152 plages physiques**. Cette reprise ajoute 15 sources distinctes au checkpoint de 99 textes. Un texte partagé entre plusieurs objets ou profils est compté une seule fois ; aucun nom propre, débogage ou texte dormant n'a été ajouté pour faire du volume.

Les aides restantes sont reliées à **82 identifiants d'objets dans les stocks de 25 wrappers PNJ personnalisés** : flag du wrapper → branche `3656DC` → commande `1A 06` → ligne de sept objets à partir de `1576B2` → table d'objets et pointeur d'aide. Huit listes de stocks sont relues en émulateur ; les autres liens sont statiques. Deux objets portent le nom Fiole de sérum : **A5 coûte 20 $ dans la pharmacie, 70 coûte 58 $**. Ne pas les confondre ni présenter A5 comme 70. Les résultats antérieurs utilisant 70 gardent cet identifiant.

Quinze plages sont remplacées en place : Charme de cristal/vitesse et paralysie, Casquette, Œuf frais, Panier-repas, Sauce spéciale, Accélérateur de rouille, Batte pro, Ours en peluche, Ruban et conseils communs aux condiments. `item_help_stage.py` garde les mots et commandes en place, sans allocation supplémentaire ni réécriture de pointeur. Le lot total conserve 3 159 octets alloués et ajoute 333 enregistrements aux IPS V77. Commandes, sprites, banque25 et table PNJ préservés.

**Validation : 30 tests ciblés réussis avec ROM privée** (14 V78 + 8 V77 + 8 V65). Hors ROM : 8 tests V78 réussis, 6 ignorés explicitement. **164 nouvelles paires V77/V78**, dont 46 changements dans les fenêtres de texte, 36 456 images échantillonnées, vingt cas par profil. Aides et huit stocks sont relus dans les deux profils ; aucun achat, équipement, consommation ou effet de soin n'est certifié. Les entrées sont forcées via la carte bancaire, sans préparation d'objet ni écriture directe WRAM. Les PNG et résultats nouveaux sont dans `tests/emulation_v78_help`.

Les anciennes preuves gardent leurs empreintes : 146 paires au checkpoint de 81 textes, 166 paires au checkpoint de 99 textes. Les tests reconstruisent ces deux IPS antérieurs avant de vérifier leurs captures ; ne pas présenter ces images comme celles de l'IPS actuel à 114 textes. Les devis et refus des quatre destinations restent acquis, sans voyage naturel certifié.

**Reste concret avant menus :**
- Bouteille d'eau ID6E : `05473C–054758` reste anglais. Une référence brute entre au milieu à `054743`, occurrence `3C8B3F` ; rôle à qualifier avant modification. L'anglais visible dans `water_guarded` est volontairement conservé comme preuve du reste.
- Message médical `0911ED–091212` toujours anglais. Les deux occurrences brutes de `0911F0` (`0047F0`, `00706A`) ressemblent à des instructions BEQ/CMP ; voir `alias_0911f0_notes.json`. Qualification CPU complète encore requise ; ne pas supprimer les garde-fous globalement.
- Helpers `387AA2` (Your/possessif), `387B19` (you/you all/you two), articles `38B532–38B54F` : qualifier les appelants et traiter par contexte sans casser le français existant.
- Limites du coursier, services avec plusieurs personnages, anciennes branches intérieures conservées et vrais parcours des scènes/générique. Puis menus généraux et relecture complète.
- Environ 36 sources manquent pour la taille de lot souhaitée ; ce nombre n'est pas un inventaire déjà prouvé. Continuer ce même lot sans nouvelle release après ce sous-ensemble.

Le contrôle ciblé `qualified_help_remaining.json` visite 106 racines pour les aides des 82 objets de boutique. Il reste une plage originale de plus de neuf caractères : la bouteille d'eau, zéro erreur d'analyse. Le seuil omet volontairement les fragments courts ; ce résultat ne prouve pas la fin de tous les textes du jeu. L'audit général actualisé contient 226 candidats sur 4 475 racines et 1 080 graines, sans erreur, avec héritage et débogage à exclure.

Sorties finales nouvelles : `/workspace/scratch/98c4eaa3ef23/current_v78_help_final` et référence `/workspace/scratch/98c4eaa3ef23/reference_v78_help_final`. Les essais initiaux `*_v78_help` exposaient encore les helpers partagés : remplacés. Anciennes sorties médicales et trains conservées selon les rapports. ROM/cœur privés décrits dans l'historique V74 ; états post-repos `reference_v71_lodging/{accents,ascii}/accept/handoff.state`. Ne publier ni ROM, cœur, états, ni dumps.

Voir `RAPPORT_V78_AIDES_CHECKPOINT.md` (état actuel) et `RAPPORT_V78_CHECKPOINT.md` (historique à 99 textes). Registre exact des sources et implantations ; les destinations des copies de banque25 sont détaillées dans les fixtures :

| Source distincte | Français | Offsets |
|---|---|---|
| @It also increases your Speed. | @Vitesse accrue | 053D10 |
| @It has the logo of your favorite baseball team. | @Logo de ton équipe préférée. | 053F68 |
| @So fresh, it's still warm! | @Frais et chaud ! | 054184 |
| @There's even a slice of your favorite cake! | @Avec ton gâteau préféré ! | 0541AE |
| @This is the best thing to take when you get poisoned. | @Idéal contre le poison. | 054792 |
| @Use by sprinkling it over food. | @À mettre sur un plat. | 054905 |
| @It tastes good with any kind of food, thereby | @Bonne avec tout plat, | 05491E |
| @increasing the recovery power of the food. | @renforce ses soins. | 054939 |
| @Quickly rusts metallic enemies when used during battle. | @Rouille les ennemis métalliques. | 054FAB |
| @The enemy will take about 200 points of damage. | @Environ 200 dégâts. | 054FD1 |
| @Wow! Look at the pine tar! It's almost all the way to the end! | @De la résine presque jusqu'au bout ! | 055ECB |
| A cute teddy bear! | Un joli nounours! | 056B5D |
| @It protects you from paralysis attacks. | @Protège de la paralysie. | 056BC5 |
| @Miscellaneous equipment that can only be used by  | @Accessoire exclusif destiné à  | 056C6D |
| @To use, sprinkle over food. | @Saupoudre ton plat. | 056D63 |
| @A good combination increases the strength of your recovery. | @Un bon mélange soigne mieux. | 056D7A |
| @I can examine each one of you for $ | @L'examen vous coûte $ | 090FF0 |
| Yes, please | Oui, merci | 091016 |
| No, thanks | Non, merci | 091024 |
| @You really don't need any treatment? | @Tu n'as vraiment besoin d'aucun soin ? | 091041 |
|   All right. |  D'accord. | 091053 |
| @Who is sick? | @Qui est malade ? | 091074 |
| @I don't think there is anything wrong with you. | @Tu m'as l'air en bonne santé. | 0910FB |
| @I don't think anyone has anything like that. | @Personne ne semble avoir ça. | 091113 |
| @Or Is it just my misunderstanding? | @Ou ai-je mal compris ? | 091127 |
| @I can only treat an illness. | @Je ne peux soigner que les maladies. | 091140 |
|   Sorry. |  Désolé. | 091153 |
| by the way, | au fait, | 091171 |
| @What a sad look in your eyes... you, the boy in a red cap. | @Tu as l'air triste, garçon au bonnet rouge... | 091178 |
| @You must be homesick. | @Tu dois avoir le mal du pays. | 09119C |
| @That's nothing you need to be ashamed of. | @Tu n'as pas à en avoir honte. | 0911AA |
| @Anybody who is on a long trip will miss home. | @Quand on voyage longtemps, la maison nous manque. | 0911C2 |
| @In this case, | @Dans ce cas, | 0911E2 |
| @You have a cold. | @Tu as un rhume. | 091214 |
| @You have sunstroke. | @Tu as une insolation. | 091222 |
| @You've been poisoned. | @Tu souffres d'un empoisonnement. | 091233 |
| @You must feel nauseous. | @Tu as la nausée. | 091245 |
| @You're all well now. | @Tu vas mieux ! | 09126F |
|   What a great doctor I am! |  Quel bon médecin je suis ! | 091278 |
| @Who do you want to see? | @Qui veux-tu voir ? | 09129A |
|  was just brought in, and is still unconscious. |  vient d'arriver sans connaissance. | 0912D5 |
| @Please pay $ | @Il faut payer $ | 0912F5 |
|  for the doctor's fee. |  pour les soins. | 091301 |
| Yes | Oui | 36EB83, 376B0B, 376C0D, 37715F, 380A46, 091311, 32E139, 380B5F, 384BA8, 384BE3, 251ABF, 25B0B7, 25B0FF, 25B147, 25B18F |
| No | Non | 36EB87, 376B0F, 376C11, 377163, 380A4A, 091315, 091B0E, 32E13D, 380B63, 384BAC, 384BE7, 251AC3, 25B0BB, 25B103, 25B14B, 25B193 |
| @Your friend, right?...  It's very serious. | @Ton ami, c'est ça ? Son état est grave. | 09132E |
| @I'm so glad that you recovered,  | @Ça va mieux,  | 09137D |
| @Come back any time you need. | @Reviens si tu as besoin de nous. | 091394 |
| @We don't have a person like that in our hospital. | @Ce patient n'est pas dans notre hôpital. | 0913A8 |
| @You don't have enough money...? | @Tu n'as pas assez d'argent ? | 0913C4 |
|   That's too bad. |  Quel dommage. | 091B30, 0913D0 |
| @If you are the patient, come into the back room. | @Si tu es le patient, va dans la salle du fond. | 0913E4 |
| @You need to be examined? | @Tu veux un examen ? | 091401 |
|   Then, you need to see the doctor... not me. |  Alors, vois le médecin... pas moi. | 091410 |
| @I'm not busy right now. | @Je suis disponible. | 09142C |
| @Shall I explain about the hospital system? | @Veux-tu savoir comment fonctionne l'hôpital ? | 091439 |
| @Yeah, well, I am actually pretty busy. | @Bon, en fait, j'ai du travail. | 09146D |
| @If a good friend of yours becomes unconscious, | @Si l'un de tes amis perd connaissance, | 091486 |
| @come to the hospital right away. | @viens à l'hôpital tout de suite. | 0914A5 |
| @As long as you have money for the doctor's fee, | @Si tu peux payer les soins, | 0914B8 |
| @you'll be able to see your friend completely recovered in no time. | @ton ami sera vite sur pied. | 0914D5 |
| @Besides being unconscious, whenever | @Même sans perdre connaissance, si | 0914FA |
| @you don't feel so well, come and talk to a doctor. | @tu te sens mal, viens consulter un médecin. | 091513 |
| @Everything I just told you applies to hospitals all over the world. | @Cela vaut pour les hôpitaux du monde entier. | 091532 |
| @Mmm, come back when necessary. | @Hum, reviens si tu en as besoin. | 0919F6, 0918BF |
| @Who needs healing? | @Qui faut-il soigner ? | 0918F7 |
|  isn't numb. |  ne souffre pas d'engourdissement. | 0919A7 |
|  isn't possessed. |  n'est pas sous emprise. | 0919BE |
|   Who needs to be healed? |  Qui faut-il soigner ? | 0919DA |
| @If you don't have any money, you'll just have to keep on going in your current state. | @Sans argent, tu devras continuer dans cet état. | 091A12 |
| @There!  You're already healed! | @Voilà ! Les soins sont terminés ! | 091A61 |
|   Can I do my job well, or what! |  Je fais du bon travail, hein ! | 091A74 |
| @Hey, now that I notice, | @Tiens, maintenant que j'y pense, | 091ABE |
| @could you sell me the mushroom growing on top of your head? | @Tu me vends le champignon qui pousse sur ta tête ? | 091ACD |
| @Come on, let's make a deal. | @Allez, faisons affaire. | 091AF2 |
| Sell | Oui / Vendre | 091B09, 37B9A4 |
| @Thanks. | @OK | 091B3D |
|   I'll pay you $50 for each mushroom. |  Je te donne $50 par champignon. | 091B41 |
| @All right, let's do it! | @D'accord, allons-y ! | 091B5A |
| @By the way, do you need any help? | @Au fait, as-tu besoin d'aide ? | 091C1C |
| @Do you need some help? | @As-tu besoin d'aide ? | 091C2F |
|  but, you need a ticket to ride. |  mais il te faut un billet. | 36DD0A |
| @Care to buy one? | @Tu en veux un ? | 36DD2C |
| @First let's go see what's happening in Youngtown. | @Voyons d'abord ce qui se passe à Youngtown. | 36E5EB |
| @Daddy... | @Papa... | 36E628 |
| @Believe in us! | @Crois en nous! | 36E66C |
| @I'm concerned about you, | @Je m'inquiète pour toi, | 36E832 |
| @(Huh, | @(Hein | 376ACE |
|  what?) |  quoi?) | 376AD6 |
| @(Do I look like a monkey?) | @(Je ressemble à un singe?) | 376AED |
| @(Cool down, dude.) | @(Du calme, mec.) | 376BC3 |
| @(Are you so serious all the time?) | @(Es-tu toujours aussi sérieux?) | 376BE7 |
| @(I've got a good story to tell you.) | @(Je connais une bonne histoire.) | 377122 |
| @(Want to hear it?) | @(Tu veux savoir?) | 377149 |
| @(Hubba hubba.) | @(Quel charme.) | 377426 |
|  and  |  et  | 378992 |
| @Welcome! | @Bonjour! | 3795A3, 3796D2, 379855, 3799D8, 379B5B, 379CDE, 379E5C |
| Buy | Acheter | 37B99E |
|   Watch out! |   Attention! | 37D47F |
| @(Incredibly enough, you found somebody's  | @(Tiens ! Tu trouves un objet perdu :  | 37D494 |
|  right under the sign!) |  sous ce panneau !) | 37D4C1 |
| @(Climb into the rocket?) | @(Monter dans la fusée ?) | 380A2A |
| @Have you ever tasted  | @Tu as déjà goûté :  | 380B42 |
| @Your balance is $ | @Ton solde est : $ | 384C44 |
| @Here...  Take it with you. | @Tiens... Prends l'argent. | 384CA6 |
| @Go think things over again. | @Va donc y réfléchir encore. | 384D94 |
| @Bye! | @Ciao | 384DB7 |
| @Please make sure it is correct. | @Vérifie bien que c'est correct. | 386D46 |
| Soften | Dépétrifier | 38B22B |
| Restore feeling | Sensibilité | 38B234 |
| Purify | Purifier | 38B246 |
| Refresh | Revigorer | 38B24F |
| @I need to charge you $ | @Cela te coûtera donc $ | 38B27F |
| @The monkey stole the  | @Le singe a volé :  | 38BADB |

## Historique V77 — version publiée

V77 est le patch actuel : treize fragments anglais traduits, un accord français corrigé ; treize plages fixes et un pont Non, 15 enregistrements ajoutés. Mineur `3738F8`/PNJ 210, billet/char `373C34`, prix `373CD8`, chameau `374307`/894 et relance `374409`. Le Non `374357` saute vers `328DBC` (11 octets), retour `37435C` ; la reprise `374351` utilise la même définition. Commandes dépliées, sprites, banque 25, table PNJ et créneau privé inchangés. Voir `RAPPORT_V77.md` et `tools/v77/README_V77.md`.

Cinq cas par profil, 48 captures relues, 48 comparaisons V76/V77 dont 28 différences textuelles uniquement, 10 500 images échantillonnées ; 23 tests ciblés V77/V76/V65 réussis. Les entrées complètes du mineur et du chameau sont forcées. Non → relance → Oui du chameau réellement vérifié. Billet/char et prix sont des appels intérieurs : ne pas certifier achat, location, argent débité ou trajet. Le mineur s'arrête à la question d'itinéraire. Aucun accès naturel ni écriture WRAM directe.

**Prochain lot concret : maison hantée `36EB50`/PNJ 411 puis singes `376ABE`/904, `376BB7`/905, `377108`/908**. Le relevé direct actualisé `tools/v77/custom_npc_roots_v77.json` contient 181 racines, zéro erreur et six candidats (les quatre ci-dessus, panneau `37D45C`, fusée `380A2A`). Il n'est ni récursif ni exhaustif et ne mesure pas un taux. Les anciennes lignes canari, Pippi, revente, mineur et chameau sont traitées. Restent services calculés/variantes, menus, générique et parcours naturel complet. Aucun 100 %.

Checkpoint initial local `6e58b18`, branche `work/v77-desert-local` ; checkpoint validé `work/v77-desert-validated`. Sorties privées retenues `/workspace/scratch/98c4eaa3ef23/validated_v77`, référence `/workspace/scratch/98c4eaa3ef23/reference_v76_desert`. Dépendances ROM/cœur/états identiques à V76/V75 ci-dessous. Ne publier que patches, outils, résultats et PNG, jamais ROM/cœur/états/dumps.

## Historique V76

V76 est le patch actuel : six plages anglaises de Pippi remplacées en place, sans allocation, réécriture de pointeur ni changement de commandes. Racine `386B63`, PNJ 319 champ 9, opérande `2036E0`. Fermeture utile : `386B63`, `386BAD`, `386BC9`, `386C58`. Sprites, banque 25 et créneau privé inchangés. Voir `RAPPORT_V76.md` et `tools/v76/README_V76.md`.

Quatre cas par profil : entrée complète, Podunk+secret, secret seul, matin. 34 captures relues, 34 comparaisons V75/V76 dont 28 changements textuels seulement, 7 524 images échantillonnées ; 23 tests ciblés V76/V75/V65 réussis. L'entrée complète suit les flags de l'état post-repos, mais tous les accès initiaux sont forcés. Les trois autres appels isolent volontairement des branches intérieures. Aucun accès naturel ni écriture WRAM directe.

**Prochaine priorité : mineur `3738F8`/PNJ 210**, puis chameau `374307`/894 et autres candidats historiques V73 non traités. Canari `3861D3`, Pippi `386B63` et revente `387221` sont traités ; le relevé demeure non récursif et non exhaustif. Branche équipée de revente, services multijoueurs, menus et parcours naturel complet restent à vérifier. Aucun 100 %.

Checkpoint initial local `56e78e0`, branche `work/v76-pippi-local`; checkpoint validé `work/v76-pippi-validated`. Sorties privées : `/workspace/scratch/98c4eaa3ef23/explore_v76` (retenue comme V76 validée après relecture) et `/workspace/scratch/98c4eaa3ef23/reference_v75_pippi`. Les preuves publiées ne contiennent que 68 PNG, résultats et comparaisons ; jamais ROM, cœur, états ou dumps. Dépendances privées identiques à V75 ci-dessous.

## Historique V75

V75 est le patch actuel : sept fragments traduits, cinq plages fixes et deux ponts Non (22 octets), neuf enregistrements ajoutés aux IPS V74. Entrée `3861D3`, PNJ 291 champ 9, opérande `203504` inchangé. Branche mélodie `32CC90`, réponse sur le chant `38636E`. Copies Non : `3302D4` → `38623F` et `330408` → `32CCEF`. Sprites, banque 25, commandes dépliées et pointeur PNJ préservés. Voir `RAPPORT_V75.md` et `tools/v75/README_V75.md`.

Cinq cas dans chaque profil : sans petit, petit Oui/Non, mélodie Oui/Non. 42 captures relues, 42 comparaisons V74/V75 dont 18 différences textuelles seulement ; 9 364 images échantillonnées, 24 tests ciblés V75/V74/V65 réussis. Entrée du PNJ forcée par carte bancaire ; petit donné par commande native A8. Mélodie appelée directement à sa branche, sans préparation de flag. Aucun accès naturel, retour du petit ni apprentissage réel de mélodie prouvé. Les deux refus sont bien distincts dans les preuves retenues.

**Prochaine priorité concrète : Pippi `386B63`/PNJ 319**, puis mines `3738F8`/210 et autres candidats historiques V73. Ne plus compter le canari `3861D3` ni la revente `387221` comme non traités dans ce relevé. Il ne constitue pas une couverture récursive/exhaustive. Branche équipée de revente, limites du coursier, plusieurs personnages, menus et parcours naturel complet restent à vérifier. Aucun 100 %.

Checkpoint initial local `f744b5a`, branche `work/v75-canary-local` ; checkpoint validé `work/v75-canary-validated`. Sorties privées retenues : `/workspace/scratch/98c4eaa3ef23/validated_v75`, référence `/workspace/scratch/98c4eaa3ef23/reference_v74_canary_final`. Les premières sorties `explore_v75` et `reference_v74_canary` sélectionnaient Oui dans les cas nommés Non : exclues. La question apparaît après un seul A, puis Droite+A choisit Non. Le probe et les PNG publiés reprennent uniquement la séquence corrigée. Les dépendances privées sont celles décrites dans V74 ci-dessous et leurs empreintes sont dans les résultats V75. Ne jamais publier ROM, cœur, états ou dumps.

## Historique V74

V74 est le patch actuel : service complet `387221`, PNJ 87 champ 9, opérande `202778` inchangé. Neuf fragments anglais traduits, deux formulations françaises améliorées. Quatre définitions « Non » en stockage protégé (44 octets), 15 enregistrements ajoutés. Voir `RAPPORT_V74.md` et `tools/v74/README_V74.md`.

Quatre scénarios par profil, 56 captures relues et comparées V73/V74, 30 différences textuelles seulement, 12 044 images échantillonnées ; 24 tests ciblés V74/V73/V65 réussis. Vente d'une Fiole : offre 29 $, portefeuille 20 → 49 $, inventaire final carte seule. Refus de l'offre : dialogue et argent vérifiés, inventaire non rouvert. Carte protégée et sortie vérifiées. Entrée forcée par carte bancaire ; don préparatoire natif déclaré, aucune écriture directe WRAM. Branche équipée seulement contrôlée statiquement. Pas d'accès naturel certifié.

**Prochaine priorité : canari `3861D3`/PNJ 291**, puis Pippi `386B63`/319 et autres lignes de `tools/v73/custom_npc_roots_v73.json`, sauf `387221` désormais traité. Ne pas refaire les audits acquis sans raison. Menus `Use/Eat/Give/Drop/Help!` encore anglais ; autres personnages, limites de coursier et parcours naturel complet restent à vérifier. Aucun 100 %.

Sauvegardes locales initiales `a6cd3ef`, `61fbc28`, branches `work/v74-resale-local`, `work/v74-resale-polish-local`. Checkpoint validé : `work/v74-resale-validated`. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v74`, référence `/workspace/scratch/98c4eaa3ef23/reference_v73_resale`. Les deux répertoires `v74_explore` et `v74_sale_explore` sont exploratoires.

Dépendances **actuelles V74** : l'ancien répertoire `60defd300f2e` et les états V33 ne sont plus disponibles. ROM récupérée auprès du fichier utilisateur et vérifiée : `/workspace/scratch/98c4eaa3ef23/private_v74/EarthBound Beginnings (USA) 1.2(1).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`. Cœur : `/workspace/scratch/c267dac1e2c1/emulator/snes9x_libretro_standard.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`. États utilisés : `/workspace/scratch/98c4eaa3ef23/reference_v71_lodging/{accents,ascii}/accept/handoff.state` (post-repos : Ninten, 30 PV, 10 PP, 20 $, carte). Leurs empreintes figurent dans les résultats V74. Ne jamais les présenter comme les états V33. Ne rien publier de ces dépendances. Les paragraphes suivants sont historiques, y compris les anciens chemins.

## Historique V73

V73 est le patch actuel : huit plages du service `37899B` (PNJ 898, opérande `205D53`) traduites, dont Oui/Non. Sept remplacements fixes et un pont de définition de « Non » : saut de cinq octets à `378A32` vers onze octets protégés à `330200`, retour à `378A37`. Les commandes dépliées, branches, scripts de repos, sprites, banque 25 et pointeur PNJ sont préservés. Voir `RAPPORT_V73.md` et `tools/v73/README_V73.md`.

Trois essais dans chaque profil : refus, acceptation et conversation après repos depuis l'état privé de l'acceptation. L'entrée complète est forcée par carte bancaire ; aucun flag ni PV préparé par l'outil. Le jeu exécute le repos et le changement de pièce ; PV observés 18 → 30, PP 10 inchangés. Pas de preuve de rencontre naturelle du PNJ. 40 captures relues, 40 comparaisons dont 18 changements uniquement textuels, 9 296 images échantillonnées et 20 tests ciblés réussis. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v73`, référence `/workspace/scratch/98c4eaa3ef23/reference_v71_lodging`. L'exploration `v73_explore` est privée.

**Prochaine priorité concrète : `387221`, champ 9 du PNJ 87, service de retour d'objets encore anglais.** Lire ensuite `tools/v73/custom_npc_roots_v73.json` : 181 racines directes de `[36BB00,3F0000)` examinées, 11 candidats après V73. Autres pistes : `3861D3`/PNJ 291 (canari), `386B63`/319 (Pippi), `3738F8`/210 (mines), dialogues et sélecteurs. Ce relevé n'est pas une fermeture récursive ni une preuve d'accès naturel/classification linguistique. L'ancien filtre NPC `330000–36BB00` et copies connues omettait ces racines ; ne plus conclure à l'exhaustivité à partir de son graphe sans erreur.

Checkpoint initial distant `work/v73-lodging` : `460ed6283742df76ecc2e0bf42ec1a9b88990976` ; checkpoint validé `work/v73-lodging-validated`. Éviter de refaire les audits V68–V72 sans changement qui le justifie. Réserve pleine/limite de trois côté coursier et autres personnages restent à valider, puis menus généraux, noms tronqués et parcours complet. Aucun 100 % certifié. Les paragraphes suivants sont historiques.

V72 est un audit sans nouvel IPS : **V71 reste le patch actuel**. Voir `RAPPORT_V72.md` et `tools/v72/README_V72.md`. Après dépôt, la réserve contient bien Fiole + sagesse + vitalité. Après livraison de deux objets sur trois, vitalité reste seule ; après livraison d'un sur deux, sagesse reste seule. Ces trois cas sont vérifiés dans les deux profils à partir d'états privés sauvegardés après le départ du coursier : six chaînes, 12 sessions, 174 captures contrôlées, 36 captures clés relues et 10 tests ciblés réussis.

La phase suivante recharge exactement l'état de passage et appelle `34B490`. Après dépôt, aucune opération intermédiaire ; après livraison partielle, retrait natif d'un Badge Franklin de l'inventaire pour libérer une case, sans toucher à la réserve ni au reliquat. Le téléphone initial et l'accès au stockage sont forcés ; le coursier arrive par le mécanisme normal. Les empreintes de passage sont publiées, pas les états. Les six touches d'accès après livraison partielle sont nécessaires ; avec un sac plein, même le bon accès refuse d'ouvrir la réserve. Ne pas compter ces premiers essais comme une lecture de reliquat.

Sorties privées retenues : `/workspace/scratch/98c4eaa3ef23/validated_v72_free_slot`. Les sorties `v72_explore` et `validated_v72` sont exploratoires et non publiées. Checkpoint validé : `work/v72-courier-storage`. Ne pas refaire ces trois contrôles sans nouvelle modification qui les justifie.

Prochain lot concret : branches de coursier sur réserve pleine et limite de trois objets, ou autres enseignes/hôtels pour chercher le prochain anglais réellement affiché. Les cas à plusieurs personnages restent non vérifiés. Ensuite menus d'action et libellés longs tronqués dans certaines listes à deux colonnes ; parcours naturel complet et générique restent nécessaires. Aucun 100 % certifié. Les paragraphes suivants sont historiques.

V71 est le patch actuel : 32 plages traduites en place, commandes, sprites et banque 25 préservés. Voir `RAPPORT_V71.md` et `tools/v71/README_V71.md`. Le wrapper privé accorde trois objets puis appelle le téléphone complet `35C597` ; Maman puis Déposer sont choisis à la manette. Après 600 images, le mécanisme normal du jeu fait arriver le coursier, jamais appelé directement par le test. Le téléphone initial reste artificiel.

Six scénarios dans chaque profil : dépôt de trois objets avec inventaire final, confirmation d'un dépôt simple, paiement refusé, argent nul, carte protégée et confirmation refusée/reprise. Seul le premier certifie l'inventaire final (carte seule) et les frais (20 → 2 $). Les autres s'arrêtent aux dialogues utiles ou au menu. La réserve n'a pas encore été rouverte après le coursier : c'est le prochain lot concret, avec le reliquat des livraisons partielles. Réserve pleine, limite de trois et variante de présentation : traductions statiquement contrôlées, affichage non certifié.

Sorties privées retenues : `/workspace/scratch/98c4eaa3ef23/validated_v71_accepted` et `/workspace/scratch/98c4eaa3ef23/reference_v70_pickup_accepted`. Les tentatives sans suffixe, `_stable` et `_final` contiennent des navigations finales non fiables et ne sont pas les preuves publiées. Ne pas les compter. Le probe public se limite aux séquences acceptées ; la fermeture A/B et des A supplémentaires peuvent laisser le menu actif ou sélectionner Parler au lieu des objets. Garder des sorties distinctes lors d'explorations.

Checkpoint initial local `013572a195040ddbfd10acb8bd6b6fb2e5d5245a`, distant `work/v71-pickup` : `158efc7a433e7207195be2a4f63c7f7e2b1f8615`. Checkpoint validé : `work/v71-pickup-validated`. Les paragraphes suivants sont historiques. Menus d'action encore anglais et parcours complet restant : pas de 100 % certifié.

V70 est le patch actuel : 24 plages du coursier traduites en place, sans allocation ni changement des commandes. Voir `RAPPORT_V70.md` et `tools/v70/README_V70.md`. Douze essais valides, 338 comparaisons V67/V70 dont 92 changements uniquement textuels ; 116 captures de coursier/inventaire relues. Les autres preuves V69 ci-dessous restent historiques.

Le téléphone complet `35C597` est appelé par une fixture privée ; après commande à la manette et attente de 600 images, le coursier arrive par le mécanisme du jeu, sans appel forcé à sa racine `0642A3`. Six cas dans chaque profil : trois objets, sans argent, refus de paiement/retour accepté, retour refusé/nouvelle réponse, deux places libres, une place libre. Frais 18 $ au total, pas par objet. Préparations natives déclarées, aucune écriture directe WRAM.

Prochain reste concret : coursier de dépôt, ou vérifier le reliquat après livraison partielle, puis sac totalement plein et autres personnages. Le cas exploratoire `no_room` n'a pas atteint le dialogue attendu et est exclu des preuves ; ne pas le compter. Le probe public conserve seulement les six cas valides. Les sorties privées principales sont `/workspace/scratch/98c4eaa3ef23/validated_v70`, références `/workspace/scratch/98c4eaa3ef23/reference_v67_courier`. La tentative exclue reste uniquement dans les sorties privées.

Checkpoint initial distant `work/v70-courier` : `80752c2d8a885c370cec00d659282b85e3cc0e78` ; checkpoint validé `work/v70-courier-validated`. Le code de décompression `b.spans_fr` reconnaît les commandes dictionnaire comme texte ; ne pas utiliser les seuls fragments littéraux du parseur pour conclure à l'absence d'anglais. Les menus Use/Eat/Give/Drop/Help! et certains chevauchements de fenêtres préexistants restent à traiter. 100 % non certifié.

V69 est un audit sans nouveau patch : les IPS V67 restent actuels. Voir `RAPPORT_V69.md`. Réserve pleine relue sur quatre pages, 10 + 10 + 10 + 6 = 36 Fioles ; dépôt refusé, retrait normal puis redépôt normal et nouveau refus. Six sessions, 50 captures, 10 676 images échantillonnées. Checkpoint `work/v69-full-storage` : `56bbfdd78971750717a258712ac1105b5fe4c716`.

Préparation privée en trois phases par commandes natives : 13 insertions de réserve `1D 18 70 00`, puis 13 autres, puis 10 et un don à Ninten avant le service. Pas d'écriture directe en WRAM ; états privés chaînés après retour à la carte. Les numéros « Réserve (1)… » désignent les pages, pas des quantités. Pour lire toutes les pages : cinq Bas+A depuis la première, puis A, puis A (le curseur reste sur la ligne de changement de page), enfin Bas avant de sélectionner l'objet. Les essais R ou cinq Bas répétés à chaque page étaient incorrects et ne sont pas des preuves. Les résultats publiés ne reprennent que la séquence correcte. Sorties privées `/workspace/scratch/98c4eaa3ef23/validated_v69`.

V68 est un **audit sans nouveau patch** : les IPS V67 restent actuels et inchangés. Voir `RAPPORT_V68.md` et `tools/v68/README_V68.md`. Retrait sur inventaire plein refusé en français, puis récupération après libération d'une case, avec réserve d'une Fiole encore intacte après le refus puis vide après récupération. Six sessions, 50 captures relues, 10 564 images échantillonnées. Checkpoint `work/v68-storage-audit` : `171a0c75eb39658da9a8db61df24a307c751c33b`.

Le probe V68 chaîne trois états privés après sortie du service. Préparations natives : 13 ajouts de Fiole (ID 70), dépôt normal d'une Fiole ; ajout d'une Fiole pour bloquer le retrait ; suppression d'une Fiole pour libérer une case, puis récupération normale. Ce ne sont pas des préparations naturelles. Les deux dernières phases exigent six touches de déclenchement, pas cinq : sinon l'essai reste au menu d'action et ne prouve rien. Les empreintes des états de passage, pas leurs contenus, sont conservées dans les résultats. Sorties privées : `/workspace/scratch/98c4eaa3ef23/validated_v68` ; exploration antérieure `v68_explore` non exhaustive. Aucun nouvel accès naturel certifié.

V67 est le patch actuel : `37BBB0` et `37BBBB`, « Just one / Multiple » → « Un seul / En lot », à taille constante. Voir `RAPPORT_V67.md`. 14 essais principaux, 86 captures relues, 18 476 images échantillonnées, 86 comparaisons V66/V67 dont six sélecteurs changent seulement dans la fenêtre de texte. Checkpoint `work/v67-quantity` : `3e9c380fe117780c612a71753ac04b106e67971c`.

Les préparations d'inventaire sont **artificielles et déclarées** : treize commandes natives `1D 00 01 01` ajoutent des Badges Franklin avant le service. Elles restent dans la fixture privée, jamais dans l'IPS. L'inventaire de 14 cases et le refus d'achat sont visibles ; le retrait vers un inventaire plein reste non testé. L'achat en lot de 1, le refus de 2 faute d'argent, le stockage vide et les soins acceptés sont contrôlés dans les deux profils. Aucun nouvel accès naturel certifié.

L'ancien dépôt local V38 `/workspace/scratch/60defd300f2e/earthboundbeginning` a une archive modifiée et reste intact. Le travail courant est dans `/workspace/scratch/98c4eaa3ef23/earthboundbeginning`, copie propre issue de main V66. Les chemins de dépendances ci-dessous sont mis à jour ; les anciens états V41 n'ont pas été retrouvés, les références V66 ont été rejouées avec les états V33.

V66 ajoute deux traductions à taille fixe : sélecteur Escargo `063734` / `06373E`, « Pick-up / Delivery » → « Déposer / Retirer ». Voir `RAPPORT_V66.md` et `tools/v66/README_V66.md`. Douze essais principaux, 178 captures relues, 36 204 images échantillonnées et 48 comparaisons avec V65 (deux paires changent, seulement le sélecteur). Checkpoint `work/v66-services` : `e3c3ec3aef576884747a5d817c907fe07884d0a2`.

Les fins d'appel Papa sans sauvegarde (gratuit/payant), le refus du téléphone sans argent, le refus bancaire de 2 $ sur compte de 1 $, Maman puis les deux choix Escargo sont maintenant contrôlés dans les deux profils. Les appels sont forcés comme en V65 : pas de nouvel accès naturel prouvé. Escargo demande un coursier au dépôt et indique une réserve vide au retrait ; son arrivée et les transferts restent à tester. Attention : ouvrir le sélecteur avec A en page 19, puis Droite+A en page 20 pour choisir réellement Retirer. L'ancienne exploration anticipait Droite et n'est pas une preuve de retrait.

V65 est terminée pour le lot décrit dans `RAPPORT_V65.md` et `tools/v65/README_V65.md`. Consulter le dernier état Git et ne pas écraser les modifications d'une autre exécution. V62/V63 n'ont pas d'IPS. Priorité utilisateur : 100 % des textes visibles, services et accès calculés, puis menus. Main est autorisée ; sauvegarder chaque gros lot.

## Ce qui est validé

V64 reste la base : quatre plages bancaires traduites. V65 corrige deux confirmations « The Fiole de sérum » au dépôt et à la récupération. L'auxiliaire partagé `38B587` est inchangé ; une copie privée conserve sa classification/dispatch et retourne sans article anglais. La phrase de dépôt devient « Cet objet sera bien au chaud. ».

Attention au stockage historique : le pointeur de récupération `259B27` est dans une ancienne copie qui chevauche des sprites. Ne pas le modifier directement. V65 relocalise les sept scripts de banque 25 du graphe de `34B490` dans neuf blocs de remplissage protégé : 338 octets sources + 10 octets de sauts + 27 octets d'auxiliaire = 375 octets. Banque 25, auxiliaire original et sprites restent identiques à V64. Voir fixtures, reconstructeur et tests V65. `330FC0–331000` est exclu de l'allocation pour conserver le créneau des probes.

593 tests passent (575 historiques + 4 V63 + 6 V64 + 8 V65). Six essais V65, 84 captures relues, 40 comparaisons V64/V65 limitées au texte. Checkpoint final du code : `work/v65-storage-safe`, `a3081132ab378f643d36ebfaa1e6e230e179b6e6`.

Les accès ont été **forcés** par un wrapper temporaire à `330FC0`, appelé par la redirection de quatre octets à `368B51`. Le wrapper enchaîne uniquement `08 pointeur` vers les scripts complets puis `02`. Les touches activent ensuite le vrai moteur ; aucune écriture directe en WRAM ni callback assembleur. Ce n'est pas une visite naturelle sur la carte.

Le cycle bancaire fait trois appels du distributeur : dépôt de 1 $, retrait de 1 $, puis refus sur compte redevenu nul. La poche revient de 19 à 20 $. Le stockage enchaîne achat puis service : dépôt confirmé, réserve contenant une Fiole, récupération confirmée, puis réserve vide. Les effets sont vérifiés à l'écran, pas par lecture dédiée des champs mémoire d'argent/inventaire.

## Prochain lot utile

1. Tester les plafonds et annulations supplémentaires ; retrait positif validé en V65, refus au-delà du solde en V66. L'ancienne réouverture via le menu principal n'était pas fiable et ne doit pas être utilisée comme preuve.
2. Vérifier plusieurs personnages et objets variés. Le retrait bloqué par inventaire plein est contrôlé en V68, la réserve pleine en V69, pour Ninten seul ; ne pas étendre ces preuves à d'autres configurations. Les préparations par commandes natives doivent rester explicitement déclarées et hors des IPS publiés.
3. Tester d'autres enseignes, hôtels, autres téléphones et effets des coursiers. Les fins d'appel Maman/Papa sans sauvegarde sont relues en V66 ; les soins acceptés en V67. Ne pas étendre cette preuve aux autres configurations.
4. Examiner les autres anciennes racines NPC sous `330000` que V62 exclut. V64 a trouvé le distributeur ainsi : 17 NPC pointent vers `0680A6`/`0680C2`. Élargir prudemment les graines avec leur provenance réelle ; certaines entrées sont héritées/dormantes. Une occurrence littérale de pointeur peut être une donnée graphique.
5. Piste du soigneur classée : NPC 149, racine `24D4A0`, « you have » est un faux positif. Les octets `15 0D` traversent les commandes `1A 15` et `0D 00` et ne sont pas un fragment textuel. La branche de refus est relue dans les deux profils ; ce contexte n'est pas modifié par V65.

Les menus d'action Use/Eat/Give/Drop/Help! restent pour la phase menus. 100 % des textes visibles n'est pas certifié.

## Dépendances privées de cet espace

Dépôt courant : `/workspace/scratch/98c4eaa3ef23/earthboundbeginning`.

- ROM : `/workspace/scratch/60defd300f2e/downloads/EarthBound Beginnings (USA) 1.2(1).sfc`, SHA256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- Cœur : `/workspace/scratch/c267dac1e2c1/emulator/snes9x_libretro_standard.so`, SHA256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.
- États V33 : `/workspace/scratch/60defd300f2e/emulation_v33/{accents,ascii}/after_combat.state`. SHA256 : accents `622aa30903aeffe159b1b748d8537776a7a2c092dda3ef70eeca26434acaf4a7`, ASCII `9364b593e11b3beeb993dfe8c63f161362f1a6e1c31402f332f5484ff9aa2ee0`.
- Runner : `tests/emulation_v18_work/libretro_runner.py` ; `--history-every 120` accélère l'échantillonnage sans perdre les commandes du journal final.
- Assembleur original : `v62_analysis/ebsrc`, Herringway/ebsrc révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`.

Ne jamais publier ROM, cœur, états ou dumps mémoire. Si le scratch est réinitialisé, récupérer main/checkpoints et poursuivre les analyses possibles sans inventer de validation d'émulateur.

## Reprise des outils

`tools/v65/service_session.py` hérite des opérations du runner V64 et ajoute le wrapper de services successifs. `tests/emulation_v65/probe.py` décrit les trois scénarios retenus. `--version 64 --case buy_store_retrieve` rejoue la référence ; utiliser une sortie distincte. Les cas V64 restent disponibles pour les essais simples.

Pour le stockage V65, ne pas précipiter les menus : après dépôt, A affiche Oui/Non ; Right+A (Non) revient à Déposer/Retirer ; Right+A (Retirer) affiche la question de récupération ; A ouvre la réserve, A choisit la Fiole, A choisit Ninten ; la confirmation suit. La séquence complète est dans le probe.

Entrées de service déjà explorées :
- `0680A6` : ATM complet, vérifie la carte ; `0680C2` est l'autre champ NPC. Dépôt : A (menu), Right+A (Dépôt), A (consigne), A (nombre), Up+A (1 $), A (merci). Les nombres démarrent sur les unités ; Left puis Up trois fois saisit 30 $.
- `35C597` : téléphone gratuit ; A ouvre Papa/Maman, Down+A choisit Maman. Papa propose la sauvegarde après présentation/niveau/EXP.
- `365592` : boutique (NPC 90), enseigne choisie selon les flags ; A puis A atteint les objets. Fiole de sérum à 20 $ disponible avec la somme initiale.
- `34B490` : stockage (NPC 1002), A ouvre Déposer/Retirer.

Le téléphone de la maison essayé dans `v64_explore` ne donnait que Biiip/R.A.S. ; ne pas le compter comme conversation naturelle réussie.

Sorties privées V65 : `/workspace/scratch/98c4eaa3ef23/validated_v65`, `reference_v64`, `explore`, `regressions_v65.log`. Les explorations intermédiaires ne sont pas toutes validées ; seuls les résultats publiés décrivent les séquences retenues. Les dépendances ROM/cœur/états restent aux chemins ci-dessus. Le dépôt contient les captures et références utiles, sans données privées.

## Publication

Le push shell n'a pas d'identifiants. Utiliser les outils GitHub create_blob (base64), create_tree avec base_tree_sha, create_commit puis create_branch pour le checkpoint ; update_ref main avec expected_sha et force=false après validation. Vérifier hashes blobs/arbre local/distant. Les publications API créent un SHA de commit différent du local : fetch puis aligner la branche locale seulement si arbre identique, en conservant une branche d'archive locale. Ne jamais force-pusher main.
