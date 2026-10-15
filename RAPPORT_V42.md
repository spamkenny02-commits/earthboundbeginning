# V42 — messages d'actions utilisant le dictionnaire anglais

Base publiée et relue : V41, commit `84afcfa90e264cfb1bdc3cd96fa18abb323ef410`.

## Résultat

**100 scripts révisés, avec 187 nouvelles occurrences de fragments français**, correspondant à 169 fragments anglais distincts. Le lot concerne des messages hérités d'actions, d'états et d'utilisation d'objets, référencés par la table des actions du remake. Les quatre raccords retirés et les 92 fragments neutres conservés ne sont pas comptés comme nouvelles traductions.

Le message anglais d'utilisation de la carte bancaire observé en V41 devient français. Les messages de garde, sommeil, attaques, souffles, spores et autres actions du lot sont également intégrés. Les menus ne sont pas modifiés.

## Compression et références

La recherche en texte simple ne trouvait pas la phrase complète de la carte parce qu'elle contient des codes de dictionnaire `15/16/17`. Le constructeur vérifie les 768 entrées source et conserve les octets et pointeurs des 234 entrées utilisées dans les fixtures. Il développe les tokens dans les plages textuelles, puis construit des copies françaises non compressées. **Aucun mot ni pointeur du dictionnaire partagé n'est modifié.** Les commandes de contrôle restent intactes.

Les 229 références raccordées sont prouvées : 109 champs de la table des actions du remake (`368211–369549`), 108 champs de la table héritée (`157B68–158EA0`) et 12 opérandes de commandes reconnues et fermées. Les deux tables ont des enregistrements de 12 octets, champ texte à +4.

Dix adresses littérales supplémentaires visent des intérieurs de texte, sans preuve suffisante d'un usage par l'interpréteur. Elles ne sont pas réécrites. Les sources anglaises restent intactes, ce qui conserve leur comportement éventuel. Il n'est donc pas affirmé que toutes les références littérales vers ces banques sont francisées.

Les IPS autonomes ajoutent chacun 329 enregistrements : 100 copies et 229 pointeurs. Tous les enregistrements et octets antérieurs de V41 sont préservés ; aucun ancien opérande n'a besoin d'être remplacé cette fois. Les réserves sont nulles dans la source et V41, sans cible HiROM ni collision IPS. Les implantations accents et ASCII sont identiques.

## Vérifications

**141 tests locaux réussis** : 17 V42 et les 124 contrôles V41 à V29/boy-girl précédents. Les contrôles de recompression V36/V37 dépendant de CoilSnake ne sont pas réexécutés ; leurs tests hors ligne et la préservation de leurs données sont vérifiés.

Les tests V42 couvrent la provenance des sources et du dictionnaire, le décodage français indépendant, la suppression des seuls tokens textuels, les commandes conservées, les références prouvées et laissées intactes, les réserves, les IPS indépendants et les différences exhaustives.

Le parcours normal Snes9x 1.63 est conforme dans les deux profils jusqu'à l'image 25 803. Les seules différences avec V18 restent les deux images VICTOIRE attendues depuis V36.

Deux nouveaux messages sont également **relus dans les deux profils par leurs commandes normales**, sans patch de test, injection d'inventaire ni écriture WRAM :

| Cas | Chaîne vérifiée | Copie française |
|---|---|---|
| Carte bancaire possédée au début | Objet 177 → action 197 → champ `368B51` | `09FBF2` → `2518BC` |
| Parer contre la première lampe | Action 8 → champ `368275` | `2F84C6` → `25A7A0` |

La fenêtre de carte bancaire affiche la phrase française complète sur trois lignes, avec les accents attendus. Le combat affiche intégralement « Ninten reste sur ses gardes. ». La pagination, les glyphes et les noms sont lisibles sur ces quatre cas. Les captures sont conservées dans le rapport d'émulation.

**Limite : l'accès effectif et l'affichage des 98 autres scripts ne sont pas validés.** Les tables conservent des entrées héritées ; une référence depuis la table du remake ne démontre pas à elle seule qu'une action est accessible au cours de cette version du jeu. Les routines de pronoms partagées et les textes propres à l'ancien scénario ont été laissés hors de ce lot.

## Fichiers

- [Constructeur, traductions et méthode](tools/v42/README_V42.md)
- [Manifeste et empreintes](tools/v42/validation_v42.json)
- [IPS accents](patches/EarthBound_Beginnings_FR_v42_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v42_ascii.ips)
- [Rapport et preuves Snes9x](tests/emulation_v42/RAPPORT_EMULATION_V42.md)

Aucune ROM, aucun état d'émulateur ni coeur n'est publié.
