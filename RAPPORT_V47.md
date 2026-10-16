# V47 — services, zoo et messages de combat

La V47 prolonge la V46 avec **21 scripts et 34 occurrences de fragments traduits**, correspondant à 28 fragments anglais distincts. Quatre ajustements non lexicaux sont comptés séparément. Les choix `Yes` / `No` restent pour la passe des menus.

Le lot couvre les réponses de services, le dépôt d'objets, l'accord pour aider au zoo et la clé auprès d'Abbott, trois messages d'asthme, la distraction, l'utilisation d'objets et de condiments, un remboursement et le plafond de dépôt bancaire. L'extraction contient aussi des textes de débogage et des restes EarthBound : ils ne sont pas intégrés dans ce lot. La présence d'un appel prouvé ne constitue pas une validation du déclenchement naturel de la scène.

Chaque patch autonome conserve les enregistrements V46 et ajoute **55 enregistrements** : 21 copies et 34 opérandes de pointeurs externes. Un raccord interne est recalculé dans une copie. Les sources restent intactes. Les 14 références littérales non prouvées sont conservées. Les réserves sont des plages nulles du banc déjà utilisé pour les traductions, sans ancienne écriture IPS ni cible de pointeur littéral, vérifiées sur la ROM originale et les deux variantes V46. Le dictionnaire partagé reste intact.

**247 tests locaux réussis** : 229 historiques et 18 V47. Ils contrôlent notamment la provenance, les appels prouvés, la reconstruction indépendante des ROM, les commandes, les alias, la totalité des différences, les anciens enregistrements, les réserves et les deux variantes. Les exclusions historiques V36/V37 nécessitant CoilSnake sont conservées.

Sous Snes9x 1.63, le parcours normal reproduit 339 commandes avec accents et 337 en ASCII. Les 109 captures avec accents et 103 captures ASCII sont identiques pixel par pixel à V46. Huit scripts supplémentaires sont relus dans chaque variante avec un routage de test de la description de carte bancaire. Ces ROM de test changent uniquement un opérande ; elles ne sont pas distribuées. Les captures montrent les textes complets, leurs accents et les retours à la ligne.

Ces essais contrôlés ne valident ni l'asthme en combat, ni l'accès naturel au zoo ou aux services concernés, ni les autres nouveaux scripts. Les menus sont reportés à leur passe dédiée. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.

- [Patch avec accents](patches/EarthBound_Beginnings_FR_v47_accents.ips)
- [Patch ASCII](patches/EarthBound_Beginnings_FR_v47_ascii.ips)
- [Construction et tests](tools/v47/README_V47.md)
- [Rapport et preuves d'affichage](tests/emulation_v47/RAPPORT_EMULATION_V47.md)
