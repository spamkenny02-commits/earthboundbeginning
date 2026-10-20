# V78 — checkpoint des aides à 114 textes

Rapport historique conservant les empreintes de ses captures. L'état actuel à 116 textes ajoute deux copies contextuelles ; voir RAPPORT_V78_COPIES_CHECKPOINT.md.

Le lot compte 114 sources distinctes et 152 plages physiques, sur une cible d'environ 150 textes avant publication. Cette reprise ajoute 15 sources ; les conseils partagés par plusieurs objets et les profils ne sont comptés qu'une fois. V77 reste publiée sur main. Le registre complet est dans REPRISE_TRADUCTION.md et tools/v78/batch_ledger.json.

La table de sept objets par boutique est identifiée à 1576B2. Le chemin de qualification relie chaque wrapper PNJ personnalisé à son flag, à la branche 3656DC, à la commande 1A06, au stock puis à la table des objets et au pointeur d'aide. Vingt-cinq wrappers proposent 82 identifiants distincts. Les noms et prix de huit listes sont relus en émulateur dans les deux profils ; les autres liens sont statiques. Le stock de pharmacie utilise A5, Fiole de sérum à 20 $, et non 70, Fiole de sérum à 58 $. Leur nom partagé ne suffit pas à identifier l'objet.

Les quinze traductions sont implantées en place. Aucun nouveau stockage, déplacement, pointeur ou opcode natif n'est ajouté. Total du lot : 3 159 octets de réserve déjà alloués et 333 enregistrements IPS ajoutés aux V77. Les sprites, banque25, table PNJ et créneau privé restent préservés. Toute référence brute entrant dans une plage source est gardée : la bouteille d'eau 05473C reste anglaise à cause de 054743.

Les appels typés des aides révèlent aussi les helpers communs : nounours, protection contre la paralysie, accessoire réservé à un personnage et combinaisons de condiments. Ils sont reliés aux objets qualifiés et comptés une seule fois. Le contrôle ciblé visite 106 racines ; parmi les littéraux originaux de plus de neuf caractères, seule la bouteille d'eau reste candidate. Ce seuil ne permet aucune affirmation d'exhaustivité générale.

| Objet / contexte | Offset | Source | Français |
|---|---|---|---|
| 38 / 053D00 | 053D10 | @It also increases your Speed. | @Vitesse accrue |
| 4A / 053F58 | 053F68 | @It has the logo of your favorite baseball team. | @Logo de ton équipe préférée. |
| 5C / 05416D | 054184 | @So fresh, it's still warm! | @Frais et chaud ! |
| 5D / 054197 | 0541AE | @There's even a slice of your favorite cake! | @Avec ton gâteau préféré ! |
| 7E / 0548FC | 054905 | @Use by sprinkling it over food. | @À mettre sur un plat. |
| 7E / 0548FC | 05491E | @It tastes good with any kind of food, thereby | @Bonne avec tout plat, |
| 7E / 0548FC | 054939 | @increasing the recovery power of the food. | @renforce ses soins. |
| 96 / 054FA2 | 054FAB | @Quickly rusts metallic enemies when used during battle. | @Rouille les ennemis métalliques. |
| 96 / 054FA2 | 054FD1 | @The enemy will take about 200 points of damage. | @Environ 200 dégâts. |
| D5 / 055EBB | 055ECB | @Wow! Look at the pine tar! It's almost all the way to the end! | @De la résine presque jusqu'au bout ! |
| 02 / 056B5D | 056B5D | A cute teddy bear! | Un joli nounours! |
| 38 / 056BC0 | 056BC5 | @It protects you from paralysis attacks. | @Protège de la paralysie. |
| 4E / 056C6D | 056C6D | @Miscellaneous equipment that can only be used by  | @Accessoire exclusif destiné à  |
| 76 / 056D63 | 056D63 | @To use, sprinkle over food. | @Saupoudre ton plat. |
| 76 / 056D63 | 056D7A | @A good combination increases the strength of your recovery. | @Un bon mélange soigne mieux. |

Trente tests ciblés réussissent avec la ROM privée : 14 V78 + 8 V77 + 8 V65. Sans ROM, huit tests V78 passent et six sont explicitement ignorés. Les contrôles couvrent les données de stock, les chemins d'aide, les références intérieures, les commandes, les préfixes IPS et les empreintes exactes de chaque snapshot.

164 nouvelles paires V77/V78 sont comparées en RGB, avec 46 différences limitées aux fenêtres textuelles et 36 456 images échantillonnées. Vingt scénarios par profil : douze appels d'aide, dont celui de l'eau encore anglaise, et huit wrappers de boutiques. L'affichage des aides et des stocks est relu ; aucun achat réussi, usage, équipement ou effet de soin n'est certifié. Les entrées sont forcées via la carte bancaire depuis l'état privé post-repos ; aucune préparation d'inventaire ni écriture directe WRAM.

Les anciennes preuves restent identifiées : 146 paires pour le checkpoint de 81 textes, 166 pour celui de 99 textes. Les tests reconstruisent leurs IPS exacts ; ces captures ne sont pas présentées comme des sorties du patch actuel. Les sorties nouvelles retenues sont current_v78_help_final / reference_v78_help_final ; les premiers essais exposant encore des helpers anglais sont remplacés.

Empreintes SHA256 des IPS actuels :

- accents : cce49955e32a23c978dd07a44cc19de5491d45a35bab4428734976cffb4040be
- ASCII : dc69a44630c1d77d16959cd27a8cc9c1be33f690bef47321db2839bceccfaa96

Reste : qualifier les références 054743 (eau) et 0911F0 (message médical), puis les helpers possessifs/pronoms/articles selon leurs vrais appelants, les limites de coursier et groupes de personnages. Menus généraux et parcours naturel complet suivent. Les 36 textes jusqu'à la cible sont un objectif de taille ; ne pas traduire d'héritage dormant pour les fabriquer.

Sauvegarde : commit intermédiaire local à 109 textes puis checkpoint validé à 114 sur work/v78-batch150. Seuls IPS, outils, rapports et PNG sont distribuables ; aucune ROM, cœur, état ni dump.
