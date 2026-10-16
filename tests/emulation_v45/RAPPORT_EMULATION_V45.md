# Snes9x V45 — inventaire et équipement

## Parcours normal

Les IPS publiés sont rejoués sous Snes9x 1.63 : 339 commandes dans le profil accents, 337 en ASCII, jusqu'à l'image 25 803. Titre, introduction, après-combat, restauration d'état et menu restent conformes. Les seules différences avec V18 sont les deux images VICTOIRE attendues. Les processus se terminent sans erreur ; résultats dans `results.json`.

## Dialogues d'inventaire — routage contrôlé

`inventory_dialogue_probe.py` part de l'état normal après combat et utilise la carte bancaire naturellement présente. Dans chaque fixture, seul le pointeur de description `368B51` est temporairement remplacé par l'entrée du dialogue à tester. Tous les autres octets ROM sont comparés à la version publiée ; aucune WRAM n'est écrite par la sonde.

Pour le dialogue d'inventaire plein, les deux premières validations affichent les questions, droite sélectionne No, puis la validation laisse l'objet. On relit « Mais, Ninten : plus de place pour d'autres objets », « Veux-tu jeter quelque chose ? », « Alors, tu laisses Carte bancaire ici ? » et « Objet laissé par Ninten : Carte bancaire. » Le dernier écran exécute aussi la copie française du message d'abandon `2F7CF8` et sa sous-routine privée.

| Écran | Accents | ASCII |
|---|---|---|
| Plus de place | [Capture](proofs/2f7c73_accents_1.png) | [Capture](proofs/2f7c73_ascii_1.png) |
| Jeter quelque chose ? | [Capture](proofs/2f7c73_accents_2.png) | [Capture](proofs/2f7c73_ascii_2.png) |
| Laisser l'objet | [Capture](proofs/2f7c73_accents_4.png) | [Capture](proofs/2f7c73_ascii_4.png) |
| Objet laissé | [Capture](proofs/2f7c73_accents_6.png) | [Capture](proofs/2f7c73_ascii_6.png) |
| Que veux-tu jeter ? | [Capture](proofs/2f7d0f_accents_1.png) | [Capture](proofs/2f7d0f_ascii_1.png) |

Les accents, les noms et les lignes sont lisibles. Les choix Yes/No restent anglais. Le test de sélection de la carte retrouve également le blocage V44 « Ne jette pas Carte bancaire. » La seconde confirmation de destruction d'un objet jetable n'est pas couverte par cette fixture.

Ce routage **ne prouve pas un ramassage naturel, une saturation réelle ou l'abandon effectif d'un objet**. Les registres d'objet proviennent du contexte de la fixture. Les ROM de test sont supprimées et ne sont pas distribuées. Empreintes et références dans `inventory_results.json`.

## Journal de fuite — routage contrôlé

`flee_message_probe.py` redirige uniquement la description de Parer, dans le premier combat, vers le script `2F84F3`. Le texte complet « Ninten : tentative de fuite... Fuite réussie ! » est lisible dans les deux profils. Le nom est produit par le jeu ; la routine privée de groupe est appelée. Ce test vérifie le texte, **pas une fuite réellement réussie**.

- [Fuite — accents](proofs/flee_accents.png)
- [Fuite — ASCII](proofs/flee_ascii.png)

Les cinq entrées de nombre de participants et les deux branches de genre sont contrôlées statiquement ; les scènes natives ci-dessus utilisent Ninten seul.

## Commande normale Équiper — inventaire de fixture

`equip_probe.py` conserve la ROM exacte des IPS et remplace seulement le premier octet d'inventaire (`0099F1`, B1 → 11) par une batte en plastique, à l'aide du runner de fixture V39. Le menu normal Équiper permet de sélectionner la batte. L'attaque passe de 2 à 6, la défense reste à 2 et l'arme apparaît équipée dans les deux profils.

- Accents : [avant](proofs/equip_accents_1.png), [après](proofs/equip_accents_3.png)
- ASCII : [avant](proofs/equip_ascii_1.png), [après](proofs/equip_ascii_3.png)

Ce test ne couvre pas l'acquisition naturelle de l'arme et n'affiche pas les deux nouvelles notifications textuelles d'attaque/défense. Ces notifications restent à vérifier dans leur scène d'origine.

Les sondes prennent `--rom`, `--core`, `--states-dir` et `--out`. Le parcours général ne nécessite pas `--states-dir`. Le coeur, les ROM et les états restent locaux.
