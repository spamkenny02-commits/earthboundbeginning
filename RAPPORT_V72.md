# V72 — réserve après coursier et reliquats

V70/V71 validaient le retrait ou la réception d'objets dans l'inventaire, mais la réserve n'avait pas été rouverte après le coursier. Cet audit chaîne un nouvel état privé après son départ et une consultation du stockage, sans réinsérer les objets attendus. **Le patch V71 reste inchangé : aucun nouvel IPS V72.**

## Portée des essais

Trois cas dans les profils accents et ASCII :

| Cas | Première phase | Consultation suivante |
| --- | --- | --- |
| Dépôt de trois objets | Dépôt d'une Fiole de sérum, d'une capsule de sagesse et d'une capsule de vitalité | Les trois objets sont présents dans la réserve |
| Livraison de deux sur trois | Deux cases libres, réception Fiole + sagesse | La capsule de vitalité reste seule en réserve |
| Livraison d'un sur deux | Une case libre, réception Fiole | La capsule de sagesse reste seule en réserve |

Le téléphone complet `35C597` est forcé ; les choix et le transfert utilisent ensuite la manette et le moteur normal. Le coursier arrive après une attente de 600 images, sans appel direct de son script. L'état de passage est sauvegardé après son départ. La deuxième phase recharge cet état et appelle le service complet `34B490` par une autre fixture privée. L'accès au téléphone et au stockage reste artificiel : ce n'est pas un parcours naturel complet.

Après les livraisons partielles, l'inventaire est plein. La deuxième fixture retire donc un Badge Franklin (ID 01) par commande native pour libérer une case avant consultation. Aucun objet du reliquat n'est donné, stocké ou retiré par la préparation. La réserve n'est pas réinitialisée. Après dépôt, aucune préparation intermédiaire. Les empreintes des états de passage prouvent le chaînage des sessions, pas une lecture des objets en mémoire ; les listes affichées constituent la preuve visuelle.

Les premières explorations à cinq touches après livraison partielle restaient dans l'inventaire. Une sixième touche atteint le vrai stockage ; sans case libre, celui-ci refuse en français avant d'ouvrir la réserve. Ces essais exploratoires ne sont pas inclus dans les preuves publiées. Le probe final ajoute explicitement la libération du Badge et conserve les bons déclenchements.

Les inscriptions et dialogues examinés sont français ; les menus d'action anglais restent réservés à la phase menus. Les listes à deux colonnes peuvent tronquer des noms longs dans les limites héritées de la fenêtre ; cet audit ne modifie pas leur mise en page. Les autres personnages, coursiers sur réserve pleine et hôtels restent à vérifier. Aucun 100 % certifié.

## Reproduction et sauvegarde

Six chaînes dans les deux profils, **12 sessions, 174 captures et 58 928 images échantillonnées**. Les empreintes des 174 PNG/RGB sont vérifiées ; la relecture visuelle se concentre sur les **24 captures de consultation** et les **12 captures d'arrivée/départ du coursier**, soit 36 images. Les autres captures gardent la provenance de la commande et du transfert déjà relus en V70/V71. Les six tests V72 passent avec la ROM privée, ainsi que les quatre tests V71 : **10 tests ciblés réussis**. Sans ROM, le test privé V72 est explicitement ignoré. La suite historique complète n'est pas relancée pour cet audit qui conserve exactement les IPS V71.

Voir [les outils V72](tools/v72/README_V72.md), [résultats accents](tests/emulation_v72/results_accents.json) et [ASCII](tests/emulation_v72/results_ascii.json). Seuls les PNG, les traces de pointeurs utiles et les empreintes sont partagés. ROM, cœur, états et dumps restent privés. Le lot est sauvegardé par commit local et checkpoint `work/v72-courier-storage` avant publication sur main.
