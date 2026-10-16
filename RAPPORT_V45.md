# V45 — inventaire, groupes et sources partiellement modifiées

Base : V44 (`fc31605`). Ce lot ciblé ajoute **20 occurrences de fragments français**, soit 18 fragments anglais distincts, dans **six scripts de messages et sept sous-routines privées**. Il complète les dialogues d'inventaire plein, de sélection d'un objet à jeter et d'abandon, ainsi qu'un journal de fuite et les notifications d'attaque/défense. Les six ajustements non lexicaux ne sont pas ajoutés au compteur.

## Groupe de personnages

La routine anglaise peut afficher un nom, « nom et un autre nom » ou « nom et ses compagnons ». Les sept copies françaises conservent les boucles, les cinq entrées selon le nombre de participants et la branche de genre. Elles affichent « et » et « ses compagnons ». Les routines d'origine et leurs 51 références littérales restent intactes ; seuls les appels des nouvelles copies utilisent les routines privées.

Les formulations d'inventaire et de fuite évitent un accord verbal dépendant du nombre de noms affichés. Le dictionnaire anglais partagé n'est pas modifié ; 28 entrées utilisées sont développées dans les copies.

## Source mixte et raccords

Le script de sélection d'un objet à jeter, `2F7D0F`, contenait déjà deux pointeurs raccordés à des copies françaises en V44. Le constructeur distingue désormais les octets de la ROM originale et ceux de la base publiée. Il accepte uniquement ces changements dans des opérandes de pointeurs prouvés, les conserve dans la nouvelle copie et refuse toute autre modification du texte ou des commandes. Un test négatif vérifie ce refus.

Chaque IPS conserve les enregistrements V44 et ajoute **19 enregistrements** : 13 copies et six pointeurs externes. Les copies contiennent 24 raccords internes. Un seul opérande déjà couvert par V44 est actualisé : `320BB4`, pour rejoindre le nouveau dialogue de sélection. Tous les autres octets antérieurs restent protégés, notamment les 14 corrections de pointeurs de la V44.

Les branches vers les intérieurs `2F7C89`, `2F7CB4` et `2F7CED` sont vérifiées jusque dans leur première question française. La correction des fins exclusives de scripts introduite en V44 est conservée.

Les choix **Yes / No / Throw away / Don't do it** restent inchangés. Les menus conservent leur passe dédiée.

## Vérification

**207 tests locaux réussis** : 26 V45 et 181 historiques, par suites isolées. Les six tests GitHub hors ROM reconstruisent les ajouts et contrôlent notamment les sources contiguës. Les tests graphiques V36/V37 nécessitant CoilSnake ne sont pas compris ; leurs tests hors ROM et la conservation de leurs octets sont vérifiés.

Le parcours normal Snes9x est conforme dans les deux profils. Les dialogues d'inventaire et le journal de fuite ont été relus dans le moteur natif avec un routage de description contrôlé. Un autre essai conserve la ROM publiée et injecte une arme dans un emplacement d'inventaire pour vérifier la commande normale Équiper. Ces fixtures ne prouvent ni un ramassage naturel, ni une saturation réelle de l'inventaire, ni les effets d'une fuite. Les deux nouvelles notifications d'attaque/défense restent à relire dans leur scène d'origine. Voir le [rapport d'émulation](tests/emulation_v45/RAPPORT_EMULATION_V45.md).

## Suite et livraison

D'autres appelants des routines anglaises restent à examiner dans leur contexte, notamment les anciens messages du papillon magique et de défaite. Ce lot ne prétend pas achever tous les raccords grammaticaux du jeu.

- [IPS avec accents](patches/EarthBound_Beginnings_FR_v45_accents.ips)
- [IPS ASCII](patches/EarthBound_Beginnings_FR_v45_ascii.ips)
- [Constructeur, sources et reproduction](tools/v45/README_V45.md)

Appliquer un seul IPS V45 directement à la ROM originale USA 1.2, sans empiler les versions. La ROM conserve sa taille de 4 Mio. Aucune ROM, sauvegarde ou fixture de jeu n'est distribuée.
