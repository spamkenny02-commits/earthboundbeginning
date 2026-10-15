# Outils V38 — descriptions d'ennemis

V38 relocalise et traduit les **114 descriptions non vides** de la banque active `361DB7–3631F2`. Elles représentent 126 fragments de texte. Les seize petits scripts de redirection vides restent inchangés et ne sont pas comptés comme traductions.

Le constructeur vérifie chaque entrée de la table `3633EA–3635F2`. Il réécrit aussi dix-sept alias, uniquement lorsque le parseur prouve que l'adresse est l'opérande d'un saut fermé. Les sources anglaises, les commandes et les corrections précédentes restent intactes.

Les copies occupent dix sous-réserves nulles et non référencées entre `328A80` et `32A450`. Le découpage évite toutes les cibles HiROM détectées dans la grande plage nulle environnante.

```bash
python3 tools/v38/build_v38.py \
  --rom '/chemin/EarthBound Beginnings (USA) 1.2(1).sfc' \
  --out patches

ROM_PATH='/chemin/original.sfc' \
  python3 -m unittest tools/v38/test_v38.py tools/v38/test_v38_offline.py -v
```

Le manifeste [`validation_v38.json`](validation_v38.json) contient les empreintes, les implantations et les 131 références réécrites. Les traductions éditables sont dans [`translations_v38.json`](translations_v38.json); [`v38_descriptions_fr.json`](v38_descriptions_fr.json) fixe les scripts et leurs octets sources.
