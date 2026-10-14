# V18 Work — premiers essais réels sous émulateur

Date : 14 octobre 2026. Base publiée : `7ed7cdcbf2f67776cf74bbd797ef1d073499df17`.

Les deux IPS **V18 Work autonomes** ont été appliqués séparément à la ROM
originale USA 1.2. Aucun IPS V17 supplémentaire n'a été appliqué.
Les empreintes des deux ROM de test correspondent aux cibles du constructeur.

## Méthode

Cœur Snes9x `1.63 1bcc369`, exécuté au moyen d'un frontal libretro sans interface
graphique. Les captures proviennent du véritable framebuffer du cœur. Les
interactions sont des événements de manette, avec exécution CPU/APU/PPU réelle.
Aucun code de triche, modification mémoire ou script de téléportation n'a été
utilisé. Le cœur chargé est figé par son SHA-256 dans `results.json`.
Des échantillons audio ont été produits, mais aucune écoute n'a été effectuée.

## Contrôles réalisés dans les deux variantes

| Parcours | Résultat observé |
|---|---|
| Écran d'accueil, crédits et écran titre | Atteints sans blocage |
| Sélection de fichier et nouveau jeu | Fonctionnels |
| Vitesse, son et style des fenêtres | Menus navigables |
| Saisie des noms et confirmation | Ninten, Ana, Lloyd, Teddy et plat favori acceptés |
| Introduction française | Affichée et terminée |
| Chambre et déplacements dans la maison | Exploration fonctionnelle |
| Menu en jeu | Parler, Objets, PSI, Équiper, Voir, État affichés |
| Lampe hantée | Rencontre, commandes, attaques, dégâts et victoire exécutés |
| Après combat | EXP affichée, retour à l'exploration |
| État sauvegardé de l'émulateur | Chargement accepté et continuation identique |

Pour le dernier contrôle, la même suite de 60 images a été exécutée avant et
après rechargement : framebuffer identique et **131 072 octets de WRAM identiques**
dans chaque variante. Ce contrôle concerne les états Snes9x, pas la sauvegarde
native du jeu.

## Affichage observé

Les caractères accentués visibles dans les options, l'introduction, les menus
et le combat sont lisibles dans la variante accents. La variante ASCII présente
les formes sans accents attendues. Aucun plantage ni corruption graphique
évidente n'a été observé dans les scènes capturées.

La traduction reste partielle : le logo et les crédits restent anglais,
le plat par défaut reste `Prime Rib`, et le graphisme de victoire affiche
encore **YOU WON!**. Ces éléments sont repérés, pas corrigés par cet essai.

## Couverture et limites

Le parcours va d'une nouvelle partie au premier combat remporté et au téléphone
de la maison. L'interaction du téléphone montre `Biiip...` et se termine : aucun
dialogue de sauvegarde native n'a été validé pendant ce parcours. Ce résultat seul
ne suffit pas à diagnostiquer un défaut du téléphone.

Les 168 segments ajoutés par V18 se trouvent majoritairement dans d'autres
dialogues et zones. **Ils n'ont pas été parcourus individuellement sous émulateur**.
Leur intégration conserve les contrôles binaires documentés, mais ces essais ne
constituent pas une validation visuelle exhaustive de V18. Restent à vérifier :
les zones suivantes, les tutoriels modifiés, les 168 segments, les pointeurs
indirects, la sauvegarde native et son chargement après redémarrage du cœur.

## Preuves et reproduction

`results.json` consigne les empreintes, les nombres de commandes et les résultats.
`accents_history.json` et `ascii_history.json` conservent les commandes et les
empreintes des captures. `screenshots/` contient une sélection de captures.
`libretro_runner.py` est le frontal effectivement utilisé. Les ROM, les états
Snes9x, les dumps WRAM et le binaire du cœur ne sont pas distribués.

Exemple :

```sh
python3 libretro_runner.py --core /chemin/snes9x_libretro.so --rom /chemin/V18_accents.sfc --out /chemin/captures
```

Le frontal lit une commande JSON par ligne sur stdin. Les chemins `load` des
historiques sont des basenames : les remplacer par les chemins des états créés
lors de la reproduction. Chaque `frames` indique le nombre d'images à exécuter;
les touches sont libérées après chaque commande.
