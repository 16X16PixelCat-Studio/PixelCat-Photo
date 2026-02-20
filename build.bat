@echo off
title PixelCat-Photo Builder
echo ========================================
echo   PixelCat-Photo v0.1.1 - Auto-Build
echo ========================================

:: Step 1: Force use of the Virtual Environment
if exist .venv\Scripts\activate.bat (
    echo Activating Virtual Environment...
    call .venv\Scripts\activate.bat
) else (
    echo [WARNING] .venv not found. Using global Python.
)

:: Step 2: Clean old build artifacts
echo Cleaning old builds...
if exist dist rd /s /q dist
if exist build rd /s /q build
if exist *.spec del /q *.spec

:: Step 3: Ensure dependencies are present
echo Checking dependencies...
python -m pip install pyinstaller pillow

:: Step 4: Run the build
echo Starting PyInstaller...
python -m PyInstaller --onefile --windowed ^
--add-data "assets;assets" ^
--icon="assets/Pixelcat-photo.png" ^
--name "PixelCat-Photo-v0.1.1" ^
main.py

echo.
echo ========================================
echo   Build Complete! Check the 'dist' folder.
echo ========================================
pause