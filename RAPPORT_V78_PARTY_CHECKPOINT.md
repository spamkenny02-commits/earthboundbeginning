# V78 — préparation du lot de 400 et contrôles à plusieurs personnages

21 octobre 2026. La cible devient **400 sources distinctes**, compteur conservé à **120/400**, 158 plages sources. Le reconstructeur, le registre généré et son test prennent cette cible. Le nom `work/v78-batch150` reste un identifiant historique. Pas de nouvelle release ; V77 reste publiée sur main.

Ce checkpoint ajoute zéro source traduite : il vérifie trois configurations qui manquaient aux preuves précédentes. Les IPS accents/ASCII reconstruits sont identiques à ceux du checkpoint coursier à 120 sources ; 384 enregistrements ajoutés à V77. Le compteur ne confond pas traduction, relecture, profils et captures.

## Préparation et transfert natifs

La fixture privée reconnaît désormais `join` avec IDs1–4, encodé en commande native `1F 11 id`. La commande `1F 11 02` est aussi présente dans le vrai script de recrutement `36E6DF`. Les sondes utilisent seulement IDs2 (Ana), puis3 (Lloyd), avec la préparation déclarée dans chaque résultat. Cela ne certifie pas leurs recrutements naturels. Les seules plages de routage de fixture restent `368B51` et `330FC0`; aucune écriture directe WRAM.

Minnie, entrée PNJ204 `36B788` forcée : ajout natif d'Ana et de la fiole ID70 au sac de Ninten. Choix de Ninten, dépôt de la fiole, réserve relue, puis choix d'Ana comme destinataire. Les captures finales montrent Ninten avec la carte seule (page17), puis Ana avec l'ours et la fiole (pages18/19), dans les deux profils. Les sélecteurs de personnages et les confirmations sont actionnés à la manette. Argent20$ conservé. Les effets de transfert sont donc observés pour ce cycle contrôlé, sans revendiquer tous les refus ou un inventaire plein d'Ana.

La branche de nom `33FC0E` est appelée avec Ninten/Ana, puis Ninten/Ana/Lloyd. Les panneaux de statut montrent réellement deux puis trois personnages. Le moteur sélectionne lui-même le helper `387B37` pour deux, `387B2F` pour trois ; les traces le vérifient et « vous » s'affiche sans espace parasite avant le point. Contrairement aux anciennes sondes plurielles, les helpers ne sont pas appelés directement par le testeur. L'entrée de la branche reste artificielle ; pas de rencontre naturelle certifiée.

## Validation et sauvegarde

**24 tests V78 réussis avec ROM privée.** `tests/emulation_v78_party` contient 56 nouvelles paires V77/V78, huit différences uniquement dans la fenêtre textuelle ; mêmes préparations, touches, état initial et nombres d'images, 11 728 images échantillonnées. Les 56 captures V78 sont relues dans les deux profils. Les tests recalculent les traces, contrôlent les helpers effectivement choisis et reproduisent les empreintes des fixtures. Les anciennes preuves gardent leurs checkpoints exacts.

Les préparations natives n'entrent pas dans les IPS. Sorties privées : `current_v78_party_validated` / `reference_v78_party_validated`. Seuls PNG, résultats sémantiques, outils et rapports sont sauvegardés dans Git ; jamais ROM, cœur, états ni mémoire brute.

## Qualification du reste et suite

L'ancienne copie `32F120` appelle encore le helper anglais `38B587`. Elle n'apparaît pas dans les 47 racines du graphe typé courant de `34B490` ; son unique pointeur brut est `34B745`, hors de ce graphe. Cette limite de graphe ne prouve pas l'absence de tout appel calculé : conserver la copie. Ne pas répéter cette seule analyse sans nouvelle raison.

Prochain candidat concret : PNJ608/champ13 pointe vers `38E2C2`, qui référence les scripts de casier `06FA0C`, `06FA2E`, `06FA68`, `06FA93`, `06FAB4`. Le code distingue les flags `0459`/`037F`, et imprime le nom IDAC, actuellement « Machine à clés ». Des liens statiques ne suffisent pas à prouver l'usage de ces dialogues hérités ; qualifier la vraie action/interaction avant de les traduire ou de les compter. Le fait qu'une sonde artificielle puisse appeler un texte ne suffit pas à le rendre pertinent.

Le fichier `tools/v78/review_coverage.json` suit les catégories encore ouvertes : services, aides, menus et commandes, combats, fin, générique, textes graphiques et relecture intégrale. Cinq libellés anglais visibles sont identifiés à partir de `38E834` (Use/Eat/Give/Drop/Help!), mais leur lecteur natif et leurs contraintes restent à qualifier avant modification. La fin et le générique ne sont pas déclarés validés. Ni le seuil de 400 ni la complétion globale ne sont atteints ou inventoriés exhaustivement.
