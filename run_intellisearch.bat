@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo          INTELLISEARCH Launcher
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

:: Check if requirements are installed by trying to import a key package
python -c "import langchain" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    echo This may take a few minutes...
    python -m pip install --upgrade pip setuptools wheel
    
    :: Try installing requirements, with fallback for compatibility issues
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo WARNING: Some packages failed to install with pip
        echo This is common with Python 3.13 due to compatibility issues
        echo.
        echo Trying individual package installation with newer versions...
        
        :: Install core packages individually with fallback versions
        pip install "requests>=2.31.0" "requests-html>=0.10.0" "python-dotenv>=1.0.0" "beautifulsoup4>=4.12.2" "nest_asyncio>=1.5.6"
        pip install "aiohttp>=3.9.0" "rich>=13.3.4" "ratelimit>=2.2.1"
        
        :: Try pydantic with broader version range
        pip install "pydantic>=2.8.0"
        if %errorlevel% neq 0 (
            echo Trying to install pydantic with specific version...
            pip install "pydantic==2.8.2"
        )
        
        :: Install LangChain components
        pip install "langchain>=0.1.0" "langgraph>=0.1.0"
        
        :: Install document processing
        pip install "pymupdf>=1.23.0" "pypdf>=4.0.0" "fpdf2>=2.8.0" "trafilatura>=1.7.2"
        
        :: Install other components
        pip install "rank_bm25>=0.2.2"
        
        :: Install LLM provider SDKs (optional but useful)
        echo Installing LLM provider SDKs...
        pip install "google-genai>=1"
        pip install "langchain-google-genai>=1.0.0"
        pip install "anthropic>=0.25.0"
        pip install "together>=1.0.0"
        pip install "voyageai>=0.2.0"
        
        :: Try vector databases (may fail on Python 3.13)
        echo Installing vector databases (may fail on Python 3.13)...
        pip install "chromadb>=0.4.0" >nul 2>&1
        pip install "faiss-cpu>=1.7.4" >nul 2>&1
        
        echo.
        echo Package installation completed with some potential issues.
        echo If you encounter import errors, you may need to install missing packages manually.
    )
    echo.
    echo Packages installation process completed.
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
echo          Starting INTELLISEARCH
echo ===============================================
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