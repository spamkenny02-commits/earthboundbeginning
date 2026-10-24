# Complément V78 — nom du joueur

Sauvegarde du commit local `32413fb0e3e02fa33ebbadf3ba4f5fd79d00a817`. Elle contient les IPS à jour, la correction de l'invite de saisie et les preuves de noms saisis au clavier puis affichés sous JOUEUR. Une correction de français existant ; zéro nouvelle source anglaise. Ni lot de 400 ni traduction complète certifiés ; main reste V77.

Restaurer les deux premiers bundles selon `RESTAURER_V78_44984fc.md` et `RESTAURER_V78_f1425be.md`. Télécharger ensuite ce bundle à côté du clone :

```sh
git bundle verify ../EarthBound_FR_V78_32413fb.bundle
git fetch ../EarthBound_FR_V78_32413fb.bundle HEAD:checkpoint/v78-restored-32413fb
```

Le prérequis est `f1425be299821bfdf67d4d2935dd1a2bd8781b05`. Conserver les modifications locales et ne sélectionner une branche que dans un arbre de travail propre. La chaîne V77 → 44984fc → f1425be → 32413fb a été restaurée et vérifiée : HEAD et arbre `009cca5acb11e9fbe4a13e85f5a6727dc50a9abf` correspondent exactement.

Bundle : 211931 octets ; Git blob `25e5a4428c642b3cf67895739b2a569b33694ddc`. Sources, IPS, rapports et PNG seulement ; aucune ROM, aucun cœur, état ou dump mémoire.

Validation : 84 tests réussis ; noms A et24 A saisis par la manette, confirmés puis rendus intégralement dans les deux profils. La seule entrée de fin est forcée ; le déclenchement naturel de l'appel demandant le nom, la victoire et un parcours complet ne sont pas certifiés. Voir `RAPPORT_V78_NOM_JOUEUR.md` pour les empreintes, le périmètre et les restes.
