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

Le CSV couvre les champs, les dialogues ordinaires et les routines déplacées déjà préparés. Les textes comprimés en place, les appels du téléphone et l’introduction se modifient encore dans leurs fichiers JSON. Il ne représente pas tous les textes anglais du jeu.

## Construire et contrôler

```sh
python traduction/atelier.py construire "ROM.sfc" --version v09 --sortie build_v09
```

Sous Windows, on peut aussi glisser la ROM source sur `Reconstruire_FR.bat`.

Cette commande vérifie la ROM source, produit les variantes avec et sans accents, puis lance le vérificateur indépendant. Les noms de ROM et de patch portent la version demandée. Le CSV produit dans le dossier de sortie indique les entrées intégrées ou exclues ; consulter également les rapports JSON pour les capacités réelles.

Les commandes, les pointeurs intérieurs, les terminaisons partagées, les glyphes et les checksums sont protégés par l'intégrateur existant. Un libellé court `No` reste exclu de la v09. Un contrôle binaire réussi ne confirme pas l'affichage ni les conditions du scénario.

Pour appliquer uniquement le patch publié sous Windows, glisser la ROM source sur `Appliquer_patch_FR.bat`. La sortie se trouve dans `build/EarthBound_Beginnings_FR.sfc`.

## Vérifier l'outil

Après reconstruction, produire le relevé des entrées exclues et des fragments encore identiques :

```sh
python traduction/atelier.py auditer build_v09/rapport_accents.json --sortie build_v09/audit.json
```

Le rapport porte les empreintes des sources de traduction. Si elles ont changé, l'audit demande une reconstruction avant de donner le statut des entrées. Les fragments identiques nécessitent une relecture : ils peuvent être des noms propres, des symboles ou du texte encore anglais. Le relevé couvre les champs et les dialogues ordinaires déjà préparés, sans prétendre mesurer le pourcentage de traduction de tout le jeu.

Les choix des quatre scènes principales de Podunk et du canari sont désormais `Oui / Non`. Les routines déplacées conservent les anciens blocs ; les alias extérieurs non retargetés peuvent encore atteindre du texte anglais. Un autre libellé `No`, à 0BD867, reste trop court et exclu.

```sh
python tests/verifier_atelier.py
python tests/verifier_encodage_fr.py
python tests/verifier_appels_telephone.py
```

Le test CSV vérifie aussi qu'une erreur en fin de fichier n'écrit pas les modifications précédentes et qu'un aller-retour sans changement laisse les sources identiques.


## Éditeur local

Ouvrir `atelier_fr.html` dans un navigateur, puis charger `traductions.csv`. Chercher un mot ou une adresse, modifier le français et enregistrer le CSV. Les identifiants et les textes anglais restent conservés. L'éditeur refuse les commandes et signale les suffixes PSI modifiés. Son aperçu est une vue de lecture, sans prétendre reproduire la police ou le déroulement du jeu.

Sous Windows, glisser le CSV sur `Importer_CSV_FR.bat`, puis la ROM originale sur `Reconstruire_FR.bat`. L'import enregistre les anciennes sources dans `sauvegardes_import/import_...` avant les modifications. En cas de besoin, restaurer ces JSON dans `traduction/`. Aucun envoi réseau n'est effectué par l'éditeur HTML.

Pour visualiser le reste du travail, charger `catalogue.json` dans l'éditeur. Ces candidats ne s'importent pas comme des traductions : vérifier leurs commandes et leur usage avant de les préparer.

```sh
python traduction/atelier.py cataloguer build_v09/rapport_accents.json --sortie build_v09/couverture
```

Le catalogue distingue les textes préparés et intégrés des candidats restant à examiner. Il corrige l'entrée du dialogue de récompense du maire, sans considérer tous les candidats comme utilisés en jeu.

Les événements et formats de l'éditeur sont vérifiés par `node tests/verifier_editeur.cjs build_v09` avec un DOM simulé. Le rendu dans un vrai navigateur reste à vérifier : le moteur de navigateur n'est pas disponible dans l'environnement de développement.
