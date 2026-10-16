# V46 — audit de préparation et corrections intégrées

La préparation de 100 entrées est conservée dans `v46_selection.json` à titre historique. **Elle ne sert pas d'entrée de traduction au constructeur final** : 98 sources ont déjà été modifiées et les deux autres brouillons sont identiques. Voir `audit_preparation_v46.json`.

Le lot final traduit deux messages de consommation et corrige sept contextes français pour les noms de groupes. Il réutilise la routine française V45, conserve les commandes et les suffixes français déjà raccordés, puis ajoute 17 enregistrements aux IPS V45. Les menus restent exclus.

```sh
python tools/v46/build_v46.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python tools/v46/run_regressions.py
python -m unittest discover -s tools/v46 -p test_v46_offline.py -v
python -m unittest discover -s tools/v46 -p test_v46_prep.py -v
```

`contexts_v46.json` déclare les sept contextes et leurs cinq formulations révisées. `v46_fixtures.json` conserve les sources, les preuves et l'audit. `validation_v46.json` contient les empreintes et les écritures. Le constructeur vérifie l'empreinte de la ROM, les IPS V45, les références et la réserve. Les IPS conservent tous les anciens enregistrements ; seules les plages explicitement déclarées peuvent remplacer leurs octets.

229 tests locaux, dont 22 V46. Les contrôles hors ROM sont répartis entre les workflows V46 et V46-prep. Le [rapport Snes9x](../../tests/emulation_v46/RAPPORT_EMULATION_V46.md) distingue le parcours normal et l'inventaire de fixture. Les scènes tardives et les groupes multiples ne sont pas revendiqués comme testés en situation naturelle.
