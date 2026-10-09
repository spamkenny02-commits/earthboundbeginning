# EarthBound Beginnings SNES — atelier français, extraction v02

## Résultat de cette étape

La TBL de base est identifiée et une première extraction reproductible est fournie.
La ROM n'a pas été modifiée. Ce dossier ne contient pas de ROM ni de patch de traduction.
Il contient le script anglais extrait de votre fichier et les outils de travail.

- 2 392 blocs candidats de script du remake : 192 731 octets.
- 700 champs textuels de menus et de noms, dont 17 noms de PSI repérés hors des tables attendues.
- 768 entrées du dictionnaire de compression.
- 6 732 blocs et points d'entrée candidats dans les banques héritées d'EarthBound ; certains se recouvrent et leur utilisation reste à vérifier.
- 8 séquences ou alias de texte défilant, dont l'introduction et « 80 years have passed since then ».
- 1 texte littéral intégré dans un autre flux de bytecode.
- 254 parcours partiels conservés pour diagnostic, incluant de nombreux départs dans du code ou des données.
- Inventaire brut complet des fragments détectés dans toute la ROM, y compris les libellés courts.

## Vérification de la v02

Le premier export n'était pas complet. La vérification a révélé des commandes et
paramètres supplémentaires, des textes après l'ancienne limite de recherche, des
séquences défilantes et des noms placés hors des tables attendues.

L'audit indépendant vérifie les octets et le réencodage de **10 601 enregistrements**.
Il retrouve **3 386 fragments longs de prose anglaise** dans la zone du remake et
constate **0 fragment manquant dans les exports** selon ce critère : suite d'octets
`$50–$AE`, au moins 12 lettres minuscules et un espace. Ce critère ne détecte pas
tous les types de texte possibles : ce n'est pas un pourcentage de traduction ni
une preuve que 100 % des textes du jeu ont été extraits.

Le SHA-256 de la ROM reste identique. Aucun patch ni traduction n'a été appliqué.
Voir `extraction/audit_verification.json` pour les résultats et les phrases de régression.

**L'extraction n'est pas encore exhaustive ni validée en jeu.** Un retour à l'identique
des octets prouve la fidélité de l'encodage, pas que le jeu utilise chaque passage,
ni que chaque frontière de bloc est la frontière voulue par les auteurs.

## Fichiers à ouvrir en premier

| Fichier | Utilisation |
|---|---|
| `EarthBound_Beginnings_base.tbl` | Lettres, chiffres et ponctuation de base pour un éditeur hexadécimal compatible TBL |
| `EarthBound_Beginnings_raw.tbl` | Vue de tous les octets ; inconnus conservés sous forme `[XX]` |
| `extraction/TOUS_LES_TEXTES_lecture.txt` | Lecture réunie des six catégories de texte extrait |
| `extraction/TOUS_LES_TEXTES.csv` | Export réuni, avec colonne française vide ; peut contenir des entrées recouvrantes ou héritées |
| `extraction/textes_banques_origine.json` | Blocs des banques d’EarthBound conservés dans la ROM ; utilisation non confirmée |
| `extraction/textes_defilants.json` | Séquences défilantes et redirections conservées |
| `extraction/textes_integres_autre_bytecode.json` | Littéral anglais précédant un flux de bytecode distinct |
| `extraction/inventaire_rom_complet.csv` | Tous les fragments candidats détectés avec l’encodage principal, y compris faux positifs |
| `extraction/inventaire_ascii_direct.json` | Balayage complémentaire en ASCII direct |
| `extraction/dialogues_lecture.txt` | Lecture des blocs, avec dictionnaire de compression développé |
| `extraction/dialogues.csv` | Colonne anglaise, colonne française vide, adresses et tailles ; séparateur point-virgule |
| `extraction/dialogues.json` | Export technique de référence avec commandes et octets originaux |
| `extraction/menus_objets_ennemis.csv` | Noms et champs de menus, avec capacités issues du format de référence |
| `extraction/fragments_remake_complementaires.csv` | Passages supplémentaires à vérifier avant traduction |
| `extraction/scripts_partiels.json` | Décodages interrompus : diagnostic, aucune fin de bloc inventée |
| `extraction/dictionnaire_compression.json` | Entrées des banques de compression `[15 XX]`, `[16 XX]`, `[17 XX]` |
| `extraction/pointeurs_candidats.json` | Occurrences littérales d'adresses 32 bits ; leur rôle reste à valider |
| `extraction/fragments_a_verifier.json` | Inventaire brut de toute la ROM, contenant aussi des faux positifs et du texte hérité |
| `extraction/champs_non_valides.json` | Champs des tables d'origine rejetés car vides, déplacés ou incompatibles |

