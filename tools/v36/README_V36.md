# Outils V36 — bannière de victoire compressée

V36 remplace le graphisme anglais **« YOU WON! »** par **« VICTOIRE »** dans le premier bloc graphique de fenêtres. Aucun fragment de dialogue n'est compté dans ce lot : les 32 blocs de `textes_comprimes_fr.json` et les 9 blocs relocalisés de `textes_relocalises_fr.json` ont été relus comme travail antérieur déjà intégré et sont seulement préservés.

Le constructeur exige la ROM USA 1.2 épinglée et l'arborescence CoilSnake au commit `346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a`. Il décompresse les 416 tuiles 2 bpp, remplace les 16 tuiles réservées aux huit glyphes de la bannière, recompresse le bloc et le relocalise dans `177800–177F6F`. Le pointeur assembleur à `047C47` est contrôlé avant sa réécriture vers l'adresse HiROM `D77800`.

```bash
python tools/v36/build_v36.py \
  --rom '/chemin/EarthBound Beginnings (USA) 1.2(1).sfc' \
  --coilsnake /chemin/CoilSnake \
  --out patches

ROM_PATH='/chemin/original.sfc' COILSNAKE_PATH=/chemin/CoilSnake \
  python -m unittest tools/v36/test_v36.py tools/v36/test_v36_offline.py -v
```

Le manifeste [`validation_v36.json`](validation_v36.json) fixe les empreintes du bloc compressé, des IPS et des ROM cibles. Le test hors ROM vérifie les trois enregistrements ajoutés à chaque IPS ; le test complet couvre la réserve nulle, les collisions, les cibles HiROM, la structure du pointeur, la décompression, l'application IPS indépendante, la différence exhaustive et les régressions boy/girl.

L'aperçu [`victoire_preview.png`](victoire_preview.png) est reconstruit à partir du même bloc binaire que les IPS. Le rendu réel du combat est documenté dans [`tests/emulation_v36`](../../tests/emulation_v36/RAPPORT_EMULATION_V36.md).
