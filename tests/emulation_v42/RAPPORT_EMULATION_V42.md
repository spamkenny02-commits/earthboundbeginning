# Snes9x V42 — carte bancaire et Parer

## Régression générale

Le parcours normal V18 Work est rejoué sous Snes9x 1.63 : 339 commandes dans le profil accents, 337 dans le profil ASCII, jusqu'à l'image 25 803. Titre, introduction, après-combat, restauration d'état et menu ont les empreintes attendues. Les seules différences avec V18 sont les deux images de la bannière VICTOIRE. Les processus se terminent sans erreur.

## Carte bancaire — deux profils

L'état après le premier combat provient du parcours normal V41. La carte bancaire est celle naturellement présente dans l'inventaire. Navigation : A → droite → A → A → A (Use). La phrase anglaise observée en V41 est remplacée par la phrase française complète, sur trois lignes, dans les deux profils.

- [Carte bancaire — accents](card_accents.png)
- [Carte bancaire — ASCII](card_ascii.png)

## Parer — deux profils

L'état de rencontre avec la première lampe provient du parcours normal V41. La suite des commandes de référence rejoint le menu de combat ; droite → bas sélectionne Parer, puis A exécute l'action. Les captures sont prises toutes les dix images, puis image par image en fin de message pour relire la phrase complète avant sa fermeture automatique.

Le texte « Ninten reste sur ses gardes. » est relu intégralement dans les deux profils. Le nom, les espaces, la ponctuation et les glyphes sont lisibles.

- [Parer — accents](guard_accents.png)
- [Parer — ASCII](guard_ascii.png)

Aucun point d'entrée artificiel, patch ROM de test, objet injecté ou octet WRAM écrit n'est utilisé. Les états de parcours sont chargés dans le profil correspondant ; les ROM V42 sont celles produites par les IPS publiés.

## Reproduction et portée

- `replay.py` : régression générale ;
- `item_use_probe.py` : carte bancaire naturellement possédée ;
- `guard_probe.py` : Parer dans le premier combat.

Les sondes prennent `--rom`, `--core`, `--states-dir` et `--out`. Les empreintes et résultats figurent dans les trois fichiers JSON voisins. Seuls deux des 100 scripts V42 sont ainsi validés par un déclencheur normal. L'accès et le rendu des 98 autres ne sont pas revendiqués. Les ROM, états et coeur restent locaux ; seules les quatre captures de preuve sont publiées.
