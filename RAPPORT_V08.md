# Traduction française v08 — maire, Pippi et audit

**752 entrées intégrées**, contre 718 en v07 : 32 dialogues supplémentaires et deux notifications communes. Le lot couvre la demande du maire, sa récompense, ses autres répliques, la rencontre de Pippi, ses réponses, son cadeau, le retour vers la ville et plusieurs habitants de Podunk.

## Intégration

Les textes restent en place et les commandes de quête, les montants, les noms variables et les paramètres d'objets sont conservés. Certaines phrases sont abrégées pour tenir aux positions d'origine. Quatre choix `No` restent anglais dans les dialogues nouvellement ajoutés ; `Oui` tient dans les trois octets de `Yes`, mais les trois octets de `Non` dépasseraient ceux de `No`. Les six entrées déjà exclues en v07 restent exclues.

Le vrai départ du dialogue de récompense du maire est `3601FC`, référencé par la commande à `360038`. Le candidat extrait à `3601F7` commençait au milieu d'une commande. La traduction utilise l'entrée confirmée et la conserve dans `sources_complementaires.json`.

La notification commune de réception d'objet, appelée pendant le cadeau de Pippi, utilise un texte bref de type `(Ninten + 1 Badge Franklin.)`. La variante donnant l'objet à un autre personnage est préparée sous la forme `(Ninten : Badge Franklin à Ana.)`. Seule la première est observée dans l'essai isolé ; l'attribution à un autre allié reste à tester. Les noms et choix de destinataire restent ceux du moteur.

## Outil

`atelier.py construire` produit maintenant automatiquement `audit.json`. Il relève les entrées exclues et les fragments encore identiques dans les champs et dialogues ordinaires préparés. Les noms propres et symboles peuvent légitimement rester identiques : le relevé demande une relecture, sans les compter tous comme anglais résiduel. Il ne couvre pas l'ensemble des formats de la ROM.

Les rapports de construction portent les empreintes des sources de traduction. `atelier.py auditer` refuse un rapport périmé si ces sources ont changé. Le test vérifie ce refus, la détection d'un fragment inchangé, l'import CSV partiel et les six refus déjà présents. Les tests d'encodage et d'appels du téléphone passent aussi.

## Contrôles et émulation

Les deux variantes passent les contrôles indépendants des 752 entrées, les checksums, l'application IPS et la conservation des positions et commandes. Le cœur d'émulation est snes9x2010 `fe690dd321fa5a46b5234a2bde089d2518c62b0e`.

Les deux ROM finales sont rejouées depuis une nouvelle partie jusqu'au premier combat, sa victoire et le retour à la maison. Quatre dialogues sont également déclenchés directement dans chaque variante : demande du maire (`36002E`), récompense (`3601FC`), rencontre de Pippi (`380F4C`) et cadeau (`38104C`). Les captures montrent les textes français, les noms variables, les choix `Oui / No` et la notification d'objet.

Ces entrées isolées détournent six octets de « À qui ? » dans des ROM de test distinctes. Elles ne valident pas le parcours normal, les calculs de récompense ni les conditions de quête. Le scénario de retour et recrutement de Pippi, déclenché depuis la maison sans la scène du cimetière, aboutit à un écran noir. Cet essai artificiel ne permet pas de conclure sur le recrutement normal. Une vérification au cimetière avec les bonnes entités et conditions reste nécessaire.

Les ROM, états, SRAM et le cœur ne sont pas distribués. Le son, les branches de groupe et une partie complète ne sont pas validés. Les graphismes anglais restent à traduire.

## Suite

Tester la rencontre et le recrutement de Pippi par le parcours normal, résoudre les libellés courts et poursuivre les dialogues du cimetière et du zoo. La v08 contient les patchs, les sources, le CSV, l'audit, les rapports et les captures des essais.
