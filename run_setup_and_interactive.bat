@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo      INTELLISEARCH Setup & Interactive Mode
echo ===============================================
echo.
echo This script will:
echo   - Check Python installation
echo   - Create/activate virtual environment
echo   - Install required packages
echo   - Check for .env configuration
echo   - Run INTELLISEARCH in INTERACTIVE mode
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

echo Python is installed:
python --version
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Check if requirements are installed by validating LangChain imports
echo Validating LangChain/LangGraph imports...
python -c "from src.import_validator import validate_imports; v = validate_imports(); v.print_status_report(); exit(0 if not v.get_missing_packages() else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    echo This may take a few minutes...
    python -m pip install --upgrade pip setuptools wheel
    
    :: Install core packages first
    echo Installing core packages...
    pip install "requests>=2.31.0" "python-dotenv>=1.0.0" "pydantic>=2.8.0" "nest_asyncio>=1.5.6"
    
    :: Install LangChain packages
    echo Installing LangChain packages...
    pip install "langchain>=0.1.0" "langgraph>=0.1.0" "langchain-core>=0.1.0" "langchain-community>=0.1.0" "langchain-text-splitters>=0.1.0"
    
    :: Install provider packages
    echo Installing LLM provider packages...
    pip install "langchain-google-genai>=1.0.0" "google-genai>=1.0.0" "langchain-together" "langchain-anthropic" "anthropic>=0.25.0" "together>=1.0.0"
    
    :: Install additional packages
    echo Installing additional packages...
    pip install "beautifulsoup4>=4.12.2" "aiohttp>=3.9.0" "requests-html>=0.10.0" "lxml>=5.0.0" "ratelimit>=2.2.1"
    pip install "pymupdf>=1.23.0" "pypdf>=4.0.0" "fpdf2>=2.8.0" "trafilatura>=1.7.2" "rank_bm25>=0.2.2" "rich>=13.3.4"
    
    :: Try installing requirements file as backup
    if exist "requirements.txt" (
        echo Installing from requirements.txt...
        pip install -r requirements.txt
    )
    
    echo.
    echo Validating imports after installation...
    python -c "from src.import_validator import validate_imports; v = validate_imports(); v.print_status_report()"
    
    echo.
    echo Package installation process completed.
    echo.
) else (
    echo All required packages are already installed.
    echo.
)

:: Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found
    echo You may need to create a .env file with your API keys
    echo Example:
    echo SERPER_API_KEY=your_serper_key
    echo TOGETHER_API_KEY=your_together_key
    echo GOOGLE_API_KEY=your_google_key
    echo.
    echo Do you want to continue anyway? (y/n)
    set /p continue="Enter choice: "
    if /i "!continue!" neq "y" (
        echo Setup cancelled.
        pause
        exit /b 0
    )
    echo.
) else (
    echo .env file found - API keys will be loaded.
    echo.
)

:: Run the application
echo ===============================================
echo      Starting INTELLISEARCH (Interactive)
echo ===============================================
echo.
echo NOTE: You will be prompted to configure your research during execution.
echo.

python app.py

:: Check if the application ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ===============================================
    echo Application encountered an error (Exit Code: %errorlevel%)
    echo Check the output above for details.
    echo ===============================================
) else (
    echo.
    echo ===============================================
    echo Application completed successfully!
    echo Check for generated report files in the current directory.
    echo ===============================================
)

echo.
pause