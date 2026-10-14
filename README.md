# EarthBound Beginnings SNES — traduction française

## Version actuelle : V24 (traduction partielle)

V24 élargit l'audit au catalogue complet et ajoute **188 plages de texte dans 99 scripts**, dont des fragments après commandes dynamiques. Les ajouts V19–V24 représentent **925 plages depuis V18 Work**.

- [Patch V24 avec accents](patches/EarthBound_Beginnings_FR_v24_accents.ips)
- [Patch V24 ASCII](patches/EarthBound_Beginnings_FR_v24_ascii.ips)
- [Rapport V24 et limites](RAPPORT_V24.md)
- [Traductions éditables](tools/v24/translations_v24.tsv)
- [Audit, constructeur et tests](tools/v24/README_V24.md)
- [Essais Snes9x](tests/emulation_v24/RAPPORT_EMULATION_V24.md)

Appliquer **un seul IPS V24 directement à la ROM originale USA 1.2**. 22 tests V23–V24 réussis; parcours Snes9x du début du jeu conforme dans les deux profils. Les nouvelles plages dans leurs scènes restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V23


V23 ajoute **120 nouveaux segments** à V22: hôtels, commerces, soins, banque, canari et indices du journal. Les ajouts V19–V23 représentent **737 segments depuis V18 Work**.

- [Patch V23 avec accents](patches/EarthBound_Beginnings_FR_v23_accents.ips)
- [Patch V23 ASCII](patches/EarthBound_Beginnings_FR_v23_ascii.ips)
- [Rapport V23 et limites](RAPPORT_V23.md)
- [Traductions éditables](tools/v23/translations_v23.tsv)
- [Constructeur et tests](tools/v23/README_V23.md)
- [Essais Snes9x](tests/emulation_v23/RAPPORT_EMULATION_V23.md)

Appliquer **un seul IPS V23 directement à la ROM originale USA 1.2**. 20 tests V22–V23 réussis; parcours Snes9x du début du jeu conforme dans les deux profils. Les nouveaux segments dans leurs zones restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V22


V22 ajoute **185 nouveaux segments** à V21: dialogues de fin de jeu, commerces, Snowman, Youngtown et désert Yucca. Les ajouts V19–V22 représentent **617 segments depuis V18 Work**.

- [Patch V22 avec accents](patches/EarthBound_Beginnings_FR_v22_accents.ips)
- [Patch V22 ASCII](patches/EarthBound_Beginnings_FR_v22_ascii.ips)
- [Rapport V22 et limites](RAPPORT_V22.md)
- [Traductions éditables](tools/v22/translations_v22.tsv)
- [Constructeur et tests](tools/v22/README_V22.md)
- [Essais Snes9x et outil de rejeu](tests/emulation_v22/RAPPORT_EMULATION_V22.md)

Appliquer **un seul IPS V22 directement à la ROM originale USA 1.2**. 20 tests V21–V22 réussis; essais Snes9x du début du jeu réussis dans les deux profils. Les nouveaux segments dans leurs zones restent à vérifier en jeu. Aucun fichier ROM distribué.

## Version précédente : V21 Work


V21 ajoute **153 nouveaux segments** à V20 et conserve les **119 ajouts V19** et les **160 ajouts V20**: **432 ajouts depuis V18 Work**.

- [Patch V21 avec accents](patches/EarthBound_Beginnings_FR_v21_accents.ips)
- [Patch V21 ASCII](patches/EarthBound_Beginnings_FR_v21_ascii.ips)
- [Rapport V21 et limites](RAPPORT_V21.md)
- [Traductions éditables](tools/v21/translations_v21.tsv)
- [Constructeur et tests](tools/v21/README_V21.md)
- [Essais Snes9x](tests/emulation_v21/RAPPORT_EMULATION_V21.md)

Appliquer **un seul IPS V21 à la ROM originale USA 1.2**, sans préinstaller les anciennes versions. 45 tests V18–V21 réussis; essais Snes9x du début du jeu réussis dans les deux profils. Les nouveaux dialogues dans les zones ultérieures restent à vérifier en jeu. Aucune ROM distribuée.

