# Traduction française v02 et premiers essais

407 entrées intégrées : 317 libellés, 88 blocs de dialogue et deux séquences d’introduction. Cela ajoute 14 dialogues de Podunk à la v01 : radio, trains, téléphone payant, champignon, condiments, plan de la ville et maire. Les commandes et paramètres sont conservés ; aucun pointeur n’est déplacé. La préposition de ciblage devient « À » suivie d’une espace pour éviter « Surthe Haunted Lamp » observé en combat.

Les deux variantes passent les vérifications indépendantes : reconstruction IPS, taille, checksum, plages de modification et 407 traductions. Les 80 glyphes accentués et leurs largeurs sont contrôlés pour la variante accents. Cinq libellés restent exclus faute de place : No, Beam, Sick, Cold, Sing. La ROM d’origine n’est pas modifiée.

## Essais réels

Cœur libretro Snes9x 2010 compilé depuis https://github.com/libretro/snes9x2010, révision `fe690dd321fa5a46b5234a2bde089d2518c62b0e`. Exécution logicielle sans écran, capture des images émises par le cœur (256 × 224 RGB565). Les PNG dans `tests/captures_v02/` sont des captures du jeu exécuté.

- Démarrage et écran titre atteints.
- Nouvelle partie, vitesse, son, fenêtres et saisie des noms : écrans accessibles. Les accents de « Stéréo », « préfère » et « préféré » s’affichent.
- Introduction : défilement, accents, lignes lisibles et passage à la maison observés.
- Menu de la maison : Parler, Objets, PSI, Équiper, Voir, État visibles.
- Premier combat contre la lampe : choix Frapper, désignation de cible, dégâts, victoire, expérience et retour dans la maison observés. Les messages de combat anglais restent à traduire.
- Dialogue de la sœur : « À moi ! » affiché avec son accent.

Les premiers essais ont été effectués par étapes adaptatives avec reprises d’états temporaires. Le parcours automatisé a ensuite été préparé depuis une ROM fraîche jusqu’à la victoire et au retour dans la maison. Les captures livrées et le dialogue de la sœur sont issus de la ROM finale. `tests/rapport_emulation.json` précise les empreintes. `runtime_validated: false` dans les rapports binaires signifie que ces scripts ne certifient pas l’ensemble du jeu ; les essais limités sont documentés ici séparément.

## Reproduire

Compiler séparément le cœur Snes9x 2010 (`make -j4`), installer numpy et Pillow puis :

```sh
python tests/emulateur.py /chemin/snes9x2010_libretro.so build/EarthBound_Beginnings_FR_v02_accents.sfc /tmp/essais --actions tests/parcours_debut.json
```

Le frontend conserve les captures, les actions et l’empreinte de la ROM dans `session.json`. Les états SNES ne sont pas publiés. Aucun cœur d’émulation ni ROM n’est inclus dans le kit.

## À poursuivre

Scénario majoritairement anglais ; noms d’ennemis, PSI et messages de combat incomplets. Les goûts des fenêtres et le clavier des noms contiennent encore des libellés anglais. Téléphone, mère, poupée, mélodie, clé, objets, dépôt, sauvegarde/chargement et défaite ne sont pas encore validés. Vérifier aussi les dialogues à remplissage par espaces et les graphismes anglais. Ces premiers essais ne constituent pas une validation complète du jeu.
