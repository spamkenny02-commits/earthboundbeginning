# EarthBound Beginnings SNES — V19 française, validation binaire (14 octobre 2026)

## Référence exacte

- Dépôt : `spamkenny02-commits/earthboundbeginning`, branche `main`.
- HEAD observé avant livraison : `46846567f22afa28880f6c84fabcb1e9a294fb0a`.
- Dernière base autonome publiée : **V18 Work**, comprenant 168 segments nouveaux depuis V17.
- Les IPS V18 Work et le catalogue de candidats utilisés ont été comparés à leurs **SHA Git de blobs publiés** : correspondance exacte dans les trois cas.
- ROM source USA 1.2 : **4 194 304 octets**, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c` ; vérifiée localement, jamais distribuée.

## Livraison V19

- **119 nouveaux segments français réellement intégrés** dans deux IPS autonomes, à appliquer individuellement à la ROM originale USA 1.2.
- 121 traductions candidates reprises de la préparation ; **deux exclues** après une nouvelle vérification des pointeurs : `35AD8D` et `35AFD1`.
- Les pointeurs littéraux originaux à `35AD84` et `35AFC8` sont annulés (mis à zéro) par la V18 Work. Le texte situé aux anciennes cibles serait potentiellement inaccessible ; les traductions correspondantes ne sont pas comptées ni insérées.
- Révisions de traduction : meilleure fidélité sur le vieux manoir, les phénomènes paranormaux, les rois et reines, les yétis et les onomatopées.
- **Aucun texte inchangé ni brouillon comptabilisé**.

| Profil | Enregistrements V18 Work | Ajouts V19 | Total V19 | SHA-256 IPS V19 |
|---|---:|---:|---:|---|
| Accents | 4 083 | 119 | 4 202 | `6a1794d1ea8f0fca7ef73f6e244e54de92ca4ae3207b81d29d3fc83374f38c18` |
| ASCII | 3 978 | 119 | 4 097 | `9b9edf7a1af355881dc6396553d0bb2916813717d33f71a470ac98c7a912c403` |

## Contrôles réellement exécutés

- **11/11** tests unitaires V19 : TSV, identifiants, longueurs, encodage, RLE IPS, troncature et append.
- **4/4** tests indépendants V19 sur la ROM réelle : empreinte de ROM, roundtrip IPS dans les deux profils, décodage de chaque texte et régression hors plages V19, vérification des pointeurs et exclusion des deux cibles invalidées.
- **10/10** tests de régression V18 Work exécutés à nouveau sur la ROM originale (dont relecture indépendante des 152 textes Work).
- **2/2** constructions autonomes V19 réussies ; 119 ajouts par profil, 0 collision avec les plages V18 Work, 0 collision interne.
- **0** octet changé hors des 119 plages de texte V19 en comparaison des ROM cibles V18 Work et V19 ; commandes et suffixes vérifiés, références HiROM littérales des candidats conservées.
- Les empreintes des deux IPS finaux correspondent à `validation_v19.json`.

## Non effectué / limites

- **Aucun test V19 en émulateur** : aucun exécutable ni cœur SNES exploitable trouvé dans cet environnement. Les essais Snes9x déjà documentés concernent uniquement la V18 Work.
- Pas de validation visuelle des coupures de ligne, des dialogues complets en situation ou de la sauvegarde native.
- Les pointeurs **indirects**, tables compactes, textes **compressés** et graphismes anglais ne sont pas encore pris en charge. La vérification des références couvre les pointeurs HiROM littéraux de quatre octets relevés par le catalogue.
- Plusieurs dialogues restent partiellement anglais. Le compte de 119 concerne des **segments**, pas 119 conversations entières.

## Reconstruction reproductible

```sh
python3 tools/v19/build_v19.py --repo . --check-only
python3 tools/v19/build_v19.py --repo . --rom "/chemin/EarthBound Beginnings (USA) 1.2.sfc" --out build_v19
python3 -m unittest discover -s tools/v19 -p test_v19.py -v
REPO_ROOT="$PWD" V19_OUT="$PWD/build_v19" ROM_PATH="/chemin/EarthBound Beginnings (USA) 1.2.sfc" python3 -m unittest discover -s tools/v19 -p test_v19_integration.py -v
```

**Appliquer un seul IPS V19 directement à la ROM originale**. Ne pas empiler V17 ou V18 Work. Aucune ROM commerciale dans les livrables.

## Étapes suivantes

1. Essais Snes9x ciblés : dialogues des gares, Spookane, désert Yucca, mont Itoi, Escargo Express et appels familiaux.
2. Étudier les deux pointeurs annulés par V18 Work avant de toucher aux cibles `35AD8D` / `35AFD1`.
3. Étendre V20 avec des dialogues multisegments et longs ; traiter ensuite tables de pointeurs indirects, compression et graphismes.

## État de publication au terme de cette exécution

La tentative de transfert des artefacts binaires vers le connecteur GitHub a été **bloquée par ses contrôles de sécurité**. **Aucun commit V19 n'a été créé ni publié**. Le dépôt `main` reste à V18 Work (`46846567f22afa28880f6c84fabcb1e9a294fb0a` lors du contrôle). La V19 est livrée comme archive locale validée, à conserver pour la prochaine exécution. Ne pas annoncer V19 comme publiée.
