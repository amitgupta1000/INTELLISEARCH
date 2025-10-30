@echo off
:: Quick launcher for INTELLISEARCH (assumes setup is complete)

echo Starting INTELLISEARCH...
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Activate virtual environment and run
call .venv\Scripts\activate.bat && python app.py

if %errorlevel% neq 0 (
    echo.
    echo Error occurred. Try running run_intellisearch.bat for full setup.
)

pause