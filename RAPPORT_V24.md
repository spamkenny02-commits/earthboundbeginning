# EarthBound Beginnings FR — V24

Lot du 14 octobre 2026, depuis V23 publiée sur main (`56d3dd3`).

## Résultats

- **213 nouvelles plages de texte intégrées**, dans 124 scripts, deux IPS autonomes accents/ASCII.
- Dialogues de Podunk, Magicant, retours de personnages, scènes du train, magasins et fragments liés aux noms et objets.
- 88 plages ne commencent pas juste après le marqueur @: elles peuvent suivre une commande dynamique ou d'autres commandes. Les anciennes versions du constructeur ne traitaient pas ces plages comme telles.
- 12 tests V24 et 10 tests V23 réussis, sans tests ignorés.
- Décodage indépendant des 213 textes français dans chaque variante, aller-retour IPS, absence de collision, conservation des anciennes modifications et des octets hors des nouvelles plages.
- Snes9x 1.63: parcours du début du jeu conforme aux cinq écrans de référence, 339 commandes accents et 337 ASCII, 25 803 images simulées par profil.
- **950 ajouts depuis V18 Work** (119 + 160 + 153 + 185 + 120 + 213). Ce nombre compte les plages modifiées, pas les scripts complets ou les phrases uniques.

## Nouvel audit de provenance

Le catalogue complet est reparsé avec le décodeur de layout existant. Le texte anglais et les commandes de chaque script doivent reproduire les octets originaux. L'audit exige des références HiROM littérales explicites vers le début du script, vérifie qu'elles restent identiques en V23 dans les deux variantes et que les commandes n'ont pas changé. Il exclut les plages occupées par les IPS V23 et toute référence littérale vers un octet d'une plage de texte.

**830 plages candidates** passent cette présélection sur V23. V24 en intègre 213; les 617 autres sont des pistes à relire, pas un lot déjà traduit ni le nombre de textes restant dans le jeu. Les compteurs d'exclusion dans `validation_v24.json` concernent des scripts ou des plages selon le contrôle; ils ne constituent pas une partition unique du catalogue.

Le constructeur conserve les espaces initiaux et finaux autour des commandes et complète les emplacements fixes par des espaces. Les commandes dynamiques ne sont pas déplacées. Les traductions abrégées et l'espacement doivent être revus dans les scènes correspondantes.

## Utilisation et reconstruction

Appliquer un seul IPS V24 directement à la ROM originale USA 1.2 sans en-tête, sans préinstaller V23. SHA-256 original: `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

```sh
python3 tools/v24/audit_v24.py --rom '/chemin/original.sfc' --out build_v24/audit.json
python3 tools/v24/build_v24.py --rom '/chemin/original.sfc' --out build_v24
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/v24 -p test_v24.py -v
```

Sources éditables, manifeste complet et empreintes dans `tools/v24/`. Le manifeste donne l'offset du premier octet de TEXTE (sans marqueur @), contrairement aux anciens lots. Aucun fichier ROM distribué.

## Limites

Le parcours émulateur teste le début du jeu, pas les 213 nouvelles plages dans leurs scènes. Les scripts peuvent rester partiellement anglais. Les pointeurs indirects ne sont pas démontrés par cet audit; les scripts non conformes, déplacés ou sans référence littérale conservée sont exclus. Les textes compressés, la sauvegarde native et les graphismes anglais (dont YOU WON) restent à traiter.

## Consolidation de la publication parallèle

Pendant la préparation, main a reçu une V24 de 63 segments dans le commit `b7273646f4b87f0962a20bdea2a30868195c5a20`. Le lot consolidé conserve les 213 plages qui passent le nouvel audit: 188 du premier lot local, 15 recouvrements avec la publication parallèle et 25 ajouts issus de celle-ci (188 + 25 = 213). Les 23 autres traductions sont préservées, avec leurs sources et patchs, dans `tools/v24_parallel_snapshot/`; leurs scripts complets ne passent pas le décodeur de layout du catalogue et elles ne sont pas incluses dans les IPS consolidés. Il s'agit d'une exclusion conservatrice, pas d'une preuve de corruption. Voir `tools/v24/consolidation_v24.json`. Les anciens chiffres 63 et les anciennes validations dans l'archive sont historiques. Les nouveaux IPS ont été reconstruits sur V23 et retestés sur la ROM originale puis en émulateur.
