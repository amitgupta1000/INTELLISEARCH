@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo       INTELLISEARCH Setup Utility
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Create virtual environment
if exist ".venv" (
    echo Virtual environment already exists.
    echo Do you want to recreate it? (y/n)
    set /p recreate="Enter choice: "
    if /i "!recreate!" equ "y" (
        echo Removing existing virtual environment...
        rmdir /s /q .venv
    ) else (
        echo Using existing virtual environment.
        goto :activate_env
    )
)

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

:activate_env
:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Upgrade pip and install requirements
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Some packages failed to install
    echo You may need to install some packages manually
    echo For FAISS on Windows, consider using conda:
    echo   conda install -c conda-forge faiss-cpu
    echo.
    pause
) else (
    echo.
    echo ===============================================
    echo Setup completed successfully!
    echo ===============================================
)

:: Check for .env file
if not exist ".env" (
    echo.
    echo NEXT STEPS:
    echo 1. Create a .env file in this directory with your API keys:
    echo    SERPER_API_KEY=your_serper_key
    echo    TOGETHER_API_KEY=your_together_key
    echo    GOOGLE_API_KEY=your_google_key
    echo.
    echo 2. Run 'run_intellisearch.bat' to start the application
    echo.
    echo Do you want to create a sample .env file now? (y/n)
    set /p create_env="Enter choice: "
    if /i "!create_env!" equ "y" (
        echo # INTELLISEARCH API Keys > .env
        echo # Replace with your actual API keys >> .env
        echo SERPER_API_KEY=your_serper_key_here >> .env
        echo TOGETHER_API_KEY=your_together_key_here >> .env
        echo GOOGLE_API_KEY=your_google_key_here >> .env
        echo.
        echo Sample .env file created. Please edit it with your actual API keys.
    )
)

echo.
pause