# V39 — descriptions d'objets encore anglaises

Base vérifiée : V38, commit `783d0f659b83ea616b1010f2f0441173c1087f74`.

## Traduction et intégration

22 descriptions d'objets entièrement anglaises dans V38 sont traduites : battes, poêles, protections, objets de soin et tickets. **32 fragments réellement nouveaux** sont comptés ; les 44 délimiteurs de noms d'objets et le marqueur dynamique isolé ne sont pas comptés comme traductions.

Les 22 références du champ description de la table d'objets (enregistrements de 39 octets, champ à +35) et 22 opérandes d'affichage `1F C0 01` reconnus par le parseur sont réécrits. Les scripts anglais sources sont conservés. Les réserves nulles non référencées vont de `32A910` à `32AFE4`, avec les trous documentés dans le manifeste.

Les deux IPS autonomes conservent exactement les enregistrements V38 et ajoutent 66 enregistrements : 22 copies et 44 pointeurs. Ils s'appliquent directement à la ROM originale USA 1.2, vérifiée par SHA-256.

## Vérification

**94 tests réussis** : 15 V39, 14 V38, 4 V37 hors ligne, 4 V36 hors ligne, 11 V35, 12 V34, 14 V33, 12 V29 et 8 boy/girl. Les suites historiques sont exécutées dans des processus séparés, car certains constructeurs modifient les constantes d'un module partagé. Les tests de recompression V36/V37 dépendant de CoilSnake ne sont pas réexécutés ; leurs IPS sont préservés et leurs contrôles hors ligne passent.

Les tests V39 vérifient la provenance des octets sources, les références, les réserves, les commandes, les anciens enregistrements, l'application IPS indépendante, les différences exhaustives et le décodage indépendant du français dans les deux profils.

Le parcours normal Snes9x 1.63 est rejoué dans les deux profils jusqu'à l'image 25 803 : titre, introduction, premier combat, après-combat, restauration d'état et menu conformes. Les deux différences de captures avec V18 sont les bannières VICTOIRE déjà attendues depuis V36.

**Contrôle d'affichage complémentaire : 22/22 descriptions relues dans chaque profil (44 cas).** Le premier objet de l'inventaire est remplacé temporairement en WRAM ; la ROM V39 reste identique. La description est ouverte par le menu normal Objets → Help!. Accents, noms dynamiques, retours à la ligne et pagination sont lisibles, sans texte nouveau tronqué détecté. L'acquisition naturelle des objets n'est pas testée. Les préambules d'équipement, certaines indications d'usage et les actions du menu sont encore anglais ; ils sont extérieurs au lot V39. Voir les preuves et la méthode dans le rapport Snes9x.

## Fichiers

- [Constructeur et traductions](tools/v39/README_V39.md)
- [Manifeste et empreintes](tools/v39/validation_v39.json)
- [IPS accents](patches/EarthBound_Beginnings_FR_v39_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v39_ascii.ips)
- [Régression Snes9x](tests/emulation_v39/RAPPORT_EMULATION_V39.md)

Aucune ROM, aucun état d'émulateur ni coeur n'est publié. Quatre planches de captures de contrôle sont conservées comme preuves d'affichage.
