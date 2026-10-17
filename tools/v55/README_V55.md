# V55 — destinations des transports

16 définitions individuelles de destination et deux fragments de dialogue. Chaque définition rejoint une copie française, puis revient avant le sélecteur d'origine. Les noms de ville, tarifs, choix et anciennes entrées intérieures sont conservés. Trois destinations Youngtown sont conditionnelles.

L'avance de chaque ligne est de 128 pixels, calculée avec la table de largeurs de la police 0 et une avance supplémentaire d'un pixel par glyphe. Aucun changement de police partagée.

Appliquer un seul IPS à la ROM originale USA 1.2. Reconstruction :

```sh
python tools/v55/build_v55.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v55/run_regressions.py
python -m unittest discover -s tools/v55 -p test_v55_offline.py -v
```

Le script d'affichage utilise une redirection temporaire de l'objet carte bancaire vers les quatre contextes. Pour trois cas Youngtown, il force uniquement le saut conditionnel dans la ROM temporaire. Aucun état WRAM n'est modifié ; le patch publié conserve les conditions d'origine. Ces essais s'arrêtent à la confirmation du tarif et ne valident pas le voyage.