Une TBL seule ne connaît pas la longueur des paramètres des commandes : les adresses,
flags, nombres et commandes peuvent donc ressembler à du texte dans un éditeur hexadécimal.
Pour traduire, utiliser les exports structurés plutôt que la seule vue hexadécimale.

## Comment la TBL a été trouvée

1. Inspection de l'en-tête SNES à l'offset fichier `$00FFC0` : titre `EARTH BOUND`,
   octet de mapping `$31`, ROM de 4 Mio, sans en-tête de copieur de 512 octets.
2. Une recherche de longues chaînes ASCII directes ne retrouvait pas les dialogues.
3. Le décodage de chaque octet avec `caractère = octet - $30` fait apparaître des phrases
   anglaises cohérentes dans les menus et la zone du remake.
4. Exemples présents dans le fichier : `$71 = A`, `$8A = Z`, `$91 = a`, `$AA = z`,
   `$60 = 0`, `$69 = 9`, `$50 = espace`. Le premier passage de l'export est
   `@Go to her.[13][02]`, à l'offset `$339A85`.
5. L'encodage a été confronté aux fonctions de texte de CoilSnake et aux longueurs
   de commandes de CCScriptWriter. Les paramètres sont conservés en hexadécimal.
6. Vérification indépendante : les 10 601 enregistrements des six catégories
   se réencodent exactement vers les octets originaux, aux mêmes offsets.

`@` est la notation conventionnelle du code `$70` utilisé en tête des lignes.
Les formes exactes de tous les glyphes de ponctuation n'ont pas été vérifiées visuellement.
Les codes spéciaux `$52`, `$8B` à `$8E` et les codes hors alphabet de base sont laissés
en hexadécimal. Les caractères français accentués ne sont pas encore attribués :
ajouter `é`, `è`, `à`, `ç`, etc. demandera une analyse et éventuellement une modification
de la police, pas seulement des lignes supplémentaires dans la TBL.

## Commandes et compression

| Octets | Interprétation du moteur de référence |
|---|---|
| `[00]` | Saut de ligne |
| `[01]` | Nouvelle ligne vierge |
| `[02]` | Fin du parcours de texte ; peut aussi terminer une chaîne chargée en ligne |
| `[03]` | Attente avec invite |
| `[13]` | Attente sans invite |
| `[04 LL HH]`, `[05 LL HH]` | Modification de flags |
| `[08 AA BB CC DD]` | Appel/référence de script |
| `[0A AA BB CC DD]` | Saut de script |
| `[15 XX]`, `[16 XX]`, `[17 XX]` | Texte provenant d'un dictionnaire |
| `[1C ...]` | Affichages dynamiques, dont noms ou valeurs selon la sous-commande |
| `[1F ...]` | Actions du jeu selon la sous-commande |

Les chaînes de dictionnaire sont accessibles par 768 pointeurs à partir de `$08CDED`.
La version lecture les développe ; la version technique conserve les commandes originales.
Cela permet d'éviter de confondre une phrase compressée avec une phrase incomplète.

## Adresses et prudence pour la suite

Pour ce fichier HiROM, les adresses exportées utilisent la fenêtre SNES `$C00000–$FFFFFF` :
`adresse SNES = offset fichier + $C00000`. Exemple : `$339A85 → $F39A85`.
Le script recherche la zone `$339A82–$39FFFF` et ne suppose pas qu'elle contient
uniquement du dialogue : elle contient également du code et des données.

Les entrées sont amorcées par des occurrences de pointeurs, puis parcourues avec
les longueurs de commandes connues. Un parcours s'arrête sur une commande non définie,
une fin de ROM ou une limite de taille. Les entrées imbriquées déjà couvertes par un bloc
plus large sont retirées de l'export principal ; les occurrences de pointeurs restent disponibles.

