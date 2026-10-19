# V76 — Pippi

## Corrections

Six plages anglaises de la fermeture issue de `386B63` sont traduites : présentation de Pippi, retrouvailles, reconnaissance de Ninten à Podunk, secret concernant sa mère et message du matin. La forme dynamique relue est notamment « Ah, Ninten, de Podunk ! » ; le nom vient toujours de la commande native du jeu.

Les six remplacements restent à leur taille d'origine. Aucun octet n'est alloué, aucune commande n'est déplacée et aucun pointeur n'est réécrit. La racine complète demeure le champ 9 du PNJ 319, opérande `2036E0`. Les quatre contextes `386B63`, `386BAD`, `386BC9` et `386C58` restent analysables et terminaux avec les mêmes commandes que V75. Sprites, banque 25 et créneau privé `330FC0–331000` sont identiques à V75.

## Validation en émulateur

Quatre scénarios par profil :

- `pippi_entry` appelle la racine complète `386B63`. Depuis l'état post-repos conservé, le moteur enchaîne présentation, retrouvailles, secret et matin.
- `podunk_and_secret` appelle directement `386BAD` pour isoler le nom dynamique, le secret et le matin.
- `secret_only` appelle directement `386BC9`.
- `morning` appelle directement `386C58`.

34 captures V76 relues et comparées à 34 captures V75 avec les mêmes états et entrées manette. 28 différences, toutes dans la fenêtre textuelle `(104,8,248,98)` ; 7 524 images échantillonnées côté V76. Les 68 PNG déclarés sont les seuls conservés. Les traces confirment les branches affichées (`386B80`, `386BC8`, `386C06`, `386C69`).

23 tests ciblés passent avec la ROM privée : V76 (7), régression V75 (8), stockage protégé V65 (8). Les deux IPS se reconstruisent avec les mêmes empreintes. Le contrôle public exécute les cinq tests hors ROM et la vérification des images.

## Limites

Les quatre accès sont contrôlés par une fixture privée de carte bancaire. Le premier appelle bien l'entrée complète, mais ne prouve pas la rencontre naturelle du PNJ sur la carte. Les trois autres sont volontairement des appels de branches intérieures, utilisés pour isoler leur rendu. Aucun flag, inventaire ou octet WRAM n'est écrit directement ; seules la redirection temporaire et son wrapper sont modifiés dans une ROM privée.

L'état initial est la référence V71 post-repos : Ninten seul, 30 PV, 10 PP, 20 $, carte bancaire. Les empreintes de la ROM, du cœur et des états figurent dans les résultats ; leurs contenus ne sont pas publiés. Aucun achèvement global ni 100 % n'est revendiqué.

## Patchs

Appliquer un seul IPS V76 directement à la ROM originale USA 1.2.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
| --- | --- | --- |
| Accents | `baa58e1c51212a8e82a601d23121b05303b7af20c1e19b58089208da31b80ab8` | `07eb5458f512bd5032f5b8905f9bf65e6c43de2e93cc2e6e6afb2aa6204574aa` |
| ASCII | `1aa6e71c81504f924ee05bf0bd3a5f75fcf11e5e9332f744feb61a4aac9f3448` | `53d3f2fd2a8e3061e9fcb29ba1ee753633895be3651ed8935bc8095357cf2ef6` |

Checkpoint initial local `56e78e0`, branche `work/v76-pippi-local`. Après validation : `work/v76-pippi-validated`, puis publication sur `main` sans force push.

Prochaine priorité concrète : mineur `3738F8`/PNJ 210, puis les autres candidats directs historiques, dont chameau `374307`. Le relevé V73 n'est ni récursif ni une preuve d'accès naturel ou d'exhaustivité. Services restants, variantes à plusieurs personnages, menus et parcours naturel complet restent à traiter.
