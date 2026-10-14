# EarthBound Beginnings FR — Préparation V18 (14 octobre 2026)

**Base : V17 autonome publiée.** Aucune traduction V18 n'est intégrée dans ce rapport.

Le catalogue `traduction/v17_priorites_non_verifiees.json` contient 150 scripts préselectionnés. Un filtrage conservateur sur les véritables enregistrements IPS V17 (accents et ASCII) donne :

- 15 scripts déjà intégrés en V17 : exclus.
- 40 scripts dont la plage anglaise majorée croise une modification V17 : exclus par prudence, **sans conclure à une collision réelle**.
- **95 scripts candidats** sans collision dans cette approximation, consignés dans `traduction/v18_preselection.json`.

Ces 95 scripts sont uniquement une **préselection** : leurs octets source, limites, références HiROM, pointeurs intérieurs, commandes et longueur de traduction doivent encore être vérifiés sur la ROM USA 1.2 avant toute intégration. Aucun dialogue V18 n'est compté comme traduit ou publié. Les textes compressés et les graphismes anglais ne sont pas validés.

La V17 est disponible dans `patches/` et son contrôle GitHub Actions sans ROM a réussi (run 38532650694). Pour V18 : auditer les 95 candidats sur ROM, compléter la sélection avec le catalogue restant si nécessaire, traduire des lots cohérents, puis reconstruire deux IPS autonomes V18 et contrôler les régressions V17.
