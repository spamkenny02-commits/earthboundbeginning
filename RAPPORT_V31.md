# V31 — finalisation de dialogues par relocalisation

Base : V30. **16 scripts révisés et relocalisés**, avec **132 fragments de texte** (dont ponctuation, espaces et nombres). Ce ne sont pas 132 nouvelles traductions : 26 fragments encore anglais dans V30 sont traduits, les autres reprennent ou révisent le français existant et conservent les éléments non linguistiques.

Les entrées principales de ces dialogues disposent désormais de copies entièrement françaises : conseils des moineaux, esprit de COMBAT, échange du trésor du chien, trésor enterré à Snowman, asthme, ressemblance avec la reine Mary, guitariste, invitation à chanter, appel maternel, déjeuner oublié, chapeau perdu, nourriture jetée, publicité du médecin, paiement des soins et tir sur le rocher.

La relocalisation permet des formulations complètes comme «Je ne peux pas sortir, encore moins ouvrir la porte», «Pas cher, rapide et beau» et les choix «Oui / Non». Les espaces de remplissage des anciennes capacités sont retirés dans les nouvelles copies. Les noms, objets et montants dynamiques, pauses et commandes restent conservés.

## Allocation et pointeurs

Deux réserves nulles sont déclarées : `[292490,292F80)` et `[24D0C0,24DB80)`. Elles sont vides dans la source et les deux profils V30, sans référence HiROM littérale entrante ni écriture IPS antérieure. Les copies occupent 3 863 octets de script, hors alignement. Les deux profils utilisent les mêmes destinations.

Les 19 références extérieures aux entrées principales sont redirigées. Les branches et appels des nouvelles copies sont recalculés aux frontières vérifiées. Les scripts V30 restent intégralement intacts et leurs 46 références littérales vers des entrées intérieures sont conservées. Ces anciennes entrées secondaires peuvent donc toujours afficher les fragments V30, notamment anglais. Cette stratégie évite de modifier des alias dont le contexte n'est pas établi.

La détection des adresses assemblées ou calculées indirectement n'est pas exhaustive. Le contrôle de réserves démontre les octets nuls, les écritures IPS et les références littérales ; les nouveaux déclencheurs narratifs doivent encore être testés dans une partie normale.

## Vérifications

**12 tests V31 réussis** : fixtures françaises, source originale, commandes et opérandes des IPS publiés, reconstruction, application IPS indépendante, comparaison exhaustive hors écritures déclarées, fermeture des copies, références recalculées, anciens scripts et alias inchangés, réserves libres, absence de chevauchement, refus d'une branche dans un texte remplacé, de débordements, de références supplémentaires et de commandes modifiées.

Le [rapport d'émulation](tests/emulation_v31/RAPPORT_EMULATION_V31.md) documente séparément le parcours normal du début et les essais d'affichage par point d'entrée temporaire. Ces essais ne remplacent pas la validation des scènes et conditions narratives réelles. Les corrections boy/girl de V29 restent conservées.

[Sources françaises](tools/v31/dialogues_fr.json) · [Destinations et empreintes](tools/v31/validation_v31.json) · [Construction et tests](tools/v31/README_V31.md).

Appliquer un seul IPS V31 directement à la ROM originale USA 1.2. Aucune ROM ni sauvegarde distribuée.
