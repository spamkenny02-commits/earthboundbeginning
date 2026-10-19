# V69 — audit de réserve pleine, patch V67 inchangé

Lire `RAPPORT_V69.md`. Pas de reconstructeur ni d'IPS V69 : le jeu reste strictement V67.

```sh
EARTHBOUND_ROM=/chemin/absolu/SOURCE.sfc python -m unittest discover -s tools/v69 -v
python tools/v69/verify_display.py
```

Sans la ROM privée, cinq tests passent et le sixième est explicitement ignoré. Pillow est nécessaire au contrôle des empreintes RGB.

```sh
python tests/emulation_v69/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out SORTIE_PRIVEE --profile accents
python tests/emulation_v69/probe.py --rom SOURCE.sfc --core snes9x_libretro.so --states-dir ETATS_V33 --out SORTIE_PRIVEE --profile ascii
python tools/v69/collect_evidence.py --source SORTIE_PRIVEE --sheets REVUE_PRIVEE
```

Les deux premières phases ne contiennent pas d'appel de service : elles ajoutent directement treize objets en réserve par `1D 18`, puis retournent. La troisième ajoute dix objets, donne un objet au personnage et appelle le service. Ce sont des préparations artificielles dans les seules fixtures privées. Les états sont chaînés après retour à la carte et les empreintes liées sont contrôlées. Les sorties brutes peuvent contenir états et journaux privés : importer seulement les PNG et résultats filtrés avec le collecteur.

La réserve est lue sur quatre pages (10/10/10/6 objets), puis un retrait, un redépôt et un nouveau refus sont effectués par la manette. Les noms `fill_13` et `fill_26` indiquent les préparations demandées, pas des comptages effectués directement en WRAM ; le dénombrement final vient des captures et du parcours des quatre pages. Les numéros de page ne sont pas des compteurs d'objets.

Le test ROM vérifie que les deux seules plages de chaque fixture et les préparations déclarées suffisent à retrouver son empreinte exacte. Aucun élément privé n'est ajouté au patch de jeu. Ces contrôles ne prouvent pas un accès naturel sur la carte ni les configurations à plusieurs personnages.
