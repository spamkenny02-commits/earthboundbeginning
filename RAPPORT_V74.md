# V74 — service de revente du PNJ 87

## Corrections

Neuf plages anglaises traduites : question « As-tu un objet à revendre ? » et les quatre sélecteurs Oui/Non du service `387221`. Deux formulations françaises sont également corrigées : « Je te propose donc $29. » remplace le blanc avant le prix ; « Je n'achète pas Carte bancaire. » remplace la fin maladroite « de toi ».

Le pointeur du PNJ 87, champ 9, opérande `202778`, reste inchangé. Sept remplacements fixes et quatre couples saut/définition ajoutent 15 enregistrements à V73. Les quatre définitions « Non » occupent 44 octets de réserve protégée :

| Définition d'origine | Copie protégée | Retour |
| --- | --- | --- |
| `38725F` | `32AABC` | `387264` |
| `3872C8` | `32F304` | `3872CD` |
| `38734B` | `32E02C` | `387350` |
| `3873AD` | `32EC5C` | `3873B2` |

Après dépliage des ponts, les commandes natives sont identiques. Les copies sont hors des anciens enregistrements, des pointeurs connus, des sprites et du créneau privé de test. Banque 25 et sprites restent identiques à V73.

## Validation en émulateur

Quatre scénarios dans chacun des deux profils, avec les mêmes entrées et les mêmes états initiaux que la référence V73 :

- Refus initial : sortie du service.
- Carte bancaire protégée : refus français, choix « Autre chose ? », sortie.
- Vente acceptée : Fiole de sérum visible avant vente, offre de 29 $, portefeuille 20 → 49 $, inventaire final avec carte seule.
- Offre refusée : réponse « Ah, OK. », portefeuille toujours à 20 $. L'inventaire après ce refus n'a pas été rouvert : ne pas en déduire une preuve de conservation de l'objet.

56 captures V74 relues et comparées à 56 captures V73 ; 30 différences, toutes dans la fenêtre de texte `(104,8,248,98)`. Les inventaires de référence restent identiques. 12 044 images échantillonnées côté V74. Les empreintes PNG/RGB, entrées manette et transitions de pointeurs sont dans `tests/emulation_v74/`. 24 tests ciblés réussis avec la ROM privée : V74 (8), régression V73 (8), stockage protégé V65 (8). Reconstruction des deux IPS reproductible.

L'accès au service est **artificiel** : fixture privée redirigeant l'action de carte bancaire vers l'entrée complète `387221`. Un don natif de Fiole (`1D 00 01 70`) prépare seulement les essais de vente. La sélection, le prix, la vente et les refus sont exécutés par le moteur, à la manette. Aucune écriture directe WRAM. L'état initial privé provient d'un repos antérieur, Ninten seul, 30 PV, 10 PP, 20 $, carte bancaire. Ce n'est pas l'ancien état V33 après combat.

La quatrième paire Oui/Non, concernant un objet équipé, est contrôlée statiquement mais n'a pas été affichée dans ces scénarios. Aucun accès naturel au PNJ 87 n'est certifié. Les menus d'objets `Use/Eat/Give/Drop/Help!`, visibles dans la preuve d'inventaire, restent anglais et seront traités dans la phase menus. Aucun taux global ni 100 % n'est revendiqué.

## Patchs

Appliquer un seul IPS directement à la ROM originale USA 1.2, jamais sur un patch précédent.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
| --- | --- | --- |
| Accents | `f5d196d2bc876a7c57e6e1331a4b68ac8bf9bd09d3b27fbc06b239de055b1904` | `3e783dc712b95b78657e4e0aba8faba65e57c6d8ad67bf650e606b46ccf401ec` |
| ASCII | `5d0c6d507bcf2b4fa3226b035f8ef614c73fba458b549aed0295e7d3dac3ff08` | `cdf2c3d37881a3b1facb86f6f994795190ac50a1abf7422d83d69a2dfbe73bf6` |

ROM, cœur, états et dumps restent privés. Les anciennes dépendances V33 ne sont plus disponibles ; la ROM fournie par l'utilisateur a été récupérée à nouveau et son empreinte originale vérifiée. Reprise précise dans `REPRISE_TRADUCTION.md`.

## Suite

Traiter le canari `3861D3`/PNJ 291, puis Pippi `386B63`/319 et les autres candidats historiques de `tools/v73/custom_npc_roots_v73.json`. L'entrée `387221` de cet ancien relevé est désormais traitée ; ce relevé n'est ni récursif ni une preuve d'exhaustivité. Restent aussi objets équipés, variantes multijoueurs, limites du coursier, menus et parcours naturel complet.

Sauvegardes locales initiales : `a6cd3ef`, puis `61fbc28` (polissage). Checkpoint validé destiné à `work/v74-resale-validated`, puis publication sur `main` sans force push.
