# V78 — checkpoint à 99 textes, lot de 150 en cours

Historique du checkpoint à 99 textes. L'état actuel à 114 textes est décrit dans RAPPORT_V78_AIDES_CHECKPOINT.md et REPRISE_TRADUCTION.md.

99 sources distinctes sont traduites par rapport à V77, dans 137 plages physiques. Cette reprise ajoute 18 sources nouvelles ; les choix partagés et profils ne gonflent pas le compteur. Sell était déjà traduit par Oui dans un service médical : sa nouvelle variante Vendre ne compte pas comme un nouveau texte. Registre complet : REPRISE_TRADUCTION.md et tools/v78/batch_ledger.json. V77 reste publiée sur main, V78 reste un lot en cours.

Les nouvelles corrections portent sur train, Youngtown, père de Lloyd, confirmation de nom, inquiétude, yaourt à la truite, solde/remise d'argent, singe/clé du zoo, Fiole de sérum, salutations d'hôtel et choix Acheter/Vendre. Les menus généraux ne sont pas encore abordés.

Les cinq scripts 251A50, 25B08C, 25B0D4, 25B11C et 25B164 chevauchent réellement les pixels de sprites. remaining_stage.py les copie dans des réserves protégées et redirige leurs cinq seuls appelants explicites. Les chaînes conservent les mots et commandes entiers, et les définitions de choix sont indivisibles. Banque25 et sprites inchangés, table PNJ inchangée, aucune modification du moteur. Les commandes copiées et les commandes des contextes dépliés sont comparées aux originales.

Allocation totale 3 159 octets (55 initiaux + 2 323 médicaux + 781 dans cette reprise) ; 318 enregistrements ajoutés à chaque IPS V77. Les allocations supplémentaires sont vérifiées hors sprites, enregistrements antérieurs, pointeurs et créneau privé.

28 tests ciblés réussis avec la ROM privée : 12 V78, 8 V77, 8 V65. Hors ROM, 7 tests V78 passent et 5 sont explicitement ignorés. Les 166 nouvelles paires V77/V78 sont vérifiées en RGB, dont 66 différences limitées aux fenêtres textuelles ; 37 060 images échantillonnées, 19 cas par profil. Les 146 anciennes paires médicales restent associées au checkpoint de 81 textes, reconstruit et vérifié séparément : ne pas les présenter comme des captures de l'IPS actuel.

Les devis des quatre destinations 11/20/36/48 $ sont suivis du refus ; les captures affichent toujours 20 $ après celui-ci. Aucun achat ni trajet réel certifié. La quatrième destination et le père sont rendus accessibles par les flags natifs déclarés 0339 et 0376 ; le singe reçoit la clé AB via une commande native préparatoire. Aucune écriture WRAM directe. Le père accepte Non et propose de noter le nom, sans saisie accomplie. Les choix Acheter/Vendre sont lisibles ; la vente n'est pas conclue. La salutation d'hôtel est relue, pas une nuit payée. L'affichage du solde et de la remise d'argent provient de branches intérieures, pas d'un retrait effectif.

Les accès initiaux sont tous forcés dans une chambre : aucun parcours naturel. Youngtown affiche la phrase traduite mais son animation suivante est hors contexte dans cette carte ; Papa et Crois en nous ne sont pas atteints ici et restent statiques. L'aide de la Fiole et les autres répliques retenues sont relues. La branche médicale 0911ED reste bloquée sur l'alias 0911F0 ; soins effectifs et maladies non parcourues restent seulement statiques.

Preuves retenues nouvelles : current_v78_remaining_retained / reference_v78_remaining_retained. Les premiers devis appelés directement sans leur contexte provoquaient un affichage incohérent dans les deux versions : exclus. Les premières séquences sélectionnaient mal destination/refus et ouvraient une autre boutique : elles sont remplacées par les séquences corrigées. Les PNG et rapports publiables sont dans tests/emulation_v78_remaining ; aucun ROM/cœur/état/dump.

Empreintes SHA256 des IPS actuels :

- accents : 1fe31a72c95a9f80221df2daf5136b0b626b3912810f7c2704e7cce70400b404
- ASCII : c7578d0e671ddb6eb3667dbcaca14fc7d968bb142ba674e362ff48a3ea1b9045

Reprise : viser encore environ 51 textes utiles avant publication, sans les inventer. Qualifier 0911F0, les helpers possessifs/pronoms/articles selon leurs appelants et les aides d'objets réellement proposés. Accélérateur de rouille est désormais une piste étayée par un stock affiché. L'audit élargi aux mots courts conserve 237 candidats sur 4 475 racines et 1 080 graines, zéro erreur ; héritage/débogage ne sont pas des dialogues à traduire. Limites du coursier, groupes de personnages, branches conservées, menus généraux, générique et parcours complet restent à terminer. Aucun taux global annoncé.

Sauvegardes : checkpoints locaux intermédiaires et branche distante work/v78-batch150. Le checkpoint antérieur à 81 textes est c53c93d ; il reste récupérable. Continuer le même lot, sans nouvelle release après ce sous-ensemble.
