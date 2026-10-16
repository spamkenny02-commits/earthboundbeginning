# V51 — textes avec entrées intérieures préservées

24 fragments traduits dans 21 contextes, sur les 28 segments reportés par V49/V50. Le décompte inclut une indication « (sourire) ». La traduction reste partielle ; ce lot ne modifie pas les menus.

## Textes

Trésor enterré, os du chien, fantômes de Spookane et prénom du fils, souvenir du chiot, pierres coiffées, prix du train et remboursement, boisson énergétique, conseils d'enquête, Ellay et ses artistes, ascension et cabane, livraison Mach Pizza, question sur l'humanité, aventures, condiment, barde et village Canari.

## Méthode

Un saut long `0A` de cinq octets remplace le début de chaque fragment. Il rejoint une copie française privée, terminée par un second saut `0A` vers l'adresse exclusive de fin du fragment source : la commande d'origine qui suit le texte reprend alors normalement. Aucun appel `08` ni nouvelle entrée de pile de retour n'est ajouté.

Le constructeur refuse tout fragment ayant une adresse littérale intérieure dans les quatre octets après son début. Les octets à partir du cinquième restent identiques à V50, ainsi que toutes les occurrences littérales des adresses intérieures. Ces adresses ne sont ni réinterprétées comme faux positifs ni réécrites. Un parcours entrant directement dans cette partie conservée pourra encore afficher de l'anglais.

Les copies utilisent uniquement des plages nulles des banques de traduction 25/32, absentes des enregistrements IPS antérieurs et sans cible littérale à l'intérieur. Les plages sont recalculées sur la ROM originale et les deux variantes V50. Les 48 ajouts IPS préservent tous les enregistrements antérieurs ; le dictionnaire partagé est inchangé. La reconstruction logique de chaque contexte suit les deux nouveaux sauts et conserve toutes ses autres commandes. Le parseur physique s'arrête désormais au premier saut : son ancienne adresse de fin n'est donc pas utilisée comme preuve.

## Limites

Quatre segments restent intacts : `33F3EE` (maison hantée), `3609EB` (adieu), `35000E` (ascenseur), `35188B` (exclamation). Leur première cible intérieure est trop proche du début. Ce ne sont pas les seuls textes anglais restants dans le jeu.

335 tests locaux passent, dont 18 nouveaux contrôles V51 : reconstruction IPS exacte, frontières du texte, réserves, refus des collisions et débordements, trajet aller/retour, conservation des commandes, des entrées et des sites de références, dictionnaire et écritures limitées aux plages déclarées. Les suites historiques utilisées sont listées dans `tools/v51/run_regressions.py` ; les anciens essais graphiques V36/V37 nécessitant CoilSnake ne sont pas inclus.

Les 212 captures du parcours normal Snes9x sont identiques à V50. Chaque nouveau début de texte est lu par redirection de la carte bancaire, plus deux descriptions complètes, dans les deux variantes. Ces 26 cas contrôlés ne prouvent pas les déclenchements naturels, tous les embranchements ni les effets de jeu. Voir le [rapport d'émulation](tests/emulation_v51/RAPPORT_EMULATION_V51.md).

## Application et empreintes

Appliquer un seul IPS V51 à la ROM originale USA 1.2 de 4 Mio, SHA-256 `e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c`.

- [Variante avec accents](patches/EarthBound_Beginnings_FR_v51_accents.ips)
- [Variante ASCII](patches/EarthBound_Beginnings_FR_v51_ascii.ips)

Les empreintes exactes des IPS et des ROM résultantes figurent dans [validation_v51.json](tools/v51/validation_v51.json). Aucun fichier ROM, état de jeu ou cœur d'émulation n'est distribué.
