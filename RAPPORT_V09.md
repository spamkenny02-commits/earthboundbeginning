# V09 — préparation de la finalisation

**1 095 entrées intégrées et contrôlées**, contre 752 en v08. Ce total comprend des noms propres conservés et des champs hérités dont l'emploi dans le remake n'est pas confirmé. Il ne mesure pas le pourcentage de traduction du jeu.

## Dialogues déplacés et choix français

Les quatre scènes du maire et de Pippi utilisent maintenant des phrases plus naturelles et les choix `Oui / Non`. Le dialogue du canari et son vendeur sont également déplacés. Cela résout le dialogue auparavant exclu et évite de retargeter un pointeur dans un appelant dont les positions avaient changé.

Les routines nouvelles occupent `31F410–31FA9F`, dans une réserve déclarée `31F410–31FAC7`. La source y est entièrement nulle et aucune adresse HiROM littérale ne vise cette réserve. Les trois attaques déplacées restent dans leur ancienne réserve `3FF920–3FF9DF`.

Les nouveaux blocs contiennent les commandes originales. Les branches internes sont dirigées vers les frontières correspondantes des traductions. Les références entrantes au début des blocs sont une liste explicite vérifiée. Les anciens blocs demeurent intacts ; les alias extérieurs pointant au milieu de ceux-ci restent à leur adresse originale. Ils peuvent encore afficher de l'anglais si le moteur les utilise. Les références calculées ou assemblées ne font pas l'objet d'une preuve exhaustive.

Le vérificateur indépendant recalcule les positions des branches traduites, vérifie les références extérieures et confirme que les alias non déplacés restent identiques. Le décodeur accepte les accents seulement lorsqu'on lui demande explicitement de relire un bloc français ; son comportement d'extraction anglaise reste inchangé.

## Noms et champs

338 champs supplémentaires sont préparés : ennemis, objets, destinations, contacts et noms par défaut. Les noms propres et les termes déjà français sont conservés. Les statistiques des ennemis et objets sont contrôlées. Quelques champs fixes nécessitent des abréviations, notamment `Mal.`, `Rh.`, `Ch.` et `M. Itoi`. Les noms de tables héritées sont proposés, sans prétendre que chaque ennemi apparaisse dans ce remake.

Le catalogue des 700 champs extraits indique **699 intégrés et un exclu**. Le libellé `No` à `0BD867` reste trop court pour `Non` ; aucune référence littérale directe n'a été trouvée, ce qui ne prouve pas qu'il soit inutilisé.

## Outil utilisable localement

`atelier_fr.html` permet de charger le CSV, chercher un texte, modifier le français, voir un aperçu de lecture et enregistrer le CSV. Les originaux et identifiants sont conservés. Il détecte les caractères impossibles, les commandes et les suffixes PSI modifiés. Son aperçu ne reproduit pas le rendu du jeu.

Le CSV comprend désormais les routines déplacées. L'import valide toutes les lignes avant la première écriture et sauvegarde les JSON précédents dans `sauvegardes_import/import_...`. Les tests effectuent une modification dans une copie isolée et vérifient la sauvegarde ainsi que la conservation du plan de déplacement.

`Importer_CSV_FR.bat` et `Reconstruire_FR.bat` constituent le parcours Windows. La reconstruction produit les deux variantes, les rapports, le CSV et l'audit. `cataloguer` produit le catalogue et la liste des candidats à examiner. L'éditeur lit ce catalogue sans permettre de l'importer comme un fichier de traduction.

Les formats et événements de l'éditeur sont testés sous Node avec un DOM simulé, puis le CSV produit est validé par l'importeur Python. Le rendu et les téléchargements dans un vrai navigateur restent à vérifier : le binaire de navigateur n'est pas installé ici. Aucun accès réseau n'est effectué par le HTML.

## Essais dans le jeu

Cœur snes9x2010 `fe690dd321fa5a46b5234a2bde089d2518c62b0e`. Les deux variantes finales passent une nouvelle partie, le premier combat, la victoire et le retour à la maison.

Six entrées de dialogue sont testées directement dans chaque variante : les deux scènes du maire, la rencontre de Pippi, sa proposition de rendez-vous, le canari et le vendeur. Les captures montrent les accents, les phrases développées, les noms et les choix français. Trois choix `Non` sont aussi testés séparément dans chaque variante, avec leurs réponses : Pippi reconnaît le courage de Ninten, puis son refus du rendez-vous affiche la réplique sur quelqu'un d'autre dans son coeur ; le maire poursuit sa réponse comme dans la branche originale.

Ces essais utilisent des ROM de test distinctes et des états issus de nouvelles parties. Ils ne valident pas les trajets et conditions du scénario. Le recrutement de Pippi déclenché depuis la maison termine sur un écran noir, comme dans les essais isolés précédents : le parcours normal au cimetière reste nécessaire. Le son, une partie complète et les menus de tous les objets/ennemis ne sont pas validés.

## Ce qui empêche encore une version finale

Le catalogue compte **349 blocs candidats de script intégrés et 2 043 à examiner**. Ces candidats peuvent contenir des faux positifs, des alias ou du texte hérité. Leur usage et leurs frontières doivent être confirmés avant une traduction fiable. Le départ erroné `3601F7` est remplacé par l'entrée de quête vérifiée `3601FC`.

Il reste notamment les textes des autres villes, des lieux et événements, les descriptions et routines encore anglaises, le générique, les graphismes anglais, les alias anciens encore appelés et une validation du jeu complet. **La v09 reste une version de travail ; le jeu n'est pas finalisé.** Le kit comprend l'outil, les patchs, les références nécessaires au catalogue, les rapports et les captures, sans ROM, cœur ou état instantané.
