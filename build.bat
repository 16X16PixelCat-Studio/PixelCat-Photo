@echo off
title PixelCat-Photo v0.2.0 Deep Clean Build
echo Cleaning environment...

:: Force refresh of PyInstaller to fix DLL issues
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python -m pip install --upgrade pyinstaller customtkinter pillow

if exist dist rd /s /q dist
if exist build rd /s /q build
del /q *.spec

echo Building v0.2.0...
python -m PyInstaller --clean --onefile --windowed ^
--collect-all tkinterdnd2 ^
--collect-all customtkinter ^
--add-data "assets;assets" ^
--icon="assets/Pixelcat-photo.ico" ^
--name "PixelCat-Photo-v0.2.0" ^
main.py

echo.
echo IMPORTANT: Move the EXE out of the dist folder to your Desktop before running!
pause