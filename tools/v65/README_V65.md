# V65 — confirmations de stockage et cycles de services

V65 prolonge V64. Deux confirmations affichaient encore « The Fiole de sérum » : dépôt et récupération. Un auxiliaire privé conserve les commandes de classification et les cinq branches de l'auxiliaire original, mais chaque branche rejoint le retour vide existant. Le nom de l'objet est donc affiché sans article anglais. L'auxiliaire partagé reste inchangé.

La phrase de dépôt devient « Cet objet sera bien au chaud. », indépendante du genre du nom. Les deux contextes sont `34B517` et l'ancienne copie `259AF0`.

## Protection des données et relocalisation

La copie historique de récupération chevauche des empreintes de sprites en banque 25. V65 n'écrit aucun nouvel octet dans cette banque. Les sept scripts de banque 25 atteints depuis le service `34B490` sont copiés dans le remplissage protégé `328A70–331000`, hors enregistrements IPS antérieurs, cibles explicites et empreintes des 464 groupes/4 177 références d'images.

Les 338 octets sources sont répartis dans neuf blocs. Les coupures conservent les commandes complètes et les mots entiers ; deux sauts relient les morceaux des scripts les plus longs. Six opérandes sûrs rejoignent les nouvelles copies ou l'auxiliaire privé. Après reconstruction des blocs et normalisation des seuls pointeurs déclarés, tous les scripts conservent exactement leurs commandes ; les sept copies conservent aussi tous leurs octets non pointeurs. L'auxiliaire privé de 27 octets porte l'allocation totale à 375 octets. Les empreintes de sprites restent celles de V64.

Le dernier créneau de 64 octets, `330FC0–331000`, reste réservé aux probes privés. Les IPS V65 n'y écrivent rien.

## Reproduction

```sh
python tools/v65/build_v65.py --rom SOURCE.sfc
ROM_PATH=/chemin/absolu/SOURCE.sfc python tools/v62/run_regressions.py
python -m unittest discover -s tools/v63 -p 'test*.py' -q
ROM_PATH=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v64 -p 'test*.py' -q
ROM_PATH=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v65 -p test_v65.py -v
python -m unittest discover -s tools/v65 -p test_v65_offline.py -v
python tools/v65/verify_display.py
```

Le dernier outil utilise Pillow et recalcule les 84 empreintes RGB ainsi que les 40 différences V64/V65, toutes limitées à la fenêtre de texte.

```sh
python tests/emulation_v65/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile accents
python tests/emulation_v65/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V41 --out SORTIE --profile ascii
```

`--version 64 --case buy_store_retrieve` rejoue la référence. Utiliser une sortie distincte. Les trois scénarios sont des entrées contrôlées : une redirection temporaire à `368B51` et une suite de commandes `08 pointeur` suivie de `02` à `330FC0`. Ce wrapper appelle les scripts complets des services. Les choix et transferts suivants utilisent uniquement la manette et le moteur ; aucune écriture directe en WRAM ni callback assembleur. Le probe vérifie que les autres octets sont ceux du patch testé. Ces essais ne prouvent pas l'accès naturel aux lieux sur la carte.

## Piste du soigneur classée

Dans `24D4E0–24D4EC`, les octets sont `03 00 18 0A 1C 04 10 1E 1A 15 0D 00`. Le découpage est `03`, `00`, `18 0A`, `1C 04`, `10 1E`, `1A 15`, `0D 00`. Le décodage brut lisait à tort `15 0D` comme une entrée du dictionnaire « you have », alors que ces deux octets appartiennent à deux commandes différentes. Ils ne sont dans aucun fragment textuel. La branche de refus du soigneur est relue en émulateur ; aucun texte de ce contexte n'est modifié par V65.
