@echo off
REM run_automated.bat
REM Quick automated research with minimal setup
REM Prerequisites: Virtual environment must already exist

echo ===============================================
echo      INTELLISEARCH - Quick Automated Mode  
echo ===============================================
echo.
echo This script provides FAST automated research with:
echo   - No user prompts during workflow
echo   - Pre-configured settings (reasoning mode, general prompt)
echo   - Minimal setup checks
echo.
echo For first-time setup, use: run_setup_and_interactive.bat
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup first: run_setup_and_interactive.bat
    echo.
    pause
    exit /b 1
)

REM Get query from user
set /p QUERY="Enter your research query: "

REM Default settings for automation
set REASONING_MODE=reasoning
set PROMPT_TYPE=general
set REPORT_TYPE=detailed

echo.
echo Configuration:
echo   Query: %QUERY%
echo   Mode: Automated (no user prompts)
echo   Reasoning: %REASONING_MODE%
echo   Prompt Type: %PROMPT_TYPE%
echo   Report Type: %REPORT_TYPE%
echo.

echo Starting automated research...
echo.

REM Run the automated workflow
.venv\Scripts\python.exe app.py "%QUERY%" --reasoning-mode %REASONING_MODE% --prompt-type %PROMPT_TYPE% --report-type %REPORT_TYPE% --automation full

echo.
echo Automated research completed!
echo Check for generated report files in the current directory.
pause