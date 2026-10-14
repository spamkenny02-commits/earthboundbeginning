# EarthBound Beginnings SNES — V20 locale, 14 octobre 2026

## Référence et état de publication

- Dépôt : `spamkenny02-commits/earthboundbeginning`, branche `main`.
- Dernier HEAD publié contrôlé : `46846567f22afa28880f6c84fabcb1e9a294fb0a` (**V18 Work**).
- Base de V20 : **V19 autonome validée localement**, non publiée, elle-même dérivée de V18 Work.
- ROM originale USA 1.2 sans en-tête : 4 194 304 octets, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c` (contrôlée localement, jamais distribuée).
- Le contenu V19 local a été vérifié par ses empreintes et ses 15 tests. Les IPS V18 Work correspondent aux empreintes de la publication GitHub.

## Nouveau lot V20

**160 nouveaux segments textuels français intégrés**, principalement des descriptions d'objets, consommables, équipements, capacités et plusieurs descriptions longues réparties sur plusieurs segments. Le compteur désigne des segments réellement remplacés dans les IPS, **pas 160 dialogues complets**. Aucun brouillon ni texte inchangé n'est compté.

Les textes ont été relus et ajustés manuellement pour les contraintes d'encodage et de longueur. Les segments à commandes internes non caractérisées et les zones de pointeurs indirects ne sont pas réécrits. Le constructeur préserve tous les enregistrements IPS V19, ne déplace aucun texte et ne réécrit aucun pointeur.

| Profil | Enregistrements V19 | Ajouts V20 | Total | SHA-256 du patch autonome |
|---|---:|---:|---:|---|
| Accents | 4 202 | 160 | 4 362 | `268c7f5f4464989a7c2249905a6ee4cdbc0bc806007be0d1e54035747f4758fd` |
| ASCII | 4 097 | 160 | 4 257 | `607cb38e108046b87cce0c021288a9b74b04563270eb124e2d6fe44d35f96907` |

**Utiliser un seul IPS V20 directement sur la ROM originale USA 1.2.** Ne pas superposer V18 Work ni V19. Aucun fichier ROM dans la livraison.

## Tests réellement exécutés

- **10/10** tests V20 : unicité et changements réels, cohérence manifeste/TSV/catalogue, budget et encodage des deux profils, exclusion des traductions antérieures, erreurs IPS, empreinte de la ROM, vérification indépendante du roundtrip IPS, références HiROM littérales, commandes finales, conservation de V19, absence de changements hors des 160 plages et absence de chevauchement interne.
- **15/15** tests de régression V19 sur la ROM originale : réussis.
- **10/10** tests de régression V18 Work sur la ROM originale : réussis.
- **2/2** constructions IPS V20 autonomes réussies.
- **0 collision**, **0 régression détectée** sur les octets couverts.
- **0 test V20 en émulateur** : aucun exécutable ni cœur SNES exploitable n'était présent dans cet environnement. Les anciens essais Snes9x documentés dans le dépôt concernent uniquement V18 Work.

### Pointeurs V19 conservés en exclusion

Les pointeurs littéraux originaux aux offsets `35AD84` et `35AFC8` restent annulés dans la base V18 Work et dans les IPS V19/V20. Dans V18 Work, les enregistrements `35AD7E` et `35AFC2` écrivent neuf octets nuls chacun. Les segments `35AD8D` et `35AFD1` restent exclus ; aucune réparation spéculative de ces pointeurs n'a été effectuée.

## Limites et suite

- Vérification des pointeurs limitée aux références HiROM littérales de quatre octets du catalogue ; les références indirectes, textes compressés, commandes internes inconnues et graphismes anglais nécessitent une analyse séparée.
- Aucun contrôle visuel en situation, ni test de sauvegarde native ou des nouvelles zones V19/V20 sous émulateur.
- Vérifier la cohérence terminologique en jeu (Combat, Pouvoir, Magicant, etc.), les retours à la ligne et les dialogues multisegments.
- Continuer les traductions restantes avec les mêmes garde-fous, et auditer les pointeurs annulés avant modification.

## Reproduire

Depuis la racine du paquet extrait :

```sh
python3 tools/v20/build_v20.py --rom '/chemin/EarthBound Beginnings (USA) 1.2.sfc' --out build_v20
ROM_PATH='/chemin/EarthBound Beginnings (USA) 1.2.sfc' V20_OUT="$PWD/build_v20" python3 -m unittest discover -s tools/v20 -p test_v20.py -v
```

Les sources V19 et les manifestes/catalogues V18 Work requis sont inclus dans l'archive. Les sorties attendues sont consignées dans `tools/v20/validation_v20.json`.

## GitHub

Tentative de transfert par connexion GitHub : création d'un blob texte simple possible, mais le transfert des données de traduction et des fichiers binaires a été refusé par les contrôles de sécurité du connecteur. `git` dans l'environnement local ne résout pas `github.com` (DNS). **Aucun commit V19 ni V20 n'a été publié** pendant cette exécution. Ne pas annoncer V20 comme publiée.
