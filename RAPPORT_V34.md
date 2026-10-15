# V34 — nettoyage des fragments anglais résiduels

Base publiée relue avant construction : V33, commit `7ef28ba`. V34 ajoute **87 fragments français réellement nouveaux dans 62 scripts**. Les entrées concernent surtout les raccords de phrases autour des noms et objets dynamiques, les messages de vente, l'utilisation d'objets, plusieurs réponses courtes et quelques dialogues encore mixtes.

L'audit a trouvé 186 fragments source encore disponibles. Le lot ne force pas un quota : le langage fictif des singes, les noms propres, les chants, rires et cris sans traduction utile restent volontairement inchangés. Ils ne sont pas comptés comme français. Aucun fragment déjà français n'est compté parmi les 87 ajouts.

## Sécurité binaire

V34 est une série de remplacements en place, sans relocalisation. Elle ne réserve donc aucune nouvelle zone nulle et ne réécrit aucun opérande. Chaque plage est encore identique à la ROM originale dans V33, ne chevauche aucune écriture IPS antérieure et ne contient aucune référence HiROM intérieure. Les scripts parents restent référencés ; leurs commandes et pointeurs d'entrée sont inchangés.

Les IPS autonomes reprennent tous les enregistrements V33 puis ajoutent exactement 87 écritures dans chaque profil. La ROM source épinglée a le SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Contrôles

- 16 tests V34 réussis avec et sans ROM : provenance, longueurs, encodage, commandes, références, absence de chevauchement, application IPS indépendante et comparaison exhaustive hors plages déclarées ;
- 14 tests V33 réussis ;
- 12 tests V29 et 8 tests boy/girl réussis ;
- parcours Snes9x 1.63 complet du début dans les deux profils, avec les cinq écrans de référence identiques à V18 Work ;
- cinq scripts inspectés dans les deux profils par un point d'entrée temporaire : utilisation d'objet, offre de vente, étudiant en architecture, arrivée tardive et dialogue d'adieu.

Le point d'entrée temporaire remplace cinq octets du message « personne à qui parler » uniquement dans les ROM de test. Il ne fait pas partie des IPS. Ces dix essais contrôlent le rendu natif, mais pas les déclencheurs narratifs ni les transactions réelles.

## Limites

Les 62 scripts n'ont pas tous été rejoués depuis leurs conditions normales. Les textes compressés et les graphismes anglais, notamment « YOU WON », restent à traiter. Aucun test absent n'est assimilé à une validation.

[Sources et constructeur](tools/v34/README_V34.md) · [Essais Snes9x](tests/emulation_v34/RAPPORT_EMULATION_V34.md)
