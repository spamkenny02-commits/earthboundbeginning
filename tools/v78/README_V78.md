# V78 — checkpoint du lot de 150

V77 reste publiée. V78 compte 99 sources distinctes dans 137 plages, cible 150 ; registre exact dans batch_ledger.json et REPRISE_TRADUCTION.md. Les variantes contextuelles de Sell, Oui/Non répétés et profils sont dédoublonnés.

build_v78.py construit successivement le groupe PNJ, medical_stage.py puis remaining_stage.py. Le dernier module copie cinq scripts superposés à des sprites dans la banque25 sans en modifier un octet. Ses cinq redirections sont gardées par un inventaire exhaustif de leurs pointeurs explicites. Les mots, commandes et définitions de choix restent entiers dans les copies. Les quatre devis du train sont parcourus depuis leur script parent ; les appels directs sans contexte sont exclus des preuves.

Construction privée : python3 tools/v78/build_v78.py --rom CHEMIN_PRIVE --out patches
Registre : python3 tools/v78/update_ledger.py
Tests : python3 -m unittest discover -s tools/v78 -v
Tests complets : définir EARTHBOUND_ROM au chemin privé.
Vérifications RGB : python3 tools/v78/verify_display.py et python3 tools/v78/verify_remaining.py

Les 146 paires médicales certifient exactement le checkpoint de 81 textes. Les 166 paires de tests/emulation_v78_remaining certifient le checkpoint actuel : 66 changements textuels, 37 060 images échantillonnées. Tests complets : 12 V78 réussis ; hors ROM, 7 réussis et 5 ignorés. Les captures médicales sont vérifiées contre leur ancien IPS reconstruit, les captures restantes contre l'IPS final.

Les probes utilisent ServiceSession, avec préparations natives flag0339, flag0376 et don AB explicitement déclarées. Aucune écriture WRAM directe. Les devis et refus sont validés, aucun voyage certifié ; les branches de retrait/remise ne prouvent pas de transfert bancaire. Hôtel : salutation seulement. Youngtown : phrase affichée, animation suivante hors contexte ; Papa et Crois en nous statiques. Les menus généraux restent pour la phase suivante.

collect_evidence.py --remaining enregistre les PNG et rapports dans tests/emulation_v78_remaining ; les dépendances et sorties binaires privées restent hors dépôt. La fenêtre des devis du train est limitée à y126, les autres à y98. Les séquences corrigées et les sorties retenues sont indiquées dans REPRISE_TRADUCTION.md.

audit_active_text.py ajoute les mots courts omis (Buy/Sell/Welcome/Bye/Care/Daddy/Believe). Ses 237 candidats incluent des données héritées et des aides sans usage établi. Ne pas traduire pour atteindre artificiellement 150. L'alias médical 0911F0 reste à qualifier.
