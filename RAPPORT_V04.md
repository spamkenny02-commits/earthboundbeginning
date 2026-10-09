# Traduction française v04

599 entrées intégrées, contre 473 en v03 : 348 libellés, 231 blocs ordinaires, 15 routines compressées, 3 routines déplacées et 2 fragments d’introduction. La traduction reste partielle. Six propositions sont exclues faute de place.

## Corrections et ajouts

- Gain d’expérience : suppression du « e » parasite avant le nom et après EXP.
- Attaques, dégâts, esquive, absence d’effet et attaques ratées : premiers messages natifs en français.
- Questions et examen sans résultat : « À qui ? », « R.A.S. » et « Rien à signaler ».
- Dialogues des vendeurs : achat, vente, équipement, argent et inventaire plein ; vente du canari.
- Premières descriptions PSI : boucliers, rayons, fuite, neutralisation et effets sur la vision. Les nombres et effets suivent l’anglais.
- Tonalités téléphoniques : « Biiiip... ».

## Cause du défaut d’expérience

« ligne arrière » occupait 13 octets au lieu des 12 de « the Back Row » à $045502. Elle écrasait le NUL $04550E, également utilisé comme chaîne vide. Le code à $0186CE charge C4550E par deux valeurs immédiates (`A9 0E 55 85 0A A9 C4 00 85 0C`). Les octets du pointeur ne sont donc pas contigus.

« rang arrière » tient dans l’espace d’origine. L’intégration refuse désormais d’écraser ce NUL ; le vérificateur indépendant contrôle aussi le terminateur et la référence machine.

## Réinsertion

Les routines compressées peuvent contenir les codes 15/16/17, qui produisent du texte à partir d’un dictionnaire anglais. Les traductions en place remplacent ces références par des lettres françaises et des espaces. Le dictionnaire partagé, les commandes, leurs paramètres et leurs positions restent inchangés.

Les phrases d’attaque ne tenaient pas en place. Trois routines fermées ($2F848C, $2F84A7, $2F84B6) sont déplacées dans la zone nulle $3FF920–$3FF9DF. Les sept références externes et le branchement interne connus sont ajustés. Les anciennes routines restent intactes. Le plan bloque si la source ou les références diffèrent, si la réserve est non vide ou visée par une adresse HiROM littérale, ou si un pointeur intérieur inattendu apparaît. Ce contrôle ne prétend pas découvrir tous les pointeurs reconstruits par le code machine.

Les sources, références et traductions de ces routines sont éditables dans `textes_comprimes_fr.json` et `textes_relocalises_fr.json`. Les 4 nouvelles routines natives d’examen découvertes par les essais y sont également conservées.

## Contrôles

Les deux variantes passent : réapplication IPS indépendante, empreinte de la ROM cible, taille de 4 Mio, checksum, champs et fragments traduits, commandes et références déplacées, conservation des statistiques des ennemis et du terminateur partagé. Les 80 glyphes accentués sont contrôlés. La ROM source reste inchangée.

Un nouveau démarrage de chaque variante confirme le premier combat, le gain d’expérience sans caractère parasite et le retour à la maison. Les reprises depuis les états de ces mêmes ROM confirment les attaques, dégâts, l’examen « R.A.S. » et le dialogue de la sœur sur l’oreiller vivant. Les essais limités sous Snes9x 2010 sont décrits dans `tests/rapport_emulation_v04.json`. Les captures proviennent du framebuffer réel de l’émulateur. Les rapports binaires conservent `runtime_validated: false` : ils ne certifient pas une partie complète.

## À poursuivre

Le scénario, les graphismes anglais, les autres types de combats, les effets de statut et les opérations des boutiques/PSI restent à traduire ou à tester. L’écran titre et les crédits ne sont pas traduits. Les menus de saisie des noms n’ajoutent pas encore les lettres accentuées au clavier.

Les cinq libellés No, Beam, Sick, Cold et Sing restent anglais dans les champs trop courts. Le bloc du canari $371E94 reste exclu : son choix « No » ne peut pas être allongé avec les pointeurs intérieurs actuels. Les propositions françaises sont conservées pour une prochaine réinsertion.

Les essais téléphoniques ne valident pas encore la sauvegarde ni le chargement d’une partie.
