# Vérification d'affichage V39 — Snes9x

## Résultat

**22 descriptions relues dans chacun des profils accents et ASCII : 44 cas.** Les nouveaux textes français apparaissent dans la fenêtre d'aide des objets. Aucun caractère corrompu, débordement hors fenêtre ou texte nouveau tronqué n'a été observé sur les pages contrôlées. Les noms dynamiques Ninten, Ana, Lloyd et Teddy sont correctement raccordés. Le texte long de protection contre le feu, la glace, la foudre et la paralysie reste lisible. La petite fusée utilise plusieurs pages ; sa fin « d'artifice » apparaît à la page suivante.

## Méthode et portée

- Snes9x 1.63, coeur SHA-256 `826bdab012551be45dcdca92a4823a43caf556f7e480e3e8a613a7fae9afd210`.
- ROM originale vérifiée, puis application de l'IPS V39 publié, sans patch de test ni remplacement de pointeur.
- Chargement de l'état normal `after_combat.state` produit par `replay.py` dans le profil correspondant.
- Contrôle du premier emplacement d'inventaire à `$7E99F1` : carte bancaire, identifiant 177.
- Remplacement temporaire de ce seul octet WRAM par l'objet à examiner. Le reste de l'état et la ROM ne sont pas modifiés par la sonde.
- Navigation avec la manette : A → droite → A (Objets) → A (objet) → quatre fois bas → A (Help!).
- Une capture après 600 images, puis A pour avancer : quatre pages capturées par objet, afin de couvrir l'en-tête, les préambules et la description.
- Relecture visuelle des pages 2 à 4 dans les deux profils ; les planches ci-dessous regroupent les zones de texte sans retouche de leur contenu.

Il s'agit d'un **inventaire contrôlé suivi du déclencheur normal du menu**, pas d'une preuve d'acquisition naturelle des 22 objets. Ce test ne valide ni l'utilisation au combat, ni les conditions narratives, ni tous les appels alternatifs vers les mêmes scripts. La clé d'émulation du manifeste binaire initial décrit la première construction ; le présent rapport et `display_validation_v39.json` documentent ce contrôle complémentaire.

## Anglais encore visible

Les actions Use / Eat / Give / Drop / Help!, les préambules d'équipement (« Must be equipped on your body. », « Ana/Teddy can equip this weapon. »), « Items for Lloyd. » et certaines indications d'utilisation restent anglais. Ce sont des textes auxiliaires extérieurs aux 22 scripts remplacés. Ils apparaissent avant ou après les descriptions françaises et ne sont pas comptés comme traduits par V39.

## Preuves

- [Accents — objets 1 à 11](accents_display_1.png)
- [Accents — objets 12 à 22](accents_display_2.png)
- [ASCII — objets 1 à 11](ascii_display_1.png)
- [ASCII — objets 12 à 22](ascii_display_2.png)
- [Empreintes des captures, identifiants des objets et résultat](display_validation_v39.json)

Les sorties des deux processus sont sans erreur. Le lanceur réutilisable a aussi été vérifié sur l'inhalateur et le pendentif étoilé dans les deux profils (quatre cas supplémentaires).

## Reproduction

Produire d'abord les états avec `replay.py`, puis :

```sh
python tests/emulation_v39/item_display_probe.py \
  --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' \
  --states-dir '/chemin/sorties_replay_v39' --out '/chemin/controle_objets'
```

`--ids 355B94 3563DD` permet une passe réduite. `inventory_fixture_runner.py` n'autorise l'écriture que d'un seul identifiant valide dans le premier emplacement contenant initialement la carte bancaire. Les ROM, états et captures de travail complets restent locaux ; les quatre planches de preuve sont conservées.

## Régression générale déjà exécutée

Le parcours normal V18 Work a été rejoué dans les deux profils : 339 et 337 commandes, jusqu'à l'image 25 803. Le titre, l'introduction, l'après-combat, la restauration d'état et le menu concordent avec les références. Les seules différences avec V18 sont `battle_step_30` et `battle_step_31`, les bannières VICTOIRE attendues depuis V36.
