# V78 — relecture des continuations françaises

615 continuations littérales distinctes ont été relues : fragments modifiés, ne commençant pas par@, comportant au moins huit caractères hors remplissage, dans la fermeture typée des PNJ placés (développeur86 exclu comme graine). La liste et les chemins exacts figurent dans `tools/v78/continuation_proofreading.json`. Il s'agit de français existant ; aucune nouvelle source anglaise n'est ajoutée au compteur. Les courts libellés et tous les assemblages dynamiques ne sont pas certifiés par cette sélection.

Trois avertissements de boutique « [nom] ne peut l'user » deviennent « [nom] : incompatible. ». La question devient « L'acheter quand même ? ». Quatre plages fixes, sans allocation ni déplacement de pointeur. Les noms, commandes, tests de compatibilité et décisions d'achat restent inchangés ; cela corrige la formulation, pas le fonctionnement des boutiques.

Douze essais de rendu : trois corps d'avertissement, Ninten et Ana, accents et ASCII. Ana est ajoutée par la commande native1F1102 ; les commandes natives0E[n]/0D01 placent l'identifiant1 ou2 dans l'argument affiché par1C0200. Source primaire locale : ebsrc `src/text/ccs/set_secmem.asm`, `copy_to_argmem.asm`, `print_character_name.asm` et macros de texte. Aucune écriture WRAM directe.

Ce sont des appels forcés des avertissements, pas des achats naturels ni des tests du calcul de compatibilité. Une attente native13 dans le harnais retient la question après le retour ; les premiers essais sans attente fermaient la fenêtre avant la capture « question » et ne servent pas de preuve positive de cette question. Les24 captures finales sont relues et gardent le hash exact du build observé.

Les82 tests V78 passent avec la ROM privée après les quatre corrections. Reconstruction complète reproduite, sorties IPS intégrées identiques octet par octet, inventaires dépendants actualisés. Aucun fichier privé distribué.

| Profil | SHA256 IPS | SHA256 cible privée |
| --- | --- | --- |
| accents | `e5cc9706fdd8a0a840fb5e1a1efa78319d682bbba2be322c76e49099070b2d3c` | `15b56d35aed8f547d84ea9fa827fee790d919cdb41bf4a73bddc721b10735e4a` |
| ascii | `4bc486a761d37d12d4b32a298cde170b8970dde65c4e4dc1fda3b7ebc26ce322` | `61216ddd9077643207899f27f1747ac6276f231bd7a65a0a3c805e5a74b5a442` |

Avec la passe précédente :16 plages françaises corrigées, toujours zéro nouvelle traduction anglaise pour cette reprise ; historique249 sources distinctes/297 plages,137 publiées/112 en attente. Les796 amorces et615 continuations sont des sélections littérales à ne pas présenter comme des textes complets du jeu. La comparaison bilingue intégrale, les autres catégories, graphiques et accès naturels de fin restent ouverts ; ni400 sources nouvelles ni un reste global sous400 ni100% ne sont établis.
