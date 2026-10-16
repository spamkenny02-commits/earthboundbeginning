# Snes9x V46 — consommation et EXP

## Parcours normal

Les ROM exactes des IPS V46 sont rejouées sous Snes9x 1.63 : 339 commandes avec accents, 337 en ASCII, jusqu'à l'image 25 803. Les processus se terminent sans erreur. Titre, introduction, après-combat, restauration d'état et menu restent conformes.

Par rapport à V18, les captures VICTOIRE `battle_step_30/31` et la nouvelle formulation d'EXP `battle_step_32` diffèrent. Une comparaison de toutes les captures avec V45 retrouve **uniquement** `battle_step_32`, dans le rectangle `(76,34)–(135,45)` : le texte passe de « gagne » à « : + ». Les pixels extérieurs sont identiques. Les résultats sont conservés dans `results.json` et `comparison_v45.json`.

- [EXP — accents](proofs/experience_accents.png)
- [EXP — ASCII](proofs/experience_ascii.png)

## Consommation par le menu Eat

`eat_probe.py` utilise l'état normal V41 après combat et la ROM exacte de chaque IPS. Le runner de fixture V39 remplace uniquement l'octet d'inventaire `0099F1`, de B1 (carte bancaire) à AF (pain). Le menu normal Objets → Eat exécute ensuite le script individuel de consommation.

La phrase complète « Objet consommé par Ninten : Pain. » est lisible dans les deux variantes, avec les accents corrects et sans débordement. Le slot d'inventaire est vide après consommation (`00`). Le menu reste anglais pour sa passe dédiée.

- [Consommation — accents](proofs/eat_accents.png)
- [Consommation — ASCII](proofs/eat_ascii.png)

Aucun pointeur de routage n'est modifié pour ce test : il exécute la commande Eat normale. L'acquisition naturelle du pain n'est pas couverte. Les preuves, empreintes et lectures du slot figurent dans `eat_results.json`.

## Portée

Les essais utilisent Ninten seul. Les messages de groupe et les contextes tardifs — Mary, porte, remise d'objet, défaite et papillon — nécessitent encore une relecture dans leurs scènes naturelles. Les tests structurels vérifient leurs commandes, leurs références et la réutilisation de la routine française V45. Aucun effet de soin particulier n'est déduit de la capture de consommation.

`replay.py` prend `--rom`, `--core` et `--out`. `eat_probe.py` prend aussi `--states-dir`. Le cœur, les ROM et les états restent privés et locaux.
