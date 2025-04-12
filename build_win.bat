@echo off
chcp 65001 > nul
echo ===================================
echo CursorVIP Windows Builder
echo ===================================

:: Check Python environment
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.x
    exit /b 1
)

:: Check and install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

:: Get version number
for /f "tokens=2 delims==" %%a in ('type .env ^| findstr VERSION') do set VERSION=%%a
echo Current version: %VERSION%

:: Clean old build files
echo Cleaning old build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__

:: Start building
echo Building Windows version...
pyinstaller @build.spec

:: Check build result
if exist "dist\CursorVIP_%VERSION%_windows.exe" (
    echo ===================================
    echo Build successful!
    echo Output file: dist\CursorVIP_%VERSION%_windows.exe
    echo ===================================
) else (
    echo Build failed. Please check error messages.
)

pause
