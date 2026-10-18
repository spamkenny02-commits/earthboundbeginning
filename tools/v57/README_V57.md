# V57 — textes d'objets

37 zones dans 23 contextes, avec 63 fragments modifiés. Cinq fragments recopiés sans changement ne sont pas comptés comme traductions nouvelles. Ce sont des occurrences, pas 63 dialogues distincts.

```sh
python tools/v57/build_v57.py --rom /chemin/original.sfc
ROM_PATH=/chemin/absolu/original.sfc python tools/v57/run_regressions.py
python -m unittest discover -s tools/v57 -p test_v57_offline.py -v
```

Les copies conservent sorties de variables, séparateurs, pauses et commandes de pile. Les branchements arbitraires sont refusés. Les anciennes entrées intérieures restent intactes. Un seul appel possessif est adapté dans la copie privée : `07E660` devient `251E10`, l'auxiliaire français « son » de V50, dont les octets sont vérifiés. Aucun appel original externe ni auxiliaire partagé n'est réécrit.

## Stockage

Les trous nuls de banque 25 peuvent être des pixels. La V57 finale utilise seulement les trous encore disponibles dans le grand remplissage original `328A70–331000`, en excluant anciens enregistrements IPS, cibles explicites et empreintes des sprites. `safe_storage.py` protège les 464 groupes, leurs en-têtes et 4 177 références d'images. Ces références peuvent partager une même image. Les empreintes finales doivent être identiques à V56 : ce contrôle prouve l'absence de nouvelle altération par rapport à cette base.

Format vérifié dans [CoilSnake, commit épinglé](https://github.com/pk-hack/CoilSnake/blob/346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a/coilsnake/model/eb/sprites.py), `SpriteGroup.from_block` et `EbRegularSprite.block_size`. Ce vérificateur ne nécessite pas CoilSnake.

## Affichage et progression

`tests/emulation_v57/probe.py --mode natural` utilise les opérations normales de la carte bancaire, sans modification de ROM ou WRAM. Le mode `controlled` redirige temporairement ses quatre octets d'adresse d'action pour lire des modèles d'objets. Il ne valide ni leur obtention naturelle ni leurs effets avec des objets appropriés ; certains modèles sont hérités. Les libellés de menus restent pour la suite.

La cible demandée de **85 % du texte n'est pas certifiée**. Le précédent « environ 80 % » était une estimation globale du travail, pas une couverture textuelle mesurée. Voir `progress_v57.json` et `RESTANT_TEXTES.md`.
