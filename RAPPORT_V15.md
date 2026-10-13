# EarthBound Beginnings FR — V15

## Livraison

La **V15 autonome** reprend toutes les modifications des V09 à V14 et ajoute **77 segments de dialogue français** dans **32 scripts** (Snowman, Ellay, Magicant, Spookane et autres PNJ). Les segments désignent des portions de texte modifiées, pas nécessairement des dialogues complets.

- [IPS V15 accents](patches/EarthBound_Beginnings_FR_v15_accents.ips) — **66 694 octets**
- [IPS V15 ASCII](patches/EarthBound_Beginnings_FR_v15_ascii.ips) — **65 208 octets**
- [Manifeste V15](traduction/v15_dialogues_fr.json)
- [Générateur V15](traduction/construire_v15.py)
- [Test IPS V15](tests/verifier_fusion_v15.py)

Les patchs sont **cumulatifs et autonomes** : appliquer **un seul IPS V15 directement sur la ROM originale USA 1.2**, sans appliquer V09 à V14 au préalable. SHA-256 de la ROM source : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Contrôles effectués

- **32/32 scripts** comparés aux octets originaux par empreinte FNV-1a : **aucun écart**.
- **36/36 références HiROM littérales** vérifiées à leur adresse dans la ROM originale.
- **80 traductions candidates** examinées. **Trois** ont été exclues après détection de **quatre pointeurs littéraux** pointant à l'intérieur de leur texte. **77 segments intégrés**.
- Les retours de ligne particuliers `00` ont été relevés dans la ROM et conservés, sans modifier les commandes ni les points d'entrée.
- **0 collision** entre les 77 nouveaux segments et les modifications IPS V14, pour les profils accents et ASCII.
- Les tests de fusion vérifient la conservation de tous les enregistrements V14, les tailles, le contenu et les offsets de chaque ajout.

### Construire et vérifier à partir de la ROM originale

```bash
python traduction/construire_v15.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v15 --comparer-publication
```

### Appliquer le patch

```bash
python traduction/appliquer_v15.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v15.sfc"
```

## Limitations

Les tests réalisés sont **binaires et structurels**. Un parcours de gameplay complet et une vérification visuelle des boîtes de dialogue sous émulateur restent à effectuer. Certains textes, noms propres et expressions n'ont pas été modifiés par prudence. Les **huit brouillons de pointeurs intérieurs** préparés séparément dans `traduction/v15_candidats_a_valider.json` ne sont **pas** intégrés par ce lot : ils exigent un traitement indépendant.

Aucune ROM commerciale n'est incluse dans le dépôt ou les patchs.
