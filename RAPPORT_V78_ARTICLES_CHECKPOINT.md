# V78 — articles des contenants et stockage Minnie, 21 octobre 2026

Checkpoint du même lot : **119 sources distinctes sur une cible de 150**, 157 plages sources. Zéro nouvelle source dans cette correction de français ; pas de nouvelle release. V77 reste publiée sur main.

Le travail local interrompu a été conservé par commits avant fusion du checkpoint distant. Le module `tools/v78/article_context_stage.py` corrige trois contextes avec six écritures, sans allocation :

| Contexte | Correction et qualification |
|---|---|
| Contenant PNJ1420 | `3803F1 → 32B500`, appel `32B50A` redirigé vers le helper neutre existant `32AA40`. Préfixe « Objet: », point final ; affiche « Objet: Badge Franklin. ». |
| Dépôt Minnie PNJ204 | `36B788 → 36B7D5`, appel `36B830` vers le même helper. Confirmation « Cet objet sera bien gardé. ». |
| Retrait Minnie PNJ204 | `36B788 → 36B9D9 → 36BA13`, préfixe `36BA48` neutre à la place de « Le ». Évite « Le Fiole de sérum ». |

Le classificateur natif reste actif ; seuls deux appelants qualifiés sont redirigés. Helpers partagés, table PNJ, banque25, sprites et copie ancienne `32F120–32F1B2` conservés. Le rôle de cette copie ancienne et du helper `38B587` reste à qualifier. Trois espaces après la puce de retrait gardent la longueur native ; les commandes et leurs positions restent inchangées.

## Validation

20 tests V78 réussis avec ROM privée : écritures exactes, commandes, références intérieures, préservation des zones protégées, empreintes des fixtures et anciens snapshots. IPS reconstruits pour accents et ASCII, 383 enregistrements ajoutés à V77.

`tests/emulation_v78_articles` contient 48 paires V77/V78, huit différences exclusivement dans la fenêtre textuelle, avec les mêmes entrées manette et états initiaux ; 10 148 images échantillonnées dans V78. Toutes les captures finales des deux profils ont été relues.

Cycle Minnie de vingt captures par profil : fiole de sérum **ID70, 58 $** donnée par commande native ; sac avec fiole page03, confirmation page04, sac sans fiole page08, réserve avec fiole page11, confirmation de retrait page13, sac avec fiole récupérée page19. Les effets de dépôt/retrait sont donc observés sur ce cycle contrôlé. Le cas de confirmation isolée utilise la variable d'objet de l'état, Badge Franklin ; il ne certifie aucun stockage à lui seul.

Les scripts sont appelés artificiellement depuis la carte bancaire. Aucun parcours naturel vers Minnie ou le contenant n'est certifié ; aucune écriture directe WRAM par le testeur. Les seules écritures temporaires de routage sont déclarées dans les résultats. Les anciennes captures des étapes 81/99/114/116/119 gardent leurs empreintes historiques et ne sont pas présentées comme captures des IPS actuels.

| Profil | SHA256 IPS | SHA256 ROM résultante privée |
|---|---|---|
| accents | `836fa895bbd721ecbd3f742c59fe816fb815b9ab329210400f52c4271c20704b` | `73b1504c12fc180d94e723ef123d8716d337fca8d321aebac5eb5a9a57065c70` |
| ASCII | `83e0955be73bcc6459c6b271708ecde386ee4d3297cb4920767180d8d1e1a137` | `0b3d7d413e86c2dd2ba842ede691e97f66a4d4015468be7734822cfb3e1d5b6c` |

Sorties privées : `current_v78_articles_cycle_final` et `reference_v78_articles_cycle_final`. Seuls PNG, résultats sémantiques, outils et IPS sont publiables. Ni ROM, cœur, états, ni dumps mémoire ne sont distribués.

## Reste concret

Limites du coursier et services à plusieurs personnages ; ancienne branche non qualifiée ; dialogues encore accessibles, parcours naturels, menus puis relecture finale. Le manque de 31 sources à la taille souhaitée n'est pas un inventaire exhaustif ni une mesure de complétion du jeu. Ne pas compter les corrections françaises ou les noms propres pour remplir le lot.
