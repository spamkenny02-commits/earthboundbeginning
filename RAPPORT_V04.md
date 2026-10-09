# Étape v04 : correction du gain d’expérience

Le « e » parasite venait du champ « the Back Row » à $045502. La traduction « ligne arrière » occupait 13 octets au lieu de 12 et écrasait le NUL $04550E. Le code à $0186CE charge précisément l’adresse C4550E comme chaîne vide (`A9 0E 55 85 0A A9 C4 00 85 0C`). Les quatre octets de pointeur ne sont pas présents côte à côte dans la ROM ; le premier contrôle de pointeurs ne pouvait donc pas détecter cette référence.

« rang arrière » tient dans les 12 octets d’origine. L’intégration protège maintenant explicitement ce terminateur partagé, vérifie la référence machine et refuse son écrasement. Le vérificateur indépendant contrôle aussi le NUL et la référence.

Un nouveau démarrage sous Snes9x 2010 confirme « Ninten gagne 1 EXP. » sans les caractères parasites. Capture : `tests/captures_v04/experience_corrigee.png`. Les deux variantes passent les contrôles binaires. La suite du travail porte sur les textes de combat et les services du début du jeu.
