# EarthBound Beginnings FR — V13, lot de 141 blocs

## Patchs autonomes

- [**V13 avec accents**](patches/EarthBound_Beginnings_FR_v13_accents.ips) — 58 013 octets, 3 385 enregistrements IPS.
- [**V13 sans accents**](patches/EarthBound_Beginnings_FR_v13_ascii.ips) — 56 527 octets, 3 280 enregistrements IPS.

La V13 comprend **toute la V12** et **141 nouveaux blocs français** (répliques de personnages, magasins, dialogues de lieux, messages système et interactions). Total ajouté depuis V09 : **236 blocs** (V10 50 + V11 27 + V12 18 + V13 141).

**Installation :** appliquer **uniquement la V13** sur une copie non modifiée de `EarthBound Beginnings (USA) 1.2.sfc`. Ne pas appliquer les anciennes versions auparavant. Empreinte SHA-256 de la ROM source : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Tests réalisés

1. **ROM source locale (4 Mio) :** SHA-256 conforme. Les **141 blocs anglais complets, commandes comprises**, ont été comparés octet par octet au catalogue via une empreinte FNV-1a agrégée : `bc54e8f9`, identique à la référence. Le contrôle distinct des 141 segments de texte donne `801abb83`.
2. **Pointeurs source :** **196 références littérales HiROM** vers les 141 blocs trouvées dans la ROM originale ; aucun bloc du lot n'est sans référence.
3. **Longueurs :** les 141 traductions tiennent dans les segments originaux. Les espaces inutilisés sont remplis avec le code d'espace `50`. Aucun déplacement des commandes, des débuts de blocs ou des adresses de branches n'est nécessaire pour ce lot.
4. **Non-régression :** les **3 244 enregistrements IPS V12 avec accents** et **3 139 sans accents** sont conservés à l'identique, sans collision avec les 141 nouveaux segments.
5. **GitHub Actions :** [test de fusion V13](https://github.com/spamkenny02-commits/earthboundbeginning/actions/runs/38471016747) **réussi** pour les deux profils, avec contrôle du manifeste, des caractères encodables, des tailles, des données IPS et de la non-régression.

Les sources sont dans [traduction/v13_dialogues_fr.json](traduction/v13_dialogues_fr.json). Les scripts [construire_v13.py](traduction/construire_v13.py), [verifier_fusion_v13.py](tests/verifier_fusion_v13.py) et [verifier_source_v13.py](tests/verifier_source_v13.py) permettent de reconstruire et contrôler les patchs. Le dernier test, qui exige la ROM personnelle, est fourni pour reproduction et n'est pas exécuté sur GitHub Actions.

## Application

```bash
python traduction/appliquer_v13.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v13.sfc"
```

Pour une variante sans accents, utiliser `--profil ascii`.

## Limites et suite

Cette passe se concentre sur les **blocs courts qui ne nécessitent pas de relocalisation**. La traduction reste partielle : des dialogues complexes, textes compressés et éléments graphiques anglais subsistent. Les tests automatiques vérifient les structures et les patchs, **pas encore le rendu réel, les embranchements ni un parcours complet sous émulateur**. Aucun émulateur SNES n'était disponible dans l'environnement de test local. La validation de gameplay reste donc ouverte.

Les prochains lots doivent traiter les dialogues multisegments et les blocs longs, avec conservation explicite des pointeurs et tests en jeu avant qualification comme version finale.
