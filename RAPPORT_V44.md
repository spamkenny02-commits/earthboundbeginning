# V44 — raccords contigus, pronoms et dialogues restants

Base : V43 (`b1b962d`). **93 nouvelles occurrences de fragments français**, correspondant à 85 fragments anglais distincts, dans **46 scripts de messages et six copies privées de routines grammaticales**. Les sept lettres ajustées dans les huées, les 13 ajustements non lexicaux et les 39 fragments conservés ne sont pas ajoutés au compteur. Les 12 choix Yes/No intégrés aux dialogues restent anglais pour la passe des menus.

Le lot couvre les dialogues de la cuillère, de Laura et de Pippi, les messages d'inventaire et de tickets, les variations de statistiques, les alliés et plusieurs actions de combat encore liées aux possessifs anglais.

## Correction de 14 pointeurs de la V43

Le placement des longues copies en premier, introduit en V43, exposait une collision dans la correspondance des adresses : la fin exclusive d'un script pouvait remplacer l'entrée du script source contigu, placé ailleurs. Les anciens tests contrôlaient la conformité des pointeurs au manifeste, mais pas suffisamment l'identité de leur destination.

L'audit retrouve **14 opérandes erronés, concernant huit scripts V43** : rayon nocturne, Combat, Vigueur, proposition d'équipement en boutique, utilisation d'objet, nettoyage, tornade et décompte. V44 les répare après vérification du pointeur d'origine, du pointeur V43 actuel et de sa commande ou de son champ de table. Ces réparations ne sont pas comptées comme de nouvelles traductions.

La correspondance exclut désormais la fin de chaque script. Un test minimal reproduit deux sources contiguës allouées dans l'ordre inverse ; d'autres contrôles vérifient que chaque référence à une entrée exacte vise sa propre copie, ainsi que les 14 réparations. L'audit des manifestes V41 et V42 n'a pas retrouvé cette collision.

## Routines françaises privées

Les copies des messages appellent des routines privées « il/elle/il » et « sa/sa/sa ». La sélection native de genre et les trois branches sont conservées ; les formulations des messages sont adaptées au déterminant français. **Les routines anglaises d'origine et leurs 28 références existantes restent intactes.** Les trois branches de chaque routine française sont vérifiées par décodage indépendant.

Le dictionnaire partagé et ses 768 entrées restent inchangés ; 36 entrées utilisées sont développées dans les copies. Les 15 références littérales non prouvées restent également intactes.

## Construction et tests

Chaque IPS autonome conserve les enregistrements V43 et ajoute **147 enregistrements** : 52 copies, 81 pointeurs externes de ce lot et 14 réparations V43. Les copies contiennent 28 raccords internes. Dix-neuf opérandes déjà couverts par les anciens IPS sont actualisés : cinq raccords de ce lot et les 14 corrections. Tous les autres octets antérieurs restent protégés.

**181 tests locaux réussis**, dont 23 V44 et 158 historiques, exécutés par suites isolées. Les six tests GitHub hors ROM contrôlent aussi le cas des scripts contigus et reconstruisent les ajouts exacts. Les anciens tests graphiques V36/V37 nécessitant CoilSnake ne sont pas compris ; leurs tests hors ROM et la conservation de leurs octets sont vérifiés.

Le parcours normal Snes9x retrouve les captures attendues dans les deux profils. Dix nouveaux messages sont relus dans le moteur natif, dans les deux profils, avec un routage de description de combat contrôlé. **Ces essais vérifient leur affichage, pas leur accessibilité naturelle ni les effets des attaques.** Les dialogues tardifs restent à relire dans leurs scènes. Voir le [rapport d'émulation](tests/emulation_v44/RAPPORT_EMULATION_V44.md).

## Livraison

- [IPS avec accents](patches/EarthBound_Beginnings_FR_v44_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v44_ascii.ips)
- [Sources et reproduction](tools/v44/README_V44.md)

Appliquer un seul IPS V44 directement à la ROM originale USA 1.2. Ne pas empiler les anciennes versions. La ROM conserve sa taille de 4 Mio ; aucune ROM, sauvegarde ou fixture de jeu n'est distribuée. Les menus restent pour leur passe dédiée.
