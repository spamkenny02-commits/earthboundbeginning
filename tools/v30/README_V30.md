# V30 — audit conservateur des textes encore anglais

La V29 est la dernière version intégrée. Cet outil prépare une **liste de candidats**, pas une V30 jouable. Il ne modifie ni ROM, ni IPS, ni pointeur. Aucune traduction n'est comptabilisée avant construction et tests des deux IPS autonomes.

Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s tools/v30 -p 'test_v30_offline.py' -v
python3 tools/v30/audit_v30.py --rom '/chemin/EarthBound Beginnings (USA) 1.2.sfc' --out /tmp/v30_candidates.json --limit 200
```

L'audit vérifie le SHA-256 de la ROM originale (4 Mio), les SHA-256 des deux IPS V29 publiés, les scripts du catalogue, les commandes hors textes, les références HiROM littérales, les modifications des deux profils et les collisions avec **tous** les enregistrements IPS antérieurs. Les textes dont une référence pointe directement à l'intérieur (y compris au premier octet) sont différés par prudence. Les fragments de moins de huit caractères sont également différés.

**Limites :** les pointeurs indirects, les textes compressés et les graphismes anglais nécessitent des extracteurs spécifiques. Un candidat issu de cet audit n'est pas une traduction validée : il doit être relu en contexte, traduit, encodé, intégré puis testé sur ROM et en émulateur. Les tests synthétiques hors ROM ne démontrent pas la validité d'un dialogue du jeu.

Le fichier de sortie contient `integrated_blocks: 0`, les motifs d'exclusion et les candidats classés par adresse. Ne jamais le publier comme patch, ni publier la ROM commerciale.
