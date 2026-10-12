# Atelier de traduction

Python 3 suffit pour exporter, importer et construire les patchs. Pour les essais en jeu, un émulateur reste nécessaire.

## Modifier les textes

Depuis la racine du projet :

```sh
python traduction/atelier.py exporter traductions.csv
python traduction/atelier.py importer traductions.csv
python traduction/atelier.py importer traductions.csv --appliquer
```

Le CSV utilise UTF-8 avec BOM et le séparateur point-virgule. Modifier seulement la colonne `francais`. Garder les identifiants comme du texte dans Excel, ainsi que les espaces, les marqueurs `@` et les suffixes PSI `[8B]`, etc. Un import peut contenir seulement les lignes modifiées. Sans `--appliquer`, aucune source n'est écrite.

L'import refuse les identifiants inconnus ou dupliqués, les originaux modifiés, les caractères impossibles à encoder, les commandes injectées et les suffixes PSI modifiés. Toutes les lignes sont validées avant la première écriture. Un champ trop long peut être accepté dans les sources : la reconstruction décide ensuite s'il peut être intégré sans danger.

Le CSV couvre les champs et les dialogues ordinaires déjà préparés. Les textes comprimés, les routines déplacées, les appels du téléphone et l'introduction se modifient encore dans leurs fichiers JSON. Il ne représente pas tous les textes anglais du jeu.

## Construire et contrôler

```sh
python traduction/atelier.py construire "ROM.sfc" --version v07 --sortie build_v07
```

Sous Windows, on peut aussi glisser la ROM source sur `Reconstruire_FR.bat`.

Cette commande vérifie la ROM source, produit les variantes avec et sans accents, puis lance le vérificateur indépendant. Les noms de ROM et de patch portent la version demandée. Le CSV produit dans le dossier de sortie indique les entrées intégrées ou exclues ; consulter également les rapports JSON pour les capacités réelles.

Les commandes, les pointeurs intérieurs, les terminaisons partagées, les glyphes et les checksums sont protégés par l'intégrateur existant. Les six propositions exclues de la v07 restent anglaises. Un contrôle binaire réussi ne confirme pas l'affichage ni les conditions du scénario.

Pour appliquer uniquement le patch publié sous Windows, glisser la ROM source sur `Appliquer_patch_FR.bat`. La sortie se trouve dans `build/EarthBound_Beginnings_FR.sfc`.

## Vérifier l'outil

```sh
python tests/verifier_atelier.py
python tests/verifier_encodage_fr.py
python tests/verifier_appels_telephone.py
```

Le test CSV vérifie aussi qu'une erreur en fin de fichier n'écrit pas les modifications précédentes et qu'un aller-retour sans changement laisse les sources identiques.
