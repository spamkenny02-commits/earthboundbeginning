# V78 — checkpoint, lot de 150 en cours
81 textes source distincts sont nouvellement traduits par rapport à V77, dans 94 plages physiques. Les répétitions Oui/Non et les deux profils ne gonflent pas le compteur. Le registre exact figure dans REPRISE_TRADUCTION.md et tools/v78/batch_ledger.json. V77 reste publiée sur main ; les IPS V78 sont des checkpoints de travail.

Le premier groupe couvre maison hantée, singes, panneau et refus de la fusée. Les services médicaux ajoutent médecin, infirmière et guérisseur avec leurs messages et choix de soins. Leurs wrappers personnalisés appellent les scripts hospitaliers anglais partagés, omis par l'ancien relevé direct. Une phrase sur le mal du pays demeure bloquée à 0911ED à cause du pointeur intérieur 0911F0 ; elle n'est pas comptée.

Les phrases longues utilisent des ponts dans des réserves nulles protégées. Les chaînes s'arrêtent aux espaces pour éviter les mots coupés à l'affichage. Les choix déplacés transportent la définition entière afin de préserver le rendu des sélecteurs. 61 ponts médicaux et sept définitions Non au total ; allocation 2 378 octets ; 219 enregistrements IPS ajoutés par profil. Le dépliage restitue les commandes originales. Table PNJ, sprites, banque 25 et créneau de probe sont inchangés.

24 tests ciblés V78/V77/V65 passent avec la ROM privée. Les contrôles V78 couvrent la réserve, les pointeurs, les commandes dépliées, les empreintes, le compteur, les entrées du probe et les images. Hors ROM, cinq tests V78 passent et trois sont ignorés explicitement. 146 paires V77/V78 sont comparées en RGB, 90 changent dans les seules fenêtres textuelles ; 39 412 images échantillonnées sur les quinze cas par profil.

Les entrées sont forcées par le jeu depuis un état post-repos, sans écriture directe WRAM. Les scènes ne constituent pas un parcours naturel. Le médecin demande 25 $ pour 20 $ disponibles : refus et manque d'argent sont vérifiés, aucun examen réussi. L'infirmière expose l'hôpital ; le guérisseur affiche ses quatre choix et un devis de dépétrification, aucun soin réel validé. Une explication hospitalière est appelée directement à sa branche intérieure. Le panneau remet nativement le Dentier dans ce contexte contrôlé. La fusée n'est pas lancée. Les autres branches médicales restent uniquement validées statiquement.

Les captures retenues sont issues des sorties finales validated_v78_words et reference_v77_words. Les essais exploratoires avec sélecteurs corrompus ou mots coupés sont exclus des preuves publiées.

Empreintes SHA256 IPS :
- accents : 29339285030ae3983a9b13f4c5d95991cfec8f0b38342b6d026f7f74107a4d75
- ASCII : 9ec1f5dcbdaa7631530dc011bf964512eaac74ef33c927cfc2b321f344664003

Reprise : poursuivre les quelque 69 textes utiles manquants avant publication, en qualifiant les appelants du train, les autres dialogues et les aides d'objets réellement utilisés. Le nouvel audit contient 264 candidats, dont de l'héritage et du débogage ; aucun taux global n'en est déduit. Menus généraux, branches optionnelles et relecture d'un parcours naturel complet restent à terminer. Aucun 100 % annoncé.

Sauvegardes locales intermédiaires : 4ebedd7 puis 3e1b209 ; checkpoint distant visé work/v78-batch150. Ne publier aucun fichier ROM, cœur, état ou dump.