Le balayage intégral conserve séparément les autres chaînes. En particulier, des
passages d'EarthBound d'origine subsistent dans la ROM : leur présence ne prouve pas
qu'ils sont affichés par le remake. Les offsets de champs issus des tables d'origine
sont aussi des hypothèses : leurs octets sont contrôlés, mais leur utilisation en jeu
reste à confirmer. Les capacités ne représentent pas une largeur d'affichage en pixels.

Les extensions de `1A` sont maintenant décodées à partir de la ROM elle-même :
la routine d'origine est interceptée à `$017B60`, la table de dispatch est à `$38BDD0`
et la lecture des paramètres utilise `$38BE58`. Par exemple, `1A 0C` lit une adresse
ASM de quatre octets ; la routine appelée peut encore consommer des octets dans le
flux de texte. L'extracteur conserve ces paramètres dans le même jeton :
`[1A 0C 34 AA F8 00 1D 03]` et `[1A 0C E5 95 F8 00 01]`. Sans cette précaution,
les paramètres de palette ou de cinématique seraient pris pour des commandes de texte.
Le fichier `outils/commandes.json` décrit les tailles supplémentaires par routine appelée.

Les octets `$C8–$CB` observés dans les menus de train sont conservés en hexadécimal.
Leur forme graphique n'est pas attribuée arbitrairement.

Les banques d'origine contiennent des débuts de blocs remplacés par des sauts vers
le remake. Les octets suivants peuvent être des fragments de l'ancien texte ou de
ses anciens paramètres. L'extraction complémentaire suit donc également les
pointeurs littéraux, au lieu de reprendre aveuglément une lecture linéaire après un saut.
Les erreurs et fragments résiduels restent accessibles dans les fichiers d'audit.

## Relancer l'extraction sous Windows

Python 3 est nécessaire, sans bibliothèque supplémentaire.
Glisser le fichier `.sfc` sur `Extraire_ROM.bat`, ou lancer :

```text
py -3 outils\extraire.py "C:\chemin\EarthBound Beginnings (USA) 1.2.sfc"
```

Sur Linux/macOS :

```text
python3 outils/extraire.py "/chemin/jeu.sfc"
```

L'outil vérifie le SHA-256 de la ROM et refuse une version différente. Il sait enlever
un en-tête de copieur de 512 octets pour cette vérification. Il ne modifie aucun octet
du fichier d'entrée et remplace seulement les fichiers de son dossier de sortie.

## Identité de la ROM analysée

- Taille : `4 194 304` octets.
- SHA-256 : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.
- Nom fourni : `EarthBound Beginnings (USA) 1.2.sfc`.
- La version « 1.2 » est celle annoncée par le nom du fichier, pas une signature interne vérifiée.

## Prochaine étape

Analyser la police et les autres modes de texte, consolider les points d'entrée à partir
des tables réellement utilisées, puis préparer la réinsertion avec relocation et mise à jour
des pointeurs. Tester des écrans courts, des dialogues à variables, les choix et les combats
avant une traduction générale. La comparaison avec la version française NES de Mother
sera effectuée ensuite, comme demandé.

## Références techniques utilisées

- CoilSnake : https://github.com/pk-hack/CoilSnake
  — commit `346cfc753644bc3703b6fc4eaa0a5d6bdcb9bb4a`, fonctions de texte,
  champs de menus et descriptions des tables.
- CCScriptWriter : https://github.com/Lyrositor/CCScriptWriter
  — commit `f021880893f25c787814332b0a8102251bcb0141`, spécification pratique
  des longueurs de commandes et des pointeurs de dictionnaire.
- Source reconstituée du moteur EarthBound : https://github.com/Herringway/ebsrc
  — consultation de l'arbre de commandes `1A` du moteur d'origine, consulté pour distinguer les commandes d’origine des extensions du remake.

L'extracteur fourni ici est un outil autonome de cette étape. Les fichiers de configuration
contiennent des descriptions de formats dérivées de ces références, et ne constituent
pas le code source du remake.

## Relancer la vérification

Après extraction :

```text
py -3 outils\verifier.py "C:\chemin\EarthBound Beginnings (USA) 1.2.sfc"
```

L'audit vérifie aussi les passages manquants de la v01 : dialogues de Maria,
chanson, Escargo Express, introduction, noms PSI et messages de la fin de la zone
compilée. Les textes qui seraient intégralement dessinés dans des images, une police
ou un encodage non identifié ne sont pas couverts par cet audit.
