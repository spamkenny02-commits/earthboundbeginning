@echo off
cd /d "%~dp0"
if "%~1"=="" (
  echo Glissez votre ROM .sfc sur ce fichier .bat.
  pause
  exit /b 1
)
py -3 outils\extraire.py "%~1"
if errorlevel 1 python outils\extraire.py "%~1"
pause
