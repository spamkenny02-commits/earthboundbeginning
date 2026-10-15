# V36 — bannière de victoire française

Base publiée relue avant construction : V35, commit `8978f6a`. V36 traduit le graphisme compressé **« YOU WON! »** en **« VICTOIRE »**. Il s'agit d'**un graphisme nouvellement traduit**, de 16 tuiles ; aucun script n'est révisé et aucun fragment de dialogue ancien n'est recompté.

L'objectif de 100 à 200 entrées n'a pas été forcé : ce lot cohérent traite une ressource graphique unique restée anglaise. L'audit des textes compressés confirme que les 32 blocs du manifeste historique et les 9 blocs relocalisés contiennent déjà leurs segments français ; V36 les préserve sans les annoncer comme nouveautés.

## Sécurité binaire

Le bloc source à `217EC1` contient 416 tuiles 2 bpp. Les 16 tuiles dédiées à la bannière sont reconstruites, puis les 6 656 octets bruts sont recompressés en 1 903 octets. La copie tient dans la réserve nulle `177800–177FD0`, avec 97 octets libres.

La réserve est nulle dans la ROM originale et dans chaque ROM V35, sans collision avec les enregistrements IPS antérieurs ni cible HiROM littérale. L'instruction de pointeur à `047C47` conserve sa structure et passe de `217EC1` à `177800` (`D77800` côté SNES). Les IPS V36 ajoutent exactement trois enregistrements à V35 : le bloc et les deux moitiés prouvées de l'opérande. Toutes les autres zones, les anciens scripts et alias, et les corrections boy/girl restent identiques.

Les deux IPS sont autonomes depuis la ROM originale USA 1.2 (`e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`). L'application indépendante donne les ROM cibles `37bcdd9e34d5995de28943ef777b94360abf5bf3e049c54a11a1e2ca8d6608da` (accents) et `03aaff53805277e25fc267554907cb4488d6f44391d367827ed0a94d98664e30` (ASCII).

## Contrôles

- 11 tests V36 : provenance, réserve, collisions, pointeur, compression, tuiles, IPS indépendant et comparaison exhaustive ;
- 7 tests V35, 12 V34, 14 V33, 12 V29 et 8 boy/girl : **64 tests réussis** au total ;
- parcours Snes9x 1.63 complet dans les deux profils : **« VICTOIRE » est affiché par le combat normal contre la lampe**, sans point d'entrée de test ;
- relecture des deux images de victoire : texte net et contenu dans la fenêtre ; toutes les autres captures sont identiques aux références.

Aucun essai artificiel n'est présenté comme narratif. Aucun fichier ROM, sauvegarde d'état, mémoire vive ni cœur d'émulateur n'est publié.

[Sources et constructeur](tools/v36/README_V36.md) · [Essai Snes9x](tests/emulation_v36/RAPPORT_EMULATION_V36.md)
