# V46 — préparation de lot texte

Base vérifiée : V45 (`4e628ac94b5f3004cbe87aa1646bef11f94c9467`) sur `main`.

## État

Le catalogue contient 345 entrées à l'état `draft`. Après exclusion des menus, des entrées V45 et des traductions dont un segment dépasse déjà sa longueur source, 229 candidats restent disponibles. Un premier lot cohérent de **100 scripts** est préparé pour V46.

Ces 100 traductions existaient déjà dans le catalogue sous forme de brouillons. Elles sont donc comptées ici comme **scripts préparés/promus**, et non comme 100 traductions nouvellement rédigées pendant cette exécution. Aucun bloc n'est déclaré intégré à la ROM.

## Sécurité

- Les commandes et octets de contrôle restent séparés des segments français.
- Les pointeurs littéraux sont conservés dans la sélection mais ne sont pas réécrits ici.
- Le lot est limité aux segments dont la traduction tient dans la longueur du segment source ; cela ne prouve pas l'absence de collisions avec les réserves de la ROM.
- Les menus et les choix de menu restent volontairement hors de cette passe.

## Blocage d'intégration

La ROM USA 1.2 et le cœur Snes9x indiqués dans la demande ne sont pas présents dans l'environnement d'exécution actuel. Ils ne sont pas non plus distribués dans le dépôt. Il est donc impossible de reconstruire honnêtement les IPS V46, de contrôler les réserves/collisions HiROM sur la ROM réelle ou d'effectuer un test émulateur ici.

Aucun IPS V46, aucune ROM et aucune capture de jeu ne sont donc annoncés.

## Suite

Dès que la ROM privée est de nouveau accessible à l'environnement de travail, le constructeur V46 devra reparser chaque script contre la ROM SHA-256 épinglée, prouver chaque opérande de pointeur avant réécriture, allouer les relocalisations dans les réserves libres, reconstruire accents/ASCII, appliquer les IPS indépendamment, exécuter les régressions et les scènes natives, puis seulement publier V46 sur `main`.