## Version précédente : V18 Work


La V18 Work autonome reprend la V17 publiée et ajoute **168 segments** : 16 dans le premier lot V18, puis 152 dans la reprise Work. Les 70 segments de `traduction/v18_brouillons_01.json` sont un lot distinct non intégré et ne sont pas ajoutés à ce compteur.

- [Patch V18 Work avec accents](patches/EarthBound_Beginnings_FR_v18_work_accents.ips)
- [Patch V18 Work sans accents](patches/EarthBound_Beginnings_FR_v18_work_ascii.ips)
- [Rapport et instructions](tools/v18_work/README_WORK.md)
- [Constructeur portable](tools/v18_work/sources/build_work.py), [tests](tools/v18_work/sources/test_work.py), [résultats binaires](tools/v18_work/validation_work.json)
- [16 premières traductions](tools/v18_work/v18_dialogues_fr.json), [152 traductions Work](tools/v18_work/v18_work_dialogues_fr.json)

**Appliquer un seul IPS V18 Work directement à la ROM originale USA 1.2**, sans préinstaller V17 ou V18. Aucune ROM n'est distribuée.

Contrôles exécutés : reconstruction des deux variantes, décodage indépendant des 152 nouveaux textes, absence de collisions, conservation de la base et de tous les octets hors du nouveau lot, **10 tests réussis**. **Premiers essais Snes9x réussis dans les deux variantes** : nouveau jeu, introduction, exploration, premier combat remporté et restauration d'état. [Rapport et limites de couverture](tests/emulation_v18_work/RAPPORT_EMULATION_V18.md). La sauvegarde native et les 168 nouveaux segments dans leurs zones restent à tester; il s'agit d'une version de développement.

```sh
python3 tools/v18_work/sources/build_work.py "/chemin/ROM_originale.sfc"
ROM_PATH="/chemin/ROM_originale.sfc" python3 -m unittest discover -s tools/v18_work/sources -p test_work.py -v
```

## Version précédente : V17 (traduction partielle)

La **V17 autonome** reprend toutes les modifications V09–V16 et ajoute **195 segments français réellement modifiés dans 117 scripts**. Les trois scripts exclus du lot de 120 ne sont pas comptés. Depuis V09, les versions V10–V17 ajoutent **766 segments/blocs** cumulés (50 + 27 + 18 + 141 + 130 + 77 + 128 + 195).

