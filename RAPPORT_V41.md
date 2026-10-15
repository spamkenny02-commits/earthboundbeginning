# V41 — services, transports et textes narratifs

Base publiée et relue : V40, commit `7e0599a86fd2af875f83832314ff566c67476c6d`.

## Travail intégré

**108 scripts révisés**, couvrant les objets au sol, l'inventaire plein, les soins, la consigne, les transports, les hôtels, les opérations bancaires, plusieurs dialogues secondaires et quatre passages de l'épilogue.

Le lot contient **197 occurrences de fragments nouvellement traduites**, correspondant à 125 fragments anglais distincts. Une même formule de service peut exister à plusieurs adresses ; chacune est intégrée, sans présenter ces répétitions comme autant de formulations différentes.

Les copies contiennent 308 fragments : 197 traductions nouvelles, 10 raccords grammaticaux retirés et 101 fragments conservés. Les 40 choix Yes/No restent inchangés pour la passe des menus. Les menus de jeu et de débogage ne sont pas traduits dans ce lot. Les scripts comportant des routines possessives partagées, des formats encore incertains et les messages de débogage ont été laissés hors sélection.

## Références et IPS

Les sources sont vérifiées sur la ROM USA 1.2 par SHA-256 et comparées aux deux ROM V40. Les sources déjà relocalisées des lots précédents sont exclues de la recherche afin de ne pas compter leurs anciennes copies anglaises comme du travail nouveau.

Les 256 références sont contrôlées : 255 opérandes de commandes reconnues et fermées, plus un champ de la table d'actions de combat. **214 références externes et 42 sauts entre les copies** sont raccordés. Les alias intérieurs sont mappés à leurs frontières de commandes conservées, sans saut dans du texte redimensionné. Les 108 scripts sources restent intacts.

Neuf références externes sont déjà couvertes par des enregistrements IPS antérieurs. Leur destination est légitimement actualisée, notamment pour que les anciennes copies françaises appellent les nouveaux messages d'inventaire plein. Le constructeur autorise ces quatre octets par référence, après vérification de l'ancienne cible et de son opcode. Tous les autres octets antérieurs sont protégés. Les neuf opérandes sont listés dans `prior_record_pointer_updates`.

Les IPS autonomes ajoutent chacun **322 enregistrements** à V40 : 108 copies et 214 références externes. Les 42 sauts internes sont inclus dans les copies. Les profils accents et ASCII ont la même implantation ; les réserves sont nulles, non ciblées et sans chevauchement avec les anciens IPS. L'application indépendante depuis la ROM originale et les différences exhaustives sont contrôlées.

## Tests et émulation

**124 tests locaux réussis** : 15 V41, 15 V40, 15 V39, 14 V38, 4 V37 hors ligne, 4 V36 hors ligne, 11 V35, 12 V34, 14 V33, 12 V29 et 8 boy/girl. Les contrôles de recompression V36/V37 dépendant de CoilSnake ne sont pas réexécutés. Leurs tests hors ligne et la préservation des données restent vérifiés.

Les tests V41 couvrent la provenance source, les preuves de références, les réserves, le décodage français indépendant, les commandes, les alias, les neuf opérandes antérieurs actualisés, les IPS autonomes, les profils et tous les octets hors des plages déclarées.

Le parcours normal Snes9x 1.63 passe dans les deux profils jusqu'à l'image 25 803 : titre, introduction, premier combat remporté, après-combat, restauration d'état et menu. Les seules différences de captures avec V18 sont les bannières VICTOIRE attendues depuis V36.

Un essai supplémentaire utilise la carte bancaire naturellement possédée, via le menu normal, sans modification de la ROM ni de la WRAM. Il affiche un ancien message anglais d'utilisation de carte, extérieur à ce lot ; ce résultat ne valide donc aucun nouveau dialogue V41. Ce message reste une piste d'analyse pour les textes suivants.

**Limite : l'affichage et les déclencheurs des 108 nouvelles scènes ne sont pas validés par le parcours du début.** Les hôtels, transports, services et l'épilogue restent à contrôler dans leurs contextes réels.

## Fichiers

- [Traductions, constructeur et méthode](tools/v41/README_V41.md)
- [Manifeste binaire](tools/v41/validation_v41.json)
- [IPS accents](patches/EarthBound_Beginnings_FR_v41_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v41_ascii.ips)
- [Rapport Snes9x](tests/emulation_v41/RAPPORT_EMULATION_V41.md)

Aucune ROM, aucun état d'émulateur ni coeur n'est publié.
