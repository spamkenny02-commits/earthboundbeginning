# EarthBound Beginnings FR — V18, reprise Work

Cette archive contient une extension locale de la V18 du 14 octobre 2026.
Appliquer **un seul** des deux patchs `EarthBound_Beginnings_FR_v18_work_*.ips`
sur la ROM originale USA 1.2, sans appliquer préalablement V16, V17 ou V18.
Les patchs Work sont autonomes et contiennent toutes les modifications de la
V18 reçue, plus le nouveau lot. Aucun fichier ROM n'est inclus.

## Résultats réellement obtenus dans cette reprise

- 152 nouveaux segments textuels intégrés, dans des dialogues et tutoriels.
- 168 segments ajoutés depuis V17: les 16 de la première V18 et les 152 du lot Work.
- 10 tests exécutés et réussis ici. Les 45 tests anciens cités dans le rapport
  initial ne sont pas inclus dans la sauvegarde reçue et n'ont pas été réexécutés.
- Deux reconstructions IPS vérifiées sur la ROM originale, avec un décodeur
  indépendant pour relire chaque traduction dans la ROM cible.
- Aucun chevauchement avec les enregistrements V18 reçus ni entre nouveaux textes.
- Tous les octets hors des plages textuelles ajoutées sont conservés, y compris
  les commandes, les marqueurs de dialogue et les références littérales relevées.
- Respect des budgets de longueur et des deux encodages.
- Pas de déplacement du texte, pas de changement de pointeur.
- Aucune publication GitHub pendant cette reprise, conformément au travail local demandé.

Les sujets traités comprennent les tutoriels d'équipement et de combat, les
trains, Spookane, Magicant, le stockage des objets et plusieurs dialogues de
personnages. Les 152 éléments sont des **segments**, pas 152 conversations
entièrement traduites. Certains dialogues restent partiellement anglais.

## Limites

Les contrôles sont binaires. Aucun essai en émulateur ni contrôle visuel de
la mise en page n'a été effectué. La carte des accents est héritée de la V18.
La recherche des pointeurs couvre les références HiROM littérales sur quatre
octets, pas les pointeurs indirects, tables compactes ou textes compressés.
Le libellé COMBAT pour la caractéristique FIGHT devra être harmonisé avec les
menus lors de la révision terminologique. Les graphismes anglais restent à traiter.

## Reconstruction

Python 3, bibliothèque standard uniquement; lancer depuis le dossier de cette archive:

```bash
python3 sources/build_work.py '/chemin/vers/la/ROM_originale.sfc'
ROM_PATH='/chemin/vers/la/ROM_originale.sfc' python3 -m unittest discover -s sources -p test_work.py -v
```

Le constructeur refuse une ROM ou un IPS de base dont l'empreinte diffère de
la référence, une traduction trop longue ou une collision.

## Fichiers

- `base/`: les deux IPS V18 reçus, gelés comme entrée du constructeur.
- `sources/build_work.py`, `sources/ips.py`: constructeur autonome et lecteur IPS.
- `sources/translations_work.tsv`: les 152 traductions modifiables.
- `sources/v18_work_candidates.json`: 913 segments candidats issus de la ROM originale
  non couverts par les deux IPS de base. Seuls les 152 choisis ont été intégrés.
- `v18_work_dialogues_fr.json`: textes anglais/français et métadonnées du nouveau lot.
- `validation_work.json`: empreintes et résultats du contrôle réel.
- `v18_dialogues_fr.json`, `RAPPORT_V18.md`: sources et rapport de la V18 reçue.
- `legacy/`: anciens scripts conservés pour historique; leurs chemins `/mnt/data`
  ne conviennent pas à cet environnement. Utiliser `build_work.py` pour cette reprise.

## Suite

Vérifier les tutoriels et dialogues modifiés en jeu, harmoniser les noms et les
caractéristiques, puis traiter les segments restants avec commandes internes.
