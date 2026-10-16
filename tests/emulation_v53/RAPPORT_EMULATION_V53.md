# Essais Snes9x V53

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` applique les IPS V53 exacts, sans autre retouche de ROM ou de WRAM. 339 commandes avec accents et 337 ASCII jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V52. Voir `results.json` et `comparison_v52.json`. Les trois différences connues avec V18 restent celles des messages de combat déjà traduits.

## Lectures contrôlées

`display_probe.py` charge l'état privé V41 après combat et utilise l'action de la carte bancaire. Seuls les quatre octets de l'opérande de description `368B51` sont redirigés ; aucune WRAM n'est retouchée. Chaque cas recharge un état frais et supprime sa ROM temporaire après l'essai.

Pour les trois dialogues, l'essai lit directement la destination dans le champ NPC publié, vérifie qu'elle correspond à la copie française, puis y redirige l'action de carte. Il exécute le début complet de chaque copie, y compris les deux gardes de l'ascenseur dans l'état choisi. Ce n'est pas une interaction avec le personnage naturel : le lien avec la table est contrôlé structurellement et sa destination est lue par la fixture.

| Cas | Résultat visible |
| --- | --- |
| `33F3EE` | Maison hantée de Spookane, choix, puis réponse française existante |
| `3609EB` | « Il est temps de se dire adieu... », arrêt avant la suite |
| `350000` | « On monte! », arrêt avant activation de l'ascenseur |
| `354D77` | Liste des prix, sélection, puis « Objet: Arme ultime, hein? » |

La confirmation marchande commence par son contexte complet et passe par la sélection d'objet. Aucune capture de préfixe isolé sans sélection préalable n'est retenue. Aucune transaction n'est confirmée après la question. Les quatre nouveaux fragments sont relus dans les deux variantes : accents, lignes et objet dynamique sans coupure visible.

[Planche avec accents](proofs/affichage_accents.png) · [Planche ASCII](proofs/affichage_ascii.png). Sept vignettes natives 256 × 224 par planche. `display_results.json` consigne les quatre cas par variante, destinations, empreintes et captures.

Les déclenchements naturels, les autres branches de l'ascenseur, la scène de fin, les chemins par les anciennes entrées et la transaction réelle restent à vérifier. Les choix Yes/No restent pour le lot des menus.

```sh
python tests/emulation_v53/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v53/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

États privés requis : `accents/after_combat.state` et `ascii/after_combat.state`. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est publiée.
