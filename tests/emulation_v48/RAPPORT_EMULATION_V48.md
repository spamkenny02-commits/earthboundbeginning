# Essais Snes9x V48

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` rejoue les commandes historiques V18 sur les ROM V48 exactes, sans retouche de ROM ou de WRAM. 339 commandes avec accents et 337 en ASCII, jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V47. Titre, introduction, combat, après-combat, restauration et menu restent conformes. Les seules différences historiques face à V18 sont VICTOIRE et l'EXP. Voir `results.json` et `comparison_v47.json`.

## Affichage contrôlé

`display_probe.py` charge l'état après combat et utilise normalement la carte bancaire. Chaque ROM de test change uniquement les quatre octets de son opérande de description à `368B51`. Aucune WRAM n'est retouchée. Pour les nouveaux scripts, l'opérande vise la copie française ; pour les descriptions complètes, il vise leur contexte existant. Le nom de l'objet utilisé dans les messages dynamiques reste celui de la carte bancaire de la fixture.

Huit nouveaux messages et cinq contextes complets sont relus dans les deux variantes :

| Source ou contexte | Contrôle |
| --- | --- |
| 06FB5D | Mauvaise clé |
| 07D9FD | Cadeau vide |
| 06FC6D | Objet immangeable |
| 06FFBB | Téléphone ne recevant que des appels |
| 07C6B6 | Utilisation impossible, nom d'objet dynamique |
| 07D991 | Inventaire plein, pronom français |
| 063D93 | Dépôt absent, titre français et nom dynamique |
| 09FD82 | Mesure des objets, nom et pronom français |
| 356270 | Arme compatible, correction « Chacun » |
| 35658B | Aliment restaurant 50 PV |
| 356676 | Boisson restaurant 100 PV |
| 32AB38 | Corps, pendentif et protection contre la glace |
| 32ADB0 | Objet pour Lloyd et usage répété |

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Chaque vignette conserve les 256 × 224 pixels de la capture et porte son adresse et sa page. Les écrans sont relus visuellement ; certains conservent des lignes de la page précédente pendant le défilement normal. Le dernier écran du générateur de gel ferme le dialogue, sans être une preuve de texte. `display_results.json` consigne toutes les empreintes, destinations, captures et codes de sortie.

Ces essais ne valident pas l'accès naturel aux scènes, les effets des objets, ni les autres scripts du lot. La fixture conserve Ninten : elle ne valide pas en situation les variantes féminines de titres ou pronoms, testées structurellement. Les ROM de test ne sont pas distribuées.

```sh
python tests/emulation_v48/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v48/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

Les états privés `accents/after_combat.state` et `ascii/after_combat.state` sont requis pour l'essai contrôlé. Aucune ROM, sauvegarde ni bibliothèque d'émulation n'est publiée.
