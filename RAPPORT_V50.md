# V50 — objets, services et possessifs

La V50 ajoute **46 occurrences de fragments traduits dans 29 contextes**, correspondant à 41 fragments anglais distincts. Elle complète des réponses de services, des descriptions d'objets, la découverte du laissez-passer, les messages de dégâts et d'EVE, ainsi que le terme « frère ». Les contextes qui se recouvrent sont dédoublonnés.

Deux messages demandent aussi des possessifs français : « sa tête » et « son niveau max. ». Quatre petites copies grammaticales privées rendent les deux variantes de genre sans modifier les routines anglaises d'origine. Seuls les appels des contextes `3479FF` et `35C6FC` sont redirigés. Les autres appelants restent inchangés.

## Audit des protections V49

L'audit reproductible couvre les **21 segments protégés** et **93 sites littéraux** ciblant leur intérieur. Deux analyses par fenêtre d'octets produisent des candidats ressemblant à des commandes porteuses de pointeur. Sans ancrage de flux validé, elles ne sont pas acceptées comme preuves. Le fichier d'audit indique explicitement qu'aucun candidat n'autorise une édition.

**Les 21 protections sont conservées.** Sept nouveaux segments sont également reportés par le même contrôle d'adresse intérieure. Aucun de ces 28 segments n'est compté dans les nouvelles traductions. L'audit n'affirme ni que toutes ces adresses sont des pointeurs, ni qu'elles sont toutes fortuites.

## Construction

Les IPS autonomes reprennent les enregistrements V49 et ajoutent **52 enregistrements** : 46 plages de texte à taille fixe, quatre copies grammaticales et deux opérandes d'appel. Les quatre copies occupent 30 octets utiles, 32 avec alignement, dans la réserve nulle `251E00–251E50`. La réserve est vérifiée sur l'original et les deux variantes V49, sans ancienne écriture IPS ou cible de pointeur littéral.

Les scripts principaux conservent leurs adresses et leurs longueurs. Hors les deux opérandes déclarés, leurs commandes restent identiques. Les routines grammaticales sources, leurs autres appels, les fontes, le dictionnaire et le texte français antérieur sont préservés. Les deux branches de chaque nouvelle routine privée sont contrôlées.

## Vérification

**317 tests locaux réussis** : 292 historiques et 25 V50. Ils vérifient notamment les reconstructions indépendantes, les commandes, la totalité des différences, les protections V49, les sept nouveaux reports, la réserve grammaticale, les appels limités aux deux contextes, les branches de genre et les références d'origine conservées. La CI V50 exécute dix tests sans ROM. Les exclusions historiques V36/V37 nécessitant CoilSnake restent inchangées.

Le parcours normal Snes9x passe dans les deux variantes : **212 captures identiques pixel par pixel à V49**. Douze contextes traduits et un repli au nom conservé font l'objet de lectures contrôlées. Certains essais entrent directement au texte ; deux utilisent un petit script d'affichage temporaire pour maintenir les termes de parenté à l'écran. Ils ne valident ni les conditions naturelles, ni le stockage réel, ni les embranchements complets. Les essais et leurs limites sont détaillés dans le rapport d'émulation.

- [Patch avec accents](patches/EarthBound_Beginnings_FR_v50_accents.ips)
- [Patch ASCII](patches/EarthBound_Beginnings_FR_v50_ascii.ips)
- [Construction et tests](tools/v50/README_V50.md)
- [Preuves d'affichage](tests/emulation_v50/RAPPORT_EMULATION_V50.md)

Appliquer un seul IPS directement à la ROM originale USA 1.2, sans empiler les versions. Les menus restent pour leur passe dédiée. Aucune ROM, sauvegarde ni bibliothèque d'émulation n'est distribuée.
