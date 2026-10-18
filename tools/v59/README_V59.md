# V59 — sources, stockage et contrôles

61 fragments, 59 zones, 39 contextes. Les IPS autonomes prolongent V58.

```sh
python tools/v59/build_v59.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v59/run_regressions.py
python -m unittest discover -s tools/v59 -p test_v59_offline.py -v
python tools/v59/audit_texts.py --rom /chemin/original.sfc --version 59 --out /chemin/audit.json
```

Les cinq premiers octets deviennent un saut vers une copie privée, qui reprend au premier octet après la zone. Les entrées intérieures restent intactes. La copie de « et » comprend la commande d’objet `1C 05 00` complète après le texte : le validateur examine aussi les commandes finales et refuse les paramètres tronqués. Aucune commande de branchement n’est acceptée dans une zone. Les commandes linéaires complètes sont comparées dans chaque contexte. Aucun auxiliaire grammatical n’est réécrit ou réutilisé par ce lot.

Le stockage utilise `tools/v57/safe_storage.py` : uniquement `328A70–331000`, hors données de sprites, enregistrements antérieurs et cibles explicites. Les empreintes des 464 groupes et 4 177 références d’images restent celles de V58.

```sh
python tests/emulation_v59/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/lectures --profile accents
python tests/emulation_v59/probe.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --states-dir /chemin/etats_v41 --out /chemin/lectures --profile ascii
python tests/emulation_v59/replay.py --rom /chemin/original.sfc --core /chemin/snes9x_libretro.so --out /chemin/parcours
```

Pour chaque entrée, le probe conserve le saut et tout le texte de la copie finale. Il remplace seulement son saut de reprise par un retour temporaire, redirige l’opérande d’action carte bancaire `368B51` et ajoute un wrapper d’appel avec pause à `330FC0` (vérifié nul). Les autres octets restent identiques ; les modifications temporaires figurent dans les résultats. Aucune intervention du testeur sur la WRAM. Les noms de porteur ne sont pas initialisés dans certaines lectures isolées. Ces lectures vérifient le rendu du texte, pas les branches de services ou leurs effets. Les reprises de parcours utilisent les IPS sans modification.

L’audit filtre les fragments encore identiques à la source et accessibles depuis des graines de personnages/actions reconnues. Il exclut les menus, manque certains accès calculés et inclut des modèles hérités et du débogage. Les 312 candidats après V59 ne constituent pas un dénominateur de couverture.
