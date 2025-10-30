@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo    INTELLISEARCH Python 3.13 Compatible Setup
echo ===============================================
echo.

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

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
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Upgrade pip and install essential tools
echo Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

:: Install packages in a specific order to avoid conflicts
echo Installing core packages...
pip install "requests>=2.31.0"
pip install "python-dotenv>=1.0.0"
pip install "beautifulsoup4>=4.12.2"
pip install "nest_asyncio>=1.5.6"
pip install "rich>=13.3.4"

:: Install pydantic with binary wheel preference
echo Installing pydantic (may take a moment)...
pip install "pydantic>=2.0.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Trying pydantic with only binary wheels...
    pip install pydantic --only-binary=:all:
    if %errorlevel% neq 0 (
        echo Warning: Could not install pydantic with binary wheels
        echo Trying with no-build-isolation...
        pip install pydantic --no-build-isolation
    )
)

:: Install aiohttp
echo Installing aiohttp...
pip install "aiohttp>=3.9.0"

:: Install LangChain components
echo Installing LangChain components...
pip install "langchain>=0.1.0" --prefer-binary
pip install "langgraph>=0.1.0" --prefer-binary

:: Install document processing libraries
echo Installing document processing libraries...
pip install "pymupdf>=1.23.0" --prefer-binary
pip install "fpdf2>=2.8.0"
pip install "trafilatura>=1.7.2"

:: Install ranking library
echo Installing ranking library...
pip install "rank_bm25>=0.2.2"

:: Try to install lxml (often problematic)
echo Installing lxml...
pip install "lxml>=5.0.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: lxml installation failed, trying older version...
    pip install "lxml>=4.9.0" --prefer-binary
)

# Optional: Try chromadb (may fail on Python 3.13)
echo Installing chromadb (optional, may fail on Python 3.13)...
pip install "chromadb>=0.4.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: chromadb installation failed - this is expected on Python 3.13
    echo You may need to use an alternative vector database or wait for chromadb update
)

# Install LLM provider SDKs (optional but useful)
echo Installing LLM provider SDKs...

# Google GenAI
echo Installing google-genai...
pip install "google-genai>=1" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: google-genai installation failed
)

# LangChain Google GenAI integration
echo Installing langchain-google-genai...
pip install "langchain-google-genai>=1.0.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: langchain-google-genai installation failed
)

# Anthropic
echo Installing anthropic...
pip install "anthropic>=0.25.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: anthropic installation failed
)

# Together AI
echo Installing together...
pip install "together>=1.0.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: together installation failed
)

# VoyageAI
echo Installing voyageai...
pip install "voyageai>=0.2.0" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: voyageai installation failed
)

# Optional: FAISS (often problematic on Windows)
echo Installing faiss-cpu (optional, may require conda)...
pip install "faiss-cpu>=1.7.4" --prefer-binary
if %errorlevel% neq 0 (
    echo Warning: faiss-cpu installation failed
    echo For FAISS on Windows, consider using conda:
    echo   conda install -c conda-forge faiss-cpu
)

echo.
echo ===============================================
echo Installation completed!
echo ===============================================
echo.
echo Testing imports...
python -c "import requests, langchain, pydantic; print('Core packages imported successfully!')"
python -c "try: from google import genai; print('Google GenAI: OK'); except: print('Google GenAI: Not installed')"
python -c "try: import anthropic; print('Anthropic: OK'); except: print('Anthropic: Not installed')"
python -c "try: import together; print('Together: OK'); except: print('Together: Not installed')"
python -c "try: import chromadb; print('ChromaDB: OK'); except: print('ChromaDB: Not installed')"
python -c "try: import faiss; print('FAISS: OK'); except: print('FAISS: Not installed')"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Core packages are working!
    echo You can now run the application with run_intellisearch.bat
) else (
    echo.
    echo Some packages may have issues. Check the output above for details.
)

echo.
pause