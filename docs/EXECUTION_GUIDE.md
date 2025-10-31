# INTELLISEARCH Execution Guide

## 🚀 Quick Start Options

INTELLISEARCH provides multiple ways to run the research tool, depending on your needs:

## 📋 Execution Options

### 1. **`run_setup_and_interactive.bat`** - Complete Setup & Interactive Mode
**🎯 Use When:** First time setup, or when you want full control over research parameters

**What it does:**
- ✅ Checks Python installation
- ✅ Creates virtual environment (if missing)
- ✅ Installs all required packages
- ✅ Validates .env configuration  
- ✅ Runs in **INTERACTIVE mode** with user prompts

**Best for:**
- First-time users
- When you want to configure each research session
- Troubleshooting environment issues
- Full control over research parameters

---

### 2. **`run_automated.bat`** - Quick Automated Research
**🎯 Use When:** Fast research with minimal setup (environment already configured)

**What it does:**
- ⚡ Quick environment check
- ⚡ Asks for research query only
- ⚡ Runs with **FULL AUTOMATION** (no user prompts)
- ⚡ Uses pre-configured settings

**Configuration:**
- **Reasoning Mode**: Reasoning (analytical)
- **Prompt Type**: General
- **Report Type**: Detailed
- **Automation**: Full (no user prompts during workflow)

**Best for:**
- Regular users with environment already set up
- Batch research operations
- When you want fast, hands-off research

---

### 3. **`app.py`** - Command Line Interface
**🎯 Use When:** Advanced usage, scripting, or custom configurations

**Interactive Mode:**
```bash
python app.py --interactive
```

**Automated Mode:**
```bash
python app.py "your research query" --automation full --prompt-type legal --report-type concise
```

**Batch Processing:**
```bash
python app.py --batch-file queries.txt --automation full
```

**Available Options:**
- `--reasoning-mode`: `reasoning` or `research`
- `--prompt-type`: `legal`, `general`, `macro`, `deepsearch`, `person_search`, `investment`
- `--automation`: `full`, `query_only`, `none`
- `--report-type`: `detailed` or `concise`
- `--batch-file`: Process multiple queries from file

---

## 🔄 Workflow Comparison

| Feature | Setup & Interactive | Quick Automated | Command Line |
|---------|-------------------|-----------------|--------------|
| **Environment Setup** | ✅ Full automatic | ❌ Must exist | ❌ Must exist |
| **Package Installation** | ✅ Automatic | ❌ Assumed installed | ❌ Assumed installed |
| **User Prompts During Research** | ✅ Yes (interactive) | ❌ None (automated) | 🔧 Configurable |
| **Configuration Control** | 🎛️ Full interactive | 🔒 Fixed presets | 🎛️ Full command line |
| **Batch Processing** | ❌ Single query | ❌ Single query | ✅ Multiple queries |
| **Best For** | First time & control | Speed & convenience | Automation & scripting |

---

## 🛠️ Prerequisites

### For `run_setup_and_interactive.bat`:
- Python 3.8+ installed
- Internet connection (for package installation)

### For `run_automated.bat`:
- Virtual environment already set up (`.venv` folder exists)
- Packages already installed
- `.env` file configured with API keys

### For `app.py`:
- Virtual environment activated
- All dependencies installed
- `.env` file configured

---

## 📝 Recommended Workflow

### **First Time Users:**
1. Run `run_setup_and_interactive.bat` for complete setup
2. Configure your `.env` file with API keys
3. Test with an interactive research session

### **Regular Users:**
1. Use `run_automated.bat` for quick research
2. Use `app.py` command line for advanced needs

### **Power Users:**
1. Use `app.py` with command line arguments
2. Create custom batch files for specific use cases
3. Integrate with other scripts and workflows

---

## 🔧 Configuration Files

### **`.env`** - Environment Configuration
Contains all API keys and system settings. Created once, used by all execution methods.

### **`requirements.txt`** - Python Dependencies  
Package list for automated installation via setup script.

### **Virtual Environment (`.venv`)**
Isolated Python environment created by setup script.

---

## 🚨 Troubleshooting

### Environment Issues:
→ Use `run_setup_and_interactive.bat` to rebuild environment

### Package Issues:
→ Delete `.venv` folder and re-run setup script

### API Key Issues:
→ Check `.env` file configuration

### Permission Issues:
→ Run Command Prompt as Administrator

---

Choose the execution method that best fits your needs! 🎯