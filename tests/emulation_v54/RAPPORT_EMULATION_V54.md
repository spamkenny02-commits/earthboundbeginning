# Essais Snes9x V54

Cœur Snes9x 1.63, SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.

## Parcours normal

`replay.py` applique les IPS V54 exacts, sans retouche supplémentaire de ROM ou de WRAM. 339 commandes avec accents et 337 ASCII jusqu'à la frame 25803. Les 109 captures avec accents et 103 ASCII sont identiques pixel par pixel à V53. Voir `results.json` et `comparison_v53.json`.

## Comparaison des choix avec V53

`display_probe.py` exécute les mêmes 14 scénarios en V53 et V54, dans les deux variantes : 56 exécutions isolées. Chaque cas recharge l'état privé V41 après combat. Seuls les quatre octets de la description de carte bancaire `368B51` sont redirigés vers le contexte choisi ; aucune WRAM n'est modifiée par la fixture. La ROM temporaire est supprimée après l'essai.

Trois captures par cas montrent le menu, le curseur après navigation et l'image après validation ou annulation. Les réponses de V54 sont comparées aux images V53 correspondantes. Les 28 comparaisons de résultat sont identiques pixel par pixel. La vérification échoue si l'une diffère.

| Cas | Entrée contrôlée | Navigation et résultat visible |
| --- | --- | --- |
| Maison hantée | destination NPC publiée à `205BFF` | Oui : réponse sur le piano ; Droite puis A : réponse négative ; B : même réponse négative |
| Stockage | `34B490` | Déposer : demande d'objet ; Retirer : absence d'objet stocké |
| Stockage répété | `34B4F0` | Retirer : absence d'objet stocké |
| Repos | `352AA1` | Les deux choix aboutissent aux mêmes messages qu'en V53 ; la fixture ne prouve pas un effet de soin réel |
| Pizza | `35E3C3` | Bas sélectionne Moyenne, deux fois Bas sélectionne Grande ; les réponses indiquent la bonne taille ; B annule |
| Paiement | `35E4E9` | Droite sélectionne Non, puis réponse de refus identique à V53 |
| Achat | `354D77` | Sélection d'objet, puis Non ; retour à la liste des prix |

Les quatorze scénarios sont relus dans les deux variantes : accents, alignement, largeur et positions du curseur. Les trois tailles de pizza restent entièrement visibles dans leur liste verticale. La confirmation marchande passe par la sélection d'un objet avant le menu Oui/Non.

- Avec accents : [planche 1](proofs/affichage_accents_1.png), [planche 2](proofs/affichage_accents_2.png).
- ASCII : [planche 1](proofs/affichage_ascii_1.png), [planche 2](proofs/affichage_ascii_2.png).

Chaque planche conserve les vignettes natives 256 × 224. `display_results.json` consigne les 56 exécutions, empreintes, commandes de navigation, captures et comparaisons.

Les appels via la carte bancaire ne constituent pas un parcours naturel des scènes. Les 85 blocs ne sont pas tous exécutés ; les autres sont contrôlés structurellement. Les résultats visibles ne prouvent pas l'état interne complet après une transaction, une commande ou un repos.

```sh
python tests/emulation_v54/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/replay
python tests/emulation_v54/display_probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/affichage
```

États privés requis : `accents/after_combat.state` et `ascii/after_combat.state`. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est publiée.