- [Patch V17 avec accents](patches/EarthBound_Beginnings_FR_v17_accents.ips)
- [Patch V17 sans accents](patches/EarthBound_Beginnings_FR_v17_ascii.ips)
- [Rapport V17](RAPPORT_V17.md), [traductions](traduction/v17_traductions_117.json), [constructeur](traduction/construire_v17.py), [tests](tests/verifier_fusion_v17.py)
- [CI V17](https://github.com/spamkenny02-commits/earthboundbeginning/actions/workflows/verifier-v17.yml)

**Appliquer uniquement V17 directement à la ROM originale USA 1.2**, sans préinstaller V09 à V16.

```sh
python traduction/construire_v17.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v17
```

**Contrôles :** 117 scripts, 130 références HiROM vers leurs débuts, 195 remplacements, zéro collision avec les enregistrements IPS V16 dans les deux profils. Les contrôles binaires ne remplacent pas un parcours sous émulateur ; le jeu reste partiellement traduit.



## Archives de préparation V17

La [présélection historique](traduction/v17_priorites_non_verifiees.json), l'[outil de préparation](traduction/preparer_v17.py), les [tests synthétiques](tests/verifier_preparation_v17.py), leur CI et le [rapport archivé](RAPPORT_V17_PREPARATION.md) sont conservés. Cette préparation est antérieure aux IPS V17 publiés et à la V21 actuelle.

## Versions précédentes

Les rapports [V16](RAPPORT_V16.md), [V15](RAPPORT_V15.md), [V14](RAPPORT_V14.md), [V13](RAPPORT_V13.md), [V12](RAPPORT_V12.md), [V11](RAPPORT_V11.md) et [V10](RAPPORT_V10_ADDON.md) restent disponibles. Les anciens patchs sont archivés dans `patches/`.

## Historique V09 et atelier


Historique de l'intégration expérimentale v09 : **1 095 entrées intégrées et contrôlées**, introduction et 16 caractères accentués. Les quatre scènes bloquées de Podunk et le canari utilisent désormais des routines déplacées, avec `Oui / Non` et des phrases naturelles. Les tables de noms et de destinations extraites sont préparées. Un atelier CLI permet l’export et l’import CSV ainsi que la reconstruction vérifiée des deux variantes. Les deux variantes passent les contrôles binaires et les premiers essais depuis une nouvelle partie. Le téléphone est testé par une entrée isolée ; son parcours normal reste à vérifier. **La traduction reste partielle.**

La sauvegarde intégrale de la TBL, des textes extraits et du repérage graphique est dans `sauvegardes/atelier_extraction_graphismes_v02.zip`. Décompresser à la racine pour retrouver tout le dossier `atelier/` (les outils et rapports principaux sont également visibles directement).

Les traductions éditables sont dans `traduction/`. Les patchs IPS et leurs rapports sont dans `patches/`. Aucun fichier ROM n'est distribué.

ROM source attendue : EarthBound Beginnings (USA) 1.2.sfc, 4 Mio sans en-tête copieur.
SHA-256 : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

Avec Python 3 :

```sh
python traduction/integrer.py "ROM.sfc" --appliquer patches/EarthBound_Beginnings_FR_v09_accents.ips
```

Le résultat est écrit dans `build/EarthBound_Beginnings_FR.sfc`. La ROM source reste inchangée. Une variante `ascii.ips` est fournie pour comparer l'affichage sans les nouveaux glyphes accentués.

Pour reconstruire depuis les traductions, décompresser la sauvegarde puis :

```sh
python traduction/integrer.py "ROM.sfc"
```

Un libellé `No` trop court reste exclu et consigné dans le rapport. Certaines légendes utilisent des abréviations françaises. Les blocs à pointeurs intérieurs conservent leurs positions grâce à un remplissage par espaces. Les graphismes avec du texte anglais restent à modifier. Les noms d'objets hérités peuvent ne pas tous être utilisés par le remake.

Rapport actuel : [RAPPORT_V09.md](RAPPORT_V09.md). Étape précédente : [RAPPORT_V08.md](RAPPORT_V08.md). Historique : [RAPPORT_V01.md](RAPPORT_V01.md). Vérifications à effectuer : [TESTS_A_FAIRE.md](TESTS_A_FAIRE.md). Sous Windows, glisser la ROM originale sur `Appliquer_patch_FR.bat`.

Le kit courant est [EarthBound_Beginnings_FR_v09_atelier_patch.zip](distributions/EarthBound_Beginnings_FR_v09_atelier_patch.zip). Il contient les deux patchs et les sources nécessaires à leur intégration. Le moteur de déplacement vérifie la réserve et les références explicites ; voir RAPPORT_V09.md.

Guide de l’outil : [traduction/ATELIER.md](traduction/ATELIER.md). Le CSV couvre les champs et dialogues ordinaires préparés ; les autres formats restent éditables en JSON.

L’audit signale les fragments identiques à relire et refuse les rapports périmés. Le catalogue contient encore 2 043 blocs candidats non préparés : leur utilisation, leurs frontières et leur traduction restent à vérifier. Les graphismes et le générique ne sont pas finalisés.

Éditeur local : ouvrir `atelier_fr.html`, charger `traductions.csv`, puis utiliser `Importer_CSV_FR.bat` et `Reconstruire_FR.bat`. Les sources précédentes sont sauvegardées avant chaque import modifiant des fichiers.


