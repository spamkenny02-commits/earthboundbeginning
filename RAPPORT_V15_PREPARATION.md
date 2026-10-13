# V15 — historique de préparation

Ce document décrit la **première étape préparatoire** de la V15, consacrée aux huit segments V14 laissés en anglais en raison de pointeurs intérieurs. Il ne s'agit pas du bilan de livraison.

**La V15 est maintenant publiée** : voir [RAPPORT_V15.md](RAPPORT_V15.md), avec **77 nouveaux segments français dans 32 scripts**, deux IPS autonomes et des tests automatisés.

Le brouillon historique `traduction/v15_candidats_a_valider.json` reste conservé, mais **ses huit propositions ne sont pas intégrées** dans la V15 : elles nécessitent une étude de relocalisation ou de préservation des points d'entrée internes. Le test `tests/verifier_preparation_v15.py` vérifie seulement leur longueur et les collisions avec la V14, pas leur sécurité d'intégration.

Le lot V15 livré provient du manifeste distinct `traduction/v15_dialogues_fr.json`, contrôlé sur la ROM source. Trois de ses 80 segments initiaux ont également été exclus pour cause de pointeurs intérieurs.
