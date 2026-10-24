# Checkpoint V78 — 44984fc

Sauvegarde de travail, pas une release finale et pas un lot400 validé. Main reste en V77.

Le bundle Git contient les commits locaux depuis mainV77 `db524666b87ecd006f4c313ad32233da2ac8137c` jusqu'à `44984fc7205167b111c3e868d11277c60f6dfb09` : sources, IPS, rapports et captures publiques. Aucun ROM, cœur, état ni dump mémoire. L'archive temporaire non suivie du poste local est exclue.

Dans un clone du dépôt disposant du commit V77, télécharger le bundle à côté du clone, puis :

```sh
git bundle verify ../EarthBound_FR_V78_44984fc.bundle
git fetch ../EarthBound_FR_V78_44984fc.bundle HEAD:checkpoint/v78-restored-44984fc
```

Examiner cette branche et ne la sélectionner que dans un arbre de travail propre. Ne pas forcer le remplacement de modifications locales. La branche restaurée contient `REPRISE_TRADUCTION.md`, `RESTANT_TEXTES.md`, le reconstructeur et les deux IPS V78. Appliquer un seul IPS à la ROM originale USA1.2 ; la ROM reste privée.

Git blob du bundle : `36e4d976db4e50108c3ff9606b29389592da39a3` ; taille9919923 octets. Le bundle a été vérifié localement et le SHA du blob distant doit être identique.

Dernière passe :796 amorces de dialogues placés et registre249 relus dans des périmètres qui se chevauchent. Douze plages françaises corrigées, zéro nouvelle traduction anglaise dans cette reprise ;249 historiques distinctes/297 plages,137 publiées/112 en attente.82 tests distincts validés ; les six nouveaux contextes sont relus sur38 captures accents/ASCII après appels forcés. Le lot400, la relecture complète et l'achèvement global ne sont pas certifiés. Voir le rapport joint.
