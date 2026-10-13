# EarthBound Beginnings FR — V11 fusionnée

**Base :** EarthBound Beginnings (USA) 1.2.sfc, SHA-256
`e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Patchs autonomes

- [**V11 avec accents**](patches/EarthBound_Beginnings_FR_v11_accents.ips) — 52 871 octets, 3 226 enregistrements IPS.
- [**V11 sans accents**](patches/EarthBound_Beginnings_FR_v11_ascii.ips) — 51 385 octets, 3 121 enregistrements IPS.

**Application :** choisir **un seul** patch V11 et l'appliquer directement à une copie de la **ROM originale USA 1.2 non modifiée**. **Ne pas appliquer V09 ou V10 auparavant** : leurs modifications sont déjà incluses.

## Contenu

- Toutes les modifications IPS de la **V09**, reprises octet pour octet.
- Les **50 dialogues** du patch additionnel **V10**, repris octet pour octet.
- **27 nouveaux dialogues** français intégrés en place : PNJ, magasins, Youngtown, école, etc. Traductions sources : [manifest V11](traduction/v11_nouveaux_dialogues.json).

La fusion a été vérifiée structurellement : aucune collision entre V09 et V10, aucune collision entre les nouveaux blocs V11 et les modifications précédentes. Les 27 nouveaux blocs ont été vérifiés sur la ROM source : limites de longueur respectées, **41 références littérales** pointent vers leurs débuts, aucune référence littérale détectée vers leur intérieur. Cinq autres candidats ont été écartés par prudence à cause de références internes possibles.

## Application automatisée (locale)

L'[outil d'application](traduction/appliquer_v11.py) vérifie l'empreinte de la ROM source et refuse de l'écraser :

```bash
python traduction/appliquer_v11.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v11.sfc"
```

Pour une version sans accents, remplacer `accents` par `ascii`.

## Vérification et reproduction

Le [script de construction](traduction/construire_v11.py) vérifie la ROM d'origine, les textes sources, les pointeurs, les collisions et l'aller-retour IPS. Il reconstruit les patchs à partir des fichiers V09 et V10 présents dans le dépôt :

```bash
python traduction/construire_v11.py "EarthBound Beginnings (USA) 1.2.sfc" --out build_v11
```

Le [test sans ROM](tests/verifier_fusion_v11.py) contrôle l'identité des enregistrements V09/V10 dans la V11, les nouveaux textes et l'absence de collisions. Un workflow GitHub Actions est ajouté pour exécuter ce test automatiquement.

**Limite importante :** validation binaire et structurelle uniquement. Les patchs V11 n'ont **pas encore** fait l'objet d'un parcours complet sous émulateur ; l'affichage, les embranchements scénaristiques et les caractères accentués doivent être testés en situation. Les 28 blocs du brouillon précédent restent à valider séparément. Aucune ROM originale ou modifiée n'est distribuée.

## Étape suivante

Effectuer les tests d'émulation V11, puis traiter les textes nécessitant une relocalisation (et les éléments graphiques anglais), sans modifier rétroactivement les patchs V09/V10.
