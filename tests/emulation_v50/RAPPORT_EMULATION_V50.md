# Essais Snes9x V50

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` utilise les ROM V50 exactes, sans retouche de ROM ni de WRAM. 339 commandes avec accents et 337 ASCII, jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V49. Titre, introduction, combat, après-combat, restauration et menu restent conformes. Voir `results.json` et `comparison_v49.json`.

## Lectures contrôlées

`display_probe.py` charge l'état après combat et utilise la carte bancaire. L'opérande de description à `368B51` est redirigé pour chaque cas. Aucune écriture WRAM de test. Trois cas entrent directement dans le texte sélectionné afin de contourner les gardes du script : surnom `3498EA`, conservation d'objet `34B517`, au revoir `361AFB`. Ils ne testent pas ces gardes ou les effets du stockage.

Le terme « frère » à `36BAFC` et son repli au nom à `36BB0F` retournent immédiatement à leur appelant et ne restent pas visibles seuls. Pour ces deux cas seulement, un petit script temporaire « Lien: » appelle la routine, puis attend. Il est placé dans les octets nuls après les copies grammaticales, dans la réserve publiée. L'essai vérifie l'absence de recouvrement et ne permet des différences que dans ce script temporaire et l'opérande de carte bancaire. **Ce script de test n'est pas dans les IPS distribués.**

Douze contextes traduits et un contrôle de repli au nom sont relus dans les deux variantes :

| Contexte | Contrôle |
| --- | --- |
| 3479FF | Question dans « sa tête », puis énigme |
| 3498EA, entrée textuelle forcée | Salutation et surnom |
| 349AC0 | Conseil de rester immobile |
| 34B517, entrée textuelle forcée | Conservation d'un objet |
| 35603F | Fusil à air Magnum, réservé à Lloyd |
| 35698B | Super aérosol, comparaison d'efficacité |
| 356E3C | Lance-flammes, usage répété |
| 35734D | Rayon laser, première réplique |
| 3573D9 | Rayon plasma, premières répliques |
| 35C6FC | « son niveau max. », sans preuve du niveau maximal réel |
| 36BAFC | Terme « frère », avec script d'attente de test |
| 36BB0F | Nom du personnage en repli, conservé de V49 |
| 361AFB, entrée textuelle forcée | Au revoir |

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Les vignettes gardent les captures de 256 × 224 pixels et indiquent le cas et la page. Les accents, retours à la ligne et noms dynamiques sont relus visuellement. Certaines captures conservent des lignes de la page précédente.

`display_results.json` consigne les empreintes, destinations, scripts temporaires, captures et codes de sortie. Les variantes féminines des possessifs sont vérifiées structurellement ; la fixture conserve Ninten. L'appel direct du repli au nom ne valide pas ses conditions de sélection. Ces essais ne valident pas les déclenchements, effets de jeu, embranchements complets ou les 29 contextes du lot.

```sh
python tests/emulation_v50/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v50/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

États privés requis : `accents/after_combat.state` et `ascii/after_combat.state`. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est publiée.
