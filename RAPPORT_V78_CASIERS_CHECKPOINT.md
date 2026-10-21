# V78 — casiers de l'école, checkpoint du 21 octobre 2026

Neuf nouvelles sources distinctes, compteur **129/400**, 167 plages physiques. Même lot en cours ; V77 reste la release sur main. Les IPS accents et ASCII sont reconstruits avec neuf écritures fixes supplémentaires : 393 enregistrements ajoutés à V77, aucune allocation supplémentaire pour ces casiers.

| Offset source | Français intégré |
|---|---|
| 06F8D9 | Verrouillé |
| 06FA14 | ouvre avec la |
| 06FA30 | Objet: |
| 06FA3B | . |
| 06FA5D | l'a |
| 06FA6B | (Clé tordue : ça coince !) |
| 06FA93 | (Ce casier est vide.) |
| 06FAB4 | Ton sac est plein. |
| 06FAD6 | le laisse. |

Le fragment « in the locker. » devient le point final après l'objet ; il reste une source préexistante distincte. « Ninten l'a » est le retour compact de réception : quatre octets disponibles pour ce suffixe. La légende neutre « Objet: » évite les accords calculés. La clé tordue a été raccourcie après une première inspection qui montrait la ponctuation seule à la ligne. Les captures publiées correspondent à la correction finale.

## Qualification et préparation

Table des placements 1CF2F5, opérande 002261 ; les six PNJ606/608/609/612/613/616 sont présents dans le secteur823. Tous utilisent la racine primaire 06F8D9 ; PNJ608 a la secondaire 38E2C2, PNJ613 la secondaire 38E397. Les formats de placement sont documentés par les sources primaires [MapSpriteModule.py](https://github.com/pk-hack/CoilSnake/blob/master/coilsnake/modules/eb/MapSpriteModule.py) et [map_sprites.py](https://github.com/pk-hack/CoilSnake/blob/master/coilsnake/model/eb/map_sprites.py). Le reconstructeur vérifie les placements et pointeurs dans la ROM fournie.

La sonde privée donne la Machine à clés AC ou la clé CD, puis utilise la téléportation native D1 (commande 1F21D1, trois octets) et le retour vide existant 38B550. Après stabilisation, marche dans le couloir, porte existante 1CFDD7 vers destination0F2105, déplacement jusqu'au casier, commande Voir, ouverture de l'inventaire, action Use ordinaire. Aucune racine de casier appelée directement par le testeur et aucune écriture WRAM. Le parcours initial depuis le début du jeu n'est pas certifié naturel. Le sac plein est préparé par douze dons natifs de Badge Franklin en plus de la carte et de la Machine.

## Résultats et limites

Quatre cas par profil : récupération PNJ608, vide PNJ613, clé tordue PNJ608, sac plein PNJ608. **108 paires V77/V78**, **28 changements limités à la fenêtre du texte**, **27 436 images échantillonnées**. Les mêmes commandes et préparations sont rejouées sur V77. Vingt-deux captures clés relues visuellement dans les deux profils : ouverture, contenu, réception, refus et inventaires finaux. La Fusée-jouet en kit ID2E est présente après réception ; elle est absente du sac plein, avec message « Ninten le laisse. ».

Les commandes natives, les flags0459/037F, les pointeurs PNJ, les sprites, la banque25 et l'emplacement temporaire de sonde sont conservés dans le patch distribué. Les sondes modifient temporairement leur propre ROM privée ; seules les traces sémantiques, scripts et PNG sont conservés dans Git. ROM, cœur, états et dumps mémoire ne sont pas distribués.

Les 26 tests V78 avec ROM privée couvrent le registre, la reconstruction et les preuves historiques ainsi que les chemins natifs des casiers et l'identité des fixtures finales. Détails et SHA256 des deux IPS : tools/v78/validation_v78.json. Les anciennes captures restent des snapshots de leur checkpoint, sans prétendre avoir été rejouées avec ce suffixe neuf.

Restent : autres contenus et flags des casiers, nouvelle tentative après libération du sac, trajets naturels complets, commandes d'objets encore anglaises (lecteur candidat38E834), autres menus, fin/générique et relecture intégrale. Ce sous-graphe ne fournit que neuf sources pertinentes ; aucune source dormante ajoutée pour atteindre artificiellement400. La couverture complète et les 100 % ne sont pas établis.
