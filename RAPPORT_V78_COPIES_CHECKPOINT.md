# V78 — copies contextuelles, checkpoint à 116 textes

Deux textes supplémentaires sont traduits sur leurs chemins qualifiés. Le lot en cours compte 116 sources distinctes et 154 plages sources traitées ; les implantations des deux sources nouvelles restent anglaises et sont préservées comme alias. Les traductions sont dans des copies. V77 reste publiée sur main ; aucun lancement de version V78 avant poursuite du lot visé à 150.

| Chemin | Redirection | Texte français |
|---|---|---|
| Aide bouteille d'eau ID6E, table 155000 + 39×6E + 35 | 1560E5 : 054733 → 330CA8 | Bois pour gagner un peu de PP. |
| Après « Dans ce cas, », dernier bloc du pont médical 0911E2 | 329025 : 0911EB → 32FC98 | Passe un coup de fil à maman : sa voix te fera du bien. |

Les commandes des deux scripts sont conservées dans les copies, sans changement de comportement. Les atomes entiers (mots avec leurs espaces et commandes) sont répartis dans des réserves provenant du remplissage original nul. Les plus grands blocs sont réservés en premier. Les sauts ajoutés relient les atomes ; le dernier garde le terminateur original. 272 octets supplémentaires, total alloué 3 431 ; 369 enregistrements ajoutés aux IPS V77. Sprites, banque25, table PNJ et créneau privé inchangés.

Les références brutes à 054743 (3C8B3F) et 0911F0 (0047F0, 00706A) ne sont pas qualifiées comme des chemins de texte ; leurs octets et les scripts originaux sont intacts. Le constructeur n'exempte aucune référence des protections. Les autres références explicites à l'ancienne aide eau, 05ABBA et 37065F, restent à qualifier et ne sont pas redirigées. Le bilan ne prétend donc pas que tous les alias sont traduits.

16 tests V78 réussis avec ROM privée. Ils reconstruisent les snapshots 81/99/114 pour leurs anciennes preuves, contrôlent les deux redirections autorisées, les copies exactes, les commandes, les réserves et les alias. Reconstruction déterministe des IPS vérifiée. Le comptage source est dédoublonné dans batch_ledger.json.

Émulation : quatre cas par profil, 36 paires V77/V78, six changements limités aux fenêtres textuelles, 7 912 images échantillonnées. Les 36 captures finales ont été relues en accents et ASCII : mots entiers, texte lisible, absence de débordement visible. L'aide copiée est appelée directement depuis l'adresse portée par l'objet. Le conseil médical passe par la branche précédente 0911E2 et son saut natif. Les deux entrées originales sont aussi appelées, et restent anglaises comme attendu. Chaque entrée initiale est forcée via la carte bancaire depuis l'état privé post-repos : aucun parcours naturel, diagnostic, navigation Aide ou effet de consommation certifié, aucune écriture WRAM directe.

Preuves publiques : tests/emulation_v78_scoped ; sorties privées : current_v78_scoped et reference_v78_scoped. Ni ROM, cœur, états ni mémoire ne sont distribués.

| Profil | SHA256 IPS | SHA256 ROM cible privée |
|---|---|---|
| Accents | b97785db00df36c39d9352d778d9e5c1c8472f6aea5b38486087d3fcc2eb232c | 10b0bc4f0126367b855100f997f49b720aa208b721b3c4423138d8b578ebdefc |
| ASCII | 759f66606bfdad05fb40a7c065e2277fe1ba24b0026e988d8bed3a106875e298 | 208f78ed82789aafc0dc11a8122d2c63e63240c586fa23eb2f548d6548a44188 |

Reste : helpers possessifs/pronoms/articles, limites du coursier et plusieurs personnages, autres alias et parcours naturels, puis menus/relecture. Il manque 34 sources à la taille de lot souhaitée ; ce nombre n'est pas une liste de restes prouvés et ne justifie pas de traduire du texte dormant. Le stockage protégé restant est très fragmenté. Continuer le même lot avec checkpoints intermédiaires.
