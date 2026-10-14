# EarthBound Beginnings FR — V28

Version du 14 octobre 2026, basée sur la V27 publiée sur `main`.

## Intégration
**49 nouvelles plages françaises dans 49 scripts**, dont des scripts à sauts ou commandes qui ne satisfont pas le décodeur de scripts complets V27. Scènes : indices, maison hantée, personnages, stockage, concerts, pizzas, banque et train. Le cumul des ajouts depuis V18 Work est de **1 515 plages**.

Sur 93 plages présélectionnées, 43 ont été exclues à cause de références HiROM littérales vers leur intérieur, et une autre parce que sa référence d'entrée était modifiée par V27. Les 49 retenues sont des textes réellement différents de l'anglais.

## Contrôles exécutés
- ROM USA 1.2 originale (4 Mio), SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c` : vérifiée.
- 49/49 plages anglaises et 49/49 préfixes de scripts (commandes incluses) : comparés aux octets de la ROM.
- 49/49 scripts avec référence d'entrée HiROM littérale ; aucune référence littérale intérieure aux 49 plages.
- Encodage et longueur vérifiés pour les deux profils ; aucun chevauchement entre ajouts ni avec V27.
- Deux IPS additionnels locaux : aller-retour sur ROM originale réussi.
- Deux IPS V28 **autonomes** : structure, préfixe IPS V27, enregistrements ajoutés et empreintes vérifiés. Les 49 références d'entrée du manifeste sont conservées par V27.

| Profil | Enregistrements V27 | Ajouts V28 | SHA-256 IPS autonome |
|---|---:|---:|---|
| Accents | 5 549 | 49 | `3db0607030f931d5acb020fa7b9f9d6af8d157099bb958a887192edef005fbd9` |
| ASCII | 5 444 | 49 | `60a70dc688b491c5574d01e86856c3e06646545d46e1838183791ea6c50df7f5` |

## Limites
**Non effectués :** roundtrip intégral des IPS autonomes V28 sur la ROM originale dans un environnement unique ; tests des nouvelles scènes en émulateur ; validation des pointeurs indirects et textes compressés. Les scènes peuvent rester partiellement anglaises. Les contrôles structurels ne remplacent pas un test de jeu.

Appliquer un seul IPS V28 **directement** à la ROM originale USA 1.2. Aucun fichier ROM commercial distribué. Le constructeur `tools/v28/build_v28.py` permet de reproduire et vérifier les deux patchs avec sa propre ROM.
