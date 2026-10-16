# Snes9x V44 — parcours normal et routines grammaticales

## Parcours normal

Les IPS finaux sont rejoués sous Snes9x 1.63 : 339 commandes dans le profil accents, 337 dans le profil ASCII, jusqu'à l'image 25 803. Titre, introduction, après-combat, restauration d'état et menu ont les empreintes attendues. Les différences avec V18 restent limitées aux deux captures VICTOIRE. Les deux processus se terminent sans erreur ; résultats dans `results.json`.

Le parcours initial a révélé une référence à une mauvaise copie dans le groupe de messages de rencontre. Après correction de la correspondance des adresses, les captures du parcours de référence sont de nouveau conformes. L'audit et les tests de destination sont décrits dans le [rapport V44](../../RAPPORT_V44.md).

## Dix messages dans le moteur natif — vingt cas

La sonde `possessive_probe.py` part de l'état normal V41 `lamp_checkpoint`, rejoint le premier combat et choisit Parer. Pour chaque cas, une copie privée de la ROM V44 remplace uniquement l'opérande de quatre octets `368275`, dans la table des descriptions d'actions, par l'adresse d'un message V44. Tous les autres octets sont comparés à la ROM publiée. Aucun octet WRAM n'est écrit par la sonde.

Cette méthode force l'affichage d'un autre message avec le sujet Ninten et l'action de garde existante. Elle **ne teste pas l'accès naturel à ces attaques, leurs animations ou leurs effets de combat**. Les ROM de fixture sont supprimées et ne sont pas distribuées. Le JSON `possessive_results.json` conserve les empreintes de base et de fixture, la destination, le résultat et la capture choisie pour chaque cas.

Les vingt captures ont été relues : phrase complète, espaces, accents et noms dynamiques sont lisibles, sans débordement observé.

| Message | Accents | ASCII |
|---|---|---|
| Corps engourdi, pronom « il » | [Capture](proofs/2f7192_accents.png) | [Capture](proofs/2f7192_ascii.png) |
| Griffe acérée | [Capture](proofs/2f8026_accents.png) | [Capture](proofs/2f8026_ascii.png) |
| Puissante queue | [Capture](proofs/2f804b_accents.png) | [Capture](proofs/2f804b_ascii.png) |
| Mine réjouie | [Capture](proofs/2f8239_accents.png) | [Capture](proofs/2f8239_ascii.png) |
| Flûte et souffle toxique | [Capture](proofs/2f835c_accents.png) | [Capture](proofs/2f835c_ascii.png) |
| Aspire par sa flûte | [Capture](proofs/2f83ca_accents.png) | [Capture](proofs/2f83ca_ascii.png) |
| Attaque de détresse | [Capture](proofs/2f8a52_accents.png) | [Capture](proofs/2f8a52_ascii.png) |
| Patte géante | [Capture](proofs/2f8b65_accents.png) | [Capture](proofs/2f8b65_ascii.png) |
| Brume glaciale | [Capture](proofs/2f9c02_accents.png) | [Capture](proofs/2f9c02_ascii.png) |
| Trompe géante | [Capture](proofs/367694_accents.png) | [Capture](proofs/367694_ascii.png) |

Les trois branches de genre des routines privées sont vérifiées par décodage indépendant. La sonde native utilise Ninten et ne prétend donc pas avoir parcouru les branches féminine et neutre dans le jeu.

## Reproduction et limites

`replay.py` prend `--rom`, `--core` et `--out`. `possessive_probe.py` prend aussi `--states-dir`, répertoire des états normaux par profil. Le coeur, les ROM et les états restent locaux.

Les dix messages testés appartiennent aux 46 scripts de messages V44. Les 36 autres messages et les scènes tardives, dont la cuillère, Laura et Pippi, restent à relire dans leur contexte naturel. Le parcours général constitue un test de non-régression du début du jeu, pas une validation de tous les dialogues.
