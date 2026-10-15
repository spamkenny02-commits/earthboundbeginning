# Essais Snes9x V37

Le parcours normal V18 Work a été rejoué avec Snes9x 1.63 dans les profils accents et ASCII : 339 et 337 commandes, jusqu'à l'image 25 803. Les écrans titre, introduction, après-combat, état restauré et menu restent identiques aux références. Les deux seules différences avec V18 sont les deux images de la bannière « VICTOIRE », déjà attendues depuis V36.

Une recherche séparée a rejoué le premier combat depuis un état obtenu par le parcours normal, sans modifier le code ni le point d'entrée. Quatorze délais de confirmation ont produit 252 captures pour V36 et autant pour V37. Aucun coup critique n'a été obtenu : la scène réelle de **« COUP CRIT! » n'est donc pas revendiquée comme validée**.

L'aperçu décompressé/recompressé a été relu : « COUP CRIT! » est net et tient dans les dix emplacements. La tentative `HP` → `PV` a été rejetée avant publication, car ses quatre tuiles partagées altéraient des fenêtres hors combat. Aucun IPS contenant cette tentative n'est conservé.

Les outils [`replay.py`](replay.py) et [`critical_probe.py`](critical_probe.py) reproduisent ces essais. Les ROM, états, WRAM et cœur restent privés et ne sont pas publiés.
