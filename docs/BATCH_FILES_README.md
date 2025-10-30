# INTELLISEARCH Batch File Guide

This directory contains several batch files to help you easily run and manage the INTELLISEARCH application on Windows.

## Available Batch Files

### 1. `run_intellisearch.bat` - Complete Launcher (Recommended)
**What it does:**
- Checks if Python is installed
- Creates virtual environment if it doesn't exist
- Installs required packages automatically (with Python 3.13 compatibility fallbacks)
- Checks for .env file and warns if missing
- Runs the INTELLISEARCH application

**When to use:** This is the main launcher. Use this every time you want to run INTELLISEARCH.

### 2. `setup_intellisearch.bat` - Initial Setup Only
**What it does:**
- Sets up the virtual environment
- Installs all required packages
- Creates a sample .env file (optional)
- Does NOT run the application

**When to use:** Run this once for initial setup, or if you need to reinstall packages.

### 3. `python313_setup.bat` - Python 3.13 Compatible Setup
**What it does:**
- Specialized setup for Python 3.13 users
- Installs packages in specific order to avoid conflicts
- Uses binary wheels when possible to avoid Rust compilation
- Handles known compatibility issues with newer Python versions

**When to use:** If you're using Python 3.13 and getting compilation errors (especially with pydantic or other packages requiring Rust).

### 4. `quick_start.bat` - Fast Launcher
**What it does:**
- Activates virtual environment and runs the app immediately
- No setup checks or package installation

**When to use:** Use this if you've already set everything up and just want to start the app quickly.

## Getting Started

### First Time Setup:
1. **If using Python 3.13:** Double-click `python313_setup.bat` first for better compatibility
2. **Otherwise:** Double-click `setup_intellisearch.bat` to set up your environment
3. **Edit the `.env` file** with your actual API keys:
   ```
   SERPER_API_KEY=your_actual_serper_key
   TOGETHER_API_KEY=your_actual_together_key
   GOOGLE_API_KEY=your_actual_google_key
   ```
4. **Double-click `run_intellisearch.bat`** to start using INTELLISEARCH

### Regular Usage:
- **Double-click `run_intellisearch.bat`** to launch the application
- OR use `quick_start.bat` for faster startup (if setup is already complete)

## Troubleshooting

### "Python is not installed" error
- Install Python 3.8 or higher from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### Pydantic/Package compilation errors (especially Python 3.13)
- **Solution 1:** Use `python313_setup.bat` instead of the regular setup
- **Solution 2:** Install Rust toolchain from [rustup.rs](https://rustup.rs/) 
- **Solution 3:** Use conda instead of pip: `conda install pydantic langchain`
- **Note:** Python 3.13 is very new and some packages may not have pre-compiled wheels yet

### Package installation failures
- Some packages (like FAISS) may require conda instead of pip
- Consider installing Anaconda/Miniconda and using conda for package management
- For Python 3.13, prefer packages with `--prefer-binary` or `--only-binary` flags

### Missing API keys
- The application requires API keys for various services
- Create a `.env` file with your keys (see setup instructions above)
- Without API keys, some features may not work

### Virtual environment issues
- Delete the `.venv` folder and run `setup_intellisearch.bat` again
- Make sure you have sufficient disk space

## Research Types Available

When you run the application, you'll be prompted to select:

1. **Prompt Types:**
   - Legal
   - General  
   - Macro
   - DeepSearch
   - Person Search
   - Investment Research

2. **Reasoning Modes:**
   - Reasoning (interpretive, analytical)
   - DeepSearch (factual, coverage-focused)

## Output
The application will generate research reports in the current directory. Look for files with names like:
- `SumairoResearchReport.md`
- `CrystalSearchReport.pdf`

---

**Need Help?** Check the main `SETUP.md` file for detailed technical instructions.