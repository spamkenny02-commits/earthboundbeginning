# Traduction française v05 — intégration expérimentale

**671 entrées intégrées**, contre 599 en v04 : 364 champs, 272 dialogues ordinaires, 30 blocs comprimés, trois blocs déplacés et deux textes d'introduction. Six propositions restent exclues, faute de place (cinq libellés et un dialogue du canari).

Les 72 ajouts couvrent le stockage chez Minnie, la séquence familiale, les montées de niveau et statistiques, 22 descriptions PSI, 16 préfixes PSI, la mélodie et sept blocs du téléphone. Les glyphes natifs de niveaux PSI sont conservés ; les valeurs numériques des descriptions ne changent pas. Le menu de sauvegarde, sa confirmation et l'arrêt de la partie sont traduits. Les messages financiers du deuxième appel à papa restent anglais, ainsi que le nom Dad dans le choix d'appel et le libellé Level dans les fichiers.

## Vérification des fichiers

Les deux variantes passent la reconstruction, le contrôle indépendant des 671 entrées, la réapplication IPS, les sommes de contrôle et la prise en charge d'un en-tête copieur. Le profil accents vérifie 80 glyphes dans cinq polices. Les 102 fragments soumis à des références intérieures gardent leurs positions. Le test d'encodage conserve les suffixes PSI natifs et rejette l'injection de commandes. Ces contrôles ne constituent pas une validation complète en jeu.

## Essais dans l'émulateur

Cœur snes9x2010, révision fe690dd321fa5a46b5234a2bde089d2518c62b0e. Captures réelles 256 × 224 et sessions avec empreinte de ROM dans tests/. L'interface de test ne restitue pas le son.

- Nouvelle partie jusqu'à la lampe, attaque, dégâts, 1 EXP et retour dans la maison : les deux variantes finales.
- Oreiller et poupée vaincus ; 10 EXP pour la poupée ; niveau 2, attaque +1 et PV max +1. Ces essais commencent dans des états du même cœur conservés lors des prototypes précédents ; les empreintes de chaque session identifient la version utilisée.
- Boîte à musique, mélodie mémorisée, arrêt du phénomène, conversation avec la mère et premier appel familial observés sur le prototype à 664 entrées.
- Menu Sauver / Rien, merci, confirmation et Suite / Dodo observés sur la version finale à 671 entrées. Le nom variable et les commandes du moteur sont conservés.
- SRAM native de 8192 octets exportée après sauvegarde au téléphone. Redémarrage **sans état instantané**, lecture du fichier SRAM, Ninten niveau 2 dans le menu et chargement dans la maison : les deux variantes finales. La variante ASCII reçoit un délai de transition plus long dans le parcours publié. Ce test confirme la lecture de cette partie, pas tous les emplacements ni les copies ou suppressions.

Les ROM, états instantanés, fichiers SRAM et le cœur d'émulation ne sont pas distribués. Les parcours nécessitant un état initial restent des traces documentées ; leur état n'est pas fourni.

## Limites et prochaine étape

La traduction reste partielle. Tester le stockage, les descriptions PSI dans leurs menus, les cadeaux et la défaite. Poursuivre les messages financiers du père, la cave et la sortie de la maison. Les espaces nécessaires aux pointeurs peuvent laisser des écarts visibles dans certains dialogues ; une relecture de mise en page reste nécessaire. Le son, les graphismes anglais et une partie complète ne sont pas validés. Le kit v04 reste inchangé pour comparaison.
