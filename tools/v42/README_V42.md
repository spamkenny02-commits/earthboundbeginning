# V42 — textes d'actions compressés par dictionnaire

Base : V41 (`84afcfa`). Ce lot traite 100 scripts hérités encore anglais et référencés par la table des actions du remake : messages d'actions, d'états et d'utilisation d'objets. Le message de carte bancaire découvert en V41 est inclus.

**187 nouvelles occurrences de fragments français**, correspondant à 169 fragments anglais distincts. Les copies comprennent 283 fragments : 187 traductions, 4 raccords retirés et 92 marqueurs ou signes conservés. Aucun menu n'est traduit par ce lot.

Les codes `15 xx`, `16 xx` et `17 xx` développent des mots du dictionnaire anglais. Le constructeur vérifie les 768 entrées de la table source, conserve les preuves des 234 entrées utilisées et remplace uniquement les plages textuelles des copies. Les copies françaises utilisent les glyphes ordinaires ; **le dictionnaire partagé et sa table de pointeurs restent intacts**.

Les 229 références prouvées comprennent 109 champs de la table d'actions du remake, 108 champs de la table d'actions héritée et 12 opérandes de commandes. Les champs des deux tables ont le même index et un enregistrement de 12 octets, avec le pointeur de texte à +4. Dix adresses littérales supplémentaires vers des intérieurs de texte ne sont pas prouvées : leurs octets et les sources anglaises restent inchangés.

```sh
python tools/v42/build_v42.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python -m unittest discover -s tools/v42 -p 'test_v42*.py' -v
ROM_PATH='/chemin/original.sfc' python tools/v42/run_regressions.py
```

Les IPS autonomes conservent tous les enregistrements V41 et ajoutent chacun 329 enregistrements : 100 copies et 229 pointeurs. Aucun opérande déjà couvert par V41 n'a besoin d'être remplacé dans ce lot. Les réserves sont nulles et non ciblées dans la source et V41 ; les deux profils partagent la même implantation.

Les descriptions anglaises proviennent de banques héritées. Leur présence dans la table du remake ne prouve pas que toutes les actions sont accessibles en partie normale. La carte bancaire et Parer sont vus par leurs commandes normales dans les deux profils ; les autres scripts restent à contrôler dans leurs situations réelles.

Sources et dictionnaire utilisé : `v42_dialogues_fr.json`. Traductions : `translations_v42.json`. Implantations, empreintes et références : `validation_v42.json`. Voir le rapport d'émulation pour les captures et les sondes reproductibles. Les menus restent pour la suite.
