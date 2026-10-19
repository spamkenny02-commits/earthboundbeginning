# V71 — coursier de dépôt Escargo

```sh
python tools/v71/build_v71.py --rom /chemin/original.sfc
EARTHBOUND_ROM=/chemin/original.sfc python -m unittest discover -s tools/v71 -v
python tools/v71/verify_display.py
python tests/emulation_v71/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v71 --profile accents
python tests/emulation_v71/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v33 --out /chemin/prive/v70 --profile accents --version 70
```

Répéter les probes pour ASCII, puis importer les captures et rapports partageables :

```sh
python tools/v71/collect_evidence.py --current /chemin/prive/v71 --reference /chemin/prive/v70 --sheets /chemin/prive/relecture
```

Six scénarios : dépôt de trois objets distincts, confirmation du dépôt d'une Fiole, paiement refusé, absence d'argent, carte bancaire protégée et confirmation refusée pour reprendre la sélection. Seul le dépôt de trois objets comprend un inventaire final vérifié. Les autres s'arrêtent au dialogue utile ou au retour au menu : ne pas leur attribuer de validation d'inventaire.

Les états attendus sont les états V33 `{accents,ascii}/after_combat.state` (Ninten seul chez lui, carte bancaire, 20 $). Le wrapper privé accorde trois objets avec `1D 00` et dépense 20 $ avec `1D 09` seulement dans le cas sans argent. Il appelle le téléphone complet `35C597`. La sélection Maman puis Déposer se fait à la manette ; une attente de 600 images laisse le coursier arriver par le mécanisme du jeu. Aucune entrée de coursier n'est appelée artificiellement, aucune écriture directe en WRAM.

La longueur décompressée et les retours à la ligne peuvent faire varier la fin des dialogues entre anglais et français. Les premiers essais de fermeture supplémentaire A/B et d'attente avant inventaire n'ont pas établi une navigation fiable pour tous les cas : ils restent privés et ne sont pas des preuves publiées. Le probe retenu s'arrête aux écrans utiles et n'ouvre l'inventaire final que pour le dépôt de trois objets, où les deux versions suivent correctement la même séquence.

Les seules écritures temporaires sont le pointeur à `368B51` et le wrapper à `330FC0`, vérifiées par empreinte. Le patch public ne contient aucune préparation. Utiliser des sorties privées distinctes pour les explorations ; `--case` remplace le rapport de sortie par ce seul cas. ROM, cœur, états, historiques bruts et dumps mémoire restent privés.

Le reconstructeur ajoute 32 plages de même taille à V70 et vérifie leur anglais décompressé, les frontières textuelles, les commandes, les sprites et la banque 25. Les tests privés sont explicitement ignorés sans ROM. Le test RGB vérifie aussi les empreintes des captures avant/après et exclut toute différence hors de la fenêtre de dialogue.
