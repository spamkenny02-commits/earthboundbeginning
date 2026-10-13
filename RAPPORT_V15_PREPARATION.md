# V15 — préparation, non publiée

La version distribuable reste V14 : 130 segments traduits dans 44 scripts. Aucun IPS V15 n'est prêt.

Le manifeste V14 laisse 12 segments inchangés. Huit phrases disposent désormais de propositions françaises dans `traduction/v15_candidats_a_valider.json`. Quatre éléments sont des noms ou onomatopées conservés.

**V15 : 8 brouillons, 0 segment intégré.** Les références vers l'intérieur de certains segments empêchent une intégration sûre sans analyse des pointeurs de la source.

Contrôles prévus : `tests/verifier_preparation_v15.py` (tailles, encodage, collisions V14). Non effectués : contrôle sur source, aller-retour IPS V15 et essai en émulateur.

Suite : auditer les pointeurs HiROM, puis préparer un lot de dialogues validés et des IPS autonomes.
