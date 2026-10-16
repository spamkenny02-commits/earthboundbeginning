# V43 — combat, services et Maria

**Correctif V44 :** un audit ultérieur a identifié 14 pointeurs de cette version visant une fin de copie au lieu de l’entrée du script contigu. Ils sont corrigés dans la [V44](RAPPORT_V44.md), avec des tests supplémentaires de destination. Utiliser désormais le patch V44.

Base publiée : V42 (`17591d5`). **56 scripts, 102 nouvelles occurrences de fragments français**, soit 91 fragments anglais distincts. Les copies contiennent 166 plages textuelles : 102 traductions, 12 ajustements d'espacement avant « ! » et 52 marqueurs ou signes conservés. Les 12 ajustements ne sont pas comptés comme traductions nouvelles.

Le lot couvre des actions et réactions de combat, l'utilisation d'objets, plusieurs réponses de services et boutiques, les variations de statistiques et les souvenirs de Maria concernant Giygas et George. Aucun menu ou choix Yes/No n'est modifié. Deux candidats uniquement référencés par l'ancienne table d'actions ont été écartés.

## Construction et protection des versions précédentes

Les textes sont copiés dans des réserves nulles, sans modifier les sources anglaises. Les scripts peuvent être compressés par dictionnaire ou déjà écrits en glyphes ordinaires. Les 72 entrées utilisées sont développées dans les copies ; le dictionnaire anglais partagé et ses 768 entrées restent intacts.

Chaque IPS conserve les enregistrements V42 et ajoute **180 enregistrements** : 56 copies et 124 références externes prouvées (49 champs de la table de combat du remake, 42 de l'ancienne table, 33 opérandes de commandes). Un appel entre deux scripts du lot est raccordé dans sa copie. Les 22 références littérales non prouvées restent inchangées et continuent de viser les sources préservées.

Deux opérandes déjà couverts par les IPS antérieurs sont actualisés après vérification de leur commande : `259ACB → 34B6D6` et `25EB84 → 2F9AE8`. Tous les autres octets antérieurs sont protégés. Le placement commence par les copies les plus longues pour réserver une plage suffisante au dialogue de Maria ; les deux profils partagent la même implantation.

## Vérifications

**158 tests locaux réussis** : 17 V43, plus les 141 tests V42 et historiques. Ils couvrent la reconstruction indépendante des IPS, les sources, les références, les commandes conservées, le décodage français, les réserves, les anciennes modifications et le dictionnaire. Les suites historiques sont exécutées dans des processus séparés. Les tests graphiques V36/V37 nécessitant CoilSnake ne sont pas compris ; leurs tests hors ROM et la conservation de leurs octets sont contrôlés.

Le parcours normal est rejoué sous Snes9x 1.63 jusqu'à l'image 25 803 dans les deux profils. Les différences avec V18 restent limitées aux deux images VICTOIRE attendues. Voir le [rapport d'émulation](tests/emulation_v43/RAPPORT_EMULATION_V43.md) pour la portée exacte des essais.

Le message d'examen `361CA1` est relu intégralement dans le premier combat via « Voir », dans les deux profils, sans injection de ROM ou de WRAM. Les 55 autres scripts du lot ne sont pas validés dans leurs scènes réelles.

L'existence d'un appel ou d'une entrée dans la table de combat ne prouve pas qu'un texte est accessible dans une partie normale. Les nouveaux dialogues, notamment Maria, les services et les actions tardives, nécessitent encore une relecture dans leurs scènes. Ce lot ne revendique pas leur validation visuelle complète.

## Livraison

- [IPS avec accents](patches/EarthBound_Beginnings_FR_v43_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v43_ascii.ips)
- [Traductions, constructeur, empreintes et tests](tools/v43/README_V43.md)

Appliquer **un seul IPS V43 directement à la ROM originale USA 1.2**, sans empiler les anciennes versions. Aucune ROM ni sauvegarde de jeu n'est distribuée.
