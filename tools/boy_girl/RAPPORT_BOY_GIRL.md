# Audit de la routine boy/girl — V26

Audit du 14 octobre 2026. Base vérifiée: V26 accents et ASCII, construits sur la ROM originale USA 1.2 (SHA-256 contrôlé). Aucun IPS ni ROM modifié par cet audit.

## Constat binaire

La routine de dialogue est à l'offset `387B05` (adresse SNES `F87B05`). Elle occupe 20 octets, jusqu'à `387B19` exclu:

```text
19 10 01 | 0B 02 | 1B 03 14 7B F8 00 | 92 9F A9 02 | 97 99 A2 9C 02
```

Les deux sorties sont `boy` (3 octets, à `387B10`) et `girl` (4 octets, à `387B14`). Chacune termine par `02`. La branche conditionnelle vise exactement le début de `girl`. Sa référence interne est à `387B0C`; aucune autre référence HiROM littérale intérieure n'a été trouvée. La routine originale est identique dans les deux ROM V26 résultantes.

## Trois appels partagés

| Pointeur | Script appelant | Phrase concernée |
|---|---|---|
| `33FAA8` | `33FA7D` | Oh, you're such a charming ... |
| `33FC1F` | `33FBDD` | What a brave ... you are! |
| `352FE6` | `352FC3` | You are a school... aren't you? |

Les trois pointeurs sont précédés du code d'appel `08` et restent inchangés dans V26. Le catalogue et les octets de la ROM concordent sur ces appels.

## Interprétation et limite de validation

La liste de commandes du projet [Mother2GbaTranslation](https://github.com/jeffman/Mother2GbaTranslation/blob/master/tools/ScriptToolGui/m12-codelist.json) décrit les codes EarthBound associés: `19 10` sélectionne un identifiant dans une position de l'équipe, `0B` teste son égalité avec la valeur donnée et `1B 03` branche lorsque le résultat est vrai. En appliquant cette sémantique aux octets présents, l'ID retourné égal à 2 mène à `girl`; les autres valeurs mènent à `boy`. Cela compare un ID, pas une propriété générique de genre.

Le petit modèle des commandes confirme boy/girl pour les résultats de sélection 1/2/3/4. Il ne simule pas la disponibilité des personnages ni leur état KO. Il ne constitue pas un essai natif du moteur sous Snes9x avec Ana en tête. Cette couverture est marquée explicitement comme non effectuée dans le manifeste.

## Problèmes de traduction à traiter ensemble

Les textes observés dans V26 sont encore hybrides: `Oh, quel charmant` + boy/girl, et `Quel brave` + boy/girl + `tu fais!`. La phrase d'école est intégralement conservée en anglais, conformément à l'exclusion V25.

Le français ajoute une contrainte: `school` + `boy/girl` compose schoolboy/schoolgirl en anglais. Une traduction commune garçon/fille ne suffit pas à construire écolier/écolière, ni à accorder les deux autres phrases.

`garçon` nécessite 6 octets et `fille` 5, contre 3 et 4 disponibles. Le test d'écriture directe démontre l'écrasement du retour `02`. Il faut donc déplacer les sorties ou la routine, ajuster sa branche interne et contrôler tous les appels. Les anciennes données et alias doivent être conservés ou redirigés explicitement.

Une piste cohérente est une routine garçon/fille pour les deux premiers dialogues avec des formulations telles que «Oh, quel amour de ...» et «Bravo, brave ...!», plus une variante scolaire un écolier/une écolière. Ce plan est une proposition technique, pas un patch livré ou testé.

## Tests exécutés

8 tests réussis: empreinte de la source, octets et retours, branche intérieure, trois appels littéraux, modèle des quatre IDs, préservation des deux profils V26, refus de la substitution française directe et maintien de la phrase scolaire exclue.

```sh
python3 tools/boy_girl/audit_boy_girl.py --rom '/chemin/original.sfc'
ROM_PATH='/chemin/original.sfc' python3 -m unittest discover -s tools/boy_girl -p test_boy_girl.py -v
```

Résultats structurés: `validation_boy_girl.json`. La V26 reste le patch courant. Aucun nouveau segment français intégré par cet audit.

## Contrôle de la V27 arrivée pendant la reprise

La publication V27 (`33a09f8`) est conservée et intégrée à la reprise. L'audit est également exécuté sur ses deux IPS: la routine et les trois appels restent identiques à la source. Les mêmes fragments d'école restent en anglais et les deux autres phrases restent hybrides. Le manifeste contient donc quatre profils audités (V26/V27, accents/ASCII). Les huit tests ont été réexécutés sur cette couverture élargie. Aucun patch V27 n'a été modifié.
