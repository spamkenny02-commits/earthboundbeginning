# V78 — commandes d'objets, aides et reprise du casier

21 octobre 2026 : **137/400 sources distinctes**, 175 plages comptées. Huit nouvelles sources depuis129 ; deux corrections supplémentaires du message de PV ne sont pas comptées comme nouvelles traductions, car une copie du même texte avait déjà été traduite en V43. Un commit local intermédiaire a préservé l'intégration avant les contrôles d'écran. Même lot, aucune nouvelle petite release.

| Offset | Source nouvelle | Français |
|---|---|---|
| 38E834 | Use | Util. |
| 38E83A | Eat | Aval. |
| 38E840 | Give | Donne |
| 38E846 | Drop | Jette |
| 38E84C | Help! | Aide |
| 05554F | The Machine that Opens Doors… | Cette machine ouvre |
| 055565 | especially when you have a slightly bad key… | les portes malgré une clé tordue. |
| 055D8B | A key to a regular locker. | Clé d'un casier. |

Les chaînes sources exactes, offsets et variantes sont dans tools/v78/batch_ledger.json. Les marqueurs de dialogue et ponctuations sources sont conservés dans les fixtures. Le message natif 2F69A1 devient « Ninten : PV au max ! » via deux fragments (2F69A5 et2F69AC), sans changer son nom calculé, ses commandes, pauses ou effets. Les champs d'objet AC/CD gardent leurs pointeurs d'aide originaux055546/055D82.

## Lecteur et largeur

Le lecteur 65816 à01369D charge l'adresse E834 puis la banque F8. La suite `TYA / STA04 / ASL / ADC04 / ASL / CLC / ADC06` calcule l'adresse de la case `F8:E834 + 6×index`. La boucle s'arrête à l'index5. La fenêtre dispose de cinq chaînes terminées par00, six octets chacune ; tous les octets du lecteur et les instructions après38E852 restent identiques. Aucun changement de routage des actions, de largeur ou de disposition de fenêtre.

La commande de consommation a été inspectée à l'écran : « Mange », puis « Mang. », étaient tronqués par la largeur graphique de cette fenêtre, malgré leur conformité aux six octets. Le libellé final « Aval. » abrège Avaler et tient entièrement. « Util. » abrège Utiliser ; « Donne », « Jette » et « Aide » restent lisibles. Aucune allocation supplémentaire.

## Scénarios

Tous les scénarios partent des états privés de l'hébergement. La préparation native est déclarée : dons d'objets, recrutement temporaire d'Ana pour le transfert, téléportationD1 pour les seuls casiers. La sonde appelle uniquement le retour vide38B550 ; les aides, les actions et les racines des casiers sont atteintes par les menus et la manette. Aucune écriture directe en WRAM. Le trajet initial complet et le recrutement naturel ne sont pas certifiés.

- Papier froissé : passage par la porte existante et utilisation ordinaire de la Machine sur le casier PNJ606 ; papier reçu et visible au sac.
- Sac plein puis reprise PNJ608 : carte, Machine et douze biscuits ; refus, consommation d'un biscuit par la commande de consommation, message de PV maximum, nouvel usage de la Machine, Fusée-jouet en kit finalement au sac.
- Aides AC/CD : ouverture ordinaire du menu d'objet, sélection Aide et pagination ; textes français et titres relus.
- Jette : Papier froissé retiré, retour au menu puis réouverture de l'inventaire pour inspection.
- Donne : sélection ordinaire de Ninten, objet Papier froissé, destinataire Ana ; absence chez Ninten et présence chez Ana vérifiées sur les captures finales.

Les premières sondes exploratoires avaient rencontré un casier vide à la place des PNJ606/609, et une sélection de personnage avait initialement visé l'ours d'Ana. Elles ne sont pas retenues comme preuves de ces objectifs. L'alignement606 et le transfert ont été corrigés et rejoués. **PNJ609/Bracelet claquant reste à valider.**

## Validation et restes

Résultat final : **28 tests V78 réussis avec la ROM privée**, **132 paires**, **60 changements limités aux deux fenêtres textuelles**, **34 084 images échantillonnées**. Vingt-six captures clés relues dans les deux profils : les cinq libellés tiennent entièrement, les deux aides sont lisibles, les inventaires confirment réception, transfert et retrait. Les premières variantes de sondes et de libellés ne sont pas les captures publiées.

Les preuves finales sont tests/emulation_v78_actions : mêmes préparations et entrées de manette sur V77 et V78, deux profils. La comparaison autorise seulement la fenêtre de dialogue `[104,8,248,98]` et la liste des commandes `[8,8,56,110]` ; toutes les autres régions doivent être identiques. Cette seconde fenêtre commence bien à y8 dans l'écran natif ; le premier masque commençait à y32 et excluait par erreur le premier libellé. PNG, scripts et traces sémantiques publics ; ROM, cœur, états et dumps restent privés.

Les IPS contiennent403 enregistrements supplémentaires par rapport à V77 : cinq écritures d'aide/PV et cinq libellés depuis le précédent checkpoint393. Registre et SHA256 finaux : tools/v78/validation_v78.json. Les anciennes captures des casiers restent liées exactement à leur ROM129 via un préfixe du patch, les nouvelles captures à la ROM137.

Suite concrète : PNJ609 et autres flags, trajets naturels, autres menus et aides accessibles, dialogues/écrans de fin, générique/textes graphiques, puis relecture exhaustive documentée. Huit sources pertinentes ont été traitées ; le jeu restant n'est pas inventorié exhaustivement et rien n'est ajouté pour gonfler le lot à400. Traduction complète et relecture complète ne sont pas certifiées.
