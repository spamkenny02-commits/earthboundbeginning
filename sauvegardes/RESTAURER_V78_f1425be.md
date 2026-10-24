# Complément du checkpoint V78 — continuations

Ce complément conserve le commit local `f1425be299821bfdf67d4d2935dd1a2bd8781b05`, après la sauvegarde initiale `44984fc`. Il contient les quatre corrections supplémentaires de boutique, les deux IPS à jour, le relevé de 615 continuations relues et les preuves de rendu. Aucune nouvelle traduction anglaise n'est comptée. Le total historique reste de 249 sources distinctes / 297 plages ; ce checkpoint ne constitue ni une release finale ni un lot de 400 validé.

Restaurer d'abord le bundle initial en suivant `RESTAURER_V78_44984fc.md`. Télécharger ensuite le présent bundle à côté du clone :

```sh
git bundle verify ../EarthBound_FR_V78_f1425be.bundle
git fetch ../EarthBound_FR_V78_f1425be.bundle HEAD:checkpoint/v78-restored-f1425be
```

Ne sélectionner la branche que dans un arbre de travail propre ; conserver toutes les modifications locales. Le bundle exige le commit initial `44984fc7205167b111c3e868d11277c60f6dfb09`. Les deux restaurations ont été testées successivement depuis une base V77 seule ; HEAD et arbre finaux correspondent au commit local.

Bundle : 315152 octets ; Git blob `9ebd479d8a3b800599e789e0a1023e873553b35a` ; arbre de travail restauré `6c97c421aaf5e5950452213f4fa61dd7a96ce5b3`. Sources, IPS, rapports et PNG seulement ; aucun fichier privé.

Validation : 82 tests V78 réussis avec la ROM privée ; 24 captures finales des avertissements et questions relues, après appels forcés et préparation native de l'argument affiché. Ces essais n'exercent ni l'achat naturel ni la décision de compatibilité. Se reporter au rapport joint pour les hashes des IPS et les limites restantes. Main reste en V77.
