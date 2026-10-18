# V57 — textes d'objets et d'inventaire

**37 zones, 63 fragments modifiés**, dans 23 contextes : manger/boire, objets reçus, rangés, lancés ou inutilisables, vélo, pancarte, Souris de sortie et réorganisation de l'inventaire. Cinq fragments conservés ne sont pas ajoutés au décompte. Certains modèles hérités ne sont pas confirmés comme naturellement accessibles dans le portage.

Deux résidus ont été trouvés par des opérations normales sur la carte bancaire : refus de la consommer et réorganisation lors du don à soi-même. Ils s'affichent désormais en français avec les vrais noms de personnage et d'objet. Les sorties dynamiques sont conservées. Un seul appel possessif est adapté dans sa copie privée vers l'auxiliaire français de V50 ; les anciens appels restent intacts.

Un essai initial avait révélé une corruption de sprite : des octets nuls pris pour de l'espace libre étaient des pixels. La version finale utilise le grand remplissage original de fin de banque 32/début de banque 33. Elle protège les 464 groupes et 4 177 références d'images contre de nouvelles écritures par rapport à V56.

Après redémarrage de l'environnement, les patchs ont été reconstruits. Les empreintes des deux ROM obtenues sont exactement celles de la V57 précédemment validée ; les vérifications sont reproduites pour la publication.

**480 tests passent** ; 212 captures de référence restent identiques à V56 et 66 essais d’affichage couvrent les deux profils.

La cible de **85 % du texte** reste non certifiée, faute de dénominateur exhaustif des occurrences actives. L'estimation globale antérieure de 80 % ne fournit pas ce taux. La priorité reste aux textes, puis aux menus. Voir [la suite identifiée](RESTANT_TEXTES.md).

[Sources et garanties](tools/v57/README_V57.md) — [Rapport d'émulation et captures](tests/emulation_v57/RAPPORT_EMULATION_V57.md).

Aucune ROM, sauvegarde ou bibliothèque d'émulation n'est distribuée. Appliquer un seul IPS V57 directement à la ROM originale USA 1.2.
