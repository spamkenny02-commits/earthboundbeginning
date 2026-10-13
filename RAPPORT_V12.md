# Rapport V12

La V12 fusionne les patchs V09, V10, V11 et ajoute 18 nouveaux dialogues.

## Patchs

- [Accents](patches/EarthBound_Beginnings_FR_v12_accents.ips)
- [Sans accents](patches/EarthBound_Beginnings_FR_v12_ascii.ips)

Appliquer uniquement la V12 sur une copie de la version USA 1.2 originale. Ne pas appliquer les versions précédentes : elles sont incluses.

## Contrôles

Les 18 nouveaux textes ont été vérifiés contre les octets source, les tailles disponibles et les références HiROM. Les blocs contenant des références internes ont été écartés. Les tests automatiques contrôlent la conservation des enregistrements V11 et les collisions.

## Commandes

```bash
python traduction/construire_v12.py "EarthBound Beginnings (USA) 1.2.sfc" --sortie build_v12
python traduction/appliquer_v12.py "EarthBound Beginnings (USA) 1.2.sfc" --profil accents --sortie "EarthBound_Beginnings_FR_v12.sfc"
```

Les tests de jeu sous émulateur restent à réaliser. Aucun fichier de jeu complet n'est distribué.
