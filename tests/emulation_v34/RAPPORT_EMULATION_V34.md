# Essais Snes9x V34

## Parcours normal

Le parcours V18 Work a été rejoué avec Snes9x 1.63 sur les IPS V34 autonomes : 339 commandes pour le profil accents et 337 pour le profil ASCII, jusqu'à l'image 25 803. Les cinq écrans de référence — titre, introduction, après combat, état restauré et menu — correspondent bit à bit aux références dans les deux profils. Les deux processus se terminent avec le code 0.

Cette régression confirme le démarrage, l'introduction, le premier combat, la restauration et le menu. Elle ne traverse pas les 62 scripts V34 dans leurs scènes normales.

## Affichage ciblé

Dix essais natifs supplémentaires couvrent cinq scripts dans les deux profils :

- `33F009` : utilisation d'un objet et ouverture de porte ;
- `34EC37` : proposition de rachat avec objet et montant dynamiques ;
- `364E88` : étudiant en architecture intérieure ;
- `36A6E3` : « Hélas ! Trop tard ! » ;
- `37B70A` : dialogue d'adieu.

Le script de sonde remplace temporairement cinq octets à `07C588` pour faire pointer le message « personne à qui parler » vers le script choisi. Cette modification n'est pas présente dans les IPS publiés. Elle vérifie le rendu par le moteur natif et les frontières dynamiques, pas le déclenchement narratif ni la transaction réelle. Les captures ont été relues dans les deux profils ; accents, texte ASCII, retours et noms/objets/montants dynamiques s'affichent sans débordement observé.

Les ROM de test, sauvegardes d'état, WRAM et cœur d'émulation ne sont pas conservés. Seuls les scripts, résultats JSON et captures PNG sont publiés.

```sh
python3 tests/emulation_v34/replay.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --out '/chemin/replay'
python3 tests/emulation_v34/probe.py --rom '/chemin/original.sfc' --core '/chemin/snes9x_libretro.so' --replay-out '/chemin/replay' --out '/chemin/probes'
```
