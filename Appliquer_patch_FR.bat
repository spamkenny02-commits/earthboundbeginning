@echo off
cd /d "%~dp0"
if "%~1"=="" (
 echo Glissez votre ROM source sur ce fichier.
 pause
 exit /b 1
)
py -3 traduction\integrer.py "%~1" --appliquer patches\EarthBound_Beginnings_FR_v03_accents.ips
if errorlevel 1 (
 echo Echec : consultez le message ci-dessus.
) else (
 echo ROM francaise creee dans build\EarthBound_Beginnings_FR.sfc
)
pause
