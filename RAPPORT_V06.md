# Traduction française v06 — intégration expérimentale

**674 entrées intégrées**, contre 671 en v05 : 365 champs, 274 dialogues ordinaires, 30 blocs comprimés, trois blocs déplacés et deux textes d'introduction. Six propositions restent exclues, faute de place.

Le dialogue financier du père et le message de manque d'argent sont traduits ; le contact Dad devient Papa. La conversation après sauvegarde utilise désormais « ta maman ». Quatre appels propres au téléphone pointent vers des sous-programmes français : ton papa / le papa de [nom], toi / [nom], tu as / vous avez, ta maman / la maman de [nom]. Les commandes de sélection du personnage et du groupe reprennent les conditions originales. Les sous-programmes anglais partagés et leurs autres appelants restent inchangés.

## Contrôles des fichiers

Les deux variantes passent la reconstruction, le contrôle indépendant des 674 entrées, la réapplication IPS, les sommes de contrôle et la prise en charge d'un en-tête copieur. Le profil accents vérifie 80 glyphes dans cinq polices. Les 116 fragments concernés gardent leurs positions. Les tests d'encodage conservent les suffixes PSI et refusent les commandes ; le test des appels refuse une position variable, un opcode différent ou une mauvaise cible originale.

La réserve 3FF550–3FF5F4 est vide et sans référence HiROM littérale dans la source. Les quatre cibles d'appel et les branchements des nouveaux sous-programmes sont contrôlés. Les références par assemblage d'adresse ou par calcul indirect ne font pas l'objet d'une preuve exhaustive. Les opcodes des dialogues restent identiques ; les quatre arguments d'appel sont explicitement remplacés et consignés dans les rapports.

## Essais dans l'émulateur

Cœur snes9x2010, révision fe690dd321fa5a46b5234a2bde089d2518c62b0e. Les captures sont des images réelles 256 × 224 ; les sessions indiquent l'empreinte exacte de leur ROM. L'interface de test ne restitue pas le son.

- Sur les deux ROM finales, nouvelle partie, première victoire contre la lampe, 1 EXP et retour dans la maison.
- Pour le téléphone, une ROM de test distincte remplace six octets au maximum à 07C588 : « À qui ? » saute vers la conversation du père, ou directement vers le passage financier. Les métadonnées distinguent l'empreinte de la ROM intégrée et celle de la ROM de test. Le script tests/preparer_essai_telephone.py reproduit ce changement.
- Cette entrée isolée confirme, dans les deux variantes, ton papa, les messages de virement et de solde avec nombres variables, l'expérience requise, Sauver / Rien, merci, la confirmation, Suite / Dodo et ta maman. Elle ne valide ni les calculs bancaires ni le parcours de quête jusqu'au téléphone. Les branches avec plusieurs alliés sont vérifiées structurellement, pas observées en jeu.
- Le dialogue de sauvegarde isolé enregistre une SRAM native de 8192 octets. Un démarrage des deux ROM finales **sans état instantané**, avec cette SRAM, retrouve Ninten niveau 1 dans les fichiers et recharge la maison. Cela confirme la lecture de cette partie enregistrée ; copies, suppressions et autres emplacements restent à tester.

Les ROM, états, SRAM et cœur d'émulation ne sont pas distribués. Pour rejouer l'essai isolé, produire fin.state avec tests/parcours_debut_v05.json et l'émulateur fourni, créer la ROM de test avec le script de préparation, puis lancer tests/parcours_telephone_isole_v06.json. La sauvegarde utilisée pendant les essais provient d'une nouvelle partie v05 rejouée avec le même cœur ; sa provenance est enregistrée dans les sessions.

## Limites et suite

La traduction reste partielle. Le libellé Level dans la liste des fichiers est encore anglais. Les espaces nécessaires aux positions fixes restent parfois visibles. Tester le téléphone via le parcours normal, les groupes de plusieurs alliés, les véritables virements, les menus PSI, le stockage, les cadeaux, la défaite et la suite du scénario. Les graphismes anglais restent à modifier. Une partie complète et le son ne sont pas validés. Les kits précédents restent inchangés.
