# V52 — Ellay et réponses de livraison

16 nouveaux fragments dans six contextes, dont 14 répliques ou suffixes lexicaux et deux onomatopées. Ils occupent 15 segments privés : l'un regroupe deux nouveaux fragments, un autre reprend un début déjà français. Les menus restent pour la suite ; la traduction reste partielle.

## Changements

- Club d'Ellay : compliment sur la chanson, « Dis... », menace, rire, compliment de Teddy, prénom, exclamation, proposition d'aller à la montagne, accord et offre d'aide.
- Appel du père : salutation et demande d'appuyer sur A.
- Pizza : demande de commande, remerciement de paiement et réponse pour argent insuffisant.
- Suffixe protégé : « Amour et paix, ouais! ».

La réponse pour argent insuffisant vient de la routine héritée `064CC9`, effectivement appelée dans l'essai de livraison depuis `35E4E9`. Elle affichait encore une phrase anglaise en V51. La recherche examine les destinations de commandes, y compris les anciennes banques ; les nombreuses descriptions héritées d'EarthBound ne sont pas comptées comme textes actifs du remake sans vérification supplémentaire.

## Conservation des adresses

La technique V51 est étendue aux segments de texte séparés uniquement par une commande d'attente `10`. Chaque segment reçoit un saut long de cinq octets vers une copie privée ; celle-ci conserve les attentes et revient par saut à la commande originale suivant le segment. Aucun appel ni nouvelle entrée de pile n'est créé.

Pour `35188B`, le préfixe français « Amour et paix, » à `351879` fournit la place du saut. Le court suffixe anglais et toutes ses entrées intérieures restent inchangés ; le chemin commençant à `351879` affiche la copie française. Les neuf opérandes de son appelant `3517D7` restent identiques. Le préfixe déjà français n'est pas compté comme nouveau fragment.

De même, le rire à `350BEF` et le compliment qui suit sont copiés ensemble. La cible intérieure à `350BFF` reste protégée. Ces chemins secondaires conservés peuvent encore afficher l'ancien texte anglais.

Le constructeur valide les frontières dans les contextes V51 complets et n'accepte entre deux fragments que des commandes `10` entières. Les autres commandes sont refusées. Les octets après les cinq premiers restent inchangés ; aucune occurrence littérale d'adresse intérieure n'est réécrite. Les copies occupent des plages nulles des banques de traduction 25/32, sans cible littérale et sans enregistrement IPS antérieur. Les 30 nouveaux enregistrements IPS s'ajoutent à ceux de V51 ; le dictionnaire partagé est inchangé.

## Validation et limites

357 tests locaux réussis, dont 22 V52 : reconstruction exacte, réserves, collisions, débordements, refus de commandes non permises, trajet des sauts, conservation des commandes et des entrées intérieures, préfixe français et neuf appels préservés. Les suites exécutées sont dans `tools/v52/run_regressions.py` ; les anciens tests graphiques V36/V37 nécessitant CoilSnake ne sont pas inclus.

Les 212 captures du parcours normal Snes9x sont identiques à V51. Dix-sept cas contrôlés par variante lisent les quinze segments, l'appelant des amoureux et la livraison. Les retours aux lignes suivantes, le prénom dynamique et la réponse d'argent insuffisant sont visibles. Voir [le rapport et les planches](tests/emulation_v52/RAPPORT_EMULATION_V52.md). Ces appels contrôlés ne valident pas l'accès naturel à la scène du club, le combat, le recrutement ou tous les embranchements.

Trois fragments reportés par V51 restent intacts : `33F3EE` (maison hantée), `3609EB` (adieu), `35000E` (ascenseur). Cela ne constitue pas un inventaire de tout l'anglais restant. Les choix et libellés de menus, les textes de débogage et les graphismes restent hors de ce lot.

## Application

Appliquer un seul IPS V52 à la ROM originale USA 1.2 de 4 Mio, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

[Patch avec accents](patches/EarthBound_Beginnings_FR_v52_accents.ips) · [Patch ASCII](patches/EarthBound_Beginnings_FR_v52_ascii.ips) · [Empreintes exactes](tools/v52/validation_v52.json).

Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.
