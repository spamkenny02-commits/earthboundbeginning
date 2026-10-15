# V41 — dialogues de services et textes narratifs

Base : V40, commit `7e0599a`. V41 révise 108 scripts : objets au sol, inventaire plein, soins, consigne, transports, hôtels, banque, dialogues secondaires et passages de l'épilogue.

**197 nouvelles occurrences de fragments** sont intégrées, correspondant à 125 fragments anglais distincts : les formulations communes sont présentes à plusieurs adresses. Dix raccords grammaticaux sont retirés sans être comptés comme de nouvelles traductions. Les 101 fragments conservés comprennent les noms, interjections, signes et **40 choix Yes/No**, laissés pour la passe des menus.

Les 256 références sont contrôlées : 255 opérandes de commandes fermées et un champ de la table d'actions de combat. Le constructeur raccorde 214 références externes et 42 sauts entre les copies, avec leurs alias intérieurs. Les octets des 108 scripts sources sont conservés.

Neuf opérandes de pointeurs déjà couverts par d'anciens enregistrements IPS doivent être actualisés. Les anciens enregistrements restent dans leur ordre ; seules ces neuf références prouvées sont ensuite remplacées. Tous les autres octets antérieurs restent identiques. La liste exacte est dans `prior_record_pointer_updates` du manifeste.

```sh
python tools/v41/build_v41.py --rom '/chemin/original.sfc' --out patches
ROM_PATH='/chemin/original.sfc' python -m unittest discover -s tools/v41 -p 'test_v41*.py' -v
ROM_PATH='/chemin/original.sfc' python tools/v41/run_regressions.py
```

Les réserves sont nulles dans la ROM originale et dans V40, sans cible HiROM ni collision avec les anciens IPS. Les deux profils ont la même implantation. Les écritures hors des nouvelles copies et des références déclarées sont refusées.

Traductions : `translations_v41.json`. Sources et preuves : `v41_dialogues_fr.json`. Empreintes, réserves, copies, alias et références antérieures actualisées : `validation_v41.json`.

Les suites sont isolées dans des processus distincts. Les tests de recompression V36/V37 dépendant de CoilSnake ne sont pas exécutés ; leurs contrôles hors ligne et la préservation de leurs données sont vérifiés. Le parcours normal du début sous Snes9x ne couvre pas les 108 nouvelles scènes. Les menus restent pour une passe ultérieure.
