# EarthBound Beginnings SNES — traduction française

## Version actuelle : V16 (traduction partielle)

La **V16 autonome** reprend toutes les modifications V09–V15 et ajoute **128 segments français dans 63 scripts modifiés**, sur un lot de **100 scripts vérifiés** (236 segments examinés). Depuis la V09 : **571 segments/blocs supplémentaires** cumulés au fil des versions V10–V16 (50 + 27 + 18 + 141 + 130 + 77 + 128), sans les brouillons.

- [Patch V16 avec accents](patches/EarthBound_Beginnings_FR_v16_accents.ips)
- [Patch V16 sans accents](patches/EarthBound_Beginnings_FR_v16_ascii.ips)
- [Rapport V16](RAPPORT_V16.md), [manifeste](traduction/v16_dialogues_fr.json), [tests](tests/verifier_fusion_v16.py)

**Appliquer uniquement V16 directement à la ROM originale USA 1.2**, sans préinstaller V09 à V15.

```sh
python traduction/appliquer_v16.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v16.sfc"
```

**Contrôles :** 100 scripts et 110 pointeurs littéraux vérifiés sur la ROM source ; 13 segments à pointeurs intérieurs exclus et 90 segments déjà modifiés conservés. [CI V16](https://github.com/spamkenny02-commits/earthboundbeginning/actions/workflows/verifier-v16.yml). Le jeu reste partiellement traduit et nécessite des tests complets sous émulateur.

## Versions précédentes

Les rapports [V15](RAPPORT_V15.md), [V14](RAPPORT_V14.md), [V13](RAPPORT_V13.md), [V12](RAPPORT_V12.md), [V11](RAPPORT_V11.md) et [V10](RAPPORT_V10_ADDON.md) restent disponibles. Les anciens patchs sont archivés dans `patches/`.

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
