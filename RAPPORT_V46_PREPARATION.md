# V46 — état de préparation

État de référence relu sur `main` : **V45**, commit `4e628ac94b5f3004cbe87aa1646bef11f94c9467`.

Cette exécution prépare un premier lot V46 de **100 scripts texte** issus du catalogue de brouillons. Les menus sont explicitement exclus. Les 100 entrées sont enregistrées avec leurs offsets, octets sources, segments français et références littérales.

### Comptage honnête

- Scripts préparés/promus depuis le catalogue : **100**
- Fragments déclarés nouvellement intégrés à la ROM : **0**
- Fragments déjà français recomptés : **0**
- IPS V46 produites : **0**
- ROM modifiée ou distribuée : **0**

Les traductions existaient déjà comme brouillons dans `traduction/dialogues_fr.json`. Elles ne sont donc pas présentées comme 100 traductions nouvellement rédigées pendant cette exécution.

### Vérifications réalisées

La sélection exclut les menus et les segments dont le texte français dépasse déjà la longueur du segment anglais selon l'encodage texte simple. Les métadonnées de commandes et de pointeurs sont conservées.

La branche `work/v46-prep` est à zéro retard sur `main` et ne contient que les quatre fichiers de préparation V46.

### Blocage

Les chemins privés suivants ne sont pas accessibles dans l'environnement actuel :

- ROM USA 1.2 : `/workspace/scratch/60defd300f2e/downloads/EarthBound Beginnings (USA) 1.2(1).sfc`
- cœur Snes9x : `/workspace/scratch/96ddda3e7189/emutest/snes9x_libretro.so`

Le contrôle local d'existence a échoué pour ces deux fichiers. Le dépôt GitHub ne contient pas la ROM et ne doit pas la contenir.

Conséquences : impossible de vérifier sur la ROM SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c` les réserves, collisions, pointeurs HiROM, roundtrip IPS ou rendu Snes9x. Aucun de ces tests n'est annoncé comme effectué.

### Prochaine reprise

Quand la ROM privée sera de nouveau accessible, V46 devra reconstruire les deux profils depuis cette ROM, reparser chaque entrée, prouver les opérandes externes, effectuer les relocalisations sûres, construire les IPS autonomes, exécuter les tests structurels et le roundtrip indépendant, puis seulement publier sur `main`.
