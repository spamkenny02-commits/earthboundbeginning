# Repérage des textes graphiques — premier passage

ROM : EarthBound Beginnings (USA) 1.2.sfc, 4 Mio, HiROM, sans en-tête copieur.
SHA-256 : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

558 PNG extraits : 20 atlas de décors, 464 groupes de sprites, 6 cartes, icônes de carte, logos, fenêtres, titre (fond et atlas brut), écran des mélodies, défaite et polices. La ROM n'a pas été modifiée. Les fichiers ne contiennent pas la ROM.

## Utilisation

Décompresser le dossier, puis ouvrir `index.html`. Cliquer sur un aperçu pour afficher le PNG à sa taille réelle. Les images utilisent leurs palettes indexées originales. Les noms de fichiers Onett/Twoson/Threed/Fourside/Summers/Scaraba viennent de CoilSnake ; le contenu de cette ROM indique Podunk/Merrysville/Spookane/Ellay/Reindeer/Snowman.

Les adresses ci-dessous sont des **offsets de fichier en hexadécimal**, pas des adresses SNES. En HiROM, l'adresse SNES correspondante est généralement l'offset + C00000. Pour les sprites, l'adresse ci-dessous est celle de la description du groupe ; `inventaire_technique.json` donne également les adresses des images de chaque frame.

Pour un décor : atlas de 16 blocs par ligne, chaque bloc fait 32×32 pixels. À la position (x,y), le numéro du bloc vaut `(y // 32) * 16 + (x // 32)`. `arrangements_XX.json` donne ses 16 tuiles ; bits 0–9 = numéro de tuile, 10–12 = palette, 14/15 = retournements. En 4 bpp, chaque tuile occupe 32 octets **dans les données décompressées**. Le bloc de graphismes doit être recompressé après édition : l'adresse de départ ne permet pas une substitution directe des pixels dans la ROM.

## Inscriptions relevées

Les lignes regroupent des inscriptions visibles ; elles ne représentent pas un comptage exhaustif de chaque occurrence. Les mots coupés dans les atlas demandent de reconstruire l'enseigne sur la carte.

