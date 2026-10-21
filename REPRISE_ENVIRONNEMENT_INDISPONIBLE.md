# Reprise après indisponibilité de l'environnement — 20 octobre 2026

**21 octobre 2026 — reprise validée des corrections Minnie/contenant.** Environnement et travail local récupérés. Six écritures, 383 enregistrements ajoutés à V77 ; aucune allocation ni source nouvelle. Compteur inchangé : **119/150**, 157 plages sources. Voir [RAPPORT_V78_ARTICLES_CHECKPOINT.md](RAPPORT_V78_ARTICLES_CHECKPOINT.md).

48 paires V77/V78, huit changements limités au texte, 10 148 images échantillonnées. Dans les deux profils, la fiole ID70 est présente dans le sac page03, absente page08, dans la réserve page11, puis revenue au sac page19. Entrée PNJ204 forcée avec préparation native ; aucun parcours naturel certifié. « Le Fiole » est corrigé.

Prochain reste : limites du coursier, services avec plusieurs personnages, contexte ancien `32F120`/helper `38B587` conservé à qualifier, dialogues et parcours naturels ; puis menus. Il manque 31 sources à la cible, sans inventaire exhaustif prouvé. Continuer le même lot ; ces corrections françaises ajoutent zéro au compteur.

## Historique antérieur à cette reprise

Le moteur d'exécution local répond : « No usable execution environment is available ». L'environnement est signalé indisponible. GitHub demeure accessible. Impossible de vérifier le répertoire de travail, ses processus/verrous, de sauvegarder un nouveau commit local, de reconstruire les IPS ou de terminer les captures. Ne pas déduire que les fichiers privés ont été supprimés : leur présence n'est simplement plus vérifiable.

## État distant confirmé

Branche work/v78-batch150, dernier checkpoint de traduction confirmé : 79a3db97f0a6d5d5e4f52392c517724041a1ce34, arbre fde25fec87320751e7cd6f0fb6461a8bb7362a85. 119 textes distincts, 157 plages sources, cible 150. Le checkpoint décrit 18 tests V78 avec ROM privée et 56 paires de grammaire ; ces résultats sont antérieurs à la présente indisponibilité. Aucun test nouveau n'a été exécuté ici. V77 reste la version publiée sur main. Les présentes notes ne changent aucun patch ni compteur et ne constituent pas une nouvelle version.

## Travail local non poussé à récupérer avant toute réinitialisation

Dans /workspace/scratch/98c4eaa3ef23/earthboundbeginning, la dernière session avait ajouté article_context_stage.py et test_article_context.py dans tools/v78, intégré le module à build_v78.py, adapté test_context_grammar.py et test_v78.py aux snapshots, et créé tests/emulation_v78_articles/probe.py avec ses captures et rapports. Les fixtures, validation et IPS locaux avaient été reconstruits. Aucun commit local de ce sous-ensemble ni push de ces fichiers n'est confirmé. Ne pas écraser ce travail par un checkout/reset du checkpoint distant.

Les corrections d'articles portent sur deux chemins qualifiés seulement :
- PNJ1420, champ9 à 207FFD : 3803F1 → 32B500, appel à 32B50A de 38B551.
- PNJ204/Minnie, champ9 à 202F3D : 36B788 → 36B7D5, appel à 36B830 de 38B56C.

Réutiliser l'auxiliaire neutre V65 existant à 32AA40. Ses six premiers octets de classification/dispatch sont identiques aux deux auxiliaires originaux ; ses cinq branches pointent vers le retour vide 38B550. Conserver le classificateur et le dispatch, sans suppression globale des articles. L'ancienne copie 32F120, avec appel à 32F157 de 38B587, n'était pas reliée par le parcours testé depuis 34B490 ; son rôle reste à qualifier. Elle est conservée, sans la déclarer définitivement dormante.

Cinq écritures prévues, sans nouvelle allocation :

| Offset | Contenu / intention |
|---|---|
| 32B50A | Pointeur HiROM vers 32AA40 |
| 36B830 | Pointeur HiROM vers 32AA40 |
| 32B501 | Littéral @Objet: suivi d'une espace, huit octets encodés |
| 32B511 | Point encodé, commandes 03 02, puis quinze octets nuls inaccessibles |
| 36B839 | Deux espaces + Cet objet sera bien gardé. + une espace, 29 octets encodés |

Le contenant passe de « Il y a [article anglais][objet] à l'intérieur ! » à une légende « Objet: [objet]. ». Minnie emploie une confirmation neutre en genre. Vérifier toutes les bornes, références intérieures, commandes, empreintes de sprites et réserves avant publication. Les auxiliaires partagés 38B52B–38B5A2, la copie 32F120–32F1B2, la banque25, la table PNJ et le créneau de test restent intacts.

