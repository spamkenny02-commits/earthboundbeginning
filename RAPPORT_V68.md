# V68 — retrait bloqué, puis récupération après libération d'une case

**Audit et validation uniquement : les IPS V67 restent inchangés.** Aucun nouveau fragment anglais n'a été rencontré dans les messages de ce lot. Il n'y a pas d'IPS V68 ni de nouvelle traduction à revendiquer.

## Séquence contrôlée dans les deux profils

| Phase | Préparation privée par le moteur | Résultat relu |
| --- | --- | --- |
| `prepare` | Treize ajouts natifs de Fiole (`1D 00 01 70`) | Carte + treize Fioles visibles ; dépôt d'une Fiole confirmé ; sortie complète du service |
| `blocked` | Un ajout natif de Fiole après rechargement de l'état précédent | Retrait refusé avant l'ouverture de la réserve : « Je crois que tu portes déjà trop de choses. » ; sortie du service |
| `recover` | Un retrait natif de Fiole (`1D 01 01 70`) après rechargement de l'état bloqué | La réserve contient toujours une Fiole ; sélection de Ninten, récupération confirmée ; nouvelle demande de retrait montrant la réserve vide |

La libération de case est une **préparation artificielle**, pas une consommation naturelle d'objet. Les accès au service sont aussi forcés par le wrapper temporaire : ce n'est pas une visite naturelle sur la carte.

Les transferts et les textes sont constatés à l'écran. Le dépôt affiche « Cet objet sera bien au chaud. », la récupération « Prends-en bien soin. » et la fin « Je ne garde aucun objet à toi. ». Les confirmations V65 restent françaises dans ce cas d'inventaire presque plein. La poche reste affichée à 20 $. Aucun champ d'argent ou d'inventaire n'est lu directement pour affirmer ces effets.

## Preuves et limites

Six sessions d'émulateur (trois phases par profil), **50 captures relues** et **10 564 images échantillonnées**. Les empreintes PNG et RGB sont vérifiables avec les outils du dépôt. Les états privés de passage sont sauvegardés seulement après retour à la carte ; leur empreinte de sortie doit être exactement l'empreinte d'entrée de la phase suivante. Les états eux-mêmes ne sont pas publiés.

Les 575 tests historiques V62 et les suites V63–V67 (33 tests) repassent, ainsi que les six contrôles V68 : **614 tests réussis** avec la ROM privée fournie aux suites concernées. Sans ROM, cinq tests V68 passent et le test privé est explicitement ignoré. Ils vérifient les préparations autorisées, la stabilité des IPS, les liens de phases, les traces, les PNG et la reconstruction des fixtures ; ils ne remplacent pas la relecture des captures.

Chaque fixture reprend le patch V67 vérifié et n'écrit que le pointeur `368B51` et le wrapper `330FC0`. Le wrapper contient les ajouts/retraits natifs déclarés, un appel du script complet `34B490` et un retour. Tailles : 58 octets pour la préparation, 10 pour le refus et 10 pour la récupération, dans la réserve de 64 octets. Aucun callback assembleur ni écriture directe en WRAM. Les six empreintes de fixture sont reconstruisibles à partir de la ROM privée ; les ancrages moteur, les sprites et la banque 25 sont contrôlés.

La convention des commandes vient des macros et handlers de la source primaire [Herringway/ebsrc](https://github.com/Herringway/ebsrc/blob/68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62/include/textmacros.asm), révision `68aec5c39e67f3ef4f0be138ee58c1ba0cc33d62`. Le résultat concret de ces commandes dans le remake est vérifié par les séquences et captures, pas déduit uniquement de cette source.

Une exploration initiale du deuxième passage n'appuyait pas assez de fois sur A : elle restait au menu d'action et n'est pas une preuve de retrait. Le probe publié utilise six touches de déclenchement aux phases `blocked` et `recover`, cinq à `prepare`, puis vérifie les vraies pages de service. Les touches A supplémentaires après le refus ne sont pas comptées comme de nouvelles branches testées.

## Sauvegarde et suite

Checkpoint Git : `work/v68-storage-audit`, `171a0c75eb39658da9a8db61df24a307c751c33b`. Sources, captures et consignes sauvegardées ; aucune ROM, cœur, état ou dump mémoire distribué. Les dépendances restent celles indiquées dans `REPRISE_TRADUCTION.md` (états V33).

Le point « retrait vers un inventaire plein » est désormais vérifié dans cette configuration à un personnage. Restent réserve pleine, plusieurs personnages, coursiers et transferts Escargo, autres enseignes, parcours naturels et relecture complète. **100 % des textes n'est toujours pas certifié.** Les menus d'action restent pour la phase suivante.

Captures : [refus accents](tests/emulation_v68/accents/blocked/page_02.png), [réserve préservée](tests/emulation_v68/accents/recover/page_03.png), [récupération](tests/emulation_v68/accents/recover/page_05.png), [réserve vide](tests/emulation_v68/accents/recover/page_07.png), [refus ASCII](tests/emulation_v68/ascii/blocked/page_02.png).
