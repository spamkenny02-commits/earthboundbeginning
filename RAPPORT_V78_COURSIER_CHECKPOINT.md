# V78 — limites du coursier et libellé téléphonique

21 octobre 2026. Même lot de traduction, **120 sources distinctes sur une cible de 150**, 158 plages sources. Une source nouvelle ; pas de nouvelle release. V77 reste publiée sur main.

## Traduction

`phone_label_stage.py` adapte le libellé `35CFFF–35D018`, dans `35CEAA` : « @No: *pssst psst pssst*  » devient « @Num.: *pssst psst pssst* ». Le contexte dit « Voici le numéro à composer » : il s'agit du numéro chuchoté, pas d'une réponse négative. Une seule source au registre ; les deux profils et les deux appels de test ne doublent pas ce compte.

Le téléphone complet `35C597` emploie le dispatch calculé natif `1A 0A`. Les traces certifient l'affichage du libellé depuis cet appel. Un chemin typé indépendant depuis `35A925` qualifie aussi le contexte ; il est conservé dans le champ historique `phone_path` des fixtures, sans prétendre qu'il s'agit du graphe typé du téléphone.

25 octets remplacés en place, commandes et pointeurs inchangés, aucune allocation. Contrôles des références intérieures, des sprites et de la banque25 conservés. Total IPS : 384 enregistrements ajoutés à V77.

## Deux chaînes nouvelles dans les deux profils

L'ancien état extérieur V33 manque. Le test repart de l'état privé après repos conservé, sort de la chambre puis de la maison avec dix segments de marche à la manette, et appelle le téléphone complet via la carte bancaire. Le coursier arrive ensuite par le mécanisme temporisé normal ; le test ne l'appelle jamais directement. Les entrées initiales téléphone/stockage restent forcées.

| Chaîne | Résultat observé |
|---|---|
| Quatre objets disponibles | Fiole ID70, capsules sagesse71, vitalité72 et vitesse73 accordées par commandes natives. Le coursier prend les trois premiers ; le récapitulatif et la réserve inspectée les montrent. Le sac final garde la carte et vitesse73. Argent 20 → 2 $, soit 18 $ au total. |
| Réserve pleine à l'arrivée | Deux préparations liées insèrent 13 puis 13 fioles en réserve. Le téléphone accepte l'envoi avec 26 objets. Dix insertions natives supplémentaires, après retour de l'appel et avant attente du coursier, remplissent artificiellement la réserve. Le coursier affiche « Après vérification, ta réserve est pleine », refuse et part. Les quatre objets restent au sac, argent toujours 20 $. L'inspection montre 10/10/10/6 objets sur quatre pages. |

L'extension optionnelle `post_operations` de la fixture privée permet ces dix insertions après l'appel. Ses octets exacts et leur ordre sont déclarés ; le comportement des anciennes fixtures sans ce paramètre reste identique. Aucune écriture directe WRAM. Les trois numéros intermédiaires de réserve sont des numéros de page, pas un dénombrement mémoire.

La limite effective de trois objets est prouvée ; le message intérieur `064240` (« Trois objets au maximum ») n'apparaît pas dans ces parcours. Ne pas confondre comportement et couverture de chaque branche. Une réserve déjà pleine avant l'appel provoque un refus au téléphone ; cet essai exploratoire ne certifie pas le refus chez le coursier.

## Preuves et contrôles

`tests/emulation_v78_courier` : 152 paires V77/V78, quatre différences limitées à la fenêtre de texte du numéro téléphonique, mêmes touches, préparations, routes et nombres d'images. 46 620 images échantillonnées dans V78. 26 captures clés relues : libellés, refus, inventaires et pages de réserve dans les deux profils. Les états privés sont liés par leurs empreintes ; ils ne sont pas publiés.

**22 tests V78 réussis avec ROM privée.** Commande : `EARTHBOUND_ROM=SOURCE.sfc python -m unittest discover -s tools/v78 -p 'test_*.py' -v` ; contrôle PNG/RGB, liens d'états, traces recalculées, commandes exactes, empreintes des fixtures, compteur et anciens snapshots. Les captures antérieures ne deviennent pas celles du nouvel IPS ; le test articles reconstruit son checkpoint de 383 enregistrements avant de vérifier ses empreintes.

| Profil | SHA256 IPS | SHA256 ROM résultante privée |
|---|---|---|
| accents | `fc1b19d83c53cf51e9f1f578b7404aa21b7103f8c3f911a0e2a78e7e9ccdda8c` | `31157766e0427b09ceb80e58445cff60784162554b3f0474bdc55770817f8243` |
| ASCII | `d9d8b604ecd93e1e547a40f886d7418f6012241ad061d663c87e2ef7da1ebe18` | `b37427e01eece7c3038e269bdf210ccfb1c099b7810419ef628cd2da5882e69f` |

Sorties privées retenues : `current_v78_courier_limits_validated` et `reference_v78_courier_limits_validated`. Les essais `explore_*`, `current_v78_courier_limits` et `current_v78_courier_limits_final` sont exploratoires ; aucun n'est présenté comme preuve finale. Seuls PNG, résultats sémantiques, outils, rapports et IPS sont publiés ; jamais ROM, cœur, états ou dumps mémoire.

Reste : services à plusieurs personnages, anciennes branches non qualifiées, dialogues accessibles puis menus et parcours naturels. Les trente sources manquant à la cible ne constituent pas un inventaire prouvé. Ne pas déclarer la traduction complète.
