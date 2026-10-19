# V69 — réserve pleine et pagination du stockage

**Audit uniquement : IPS V67 inchangés, aucun IPS V69.** Aucun nouveau texte anglais n'est rencontré dans les messages de ce lot.

## Résultat vérifié dans les deux profils

La réserve est préparée avec 36 Fioles de sérum par les commandes natives de stockage, en trois passages privés. Ninten reçoit aussi une Fiole pour essayer le dépôt. L'accès au service est forcé comme dans les lots précédents ; cette préparation n'est pas un remplissage naturel par 36 dépôts manuels.

Le dépôt est refusé avec « Désolé. Mon casier est plein. ». Le retrait est ensuite ouvert et les **quatre pages sont relues : 10 + 10 + 10 + 6 Fioles = 36 objets visibles**. Les intitulés « Réserve (1) », « Réserve (2) », etc. sont des **numéros de page**, pas des quantités.

Une Fiole de la dernière page est récupérée normalement par les touches ; l'inventaire montre ensuite la carte et deux Fioles. Une Fiole est redéposée normalement. Un nouveau dépôt est de nouveau refusé avec le même message de casier plein. La réserve est rouverte à la fin. Les confirmations restent françaises : « Prends-en bien soin. » et « Cet objet sera bien au chaud. ». La poche reste affichée à 20 $ ; aucune lecture dédiée des champs mémoire d'argent ou d'inventaire n'est utilisée comme preuve de ces effets.

## Preuves et préparation privée

Six sessions (trois passages par profil), **50 captures relues et 10 676 images échantillonnées**. Les cinq tests hors ROM vérifient les opérations autorisées, les empreintes des IPS V67, les liens d'états entre passages, les séquences/traces et les PNG. Un sixième test, avec ROM privée, reconstruit les fixtures et contrôle les ancrages moteur, les sprites et la banque 25. Les empreintes RGB sont recalculables séparément.

Les 575 tests historiques V62 et les 39 tests V63–V68 repassent, ainsi que les six tests V69 : **620 tests réussis** avec les dépendances privées fournies aux suites concernées. Le passage sans ROM exécute cinq tests V69 et ignore explicitement le test privé. Les tests de traces et d'empreintes ne remplacent pas la relecture des captures.

Les opérations de préparation sont `1D 18 70 00` (insertion native en réserve) et `1D 00 01 70` (don natif à Ninten). La convention et la boucle bornée sont documentées dans la source primaire [handler de stockage](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/src/text/ccs/escargo_express_store.asm), [routine de stockage](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/src/misc/escargo_express_store.asm) et [structure de jeu](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/include/structs.asm), révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`. Le comportement dans le remake est confirmé par le refus et les quatre pages réelles, pas déduit de cette source seule.

Les deux premières fixtures insèrent treize objets chacune puis retournent à la carte ; la troisième en insère dix, donne une Fiole et appelle le script complet `34B490`. Leurs wrappers font respectivement 53, 53 et 50 octets dans la réserve de 64 octets `330FC0`. Les seules autres écritures sont les quatre octets de redirection à `368B51`. Les IPS distribués ne contiennent aucune préparation, aucun wrapper ni nouvel octet. Aucun hook assembleur et aucune écriture directe en WRAM.

Les états privés de passage sont sauvés après retour à la carte. L'empreinte de sortie de chaque passage doit être identique à celle rechargée par le suivant. Seules ces empreintes, les traces de curseurs et les captures sont publiées ; pas les états ni les journaux bruts.

La pagination conserve le curseur sur la ligne de changement de page. Le probe publié fait cinq Bas puis A pour passer de la première à la deuxième page, puis A pour les troisième et quatrième pages. Bas revient ensuite au premier objet de la quatrième page. Les explorations utilisant R ou répétant cinq Bas à chaque page n'ont pas été retenues comme preuve de lecture des quatre pages.

## Sauvegarde et limites

Checkpoint `work/v69-full-storage` : `56bbfdd78971750717a258712ac1105b5fe4c716`. Les fichiers privés restent hors dépôt. Une copie locale non suivie de `tools/v68/service_session.py`, identique au blob publié, a été conservée dans `preserved_before_v69` avant la mise à jour Git ; aucun travail existant n'a été écrasé.

La réserve pleine est donc vérifiée dans cette configuration à un personnage, avec objets identiques et préparations artificielles. Restent plusieurs personnages, objets variés, coursiers/transferts Escargo, autres enseignes et parcours naturels. Les scripts ont été appelés artificiellement ; **aucun nouvel accès naturel ni 100 % des textes n'est certifié**. Les menus d'action restent pour la phase suivante.

Captures : [casier plein](tests/emulation_v69/accents/exercise/page_02.png), pages [1](tests/emulation_v69/accents/exercise/page_05.png), [2](tests/emulation_v69/accents/exercise/page_06.png), [3](tests/emulation_v69/accents/exercise/page_07.png), [4](tests/emulation_v69/accents/exercise/page_08.png), [récupération](tests/emulation_v69/accents/exercise/page_11.png), [redépôt](tests/emulation_v69/accents/exercise/page_16.png), [nouveau refus](tests/emulation_v69/accents/exercise/page_19.png).
