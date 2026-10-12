@echo off
cd /d "%~dp0"
if "%~1"=="" (
 echo Glissez la ROM originale sur ce fichier pour reconstruire les deux variantes.
 pause
 exit /b 1
)
py -3 traduction\atelier.py construire "%~1" --version v09 --sortie build_v09
if errorlevel 1 (
 echo Echec : consultez le message ci-dessus.
) else (
 echo Patchs, ROM et rapports crees dans build_v09.
)
pause
