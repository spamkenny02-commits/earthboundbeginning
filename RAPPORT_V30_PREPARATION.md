# EarthBound Beginnings FR — préparation V30

Base vérifiée sur GitHub `main` : V29, commit `0db05d88885d3d5e5fe2eb36bc0cb3472a20e4ac` (14 octobre 2026). Le README, les rapports V28/V29, les constructeurs V28/V29, les manifestes et tests V29 ont été consultés avant modification.

## Travail effectué

Ajout d'un audit conservateur des candidats V30. Il relit la ROM originale et les IPS V29 des deux profils, contrôle l'empreinte des fichiers, les frontières de texte reconnues, les références HiROM, les commandes et les plages occupées. Il exclut les textes à pointeurs entrants (y compris les alias intérieurs), les plages déjà modifiées et les scripts dont les commandes ou les références ont changé. Il produit un JSON de candidats sans changer aucun octet du jeu.

## Validation et limites

- **10/10 tests synthétiques Python réussis** pour les limites, collisions, références, différences entre profils et conservation des commandes.
- **0 bloc traduit et 0 bloc intégré** dans cette préparation.
- **Aucun IPS V30 construit ou publié** : les IPS V29 restent les derniers patchs autonomes disponibles.
- **Audit du catalogue complet sur ROM : non effectué**, car la ROM originale USA 1.2 n'était pas disponible dans l'environnement de cette exécution.
- **Roundtrip V30 sur ROM, régression binaire complète V30 et émulation V30 : non effectués** ; il n'existe pas encore de patch V30 à tester.

## Suite

Exécuter l'audit sur une ROM USA 1.2 dont le SHA-256 est vérifié, relire les textes et les références, traduire un lot substantiel (100 à 200 si sûr), produire les deux IPS autonomes V30, contrôler la régression V29, le roundtrip et les scènes sous émulateur. Traiter les pointeurs indirects, textes compressés et graphismes séparément sans inventer de validation.
