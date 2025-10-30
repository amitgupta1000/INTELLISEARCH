INTELLISEARCH quick setup

1) Create and activate a Python virtual environment (Windows PowerShell):

   python -m venv .venv; .\.venv\Scripts\Activate.ps1

2) Upgrade pip and install build tools:

   python -m pip install --upgrade pip setuptools wheel

3) Install requirements:

   pip install -r requirements.txt

4) FAISS on Windows (optional, recommended via conda if pip wheel not available):

   # If you have conda
   conda create -n intellisearch python=3.10 -y; conda activate intellisearch
   conda install -c conda-forge faiss-cpu

   # Or try pip (may fail on some Windows setups)
   pip install faiss-cpu

5) Environment variables:

   - Create a .env file in the project root with any API keys you need, for example:

     SERPER_API_KEY=your_serper_key
     TOGETHER_API_KEY=your_together_key
     GOOGLE_API_KEY=your_google_key

   The project uses python-dotenv to load these.

6) Run a quick smoke test (after installing dependencies):

   python app.py

## Available Research Types

### Person Search 
Use prompt type "5: Person Search" for comprehensive digital profiling across multiple platforms:

**Example queries:**
- "Create a profile of [Person Name]"
- "Research background of [CEO/Professional Name]"
- "Find digital presence of [Individual Name]"

**Platforms searched:**
- Professional: LinkedIn, Naukri.com
- Social Media: Facebook, Twitter, Instagram  
- Legal: IndiaKanoon.org, CaseMine.com, AirLaw.com

**Report includes:**
- Professional background and career timeline
- Social media presence and public statements
- Legal involvement and court cases
- Educational background and achievements
- Digital reputation analysis
- Cross-platform verification

**Ethics Note:** Only searches publicly available information and respects privacy boundaries.

### Investment Research (New!)
Use prompt type "6: Investment Research" for comprehensive analysis of Indian companies from an investment perspective:

**Example queries:**
- "Investment analysis of Reliance Industries Ltd"
- "Investment prospects of Bajaj Finance Ltd"
- "Investment evaluation of HDFC Bank Ltd"

**Data sources:**
- Stock Exchanges: BSE, NSE, SEBI filings
- Financial Platforms: Screener.in, MoneyControl, ValueResearch
- News Sources: Economic Times, Mint, Business Standard
- Global Sources: Bloomberg, Reuters, Sustainalytics

**Report includes:**
- Investment thesis and recommendations (Buy/Hold/Sell)
- Financial performance analysis and key ratios
- Business fundamentals and competitive position
- Growth prospects and market opportunities
- Comprehensive risk assessment and ESG factors
- Valuation analysis with target price estimation
- Bull/bear case scenarios and sensitivity analysis

**Disclaimer:** Provides research analysis only, not personalized investment advice.

Troubleshooting:
 - If imports still show as unresolved in your editor, make sure the workspace interpreter is set to the venv.
 - On Windows, some packages (e.g., pymupdf, faiss-cpu) might need prebuilt wheels; use conda where possible.
 - If using Colab/remote environment, run 'pip install -r requirements.txt' inside that environment.