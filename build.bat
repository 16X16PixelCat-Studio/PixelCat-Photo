@echo off
title PixelCat-Photo v0.1.2 Builder
echo ========================================
echo   Building PixelCat-Photo v0.1.2
echo ========================================

:: Activate Virtual Environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: Clean old build artifacts
echo Cleaning old builds...
if exist dist rd /s /q dist
if exist build rd /s /q build
if exist *.spec del /q *.spec

:: Install/Update Dependencies
echo Checking dependencies...
python -m pip install pyinstaller pillow tkinterdnd2

:: Run the Build
echo Starting PyInstaller...
python -m PyInstaller --onefile --windowed ^
--collect-all tkinterdnd2 ^
--add-data "assets;assets" ^
--icon="assets/Pixelcat-photo.png" ^
--name "PixelCat-Photo-v0.1.2" ^
main.py

echo.
echo ========================================
echo   Build Complete! Check the 'dist' folder.
echo ========================================
pause