# Outils V37 — graphisme de coup critique

V37 remplace **« SMAAAASH!! »** par **« COUP CRIT! »** dans le bloc compressé de fenêtres déjà relocalisé par V36. V37 ne révise aucun script et ne compte aucun dialogue ancien comme nouveau.

Le constructeur part des IPS autonomes V36, prouve que leur unique enregistrement dans `177800–177FD0` est le bloc graphique attendu, puis remplace ses vingt tuiles dédiées. Les 6 656 octets bruts sont recompressés en 1 717 octets. L'IPS V37 ajoute un seul enregistrement contrôlé à `177800`; le pointeur V36 vers `D77800` reste inchangé.

```bash
python tools/v37/build_v37.py \
  --rom '/chemin/EarthBound Beginnings (USA) 1.2(1).sfc' \
  --coilsnake /chemin/CoilSnake \
  --out patches

ROM_PATH='/chemin/original.sfc' COILSNAKE_PATH=/chemin/CoilSnake \
  python -m unittest tools/v37/test_v37.py tools/v37/test_v37_offline.py -v
```

Le manifeste [`validation_v37.json`](validation_v37.json) fixe les empreintes, la liste exacte des vingt tuiles et les ROM cibles. L'aperçu [`v37_preview.png`](v37_preview.png) est produit depuis le même bloc que les IPS.

La traduction `HP` → `PV` a été testée puis exclue : les tuiles 8, 9, 24 et 25 sont partagées par d'autres éléments d'interface, ce que le replay Snes9x a révélé. Le rapport d'émulation documente aussi la recherche, non concluante, d'un coup critique naturel.
