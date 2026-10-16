# V46 — reprise avec la ROM et raccords de groupe

Base binaire : V45 (`4e628ac`). La branche `work/v46-prep` est reprise dans l'historique, puis auditée avec la ROM originale fournie. Son empreinte est conforme : `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`, taille 4 Mio. Le cœur Snes9x 1.63 est également disponible dans cet environnement.

## Audit de la préparation

Sur les 100 candidats préparés, **98 scripts ont déjà été modifiés par les versions précédentes**. Les deux autres brouillons sont identiques à leur source : « Hum. » et « Zombie! ». Le constructeur préparatoire aurait refusé la première entrée. La sélection est conservée comme archive ; aucune de ses entrées n'est comptée comme nouvellement intégrée en V46.

Le nouvel audit est enregistré dans `tools/v46/audit_preparation_v46.json`. Les tests préparatoires acceptent les quatre segments composés uniquement d'espaces, en exigeant leur conservation exacte. Le constructeur préparatoire a été remplacé ; il utilisait notamment des offsets absolus du parseur comme des offsets relatifs.

## Changements réellement intégrés

**Deux messages de consommation encore anglais sont traduits** : le chemin individuel `097BAB` et le chemin de groupe `35ECD5`. Le menu Eat utilise bien le chemin individuel dans l'essai natif. Les deux copies françaises affichent « Objet consommé par [nom(s)] : [objet] ». Les commandes, les noms dynamiques et les effets existants sont conservés. Le chemin de groupe utilise la routine française V45 ; son suffixe « ensemble » déjà traduit reste intact.

**Sept contextes français encore liés à la routine anglaise des groupes sont corrigés** : papillon magique, défaite, remise d'objet, disparition de Mary, deux messages d'EXP et ouverture de porte. Ils réutilisent la copie française V45 de `07E6D7`. Cinq formulations deviennent indépendantes du nombre de participants : « défaite », « retour de », « + … EXP » et « porte ouverte ». Ces révisions de textes déjà français ne sont pas comptées comme de nouvelles traductions.

Les routines anglaises globales, les copies françaises V45 et le dictionnaire partagé restent inchangés. Les menus et les choix restent pour leur passe dédiée.

## Intégration et contrôles

Chaque IPS autonome conserve les enregistrements V45 et ajoute **17 enregistrements** : deux copies de messages, trois références vers ces copies, sept raccords de groupe et cinq plages françaises révisées. Les seules écritures en réserve occupent 93 octets (95 avec l’alignement) dans une plage nulle, non ciblée et non couverte par les anciens IPS. Les contrôles vérifient chaque référence et interdisent les écritures hors plages déclarées.

**229 tests locaux réussis** : 207 historiques et 22 V46, dont les trois tests préparatoires corrigés. La reconstruction IPS indépendante, les empreintes, les commandes, le dictionnaire, les anciens pointeurs réparés et l'audit des 100 candidats sont contrôlés. Les tests graphiques V36/V37 nécessitant CoilSnake restent exclus ; leurs tests hors ROM et la conservation de leurs octets sont vérifiés.

Sous Snes9x, le parcours normal passe dans les deux variantes. Par rapport à V45, une seule capture change : le texte de l'EXP, uniquement dans un rectangle de 59 × 11 pixels. Titre, introduction, après-combat, restauration et menu restent identiques. Le menu Eat affiche le nouveau texte complet avec le pain de test ; l'objet est consommé. Les scènes tardives et les groupes de plusieurs personnages restent à vérifier en situation naturelle. [Rapport et captures Snes9x](tests/emulation_v46/RAPPORT_EMULATION_V46.md).

## Livraison

- [IPS avec accents](patches/EarthBound_Beginnings_FR_v46_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v46_ascii.ips)
- [Sources et reproduction](tools/v46/README_V46.md)

Appliquer un seul IPS V46 directement à la ROM originale USA 1.2. La ROM conserve sa taille de 4 Mio. Le fichier reçu reste privé et n'est pas modifié ; aucune ROM, sauvegarde ou fixture de jeu n'est publiée.
