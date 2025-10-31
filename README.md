# INTELLISEARCH 🔍

An advanced AI-powered research pipeline that conducts comprehensive web searches, analyzes content, and generates detailed reports using LangGraph workflows and multiple LLM providers.

## 🌟 Features

- **Multi-LLM Support**: Google Gemini, Anthropic Claude, Together AI
- **Advanced Web Scraping**: Multiple strategies including requests-html, aiohttp, and fallback methods
- **Intelligent Content Analysis**: AI-powered relevance evaluation and ranking
- **Vector Search**: ChromaDB and FAISS integration for semantic search
- **Flexible Reports**: Configurable word limits (600-1200 for concise, 800-3000 for detailed)
- **PDF Generation**: Automatic PDF report creation
- **Windows Automation**: One-click batch file setup and execution

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13.7)
- Windows OS (batch files included)
- API Keys for your chosen LLM providers

### Execution Options

**📋 See [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) for detailed execution options**

#### **Option 1: Complete Setup & Interactive Mode (Recommended for first time)**
```batch
run_setup_and_interactive.bat
```
- Handles complete environment setup
- Interactive mode with full control
- Best for first-time users

#### **Option 2: Quick Automated Research (Fast execution)**
```batch
run_automated.bat
```
- Fast automated research
- No user prompts during workflow
- Requires environment already set up

#### **Option 3: Command Line Interface (Advanced)**
```bash
# Interactive mode
python app.py --interactive

# Automated with custom settings
python app.py "your research query" --automation full --prompt-type legal

# Batch processing
python app.py --batch-file queries.txt --automation full
```

### Installation

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd INTELLISEARCH
   ```

2. **Run the automated setup**
   ```batch
   run_intellisearch_clean.bat
   ```
   
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up configuration
   - Run the application

### Manual Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   Create a `.env` file:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   TOGETHER_API_KEY=your_together_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   VOYAGE_API_KEY=your_voyage_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
INTELLISEARCH/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env                           # API keys (create this)
├── .gitignore                     # Git ignore rules
├── run_intellisearch_clean.bat    # Windows launcher (recommended)
├── run_intellisearch.bat          # Alternative Windows launcher
├── setup_intellisearch.bat        # Setup-only batch file
├── quick_start.bat                # Quick start launcher
├── src/                           # Source code
│   ├── api_keys.py               # API key management
│   ├── config.py                 # Configuration settings
│   ├── data_types.py             # Data structures and models
│   ├── graph.py                  # LangGraph workflow definition
│   ├── llm_calling.py            # LLM interaction utilities
│   ├── llm_utils.py              # LLM utilities and providers
│   ├── nodes.py                  # Workflow node implementations
│   ├── prompt.py                 # Prompt templates
│   ├── scraper.py                # Web scraping utilities
│   ├── search.py                 # Search engine integration
│   ├── utils.py                  # General utilities
│   └── conditions.py             # Workflow conditions
├── tests/                         # Test files
│   └── test_workflow.py          # Workflow tests
├── scripts/                       # Utility scripts
│   └── env_check.py              # Environment checker
└── docs/                          # Documentation
    ├── SETUP.md                  # Detailed setup instructions
    ├── BATCH_FILES_README.md     # Batch file documentation
    ├── PACKAGE_STATUS.md         # Package compatibility info
    ├── WORD_LIMITS_UPDATE.md     # Word limits configuration
    ├── PACKAGE_UPDATES_SUMMARY.md # Recent package updates
    └── SESSION_CLEANUP_FIXES.md  # Bug fixes documentation
```

## 🛠️ Configuration

### Report Types
- **Concise Report**: 600-1200 words, focused summary
- **Detailed Report**: 800-3000 words, comprehensive analysis

### Supported LLM Providers
- **Google Gemini**: Primary recommendation (gemini-2.0-flash)
- **Together AI**: High-performance alternative
- **Anthropic Claude**: Advanced reasoning capabilities

### Search Configuration
- **Serper API**: Primary search provider
- **Fallback methods**: Built-in alternatives when APIs unavailable

## 🔧 Advanced Usage

### Custom Prompts
The system supports multiple prompt types:
- `general`: Standard research queries
- `legal`: Legal document analysis
- `macro`: Economic and market research
- `deepsearch`: Deep investigative research
- `person_search`: People and biography research

### API Configuration
Set your preferred providers in `.env`:
```env
# Primary LLM (choose one)
GOOGLE_API_KEY=your_key_here
# OR
TOGETHER_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here

# Search provider
SERPER_API_KEY=your_key_here

# Optional: Embeddings
VOYAGE_API_KEY=your_key_here
```

## 🐛 Troubleshooting

### Common Issues

1. **Package Installation Failures**
   - Use `run_intellisearch_clean.bat` for automated resolution
   - Python 3.13 compatibility ensured

2. **API Key Issues**
   - Verify `.env` file exists and contains valid keys
   - Check key formats match provider requirements

3. **Web Scraping Failures**
   - Application includes multiple fallback methods
   - Check internet connectivity and firewall settings

### Python 3.13 Compatibility
All packages have been updated for Python 3.13 compatibility:
- `pydantic>=2.8.0`
- `requests-html>=0.10.0`
- `ratelimit>=2.2.1` (replaced problematic ratelimiter)

## 📊 Performance

- **Concurrent Processing**: Async/await throughout
- **Rate Limiting**: Built-in API rate limiting
- **Caching**: Intelligent content caching
- **Resource Management**: Proper session cleanup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain/LangGraph**: Workflow orchestration
- **Google Gemini**: Primary LLM provider
- **Together AI**: High-performance inference
- **Anthropic**: Advanced AI capabilities

## 📞 Support

For issues and questions:
1. Check the `docs/` folder for detailed documentation
2. Review troubleshooting section above
3. Open an issue in this repository

---

**Made with ❤️ and AI** - Combining the power of multiple LLMs for comprehensive research automation.