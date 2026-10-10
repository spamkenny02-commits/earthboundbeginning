#!/usr/bin/env python3
"""Construit les fichiers français éditables depuis les exports de référence."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS='''Haunted Lamp|La lampe hantée
Cursed Pillow|L'oreiller maudit
Possessed Doll|La poupée possédée
Cheerful Crow|Le corbeau joyeux
Spiteful Crow|Le corbeau hargneux
Stray Dog|Le chien errant
Guard Dog|Le chien de garde
Frail Snake|Le serpent frêle
Rattlesnake|Le serpent à sonnette
Red Snake|Le serpent rouge
Dirty Rat|Le rat crasseux
Nasty Zombie|Le zombie féroce
Gangster Zombie|Le zombie gangster
Suburban Zombie|Le zombie de banlieue
Pseudo Zombie|Le faux zombie
Alarm Ghost|Le fantôme d'alarme
Alligator|L'alligator
Crocodile|Le crocodile
Medieval Armor|L'armure médiévale
Bionic Batty|La chauve-souris cyborg
Bionic Centipede|Le mille-pattes bionique
Bionic Scorpion|Le scorpion bionique
New Age Retro Hippie|Le hippie rétro
Start New Game|Nouveau jeu
Text Speed:|Vitesse:
Fast|Vite
Medium|Normal
Slow|Lent
Continue|Suite
Copy|Dupl
Delete|Efface
Set Up|Options
Copy to where?|Copier où ?
Are you sure you want to delete?|Effacer cette sauvegarde ?
No|Non
Yes|Oui
Please select text speed.|Choisis la vitesse.
Please select sound setting.|Choisis le mode sonore.
Stereo|Stéréo
Mono|Mono
Which style of windows do you prefer?|Quel style de fenêtre préfères-tu ?
Please name him.|Quel est son nom ?
Name her, too.|Quel est son nom à elle ?
Name your friend.|Nomme ton ami.
Name your other friend.|Nomme ton autre ami.
Favorite homemade food?|Quel est ton plat préféré ?
Favorite food:|Plat préféré:
Beam|Rayon
Are you sure?|C'est bon ?
Yep|Oui
Nope|Non
Fainted|K.O.
Petrified|Pétrifié
Paralyzed|Paralysé
Sick|Malade
Poisoned|Empoisonné
Sunstroke|Insolation
Cold|Rhume
Mushroomized|Champignon
Possessed|Possédé
Asthma|Asthme
Bash|Frapper
Goods|Objets
Auto Fight|Auto
PSI|PSI
Guard|Parer
Sing|Chanter
Shoot|Tirer
Check|Voir
Run Away|Fuir
Mirror|Miroir
Do Nothing|Attendre
Talk to|Parler
Equip|Équiper
Status|État
Level:|Niv.:
Hit Points:|Points vie:
Psychic Points:|Points PSI:
Experience Points:|Expérience:
Exp. for next level.|Exp. niveau suivant
Offense:|Attaque:
Defense:|Défense:
Speed:|Vit.:
Guts:|Cran:
Vitality:|Vitalité:
IQ:|QI:
Luck:|Chan:
@Press the -A- Button for PSI info.|@Touche -A- : infos PSI.
Register your name, please|Inscris ton nom, s'il te plaît
Offense|Attaque
Recover|Soins
Assist|Aide
Other|Autres
PP Cost|Coût PP
To enemy|Sur l'ennemi
To one enemy|Sur un ennemi
to One Enemy|Sur un ennemi
To row of foes|Sur une rangée
To all enemies|Tous les ennemis
To one of us|Sur un allié
to One Friend|Sur un allié
To all of us|Tous nos alliés
To |À 
 the Front Row|la première ligne
the Front Row|ligne avant
the Back Row|rang arrière
  Weapon|     Arme
      Body|     Corps
     Arms|     Bras
     Other|    Autres
Weapons|Armes
Body|Corps
Arms|Bras
Others|Autres
(Nothing) |(Rien)
None|Rien
To:|À:
Use|Util
Give|Don
Drop|Jet
Help!|Aide
Who?|Qui ?
Which?|Lequel ?
Where?|Où ?
Whom?|À qui ?
Stored Goods|Réserve
Call:|Appel
Franklin badge|Badge Franklin
Teddy bear|Ours en peluche
Super plush bear|Super ours en peluche
Old bone|Vieil os
Broken gadget|Gadget cassé
Broken air gun|Fusil à air cassé
Inhaler|Inhalateur
Broken laser|Laser cassé
Broken iron|Fer cassé
Broken pipe|Tuyau cassé
Broken cannon|Canon cassé
Broken tube|Tube cassé
Broken bazooka|Bazooka cassé
Broken trumpet|Trompette cassée
Broken harmonica|Harmonica cassé
Broken antenna|Antenne cassée
Plastic bat|Batte en plastique
Wooden bat|Batte en bois
Aluminum bat|Batte en aluminium
Nail bat|Batte à clous
Lucky bat|Batte porte-bonheur
Screwball bat|Batte courbe
Slugger bat|Batte de frappeur
Magicant bat|Batte de Magicant
Hank's bat|Batte de Hank
Home-run bat|Batte de champion
Knit cap|Bonnet
Fry pan|Poêle
Non-stick pan|Poêle antiadhésive
Iron skillet|Poêle en fer
Slap bracelet|Bracelet claquant
Thick fry pan|Poêle épaisse
Peter's pan|Poêle de Peter
Spirit bat|Batte spirituelle
Stellar cannon|Canon stellaire
Zap gun|Pistolet électrique
Stun gun|Pistolet paralysant
Air gun|Fusil à air
Magnum air gun|Fusil à air Magnum
Zip gun|Pistolet artisanal
Deluxe fry pan|Poêle de luxe
Extreme cannon|Canon extrême
Mushroom soup|Soupe aux champignons
Hot chocolate|Chocolat chaud
Galoshes|Bottes de pluie
Toy rocket kit|Fusée-jouet en kit
Model rocket kit|Maquette de fusée
George's Diary|Journal de George
Butterfly yo-yo|Yo-yo papillon
Slingshot|Lance-pierre
Boomerang|Boomerang
Trick yo-yo|Yo-yo acrobatique
Combat yo-yo|Yo-yo de combat
Travel charm|Charme du voyageur
Great charm|Grand charme
Crystal charm|Charme de cristal
Rain pendant|Pendentif de pluie
Flame pendant|Pendentif de flamme
Earth pendant|Pendentif de terre
Night pendant|Pendentif de nuit
Sea pendant|Pendentif marin
Star pendant|Pendentif étoilé
Complex kit|Kit complexe
Cheap bracelet|Bracelet bon marché
Copper bracelet|Bracelet de cuivre
Silver bracelet|Bracelet d'argent
Gold bracelet|Bracelet d'or
Miracle band|Bracelet miracle
Diamond band|Bracelet de diamant
Crumpled paper|Papier froissé
Baseball cap|Casquette
Girl's hat|Chapeau de fille
Dentures|Dentier
Ticket stub|Talon de billet
Ribbon|Ruban
Red ribbon|Ruban rouge
Goddess ribbon|Ruban de déesse
Coin of slumber|Pièce du sommeil
Coin of defense|Pièce de défense
Onyx hook|Crochet d'onyx
Last weapon|Arme ultime
Shiny coin|Pièce brillante
Souvenir coin|Pièce souvenir
Double burger|Double hamburger
Cookie|Biscuit
Bag of fries|Sachet de frites
Hamburger|Hamburger
Boiled egg|Œuf dur
Fresh egg|Œuf frais
Picnic lunch|Panier-repas
Roasted corn|Maïs grillé
Pizza|Pizza
Chef's special|Spécialité du chef
Large pizza|Grande pizza
PSI caramel|Caramel PSI
Magic truffle|Truffe magique
Brain food lunch|Repas cérébral
Rock candy|Sucre candi
Croissant|Croissant
Bread roll|Petit pain
Medium pizza|Pizza moyenne
Skip sandwich|Sandwich express
Can of fruit juice|Jus de fruits
Peanut cheese`bar|Barre aux cacahuètes
Sports drink|Boisson énergétique
Life-up cream|Crème de vie
Bottle of water|Bouteille d'eau
Cold remedy|Remède contre le rhume
Vial of serum|Fiole de sérum
Wisdom capsule|Capsule de sagesse
Physical capsule|Capsule de vitalité
Speed capsule|Capsule de vitesse
Fight capsule|Capsule de cran
Force capsule|Capsule de force
Ketchup packet|Sachet de ketchup
Friendship ring|Bague de l'amitié
Tin of Cocoa|Boîte de cacao
Ocarina|Ocarina
IC-chip|Puce électronique
Jar of hot sauce|Sauce piquante
Salt packet|Sachet de sel
Sugar packet|Sachet de sucre
Jar of delisauce|Sauce spéciale
Wet towel|Serviette humide
Refreshing herb|Herbe rafraîchissante
Magic herb|Herbe magique
Horn of life|Cor de vie
Counter-PSI unit|Unité anti-PSI
Shield killer|Brise-bouclier
Bazooka|Bazooka
Heavy bazooka|Bazooka lourd
HP-sucker|Aspire-PV
Hungry HP-sucker|Super aspire-PV
Super spray|Super aérosol
Slime generator|Générateur de gel
Flashdark|Lampe noire
Ruler|Règle
Flea bag|Sac de puces
Words of love|Mots d'amour
Protractor|Rapporteur
Bottle rocket|Petite fusée
Big bottle rocket|Grande fusée
Multi`bottle rocket|Salve de fusées
Bomb|Bombe
Super bomb|Super bombe
Insecticide spray|Insecticide
Rust promoter|Accélérateur de rouille
Rust promoter DX|Rouille express DX
Swear words|Gros mots
Stone of Origin|Pierre des origines
Poison needle|Aiguille empoisonnée
Flamethrower|Lance-flammes
Real rocket|Vraie fusée
Defense shower|Douche défensive
Letter from mom|Lettre de maman
Sudden fight pill|Pilule de courage
Bag of Dragonite|Sac de Dragonite
Defense spray|Spray défensif
Piggy nose|Groin de cochon
For Sale sign|Pancarte à vendre
Bread loaf|Pain
Banana|Banane
Letter from Tony|Lettre de Tony
Canary chick|Bébé canari
Chicken|Poulet
Basement key|Clé de la cave
Key to the zoo|Clé du zoo
Bad key machine|Machine à clés
Mouthwash|Bain de bouche
Trout yogurt|Yaourt à la truite
Bicycle|Vélo
ATM card|Carte bancaire
Old pass|Vieux laissez-passer
Noble seed|Graine noble
Live Show ticket|Billet de concert
Receiver phone|Téléphone récepteur
Red weed|Herbe rouge
Bullhorn|Mégaphone
Debugger|Débogueur
Flight plan A|Plan de vol A
Flight plan B|Plan de vol B
Flight plan C|Plan de vol C
Calorie stick|Barre calorique
Carton of cream|Brique de crème
Plain roll|Pain nature
Time machine|Machine temporelle
Key to the manor|Clé du manoir
Meteorite piece|Fragment de météorite
Secret herb|Herbe secrète
Neutralizer|Neutraliseur
Carton of milk|Brique de lait
Sprig of parsley|Brin de persil
Cheeseburger|Hamburger au fromage
Crisp apple|Pomme croquante
Juicy pear|Poire juteuse
PSI stone|Pierre PSI
Town map|Plan de la ville
Magic ribbon|Ruban magique
Magic candy|Bonbon magique
Key to the locker|Clé du casier
Insignificant item|Objet insignifiant
Magic tart|Tarte magique
Tiny ruby|Petit rubis
Monkey's love|Amour de singe
Eraser eraser|Efface-effaceur
Tendakraut|Choucroute Tenda
T-rex's bat|Batte de T-Rex
Big league bat|Batte pro
Ultimate bat|Batte ultime
Laser beam|Rayon laser
Plasma beam|Rayon plasma
Defense ribbon|Ruban de défense
Talisman ribbon|Ruban talisman
Saturn ribbon|Ruban Saturne
Coin of peace|Pièce de paix
Rope|Corde
Protection coin|Pièce protectrice
Magic coin|Pièce magique'''
# Chaque entrée remplace les fragments de texte du bloc, dans leur ordre.
# Les commandes sont récupérées à l'identique depuis les octets de référence.
FIELDS += '''
PK Fire |PK Feu 
PK Freeze |PK Glace 
PK Thunder |PK Foudre 
PK Flash |PK Éclat 
PK Starstorm |PK Météores 
Lifeup |PV+ 
Healing |Soins 
Shield |Écran 
PSI Shield |Écran PSI 
Offense up |Attaque+ 
Defense down |Défense- 
Hypnosis |Hypnose 
PSI Magnet |PSI Aimant 
Paralysis |Paralysie 
Brainshock |Confusion 
Teleport |Téléport '''
DIALOGUES='''2FA66C|MAJ|min|Au choix|Effacer|OK
2FA6A7|MAJ|min|Effacer|OK
3675EA|Le badge Franklin renvoie le rayon !
36761A|            || gagne | EXP
36765C|            || gagne | EXP
3678E0|| respire normalement !
367907|| tousse|sans arrêt !
367A28|| cède !
367A3D|Mais | résiste !
367AD2|| te|défie !
367B9A|| a |abandonné le combat !
367D77|| est à bout.
37F0D4|| s'approche...
37F192|| barre la route !
37F373|| attaque !
37F389|| barre la route !
37F3A6|| te poursuit !
37F3C2|| te piège !
37F3DB|Tu rencontres 
37F425|Tu vois 
37F439|Tu défies 
37F44F|Tu défies 
37F467|| est en miettes !
37F488|| est|en miettes !
37F4AB|| reprend sa forme !
37F4CD|| retourne à la poussière !
37F4FB|| a perdu !
37F51F|| s'immobilise !
37F53A|| se calme !
37F552|| disparaît !
37F56A|L'image de | s'évanouit dans l'air !
37F599|| tombe en morceaux !
37F5BC|| tombe|en morceaux !
37F5E1|| est hors jeu !
37F5FB|| finit|en tas de duvet !
33A03A|Tu frappes peut-être aux portes au hasard, mais...|N'oublie jamais que, qui que tu sois...|quelqu'un t'aime quelque part.|C'est beau, non ?|Je pourrais être poète, tu ne crois pas ?
33A184|Voilà le livreur de pizzas !|Hé, une seconde...|Je ne sens aucune pizza derrière la porte !|Pas question !|Je ne me ferai plus avoir.
33A220|Les trains ne roulent toujours pas ?|Que se passe-t-il donc ?|Sans leur sifflet au loin, impossible de dormir...
33A2BA|Le doux sifflet d'un train au loin apaise mon âme.|Les trains roulent à nouveau. Je peux enfin bien dormir.
33A340|Tu écoutes la radio ?|Oui|Non
33A384|Il y a un groupe que j'aime bien...|Une chanson fait <yeah, yeah, yeah>... enfin, je crois.|À bien y penser, ça n'a pas grand intérêt...
33A6B8|Hmm...|Je veux appeler mes parents pour qu'ils me ramènent...|Mais ce téléphone vert coûte un dollar. Je tiens à mes sous.|Avec tous ces appels, mon argent de poche partirait vite.|Si seulement il était noir ! Ceux-là sont gratuits !
33A7BE|Oups ! (Boum) Pardon !|Je suis... (argh) ...coincé dans ce coin.|Tout à l'heure, j'ai... (zut) vu ce champignon sur ma tête.|Depuis, j'ai du mal à marcher dans la bonne direction.|Le drôle de type à l'accueil veut l'acheter,|mais le médecin dit de le traiter comme une mycose !|Qui croire ? Je suis bien embêté !
33A96E|*grommelle*|Ces zombies empestent.|Les animaux du zoo sont en liberté. Le maire ne fait rien.|Routes barrées.| Des gamins entrent chez moi.|Même les oiseaux ne chantent plus !|Cette ville tourne mal. Je reste chez moi aujourd'hui.|Pas même un orteil dehors.
33AA9A|As-tu déjà essayé les condiments avec tes plats ?|C'est vraiment incroyable !|Ils assaisonnent tes plats tout seuls, comme par magie !|Si le condiment va bien avec ton plat,|tu récupères BEAUCOUP plus de PV !|Essaie donc ! En plus, ça ne coûte pas cher !
33ABF8|Hein... Tu es perdu, petit ?|Tu as l'air perdu.|Avec un plan de la ville, tu trouveras ton chemin.|Sais-tu que <X> affiche ton plan si tu es perdu ?|Ça marche aussi quand tu sais où tu vas.|Eh oui ! <X> affiche le plan ! Ho ho ho !|Bon...| Reviens me voir.| (tousse)
33AE0C|Tu es un ami de | ?
33AE2C|Hmm... Tu peux me parler de l'autre côté du bureau ?|Sinon, je n'ai pas vraiment l'air... d'un maire.
33AEAC|Reviens vivant,| et tu seras un héros !|Si je me sentais mieux,| je viendrais avec toi...| *Hum hum*| *tousse*
339A92|Qu'attends-tu ?
339AAE|Tu sais quoi faire.
339ACB|Elle t'attend.
339C02|(On entend un aspirateur en marche...)
339D9E|Qui est là ?|Ah, un gamin.|Tu ne m'auras pas avec ta sonnette !
339DF7|Pourquoi frapper chez des inconnus ?|Ta mère ne t'a pas dit de t'en méfier ?
339EE7|Hahaha...|P-personne ici !
339F10|Oh, laisse-moi.|Je ne suis personne.
33A448|Tu es vraiment ennuyeux, hein ?|Va donc ennuyer quelqu'un d'autre.
33A497|Conseils de survie|<Hôtel :> Une nuit rend tous tes PV et PP.|<Défaite :> Reprendre rend tous tes PV, mais aucun PP.|Tu perds aussi la moitié de ton argent de poche.
33A577|Conseils pratiques|<Distributeur :> Il permet de retirer de l'argent.|On en trouve dans les hôtels, magasins et gares.|<Téléphone :> Il permet de sauvegarder ta partie.|Les noirs sont gratuits. Les verts coûtent $1.|On en trouve aussi près des distributeurs.
33A940|<Podunk>|Paix et belles fleurs.
33AD70|1er étage : Accueil|2e étage : Pharmacie|3e étage : Articles de sport|4e étage : Restauration|5e étage : Animaux
33ADEC|Les animaux restent dehors.
33AF88|<Lapin commun>|Les savants du monde entier le trouvent adorable.
33AFD2|<Tigre rare>|Il change de rayures quand elles sont sales.
33B036|<Éléphant d'Afrique>|De tous les animaux du zoo, c'est le pire sauteur.
33B088|<Alligator commun>|Il adore l'eau, mais il arrive souvent en retard.
33B0D6|<Panda géant>|L'un des mangeurs les plus difficiles qui soient.
33B11A|<Manchot de Humboldt>|Il vient du Chili et du Pérou.|Pas un manchot humble !|C'est un incorrigible vantard.
33B198|Gorille de l'Est|L'empreinte de son nez est unique, comme celle d'un doigt.|S'il commet un crime, les preuves sont sur son visage.
33B23D|<Flamant nain>|Sa couleur rose vient de son alimentation.|On cherche des aliments qui lui donneraient d'autres couleurs.
33B2C2|<Hyène tachetée>|Plus proche du chat que du chien, elle adore les blagues.
33B315|Les alligators, mes préférés !
33B336|Ohoho !|Vous pourriez prendre exemple sur mes petits-enfants.|Chérissez chaque souvenir et chaque découverte.
33B5CD|Mon fils joue au malade pour rater l'école.|J'ai fait pareil pour éviter le travail !|Le voir heureux en valait la peine.|Je suis un super papa, non ?
33B67F|Il paraît que certains singes savent chanter !|Mais il paraît aussi qu'ils savent mentir.|Un singe mentirait-il sur ses talents de chanteur ?
33B715|(Une inscription.)|Le monde est meilleur quand on est aimé. Je t'aime.
33B76A|En attente.
33B779|R.A.S.
33B786|Cui-cui
33BE79|(Des rochers bloquent les rails.)
33C256|Ouaf, ouaf.|(Pardon. Parfois, un chien doit aboyer.)
33C299|Des produits d'ici.|Des saveurs d'amis.|Marché de Reindeer
33C2DA|Bienvenue|au pays du burger !|Mange à ta faim|le meilleur du coin !
33C327|Air et eau purs,|la ville sans souci !|<-Reindeer>
33C365|Tu aimes voyager en train ? Parfait !|La gare de Reindeer est au nord.|Suis simplement les rails !
33C3DE|Des lits doux et chauds.|Une table raffinée.|Hôtel du Soleil Couchant, à l'ouest.
33C443|Pour des achats imbattables,|visitez notre grand magasin juste en face !
36A9DB|Aide-nous !
36AA33|Mon fils, tu es plus brave que prévu.|Tu ne peux pas partir le ventre vide.|Voici du |.|Mange, puis dors bien.
36AAED|Pour remanger du |, reviens à la maison.
36AB32|Aidez mon petit | autant que possible.
36ABB9|Oh, tu ne peux plus rien porter, pas vrai ?
36ABFC||! Tout va bien ?|Mon Dieu ! Qu'arrive-t-il à la maison ?|Oh là là,|oh là là...|Si ton père était là, tout irait peut-être mieux.|J'aimerais tant...
36ACA3|Décroche !|C'est peut-être papa.
36ADF1|| décrocha le téléphone.|Allô, |?| C'est papa.|Tout le monde va bien ?|Les infos parlent de phénomènes étranges partout.|Je voulais savoir si vous alliez bien.|Comment ?|Je vois.|Je vois...|Hmm...|On dirait qu'un fantôme hante notre maison !
36AF40|Un fantôme devait hanter notre maison.|Heureusement que tu étais là !|Bravo !|Je ne comprends pas...|Ton arrière-grand-père étudiait les PSI.|Pour comprendre tout ça,|cherche ses vieilles affaires dans la cave.|J'ai rangé la | en lieu sûr...|...mais je ne sais plus où...|Bref, tu es notre seul espoir.|Tu es assez grand pour découvrir le monde.|Il est temps de partir à l'aventure.||, fonce !|Reviens quand même voir ta famille.|À+ !|Ah... Appelle-moi pour sauvegarder ta partie.|Appelle quand tu veux.|Clac!|Biiiiip !
36B28A|Frérot, j'ai peur !|Cet oreiller est vivant !
36B2D2|Frérot !|La maison va vraiment s'écrouler ?|Bouhouhou !
36B323|Mimmie et maman sont en danger aussi !|Bouhouhou !
36B35A|À moi !
36B371|J'étais terrifiée...|Oh ! Je crois qu'il y a quelque chose dans la poupée.
36B3D6|Moi, c'est Mimmie, pas Minnie !
36B403|Frérot, voici du jus.|Tu as soif, non ?
36B458|Désolée, tu ne peux plus rien porter.
36B493|Dans la poupée,| | trouva une boîte à musique.|En remontant la boîte...|Une mélodie se fit entendre.
36B582|OUAF, OUAF !|(Tu peux parler aux animaux, non ?)|(Un petit secret...)|(Et si tu m'examinais ?)
36B5F1|OUAF !|(Pas mal, hein ?)|(Quand tu trouves quelque chose d'étrange, examine-le.)
36B658|Le collier du chien cachait la | !
36B6B8|Ouaf...|(Oh...|Tu ne peux plus rien porter.)
36B6F8|C'est fermé.
36B752|Cette clé ne convient pas.
36B788|Moi, Minnie|Que veux-tu ?|Dépôt|Retirer
36B86C|Tu veux me confier autre chose ?|Oui|Non
36B8C1|Tu n'as rien à me confier.
36B8F3|Tu as besoin d'autre chose ?
36B91C|Désolée.|Casier plein.
36B944|Je ne garde aucun de tes objets.
38A32A|C'est fermé à clé.
38A345||!|Les combats t'ont épuisé.|Tu veux essayer encore une fois ?|Oui| |Non
38A3D7|Tu es sûr ?|À ta prochaine aventure,|tu reprendras à ta dernière sauvegarde.|D'accord ?|Non| |Oui
38A466|Ayant repris des forces...|| revint à la charge !|Courage, | !
38A4C3|| comprit que ce n'était qu'un mauvais rêve.|Courage, | !'''

DIALOGUES += '''
371C72|Regarde, les animaux se sont enfuis.|Il ne reste que ce |.|Tu veux l'acheter ?|Oui|Non
371CFC|Alors, pour 85 $ ?|Oui|Non
371D56|Merci ! Prends-en soin.|Reviens nous voir !
371D9E|Oh ? Tu n'as pas assez d'argent.
371DC9|Oui, je comprends.|Il ne sait même pas chanter.
371E06|Tu le veux gratuitement ?|Prends-le !
371E63|Tu ne peux plus rien porter.
371E94|Et le canari ?|Ah...| ils sont mignons, hein ?|Oui|Non|Imbécile !
371EF2|Regarde, les animaux se sont enfuis...
371F27|Quelque chose contrôle les animaux.
371F57|Bonjour !|Que veux-tu ?
371F7F|Merci !
371F8C|Tu regardes seulement ?
371FA7|Tu cherches|quelque chose ?
371FCA|Tu veux| |?
371FE0|Qui va le porter ?
371FF7|Tu veux l'équiper ici ?
372017|Je rachète| |pour | $?
372040|| ne peut l'équiper.|Tu l'achètes quand même ?
372077|Tu n'en veux pas... Hmm...
3720A4|Tu n'as pas assez !
3720BE|Tu portes trop de choses.|Tu veux m'en vendre ?
37210C|Que me proposes-tu ?
372127|Le |?|Je t'en offre | $.
372154|Tant pis
372160|Tu n'as rien à me vendre.
37219E|Je ne rachète pas |.
3721BF|Merci bien !
372215|Autre chose ?
372234|Que veux-tu ?
37224D|| porte trop de choses.|Quelqu'un d'autre le prend ?
372295|Tout ça ?
3722A6|Tu n'as pas assez pour tout payer.
3722DF|Tu ne peux pas tout porter.
372304|D'accord.
372311|Salut !|Que veux-tu ?
372337|Cool, merci.
372347|Si tu n'achètes rien, va voir ailleurs.
372380|Que veux-tu ?
372394|Tu veux| |?
3723AA|Qui va le porter ?
3723C1|Tu veux l'équiper ?
3723DA|Je te rachète|le |pour | $ ?
37240F|| ne peut l'utiliser !|Tu l'achètes ?
372442|D'accord.
372452|Tu n'as pas assez !
37246C|Tu ne peux plus rien porter !|Tu veux vendre des objets inutiles ?
3724C4|Tu as quoi ?
3724D6||?|Je t'offre | $ ?|Ça te va ?
37250D|Ça me plaisait pourtant. Dommage.
372535|Tu n'as rien à vendre, je crois.
37256B|Je refuse ça !
372583|Cool, merci.
3725D7|Autre chose ?
3725F6|Que veux-tu d'autre ?
372619|On dirait que | ne peut plus rien porter.|Quelqu'un d'autre le prend ?
372670|Tout ça ? D'accord.
372687|Tu n'as pas assez pour tout ça !
3726AB|Tu ne peux pas tout porter.
3726D6|Rien ? Je ne peux pas te vendre du vide !
372705|Bonjour !|Que veux-tu ?
372729|À bientôt !
372737|Bonne journée !|(Sourire)
37275B|Regarde.
37276A|Le |?
372775|Qui va le porter ?
37278A|Tu veux l'équiper ?
3727A3|Je te rachète| |pour | $.
3727DB|| ne peut l'utiliser|Tu le veux ?
372803|D'accord
37280F|Oh... Tu n'as pas assez d'argent.
372839|Tu portes trop d'objets.
372854|Que me proposes-tu ?
372870|Le |?|Je t'en offre | $.
372899|Rien ?
3728A5|Oh... Tu n'as rien.
3728C2|Je ne peux pas racheter| |...
3728F1|Merci !
372942|Autre chose ?
372953|Que veux-tu ?
37296C|| porte trop d'objets.|Un autre le prend ?
3729A1|Tu aimes les féculents, toi.
3729C1|Désolé, tu n'as pas assez pour tout ça.
3729EF|Tu ne peux tout porter.
372A0D|Tu veux... rien ?
372A22|Un bouclier de lumière protège un allié.|Réduit de moitié les dégâts des attaques ennemies.
372A89|Protège le groupe par un bouclier de lumière.|Réduit de moitié les dégâts des attaques ennemies.
372AEE|Protège une personne par un bouclier de force.|Réduit les dégâts de moitié et en renvoie une partie à l'ennemi.
372B68|Protège le groupe par un bouclier de force.|Réduit les dégâts de moitié et en renvoie une partie à l'ennemi.
372BE0|Un autre bouclier annule ces effets.
372C15|Un rayon de lumière inflige environ 80 dégâts à un ennemi.
372C5E|Deux rayons de lumière infligent environ 220 dégâts à un ennemi.
372CAB|Un rayon de lumière élimine un ennemi sur-le-champ.
372CEE|Un rayon de lumière frappe tous les ennemis.|Inflige environ 600 dégâts.
372D42|Tente de fuir le combat par la quatrième dimension.|Les alliés mortellement touchés tombent avant la fin du transfert.
372DCB|Détruit le bouclier d'un ennemi.|Agit sur les boucliers physiques et psychiques.
372E22|Peut priver un ennemi de PSI un temps.
372E4D|Aveugle un ennemi.
372E86|Aveugle tous les ennemis.
372EBB|Permet de lire les pensées des gens ou des animaux.
372EF4|Machines : effet réduit.
372F11|Sans effet sur les boss.
372F2F|Peut être moins efficace sur certains ennemis.
372F61|Augmente la vitesse d'une personne jusqu'à la fin du combat.
33C6E8|Rien à signaler.
347960|Rien à signaler.
3744AD|Rien à signaler.'''

DIALOGUES += '\n33ED82|Biiiip...\n36ADB4|Biiiip...'

DIALOGUES += '''
36B715|| ouvrit la porte.
36B7D5|Que veux-tu me confier ?||?|Je le garderai en lieu sûr.
36B96F|Tu devrais garder ça.
36B99B|Tu portes déjà trop d'objets.
36B9D9|Que veux-tu|récupérer ?
36BA13|Le |?|Prends-en soin.|Tu veux autre chose ?|Oui|Non
36BACB|À bientôt, |...|Prends soin de toi !'''

DIALOGUES += '''
36A934|Frérot !
36A96E|Le téléphone !||, décroche !
36A9EC|Oh ! Tu es blessé !'''

DIALOGUES += '''
372FAC|Augmente la vitesse du groupe jusqu'à la fin du combat.
372FF5|Augmente la défense d'une personne jusqu'à la fin du combat.
373042|Augmente la défense du groupe jusqu'à la fin du combat.
37308D|Réduit la défense d'un ennemi jusqu'à la fin du combat.
3730DD|Réduit la défense des ennemis jusqu'à la fin du combat.
37312E|Augmente l'attaque d'une personne jusqu'à la fin du combat.
37317B|Augmente l'attaque du groupe jusqu'à la fin du combat.
3731C6|Les utilisations successives cumulent cet effet.
373201|Trouble l'esprit d'un ennemi.
373220|Cette technique s'appelle aussi <Cyclone mental>.
37325C|Soigne rhume, poison, insolation et sommeil.
373296|Aux effets de Soins [8B] s'ajoute le soin des nausées, de la confusion et de la cécité.
3732F2|Aux effets de Soins [8C] s'ajoute le soin de la pétrification et de la paralysie.|Ranime aussi un allié inconscient, sans rétablir tous ses PV.
373398|Aux effets de Soins [8D] s'ajoute le retour de tous les PV d'un allié ranimé.|Cette technique s'appelle aussi <Super guérison>.
37342A|Des flammes jaillissent des doigts : environ 80 dégâts par ennemi d'un rang.
373488|Des flammes jaillissent des doigts : environ 160 dégâts par ennemi d'un rang.
3734E7|Des flammes jaillissent des doigts : environ 280 dégâts par ennemi d'un rang.
373546|Des flammes jaillissent des doigts : environ 400 dégâts par ennemi d'un rang.
3735A5|Un vent glacial inflige environ 180 dégâts à un ennemi.|Peut le geler entièrement.
373628|Un vent glacial inflige environ 360 dégâts à un ennemi.|Peut le geler entièrement.
3736AB|Un vent glacial inflige environ 540 dégâts à un ennemi.|Peut le geler entièrement.
37372E|Un vent glacial inflige environ 540 dégâts à tous les ennemis.|Peut les geler entièrement.'''

DIALOGUES += '''
36ACF9|Le phénomène s'est arrêté... pour l'instant.'''

DIALOGUES += '''
38D12D|| retint la mélodie.'''

DIALOGUES += "\n35A9C3|La carte téléphonique n'a plus de crédit.|| décroche le téléphone.\n35C53A|| décroche le téléphone.\n35C597|| décroche le téléphone.\n35C768|De quoi as-tu besoin ?|Sauver|Rien, merci|Bon vent !\n35C7C8|D'accord... Je pensais aussi aller dormir.|J'ai sauvegardé tous tes combats.|Bonne nuit.|Suite|Dodo|Tu travailles dur, comme |.|Mais ne te fatigue pas trop.\n35C8E9|On fait une belle équipe !|Éteins la console plutôt que d'appuyer sur RESET.|D'accord ?\n35C960|(Clac ! Biiiip...)"

FIELDS += '\nDad|Papa\nLevel:|Niv.'
DIALOGUES += '\n35C583|Manque d’argent.\n35C5D9|Ici |.|J’ai versé $|pour |.|Après ce que | dépensé, il reste|$| en banque.|Dépense avec prudence.|Pour le prochain niveau...|| EXP : |.'

def main():
    import sys
    sys.path.insert(0,str(ROOT/'atelier/outils'))
    from extraire import parse,render
    mapping=dict(line.split('|',1) for line in FIELDS.splitlines())
    rows=json.loads((ROOT/'atelier/extraction/champs_menus_objets_ennemis.json').read_text(encoding='utf-8'))
    extra=json.loads((ROOT/'traduction/sources_complementaires.json').read_text(encoding='utf-8'))
    names=[dict(r,text_fr=mapping[r['text_en']],status='draft') for r in rows if r['text_en'] in mapping and mapping[r['text_en']]!=r['text_en']]
    names.extend(dict(r,status='draft') for r in extra['fields'])
    for r in names:
        if r['source']=='ENEMY_CONFIGURATION_TABLE':r['article_in_name']=True
    blocks={r['id']:r for r in json.loads((ROOT/'atelier/extraction/dialogues.json').read_text(encoding='utf-8'))}
    blocks.update({r['id']:r for r in extra['blocks']})
    translated=[];errors=[]
    for line in DIALOGUES.splitlines():
        id,*values=line.split('|');r=blocks[id];raw=bytes.fromhex(r['raw_hex']);parsed=parse(raw,0,max_bytes=len(raw)+1)
        if len(values)!=len(parsed['spans']):
            errors.append({'id':id,'provided':len(values),'needed':len(parsed['spans']),'english':[render(raw[a:b]) for a,b in parsed['spans']]});continue
        result=bytearray();last=0;parts=[]
        for (a,b),fr in zip(parsed['spans'],values):
            en=render(raw[a:b]);prefix='@' if en.startswith('@') else ''
            fr=prefix+fr
            if en.startswith('  '):fr='  '+fr
            parts.append(dict(offset=a,original=en,french=fr));last=b
        translated.append(dict(r,text_fr_segments=parts,status='draft'))
    for filename,content in [('menus_objets_fr.json',names),('dialogues_fr.json',translated),('erreurs_preparation.json',errors)]:
        (ROOT/'traduction'/filename).write_text(json.dumps(content,ensure_ascii=False,indent=2), encoding='utf-8')
    print('Champs',len(names),'dialogues',len(translated),'erreurs',len(errors))
    for e in errors:print(e)
if __name__=='__main__':main()
