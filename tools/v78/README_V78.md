# V78 — checkpoint du lot de 150
V77 reste publiée. Ce répertoire contient 81 traductions distinctes sur une cible de 150, implantées dans 94 plages. Le registre batch_ledger.json et REPRISE_TRADUCTION.md donnent les textes source, le français et chaque offset.

build_v78.py vérifie la ROM source et les IPS V77, construit le groupe PNJ puis appelle medical_stage.py pour les services médicaux. medical_translations.json contient aussi une entrée bloquée qui n'est pas comptée : 0911ED, pointeur intérieur 0911F0. Les allocations proviennent de safe_storage ; aucun déplacement aveugle d'alias. Les sauts de texte préservent les mots entiers ; les définitions de choix déplacées comprennent leurs commandes 19 02 et 02. Les commandes natives sont comparées après dépliage des ponts.

Construction privée : python3 tools/v78/build_v78.py --rom CHEMIN_PRIVE --out patches
Tests hors ROM : python3 -m unittest discover -s tools/v78 -v
Tests complets : définir EARTHBOUND_ROM au chemin privé avant la commande précédente.
Vérification RGB : python3 tools/v78/verify_display.py

tests/emulation_v78/probe.py exécute quinze cas par profil à partir des états post-repos. collect_evidence.py ne copie que les PNG et les rapports ; les états, ROM et dumps restent privés. Résultats : 146 paires, 90 différences textuelles, 39 412 images échantillonnées. La fenêtre du choix de soins s'étend jusqu'à y126 ; les autres sont limitées à y98. Les accès initiaux sont tous forcés. Maladies, soins effectifs, rencontre naturelle et lancement de fusée ne sont pas certifiés par ces essais.

audit_active_text.py étend l'ancien audit aux appels transitifs et aides d'objets. Ses 264 candidats incluent des données héritées : qualifier les usages avant traduction. Continuer le même lot et garder les menus généraux après les textes/services.
