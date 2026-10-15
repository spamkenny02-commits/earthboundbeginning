# V35 — résidus anglais masqués par les anciens IPS

Base publiée relue avant construction : V34, commit `fc9e5b9`. L'audit de la ROM V34 appliquée a distingué les textes français, les octets simplement occupés par un ancien IPS et les fragments encore identiques à la source. V35 révise **31 scripts complets** et relocalise leurs **141 fragments** : **32 sont nouvellement traduits**, 99 étaient déjà français et 10 sont des noms, cris ou signes volontairement conservés.

Le lot corrige notamment seize réponses « No » devenues « Non », les questions longues du trésor et du singe, « Maison hantée », plusieurs raccords autour d'un nom dynamique, « Tu veux un », « ton sang » et l'indication « gauche » du labyrinthe. Le seuil de 100 nouveaux fragments n'a pas été forcé : parmi les 154 fragments identiques encore actifs dans le périmètre vérifiable, la majorité était du parler-singe, des noms propres, des chants, des rires ou des cris.

## Sécurité binaire

Les quatre réserves `167800–168000`, `16F800–170000`, `177800–177FD0` et `257BA0–258000` sont nulles dans la ROM originale et V34, sans écriture IPS antérieure ni cible HiROM littérale. Les deux profils utilisent les mêmes destinations et le même ensemble d'appels.

Le constructeur vérifie le layout source, les commandes, l'encodage, la fermeture des scripts et les frontières internes. Les scripts et alias d'origine restent inchangés. Les appels provenant des copies V31 à V33 sont reparsés; seuls les opérandes effectivement prouvés sont réécrits. Les corrections boy/girl et toutes les zones antérieures sont conservées hors des pointeurs déclarés.

Les IPS accents et ASCII sont autonomes depuis la ROM USA 1.2 épinglée (`e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`). Leur application par un lecteur IPS indépendant donne respectivement les ROM cibles `442444c7c563d00f6de92817ebad9b53028cf4c2e0f11ce38f240cb3d388acb6` et `e41472c69bf32c6c57cd66bcff14206d6abb5d177ab1db50fd0b430ff67625e3`.

## Contrôles

- 7 tests V35 : provenance complète, réserves, références, bytecode, branches internes, application IPS indépendante et comparaison exhaustive ;
- 12 tests V34, 14 tests V33, 12 tests V29 et 8 tests boy/girl : **53 tests réussis** au total ;
- parcours Snes9x 1.63 complet du début dans les deux profils, avec cinq captures identiques aux références V18 Work ;
- dix sondes temporaires sur cinq copies : quatre affichent les nouveaux textes sans débordement observé; la cinquième (`38535C`) ne rend pas sa branche conditionnelle dans ce contexte artificiel.

Les sondes remplacent temporairement cinq octets du message « personne à qui parler ». Elles ne font pas partie des IPS et ne valident pas les déclencheurs narratifs normaux.

## Limites

Les 31 scènes n'ont pas été rejouées depuis leurs conditions normales. La branche conditionnelle de `38535C`, les textes compressés et les graphismes anglais, notamment « YOU WON », restent à traiter. Aucun essai absent n'est présenté comme exécuté.

[Sources et constructeur](tools/v35/README_V35.md) · [Essais Snes9x](tests/emulation_v35/RAPPORT_EMULATION_V35.md)
