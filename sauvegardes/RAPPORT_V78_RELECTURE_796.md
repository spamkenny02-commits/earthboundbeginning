# Relecture V78 : dialogues placés et noms

Cette reprise corrige du français existant : **zéro nouvelle traduction anglaise**. Les28 sources du checkpoint3185898 restent historiques. Total inchangé :249 sources distinctes/297 plages originales,137 publiées/112 en attente. Ni le lot400 en une exécution, ni une exception globale sous400, ni la traduction complète ne sont certifiés.

## Relecture et corrections

Le registre V78 de249 sources a été relu face à ses sources. L'indice d'eau télépathique rétablit « au loin ». La seconde introduction télépathique distingue l'interlocuteur (« Tu m'es inconnu ») ; « Au sud. » libère l'octet nécessaire sans agrandir le script. Les deux racines modifiées sont relues sur21 vues uniques par profil après appel forcé. Ce ne sont pas des activations naturelles.

Une autre passe manuelle couvre796 amorces littérales distinctes commençant par@, de huit caractères minimum, dans la fermeture typée des PNJ placés ; PNJ développeur86 exclu comme graine. La liste exacte et ses chemins sont conservés dans `tools/v78/placed_dialogue_proofreading.json`. Cette sélection ne couvre pas les continuations séparées par commandes, tous les textes du jeu, ni leur fidélité bilingue complète. Elle ne vaut pas796 nouvelles traductions.

Six contextes corrigés : apostrophe « m'en doutais » ; ponctuation « Bon, alors. » ; « gare Union » ; « J'aime ce lieu. » ; « Une voix dans la tête de [nom] » ; « Je suis une dame ! ». Cela représente huit plages françaises, dont les deux plages supplémentaires servent à reprendre les espaces et la ponctuation. Les deux derniers scripts sont recomposés dans leurs limites d'origine, sans référence intérieure ; commandes, sauts externes, noms dynamiques et points d'entrée sont conservés. Aucun nouvel espace alloué. Les quatre autres corrections restent à taille fixe.

La phrase3479FF « a une question dans ... tête » est un faux positif de lecture isolée : l'auxiliaire français251E00 fournit « sa ». Elle reste inchangée.

## Catalogue supplémentaire

Les effets des six identifiants supplémentaires54/8A/84/9C/BF/AC sont inclus dans l'union de154 objets qualifiés (94 était déjà présent). Aucun candidat alphabétique anglais inchangé ni erreur de parsing dans cette fermeture ; cela ne certifie pas tous les objets obtenables ou leurs effets naturels.

BF : « Machine temporelle »83px devient « Machine du temps »78px, dans une colonne de80px. Le champ25 octets est seul modifié ; prix, effets et aide restent identiques. Deux inventaires accents/ASCII sont relus après remise temporaire native, pas après une acquisition naturelle. Les comparaisons V77/V78 comprennent aussi le libellé préexistant « Lequel ? » de V78 ; les deux fenêtres sont explicitement déclarées.

Attention : les fichiers `inventory.png` du probe générique de la boutique sont des noms d'actions, pas une certification automatique d'inventaire. Pour BF, l'achat poursuit le dialogue d'histoire « Prends ce bouton... ». La vue d'inventaire BF est donc certifiée séparément après remise native. Ne pas transformer les14 achats en14 inventaires vérifiés.

## Validation

Douze appels forcés pour les six corrections,38 captures relues dans les deux profils. Aucune écriture WRAM directe ; aucun effet ou accès naturel de fin certifié. Rapports typés et PNG : `tests/emulation_v78_french_review`. Les scènes conditionnelles ont également été rejouées ; leurs rapports gardent les hashes du build réellement observé. Les anciennes scènes d'achats et du formateur de noms gardent leurs propres hashes, sans être renommées en preuves du dernier ROM.

82 tests distincts validés avec la ROM privée :80 réussites lors de la passe générale, puis quatre tests ciblés réussis (dont deux déjà inclus) après ajout de la nouvelle étape au registre des enregistrements IPS et du contrôle d'intégrité des38 captures. Le premier contrôle du registre omettait les six nouveaux enregistrements ; cette liste de contrôle a été corrigée. Les deux IPS intégrés sont identiques aux sorties de la reconstruction complète. Les inventaires dépendants ont été actualisés après les corrections.

| Profil | SHA256 IPS | SHA256 cible privée |
| --- | --- | --- |
| accents | `7209d90d7af4a3dd99d2d12cbd31361afdb2bb2e0be10d2f10ed6ebee366de9d` | `36ae258de422b0f88bfa8ba16114aeb479b6d7950a59647fc44a76c68210721c` |
| ascii | `39e1eda380abe4331bda6a350ba927d88df1e1deffa7d8e6205d4cad301c83fe` | `335c6324c91870e8a24eb5ed302809ddec6e09c58ac9c2c32e9da47dff783334` |

## Reprise

Poursuivre les continuations françaises et les assemblages de variables, puis les autres catégories et graphiques. Les amorces796 et le registre249 sont des couvertures limitées et se chevauchent : ne pas les additionner comme textes uniques du jeu. Les racines héritées non qualifiées, accès calculés, activation naturelle des fins et nom dynamique final restent ouverts. Aucun état tardif n'est disponible dans les dépendances privées actuelles ; les états précoces permettent les appels contrôlés, pas une validation de partie complète.

Sauvegarde locale et checkpoint Git ; aucune release V78 et aucun100% annoncé. Le push shell sans identifiants a échoué. ROM, cœur, états, traces de registres et dumps mémoire ne sont pas inclus.
