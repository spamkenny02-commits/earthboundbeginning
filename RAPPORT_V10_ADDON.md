# EarthBound Beginnings FR — v10 (add-on de la v09)

## Avancée du 13 octobre 2026

La ROM source **EarthBound Beginnings (USA) 1.2.sfc** a été vérifiée par SHA-256 :
`e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

**50 dialogues courts** ont été traduits et préparés sous forme de patch IPS *additionnel* (et non de ROM complète). Les deux profils sont prévus : accents et ASCII. Ils concernent notamment des dialogues de personnages, des messages de magasin, la reine Mary, le gang BB et Youngtown.

La vérification locale sur la ROM source a confirmé :
- 50 blocs modifiables sans déplacement ;
- 70 références littérales HiROM vers leurs débuts ;
- aucune référence littérale vers le milieu de ces 50 blocs ;
- 22 autres candidats refusés (18 trop longs, 4 avec pointeurs intérieurs) ;
- deux IPS de 2 449 octets chacun ;
- application des IPS sur une copie de la ROM source, conservation de tous les octets hors des 50 blocs et décodage exact des remplacements.

Empreintes SHA-256 :
- accents : `21480d84a36e6610221fc548554e1e987d99ce5bae9ab04b0710d4fb6124fc8f`
- ASCII : `3924d364c21938907c75c916a4bd5075308678e15db2df7324899181e4188f5e`

### Construction

```bash
python traduction/construire_addon_v10.py "EarthBound Beginnings (USA) 1.2.sfc" --base-v09 "ma_rom_FR_v09.sfc" --out build_v10
```

La ROM d'origine est nécessaire pour les contrôles. Le script refuse un bloc qui ne correspond plus à l'original dans la ROM v09 fournie. Appliquer ensuite le patch v10 du **même profil** (accents ou ASCII) après la v09.

Sources : [traductions v10](traduction/v10_inplace_fr.json), [générateur](traduction/construire_addon_v10.py). Les versions précédentes restent inchangées.

### Limites / suite

Ce sont des **tests structurels**, pas encore des tests de jeu. L'add-on doit encore être appliqué à une ROM v09 complète et parcouru dans un émulateur. Les 22 candidats exclus demandent une relocalisation ou une traduction plus courte. Les 28 blocs du brouillon v10 précédent restent un chantier distinct, sans garantie d'intégration. Aucun fichier ROM protégé n'est distribué.
