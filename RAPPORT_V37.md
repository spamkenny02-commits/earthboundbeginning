# V37 — graphisme français du coup critique

Base publiée relue : V36, commit `dbbefe5`. V37 traduit le graphisme compressé **« SMAAAASH!! »** en **« COUP CRIT! »**. Il s'agit d'un graphisme nouvellement traduit sur vingt tuiles ; aucun script ni fragment de dialogue n'est recompté.

Le quota de 100 à 200 entrées n'est pas artificiellement rempli : ce lot poursuit l'interface graphique compressée. Une seconde proposition, `HP` → `PV`, a été essayée puis rejetée lorsque l'émulateur a prouvé que ses quatre tuiles servent aussi à d'autres fenêtres.

## Sécurité binaire

V36 possède déjà la réserve `177800–177FD0` et son pointeur assembleur à `047C47` vise `D77800`. V37 vérifie l'empreinte exacte de ce bloc avant de le remplacer; aucun autre enregistrement IPS ni cible HiROM ne chevauche la réserve. Le pointeur n'est pas réécrit.

Le bloc brut de 6 656 octets est recompressé en 1 717 octets. Les IPS autonomes conservent tous les enregistrements V36 et ajoutent exactement un remplacement contrôlé. L'application IPS indépendante donne les ROM cibles `6b6b0b241eb56f0e1be446e9b6cd0671bba02cbc90c7797285f8c18403ef1ef2` (accents) et `7c5138b2eef6a3371bab2f1b83d6cc556ac3a18c42ff1ef99c6c3daf9ed87b93` (ASCII).

## Contrôles

- 10 tests V37 : propriété V36, collision, pointeur, vingt tuiles exactes, compression, IPS indépendant et différence exhaustive ;
- 64 tests de régression V36/V35/V34/V33/V29/boy-girl : **74 tests réussis** au total ;
- parcours Snes9x complet réussi dans les deux profils, sans nouvelle différence inattendue ;
- 504 captures de recherche sur quatorze temporisations : aucun coup critique naturel obtenu, donc la scène réelle « COUP CRIT! » reste à valider ;
- aperçu graphique relu : dix caractères nets, sans débordement.

La recherche utilise un état temporaire issu du parcours normal pour accélérer les répétitions, pas un point d'entrée modifié. Aucun état, ROM, WRAM ni cœur n'est publié.

[Sources et constructeur](tools/v37/README_V37.md) · [Essais Snes9x](tests/emulation_v37/RAPPORT_EMULATION_V37.md)
