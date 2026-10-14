# EarthBound Beginnings FR — Préparation V17 (archive historique)

Ce rapport décrit la préparation avant publication de V17. La version courante est V21; voir `README.md` et `RAPPORT_V21.md`. Les états ci-dessous sont historiques.

## Point de départ vérifié

La branche `main` contient la **V16**, avec ses deux IPS autonomes et 128 segments supplémentaires publiés (63 scripts modifiés). La V16 demeure la dernière livraison intégrable ; **aucun IPS V17 n'est annoncé**.

## Avancement de cette passe

- Préparation d'un outil de présélection de scripts du catalogue V09. Il exige la **ROM personnelle USA 1.2** (SHA-256 contrôlé) et les **deux IPS V16**.
- Reconstitution des octets source des scripts, y compris commandes `[XX]`, marqueurs `@` et retours de ligne `00` ou `03 00`. Rejet des layouts ambigus ou non conformes.
- Vérification des pointeurs HiROM littéraux déclarés, recherche de pointeurs vers l'intérieur des segments, contrôle des collisions avec **les deux profils** de la V16 et entre candidats.
- Sortie de manifestes **anglais inchangés**, destinés à une traduction et à une revalidation ultérieures. Les commandes, offsets et IPS précédents ne sont pas modifiés.
- Présélection statique séparée de **150 scripts du catalogue** pour organiser la relecture. Cette liste n'est pas une preuve d'intégrabilité et ne compte pas comme traduction.

## Tests et limites

- **10 tests synthétiques locaux réussis** : IPS ordinaire/RLE, commandes, deux formes de retours de ligne, contrôle des pointeurs, détection des pointeurs intérieurs, collisions accents/ASCII, rejets des sources non conformes.
- **Non effectués** : exécution sur la ROM source commerciale (absente de l'environnement), génération ou roundtrip d'un IPS V17, test de pointeurs indirects, gameplay en émulateur.
- La CI GitHub est configurée pour refaire les tests synthétiques et la non-régression IPS V15/V16 ; son résultat doit être vérifié séparément après publication.

**Bilan V17 : 0 bloc français intégré, 0 patch V17 publié.** Les 150 candidats sont uniquement des pistes de travail.

## Exécution locale (ROM non distribuée)

```bash
python traduction/preparer_v17.py "EarthBound Beginnings (USA) 1.2.sfc" \
  --limite 120 --sortie build_v17/candidats.json --rapport build_v17/audit.json
python tests/verifier_preparation_v17.py
```

Les sorties `build_v17/` sont locales. L'outil refuse une ROM dont le SHA-256 ne correspond pas. Les candidats devront ensuite être traduits, vérifiés contre les deux IPS, contrôlés pour les limites d'affichage et validés sous émulateur avant de publier une V17 jouable.

## Audit source ultérieur conservé depuis main

La ROM originale USA 1.2 a ensuite été vérifiée localement (SHA-256 conforme). Sur 2 392 scripts extraits, 1 627 passaient les contrôles de source et de pointeurs littéraux. Parmi les 500 premiers candidats, 259 ne chevauchaient aucun enregistrement des deux IPS V16. Un sous-lot de 120 scripts anglais avait été préparé pour traduction. Dix tests synthétiques avaient réussi localement et sur GitHub Actions.
