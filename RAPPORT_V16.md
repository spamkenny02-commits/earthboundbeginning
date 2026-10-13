# EarthBound Beginnings FR — Rapport V16

## Livraison

La **V16 autonome** conserve les modifications des versions V09 à V15 et ajoute **128 nouveaux segments français** répartis dans **63 scripts effectivement modifiés**.

Un lot de **100 scripts** a été examiné, soit **236 segments** :
- **128** nouveaux segments traduits en V16 ;
- **90** segments déjà couverts par des modifications V09–V15 : aucune réécriture pour éviter une collision ;
- **13** segments exclus car un pointeur HiROM littéral mène à l'intérieur de leur texte ;
- **5** segments laissés inchangés pour d'autres raisons (noms, expressions ou traductions identiques).

Les 100 scripts couvrent des panneaux du zoo, des conversations de PNJ, des hôtels, des gares et des dialogues de plusieurs villes.

## Patchs autonomes

- [V16 avec accents](patches/EarthBound_Beginnings_FR_v16_accents.ips) — **71 681 octets**
- [V16 sans accents](patches/EarthBound_Beginnings_FR_v16_ascii.ips) — **70 195 octets**
- [Manifeste éditable](traduction/v16_dialogues_fr.json)
- [Générateur reproductible](traduction/construire_v16.py)
- [Test IPS sans ROM](tests/verifier_fusion_v16.py)
- [CI GitHub Actions](https://github.com/spamkenny02-commits/earthboundbeginning/actions/workflows/verifier-v16.yml)

**Installation :** appliquer **un seul patch V16 sur la ROM USA 1.2 originale**, sans appliquer les versions antérieures. SHA-256 de la ROM originale : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

## Contrôles effectués

- Les **100 scripts** ont été vérifiés par empreinte FNV-1a sur les octets de la ROM source : **100 conformes**.
- Les **110 références HiROM littérales** déclarées ont été vérifiées sur la ROM source : **110 conformes**.
- Les **5 retours de ligne spéciaux `00`** ont été conservés ; les autres retours `03 00` et les codes de fin de dialogue restent à leur place.
- Un balayage des références HiROM littérales a trouvé **17 références** vers l'intérieur de **13 segments**, qui ont été exclus.
- Les **128 nouveaux segments** ne chevauchent aucun enregistrement IPS V15, en profil accents ou ASCII.
- Les tests automatiques vérifient la conservation intégrale des enregistrements IPS V15, l'encodage, les tailles et les offsets V16.

Reconstruire et comparer les IPS publiés :

```bash
python traduction/construire_v16.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v16 --comparer-publication
```

Appliquer localement sans écraser l'original :

```bash
python traduction/appliquer_v16.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v16.sfc"
```

## Avancement et limites

Le catalogue initial recense **3 092 entrées**, dont **2 043 blocs candidats** signalés lors de la V09. Ce nombre ne correspond pas directement à des dialogues indépendants ni à un dénominateur fiable pour un pourcentage de traduction. La V09 comptait **1 095 entrées intégrées** ; les V10 à V16 ont apporté **571 segments/blocs supplémentaires** (50 + 27 + 18 + 141 + 130 + 77 + 128), sans dédoublonnage avec le catalogue.

**La traduction reste partielle.** Les contrôles réalisés sont binaires et structurels. Il reste à tester les boîtes de dialogue et les parcours de jeu sous émulateur, puis à traiter les textes longs, les données compressées et les pointeurs internes. Aucune ROM commerciale n'est distribuée.
