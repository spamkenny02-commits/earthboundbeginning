# V48 — phrases communes des objets et messages hérités

La V48 ajoute **66 occurrences de fragments traduits dans 40 scripts de messages ou de descriptions et quatre routines grammaticales privées**. Ces fragments correspondent à 60 textes anglais distincts ; 13 ajustements non lexicaux sont séparés. Deux occurrences `@Anyone` deviennent aussi `@Chacun` dans des descriptions d'armes déjà françaises.

Le lot couvre les conditions d'équipement, les PV récupérés par les aliments et boissons, l'utilisation unique ou répétée, les objets pour un personnage, les dégâts en combat, l'abandon et l'utilisation d'objets, les cadeaux vides, les clés incorrectes, les livraisons et quelques réponses génériques. Les descriptions françaises appelaient encore certaines phrases anglaises partagées. Leur raccordement est maintenant français. Aucun menu n'est traduit dans cette version.

## Construction

Les IPS autonomes partent de la ROM originale USA 1.2 et conservent les enregistrements V47. Ils ajoutent **367 enregistrements** : 44 copies, 321 opérandes externes prouvés et deux corrections textuelles de sept octets. Sept raccords internes sont recalculés, dont la réutilisation de deux routines françaises V44/V45. Onze opérandes situés dans des écritures antérieures sont actualisés après preuve. Les sources, les deux références non prouvées et les appels d'origine des nouvelles routines grammaticales restent intacts. Les 170 entrées de dictionnaire nécessaires sont développées dans les copies ; le dictionnaire partagé ne change pas.

La ROM dispose désormais de nombreux petits espaces libres dans les bancs de traduction. L'allocateur place les copies par taille décroissante et réutilise les restes des premières réserves au lieu de les abandonner. Chaque réserve est nulle sur l'original et les deux variantes V47, sans ancienne écriture IPS ni cible de pointeur littéral. Des tests couvrent explicitement le remplissage fragmenté et l'épuisement des réserves.

Le script `097F8A` est reporté : la référence `0A95EC` cible `097F97`, au milieu du texte anglais. Le constructeur refuse cette réinsertion. Ni ce script ni cette référence ne sont modifiés.

## Vérification

**272 tests locaux réussis** : 247 historiques et 25 V48. Ils vérifient la provenance, les réserves, les appels, les commandes, le décodage indépendant, les deux profils, les écritures antérieures, les pronoms et titres privés, les corrections `Chacun`, le dictionnaire, les alias contigus et le refus d'un alias au milieu du texte. Les exclusions historiques V36/V37 nécessitant CoilSnake sont conservées.

Le parcours normal Snes9x passe dans les deux variantes : 339 commandes avec accents, 337 en ASCII, et **212 captures identiques pixel par pixel à V47**. Huit nouveaux messages et cinq contextes de descriptions sont relus dans chaque variante par routage contrôlé de l'action de carte bancaire. Les captures contrôlent le rendu, les accents, les pages, les noms dynamiques et les nombres de PV. Elles ne prouvent pas l'accès naturel à ces scènes ni les effets de jeu des objets. Les variantes grammaticales féminines sont contrôlées structurellement, sans scène féminine rejouée.

- [Patch avec accents](patches/EarthBound_Beginnings_FR_v48_accents.ips)
- [Patch ASCII](patches/EarthBound_Beginnings_FR_v48_ascii.ips)
- [Construction et tests](tools/v48/README_V48.md)
- [Preuves d'affichage et limites](tests/emulation_v48/RAPPORT_EMULATION_V48.md)

Appliquer un seul IPS à l'original, sans empiler les versions. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.
