# V27 — reconstruction et tests

Depuis la racine du dépôt :

```sh
python3 tools/v27/audit_v27.py --rom '/chemin/ROM_originale.sfc' --out build_v27/audit.json
python3 tools/v27/build_v27.py --rom '/chemin/ROM_originale.sfc' --out build_v27
ROM_PATH='/chemin/ROM_originale.sfc' python3 -m unittest discover -s tools/v27 -p test_v27.py -v
python3 -m unittest discover -s tools/v27 -p test_v27_offline.py -v
```

ROM originale USA 1.2 sans en-tête requise. Les IPS V27 sont autonomes : appliquer un seul patch directement sur l'original, jamais par-dessus V26. Aucun fichier ROM n'est distribué.

**Statut de vérification au moment de la publication :** 176 plages et 124 scripts vérifiés contre la ROM originale, 181 références littérales concordantes, IPS structurés et régression synthétique vérifiés dans les deux profils. Le roundtrip intégral V27 sur ROM et le parcours en émulateur restent à exécuter. Voir `RAPPORT_V27.md`.
