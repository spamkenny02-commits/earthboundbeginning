# V38 — banque française de descriptions d'ennemis

Base publiée relue : V37, commit `4d35e9f`. V38 traduit **114 descriptions d'ennemis réellement nouvelles**, soit 126 fragments dans 114 scripts. Aucun texte déjà français n'est recompté. Les seize entrées vides de redirection de la banque sont conservées sans être comptées.

## Relocalisation et références

Les scripts sources `361DB7–3631F2` restent intacts. Le constructeur place leurs copies françaises dans dix sous-réserves nulles, non occupées et non ciblées, de `328A80` à `32A2B8`. Il évite les cibles HiROM qui parsèment les grandes plages nulles voisines.

La table de descriptions fournit 114 références prouvées. Dix-sept autres appels sont des alias de saut; chacun est réécrit seulement après que le parseur a reconnu son opcode, son opérande et sa fermeture. Au total, 131 références sont raccordées aux copies françaises. Les commandes, frontières et profils accents/ASCII ont la même implantation.

Les IPS autonomes conservent tous les enregistrements V37 et ajoutent 245 enregistrements : 114 copies et 131 réécritures de pointeurs. Leur application indépendante depuis la ROM USA 1.2 produit `fc534f9e4bcacc439e1f1c1b1d307c233175b50cae82eb2617009e1d299a34a7` (accents) et `a377b13634eb4dca3f7992694fdb7e439714e811d24c78d622ba3dfec878d28c` (ASCII).

## Contrôles et limite d'émulation

- 14 tests V38 : provenance, réserves, références, commandes, fermeture des scripts, IPS indépendant et différence exhaustive;
- 75 tests de régression V37/V36/V35/V34/V33/V29/boy-girl : **89 tests réussis** au total;
- parcours Snes9x normal réussi dans les deux profils;
- sélection naturelle de « Voir » contre la première lampe : le nom de l'ennemi apparaît, mais pas la banque descriptive.

Les nouvelles copies ne sont donc pas annoncées comme validées dans leur rendu réel. Aucun point d'entrée artificiel, ROM, état, capture temporaire ou coeur n'est publié.

[Sources et constructeur](tools/v38/README_V38.md) · [Essais Snes9x](tests/emulation_v38/RAPPORT_EMULATION_V38.md)
