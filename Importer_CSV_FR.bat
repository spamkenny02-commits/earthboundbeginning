@echo off
cd /d "%~dp0"
if "%~1"=="" (
 echo Glissez un CSV exporte par l'atelier sur ce fichier.
 pause
 exit /b 1
)
py -3 traduction\atelier.py importer "%~1" --appliquer
if errorlevel 1 (
 echo Echec : aucune modification de traduction invalide n'a ete acceptee.
) else (
 echo Import termine. Reconstruisez avec la ROM originale pour verifier les tailles.
)
pause
