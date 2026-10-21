@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .build-venv
if errorlevel 1 goto fail
.build-venv\Scripts\python -m pip install "pyinstaller==6.11.1"
if errorlevel 1 goto fail
.build-venv\Scripts\python -m unittest discover -v
if errorlevel 1 goto fail
.build-venv\Scripts\python -m PyInstaller --clean --noconfirm --onefile --name THORNS --add-data "static:static" --add-data "creature_catalog.json:." launcher.py
if errorlevel 1 goto fail
echo Built dist\THORNS.exe. Test it on Windows before distribution.
pause
exit /b 0
:fail
echo Build failed. Review the error above.
pause
exit /b 1
