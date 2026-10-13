# EarthBound Beginnings FR — Rapport V14

## Résultat

La **V14 autonome** fusionne toutes les modifications des V09 à V13 et ajoute **130 segments de texte français** répartis dans **44 scripts multisegments** (PNJ, magasins, Snowman, Magicant, Ellay, etc.). Il s'agit de 130 portions de dialogue réellement modifiées, et non de 130 conversations distinctes.

- [Patch V14 avec accents](patches/EarthBound_Beginnings_FR_v14_accents.ips) — **63 835 octets**.
- [Patch V14 sans accents](patches/EarthBound_Beginnings_FR_v14_ascii.ips) — **62 349 octets**.
- [Manifeste source](traduction/v14_multisegments_fr.json).
- [Générateur reproductible](traduction/construire_v14.py) et [tests automatiques](tests/verifier_fusion_v14.py).

**Application :** appliquer **un seul patch V14 directement sur la ROM USA 1.2 originale**, jamais sur une ROM déjà patchée V09–V13. SHA-256 source : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Audit technique réalisé

- Les **44 scripts anglais complets** ont été comparés par empreinte FNV-1a à leurs octets réels dans la ROM source USA 1.2 : **44 conformes, 0 anomalie**.
- Les **47 références HiROM littérales** déclarées pour ces scripts ont été vérifiées dans la ROM : **47 conformes**.
- Les codes de commande, sauts de ligne et marqueurs `@` restent aux mêmes positions ; le format original distingue `00` et `03 00` pour les retours à la ligne. **7 retours `00`** ont été identifiés et consignés.
- Un balayage des pointeurs littéraux a repéré **16 références vers l'intérieur de 8 segments**. Ces 8 segments ont été **exclus par prudence** : le lot préparatoire comptait 138 traductions, le patch publié en conserve **130**.
- Aucun des 130 segments retenus ne chevauche une modification du patch V13. Les textes plus courts sont complétés par des espaces sans déplacement de données.
- Le test GitHub Actions vérifie la conservation intégrale des enregistrements IPS V13, l'encodage, les longueurs, le nombre de segments et l'absence de collision.

Pour reconstruire les deux IPS et vérifier qu'ils sont identiques aux versions publiées :

```bash
python traduction/construire_v14.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v14 --comparer-publication
```

Pour appliquer le patch localement :

```bash
python traduction/appliquer_v14.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v14.sfc"
```

## Suite vers V15

Traiter les scripts restants en lots plus larges, notamment les commandes dynamiques, dialogues longs et textes compressés. Tester la lisibilité et les embranchements sous émulateur SNES dès qu'un émulateur et des sauvegardes de référence sont disponibles.

**Limite :** ces tests sont binaires et structurels ; aucun parcours complet du jeu sous émulateur n'a été effectué. Aucun fichier ROM commercial n'est publié.