| Élément | Anglais observé / point à vérifier | Offset | État |
|---|---|---|---|
| Titre — fond | EARTH BOUND (partiel), BEGINNINGS, copyrights | `311409` | Confirmé visuellement |
| Titre — objets bruts | Lettres animées : disposition à reconstruire | `313A15` | À reconstruire |
| Nintendo | produced by / Nintendo | `2CFACB` | Confirmé visuellement |
| APE | presented by / Shigesato Itoi | `2CFC5F` | Confirmé visuellement |
| HALKEN | HALKEN | `2DC01C` | Confirmé visuellement |
| ProducedBy | produced by / SHIGESATO ITOI | `2DC208` | Confirmé visuellement |
| PresentedBy | presented by / Nintendo | `2DC3D6` | Confirmé visuellement |
| Ancien écran illustré | EARTH BOUND / THE WAR AGAINST GIYGAS! / GAS ; petites enseignes à relire | `2E9201` | Confirmé visuellement |
| Interface — fenêtres | YOU WON! / AUTO / SMAAAASH!! / HP / PP | `217EC1` | Confirmé visuellement |
| Mélodies — illustrations | Doll / Canary / Monkey / Piano / Dragon / Cactus / EVE / Grave Stone | `20B16D` | Confirmé visuellement |
| Carte — pictogrammes | REINDEER / PODUNK / MERRYSVILLE / CEMETERY / SUBURBS / MT. ITOI / DESERT / FOOD / HOSPITAL / DEPTSTORE / HINT / SHOP / HOTEL | `2CF1F9` | Confirmé visuellement |
| Carte 0 — Podunk | PODUNK / 1/100 | `2C9687` | Confirmé visuellement |
| Carte 1 — Merrysville | MERRYSVILLE / 1/100 | `2CBCA9` | Confirmé visuellement |
| Carte 2 — Spookane | SPOOKANE / 1/100 | `2D0000` | Confirmé visuellement |
| Carte 3 — Ellay | ELLAY / 1/100 | `2D33B0` | Confirmé visuellement |
| Carte 4 — Reindeer | REINDEER / 1/100 | `2D63EB` | Confirmé visuellement |
| Carte 5 — Snowman | SNOWMAN / 1/100 | `2D954C` | Confirmé visuellement |
| Décor 00 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `18AA80` | À approfondir |
| Décor 01 | PODUNK TOWN / TOWNHALL / PODUNK DEPT STORE / BURGER SHOP / HOSPITAL / HOTEL / STOP | `1A8340` | Confirmé visuellement |
| Décor 02 | HOTEL | `390D07` | Confirmé visuellement |
| Décor 03 | DRUGSTORE / WELCOME TO SPOOKANE / HOSPITAL / HOTEL / ZZ | `39612A` | Confirmé visuellement |
| Décor 04 | ELLAY DEPT STORE / BURGER / HOUSE / POLICE / HOSPITAL / HOTEL / STOP | `39CE9E` | Confirmé visuellement |
| Décor 05 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3A35F9` | À approfondir |
| Décor 06 | ZOO | `3A6CFB` | Confirmé visuellement |
| Décor 07 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3B0000` | À approfondir |
| Décor 08 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3B39E3` | À approfondir |
| Décor 09 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3B967B` | À approfondir |
| Décor 10 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3C0000` | À approfondir |
| Décor 11 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3C6872` | À approfondir |
| Décor 12 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3CB6B1` | À approfondir |
| Décor 13 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3D3F2F` | À approfondir |
| Décor 14 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3DA625` | À approfondir |
| Décor 15 | REINDEER STATION | `3E0000` | Confirmé visuellement |
| Décor 16 | REINDEER HOSPITAL / DEPT STORE (fragmenté) / BURGER SHOP / PIZZA / HOTEL / STOP | `3E5EC3` | Confirmé visuellement |
| Décor 17 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3EC066` | À approfondir |
| Décor 18 | STATION / MERRYSVILLE HOSPITAL / TWINKLE ELEMENT... (fragmenté) | `3F31B6` | Confirmé visuellement |
| Décor 19 | Aucune inscription clairement lue lors de ce passage ; petites inscriptions à vérifier | `3DD754` | À approfondir |
| Sprite 410 | HELI (et version miroir) | `1F7CCF` | Confirmé visuellement |
| Sprite 436 | YOU ARE HERE | `1F7F69` | Confirmé visuellement |
| Sprite 446 | HINT | `1F8083` | Confirmé visuellement |
| Sprite 87 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F5BF2` | À approfondir |
| Sprite 205 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F67EC` | À approfondir |
| Sprite 206 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F6815` | À approfondir |
| Sprite 207 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F683E` | À approfondir |
| Sprite 213 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F6904` | À approfondir |
| Sprite 248 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F6C7F` | À approfondir |
| Sprite 259 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F6D92` | À approfondir |
| Sprite 406 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F7C5B` | À approfondir |
| Sprite 442 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F800F` | À approfondir |
| Sprite 459 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F81D8` | À approfondir |
| Sprite 460 — petite inscription | Petite inscription ou symbole ; lecture à confirmer | `1F8201` | À approfondir |

## Générique supplémentaire

`Staff/staff_text.md` contient les rôles et noms du générique, décodés séparément. Son bloc commence à `17FBE8` et occupe 1026 octets, terminateur FF inclus. `staff_raw.bin` conserve les octets sources et `staff_chars.yml` la correspondance de glyphes. Ce texte doit être ajouté au corpus à traduire ; il ne faut pas le traiter comme une unique image. La correspondance héritée a été utilisée : à valider visuellement lors de l'exécution.

## Limites

Ce premier passage ne prouve pas que tous les mots anglais dessinés ont été trouvés. Les petites inscriptions, les sprites de combat, les fonds de bataille et les routines spécifiques du hack restent à examiner. Les assets hérités (notamment l'écran « THE WAR AGAINST GIYGAS! ») sont présents dans la ROM ; leur affichage dans cette version n'a pas été confirmé en émulateur. Les palettes alternatives des décors ne sont pas toutes rendues. Le titre est fourni en fond + atlas d'objets : sa disposition animée reste à reconstruire.

## Reproduction

Extraction avec CoilSnake, commit `346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a` : https://github.com/pk-hack/CoilSnake

Installer ses dépendances et compiler `native_comp`, puis :

```sh
python reperer_graphismes.py "ROM.sfc" dossier_sortie chemin_CoilSnake
```

Le script n'écrit jamais dans la ROM. Les assets du hack sont lus par leurs pointeurs actuels ; la table des sprites a été déplacée à 1F840A, contrairement à celle du jeu d'origine. `inventaire_technique.json` conserve les pointeurs de données et leurs références.
