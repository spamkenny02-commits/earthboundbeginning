# V39 — descriptions d'objets

Base : V38 (`783d0f6`). V39 traduit 22 descriptions encore intégralement anglaises : armes, protections, tickets et objets de soin. Les copies contiennent 32 fragments nouvellement traduits ; les délimiteurs et marqueurs dynamiques ne sont pas comptés.

Les références sont vérifiées dans le champ description (offset 35, enregistrements de 39 octets) de la table d'objets `155000`, ainsi que dans les commandes d'affichage `1F C0 01` reconnues par le parseur. Les 22 références de chaque type sont raccordées aux copies. Les scripts sources sont conservés.

Les réserves, les pointeurs, les commandes, les profils, les enregistrements IPS précédents et les différences exhaustives sont contrôlés à chaque construction. Le SHA-256 de la ROM originale et ceux des IPS V38 doivent correspondre.

```sh
python tools/v39/build_v39.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python -m unittest tools/v39/test_v39.py tools/v39/test_v39_offline.py -v
```

Traductions : `translations_v39.json`. Sources et références : `v39_descriptions_fr.json`. Empreintes et implantations : `validation_v39.json`.

Un contrôle complémentaire affiche les 22 descriptions dans chaque profil via le menu normal Objets → Help!, avec un inventaire temporaire en WRAM. Textes, glyphes et pagination sont relus ; l'acquisition naturelle et l'usage en combat ne sont pas couverts. Voir `tests/emulation_v39/RAPPORT_EMULATION_V39.md` et ses quatre planches de preuve.
