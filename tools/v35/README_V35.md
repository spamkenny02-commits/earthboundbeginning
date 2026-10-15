# Outils V35

V35 part de l'IPS autonome V34 et relocalise 31 scripts complets après vérification de leur layout source, de leurs commandes, de leurs appels actifs et des appels issus des copies V31 à V33. Les 32 fragments réellement nouveaux sont déclarés dans `translations_v35.json`; les 109 autres fragments des copies étaient déjà français ou volontairement non linguistiques.

```sh
python tools/v35/build_v35.py --rom '/chemin/EarthBound Beginnings (USA) 1.2(1).sfc' --out patches
ROM_PATH='/chemin/EarthBound Beginnings (USA) 1.2(1).sfc' python -m unittest tools/v35/test_v35.py
```

Appliquer un seul IPS V35, accents ou ASCII, directement à la ROM originale USA 1.2. Ne pas cumuler les versions. Les anciennes copies et les scripts sources restent intacts; seuls les appels prouvés par le parseur sont redirigés.
