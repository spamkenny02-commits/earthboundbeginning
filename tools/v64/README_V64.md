# V64 — services et anciennes entrées du distributeur

V64 prolonge les IPS V61 (V62/V63 sont des audits sans patch). Quatre fragments sont remplacés à taille fixe : l'invitation à insérer la carte, la consigne de dépôt et deux libellés de solde. Les paramètres, commandes, pointeurs et sprites sont inchangés ; aucune allocation.

Le distributeur utilise les anciennes racines `0680A6` et `0680C2`, exclues par le filtre de graines V62. Dix-sept lignes NPC pointent vers cette paire. `audit_bank.py` suit 20 scripts et 30 références depuis ces deux champs, sans blocage ; cela ne couvre pas tous les appels calculés/assembleur du jeu. Le retrait/dépôt était en majorité déjà français : seules les quatre plages inventoriées sont corrigées.

```sh
python tools/v64/build_v64.py --rom SOURCE.sfc
ROM_PATH=/chemin/absolu/SOURCE.sfc python tools/v62/run_regressions.py
python -m unittest discover -s tools/v63 -p 'test*.py' -v
ROM_PATH=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v64 -p test_v64.py -v
python -m unittest discover -s tools/v64 -p test_v64_offline.py -v
python tools/v64/verify_display.py
```

La dernière commande utilise Pillow, vérifie les empreintes RGB des 122 captures et recalcule les 22 comparaisons avec V61.

## Essais privés

```sh
python tests/emulation_v64/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile accents
python tests/emulation_v64/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile ascii
python tools/v64/audit_bank.py --rom SOURCE.sfc --profile accents --out AUDIT.json
```

L'entrée de service est forcée par une seule modification temporaire de l'opérande `368B51` de l'action carte bancaire. Aucun autre octet de la ROM V64 n'est changé pour le probe ; aucune écriture directe en WRAM, aucun callback ou wrapper ajouté. Une fois le script lancé, les branches utilisent les touches et les routines réelles du moteur.

Les treize cas comprennent onze entrées de service complet et deux entrées isolées : invitation de carte sans tester la condition d'absence de carte, et consigne de retrait sans tester un compte positif. Les scripts complets couvrent compte nul, dépôt de 1 $, dépôt trop élevé, annulations, Papa/sauvegarde, début d'appel Maman, achat, manque d'argent, refus de stocker la carte et stock vide. Les conversations ne sont pas toutes déroulées jusqu'au raccrochage. Le retour au jeu entre deux visites de distributeur n'a pas permis de valider ici un retrait positif : il reste à établir, et ne figure pas parmi les cas validés.

`--case` rejoue un cas, `--version 61` permet sa référence antérieure. Utiliser des sorties séparées pour conserver chaque rapport. Le runner historique accepte désormais `--history-every N` pour limiter les réécritures du journal privé pendant l'échantillonnage ; par défaut N=1, comportement antérieur conservé. V64 utilise 120, avec écriture immédiate aux captures, sauvegardes et à la sortie. Les commandes, frames et réponses restent toutes dans le journal final.

Ne pas publier ROM, cœur, états ou dumps. Les entrées forcées vérifient les réponses et leur affichage, pas l'accès naturel à un commerçant ou à un téléphone sur la carte. Les racines NPC et les traces sont des preuves distinctes.
