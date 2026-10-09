# Traduction française v03

473 entrées intégrées, contre 407 en v02 : 348 libellés (dont 23 noms d’ennemis), 123 blocs de texte et deux séquences d’introduction. Cinq propositions sont toujours exclues faute de place.

## Ajouts

- 33 messages de combat : rencontre, attaque, défaite, disparition, immobilisation, expérience et certains effets de statut.
- 23 noms d’ennemis : lampe, oreiller, poupée, corbeaux, chiens, serpents, zombies et autres adversaires. Les noms français portent leur article. Le réglage qui ajoutait « The » est désactivé uniquement pour ces entrées.
- Deux scripts du clavier des noms : « MAJ », « min », « Au choix », « Effacer ».
- Choix de fenêtres : Nature, Menthe, Thon, Mayonnaise, Raisin.
- La défense se nomme désormais « Parer ». Trois commandes trouvées dans le menu de combat du remake : Voir, Jeter, Tirer.

Les huit nouveaux libellés et les deux scripts de clavier sont répertoriés avec leur adresse, octets source et justification dans `traduction/sources_complementaires.json`. Ce fichier est une référence nécessaire pour reconstruire les traductions.

## Intégration

Les scripts conservent les commandes, variables et pointeurs. Lorsque des pointeurs visent l’intérieur d’un bloc, les fragments français sont complétés par des espaces pour garder les positions. Aucune relocalisation n’est effectuée.

La table des ennemis contient un octet « The Flag » suivi du nom sur 25 octets dans chaque enregistrement de 94 octets. Cette structure est confirmée par [CoilSnake eb.yml](https://github.com/pk-hack/CoilSnake/blob/master/coilsnake/assets/structures/eb.yml). Seuls cet octet et le champ du nom sont modifiés. Les vérifications indépendantes contrôlent que les statistiques et autres paramètres de chacun des 23 ennemis restent identiques.

Les deux variantes passent les contrôles de checksum, taille, application IPS, 473 traductions et conservation des données des ennemis. Les 80 glyphes français sont contrôlés pour la variante accents. La ROM source reste inchangée.

## Essais

Cœur Snes9x 2010 libretro, révision `fe690dd321fa5a46b5234a2bde089d2518c62b0e`. Exécution logicielle et captures du framebuffer réel. Le parcours `tests/parcours_v03.json` couvre le démarrage, la création de partie, le clavier, l’introduction, la maison, le premier combat et le retour à la maison. Les résultats détaillés, empreintes et sessions sont dans `tests/rapport_emulation_v03.json`.

```sh
python tests/emulateur.py /chemin/snes9x2010_libretro.so build/EarthBound_Beginnings_FR_v03_accents.sfc /tmp/essais --actions tests/parcours_v03.json
```

Les captures dans `tests/captures_v03/` proviennent de l’émulateur. Aucun cœur, état SNES ou fichier ROM n’est distribué. Le champ `runtime_validated: false` des rapports binaires signifie que les scripts de vérification ne certifient pas une partie complète ; les essais limités sont décrits séparément.

## À poursuivre

La traduction reste partielle. Les attaques et dégâts emploient encore des routines anglaises, et un texte résiduel est visible autour de l’expérience : un « e » avant le nom et après EXP. Ce défaut est présent avec et sans accents, mais absent dans l’essai de la ROM anglaise ; il reste à corriger. Les messages de combat à plusieurs membres du groupe, les ennemis autres que la lampe, les statuts et certains noms hérités restent à vérifier en jeu. Le clavier traduit conserve l’alphabet anglais pour la saisie : ajouter des touches accentuées nécessite un travail distinct.

Téléphone, sauvegarde/chargement, mère, poupée, mélodie, chien, dépôt et graphismes anglais restent à tester ou traduire. Les nouveaux messages ont été raccourcis pour tenir en place ; une relecture en contexte demeure nécessaire hors du premier combat.
