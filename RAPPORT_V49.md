# V49 — phrases anglaises dans les dialogues mixtes

La V49 traduit **207 occurrences de fragments lexicaux**, plus **quatre ajustements non lexicaux**, dans **84 entrées de contexte**. Ces contextes peuvent se recouvrir : les plages communes sont dédoublonnées et ne sont écrites ou comptées qu'une seule fois. Le lot correspond à 198 fragments anglais distincts et 211 écritures textuelles.

L'audit porte sur les scripts principaux déjà partiellement français. Il complète notamment Magicant, les souvenirs de Maria, la chanson des huit mélodies, les services, les indices de progression, l'école, les appels familiaux, les descriptions d'objets et des répliques du chalet. Les choix Yes/No et les libellés de menus restent pour leur passe dédiée. Ce lot ne constitue pas une déclaration de traduction complète de ces scènes : des segments protégés restent anglais.

## Réinsertion

Chaque traduction tient dans la capacité de sa plage originale et reçoit des espaces de complément. Les adresses, longueurs des scripts, commandes et opérandes restent fixes. Les octets déjà français sont conservés. Les IPS autonomes contiennent tous les enregistrements V48, suivis de 211 enregistrements textuels ; certaines anciennes écritures textuelles sont ainsi recouvertes uniquement dans les plages anglaises déclarées.

Chaque plage est un segment de texte complet d'un contexte analysé dans les deux profils, identique à la ROM originale avant traduction. Le constructeur refuse le dépassement de capacité et les écritures qui se recouvrent. Il écarte **21 segments** parce qu'une adresse littérale cible leur intérieur : la provenance de ces références reste à examiner. Les textes et adresses concernés sont conservés dans `v49_fixtures.json`. Une entrée de catalogue partielle suspecte, un emplacement réservé au débogage et des menus sont également exclus. Ni les routines grammaticales, ni les fontes, ni le dictionnaire partagé ne changent.

Le parseur de segments V49 accepte les accents déjà installés et les tokens de dictionnaire anglais. Les commandes restent séparées de ces tokens textuels. La description du Badge Franklin rend le symbole gamma par son nom dans la phrase française.

## Vérification

**292 tests locaux réussis** : 272 historiques et 20 V49. Les tests V49 reconstruisent les fixtures, appliquent les IPS avec un lecteur indépendant, décodent les nouvelles plages, comparent les commandes et branches de chaque contexte, et vérifient l'intégralité des différences. Ils contrôlent les textes français antérieurs, les menus, les segments reportés, le dictionnaire, les copies grammaticales, les capacités et les recouvrements. Les exclusions historiques V36/V37 nécessitant CoilSnake restent inchangées.

Les deux variantes passent le parcours Snes9x normal, avec 212 captures identiques pixel par pixel à V48. Treize contextes font également l'objet de lectures contrôlées dans chaque variante. Ces essais d'affichage ne valident pas leur déclenchement naturel, les embranchements, ni l'ensemble des 84 entrées. Voir le rapport d'émulation pour les pages capturées et la garde de stockage contournée dans une fixture.

- [Patch avec accents](patches/EarthBound_Beginnings_FR_v49_accents.ips)
- [Patch ASCII](patches/EarthBound_Beginnings_FR_v49_ascii.ips)
- [Construction et tests](tools/v49/README_V49.md)
- [Affichage et limites](tests/emulation_v49/RAPPORT_EMULATION_V49.md)

Appliquer un seul IPS directement à la ROM originale USA 1.2. Ne pas empiler les versions. Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée.