Ce sous-ensemble représente des corrections de contexte, pas de nouvelles sources ajoutées au registre : garder 119/150 et 157 plages sources. La construction locale avait ajouté cinq enregistrements (377 → 382), avec les empreintes suivantes observées avant indisponibilité, à reproduire plutôt qu'à considérer comme validées à nouveau :
- IPS accents : d1efcbe101164ef719d75bea1d0cc87bdda66405375a78143929033ad258b020 ; ROM cible privée : fe54b46cc909d1b93492e176a34d905be25e4ff2427159fcaea1f5082947d25c.
- IPS ASCII : 66e92303b7884db337d0f6522dee3d5cbcc899a07e4b709cf340031d0ffb7daf ; ROM cible privée : c9761d5d07af8872d0ed238206b4fa95f61fee229cdcac2c1ab3b8cde50b0797.

## Point exact des validations interrompues

Une première série de vingt tests passait avec les anciennes vingt paires d'articles (quatre différences textuelles, 4 604 images échantillonnées). Ces captures ont été relues : la légende et la confirmation intérieure fonctionnaient, avec Badge Franklin comme variable native courante. L'entrée complète de Minnie choisissait encore la carte bancaire et affichait son refus ; elle ne prouvait pas le dépôt de la fiole.

La sonde a ensuite été corrigée pour choisir la seconde colonne de l'inventaire, et le test hors ROM attend désormais vingt-quatre paires. Une nouvelle série d'émulations a été lancée mais sa fin, la collecte, la relecture et les tests finaux ne sont pas confirmés. Ne pas présenter les vingt anciennes paires ni les vingt anciens tests comme une validation de cette dernière série.

Sonde prévue, trois cas par profil, entrées artificielles via carte bancaire :
- Contenant : entrée 32B500, deux pressions A ; variable d'objet native, aucun contenant naturel ni acquisition certifiés.
- Minnie : entrée 36B788, don natif de l'objet70 (Fiole de sérum à 58 dollars, distinct de A5 à 20 dollars), puis séquences [A], [A], [A], [Right,A], [A], [Right,A], [A].
- Confirmation intérieure : entrée 36B82E, aucune étape suivante ; arrêt à la pause, aucun dépôt complet certifié.

Sorties privées attendues : current_v78_articles et reference_v78_articles, dans /workspace/scratch/98c4eaa3ef23. Les anciens résultats, sondes et captures doivent être distingués de la nouvelle série. Ne certifier un effet d'inventaire qu'après observation de l'interface correspondante. Aucune écriture WRAM directe ni parcours naturel n'est revendiqué.

## Dépendances et reprise

Rétablir un environnement d'exécution avec accès au répertoire local et aux dépendances privées. Derniers emplacements connus, non vérifiables ici :
- ROM originale : /workspace/scratch/98c4eaa3ef23/private_v74/EarthBound Beginnings (USA) 1.2(1).sfc, SHA256 e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c.
- Cœur : /workspace/scratch/c267dac1e2c1/emulator/snes9x_libretro_standard.so.
- États : /workspace/scratch/98c4eaa3ef23/reference_v71_lodging/{accents,ascii}/accept/handoff.state.

Lire les changements locaux et les sauvegarder avant de récupérer le nouveau commit documentaire distant. Réconcilier sans force push. Terminer la série Minnie/contenant, collecter et relire les vingt-quatre paires si la sonde produit les résultats attendus, reconstruire les snapshots antérieurs pour leurs preuves, puis exécuter les vingt tests V78 et une reconstruction déterministe séquentiellement. Faire un commit local et un checkpoint distant de ce sous-ensemble seulement après vérification.

Ensuite : autres appelants d'articles réellement qualifiés, limites du coursier, plusieurs personnages et accès calculés ; puis menus et validation naturelle complète. Ne pas déclarer la traduction terminée. La tâche récurrente est à suspendre faute de moteur local, puis à réactiver lorsque cette dépendance sera rétablie. Ne jamais publier ROM, cœur, états ni dumps mémoire.

## Préparation structurée ajoutée pendant le blocage

Les cinq écritures et les trois scénarios ci-dessus sont maintenant conservés dans [tools/v78/pending_article_context.json](tools/v78/pending_article_context.json). Ce manifeste reste explicitement en attente et n'est pas intégré au constructeur. Vérifications effectuées sans environnement local : syntaxe JSON par aller-retour, cinq écritures, calcul des deux opérandes PNJ, longueurs logiques des textes/commandes/remplissages et douze captures attendues par profil. Ce contrôle de données ne remplace ni l'encodage réel dans la ROM, ni les tests Python, ni les vingt-quatre comparaisons d'émulation. Aucun compteur, IPS ou résultat publié n'a été modifié. L'environnement reste à rétablir avant intégration.
