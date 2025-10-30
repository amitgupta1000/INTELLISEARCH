# setup.py
# This file handles initial setup, including package imports and global initializations.
# It should be run once at the beginning of your application.

import logging
import os
import sys
import subprocess
import time # Import time for cache initialization
from typing import Any

# Configure logging early
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Package Installation ---
def install_packages():
    """Installs required Python packages using pip."""
    packages = [
        "langchain", "langchain-voyageai", "langchain_community", "langchain-together", "langchain-google-genai", "langchain_anthropic",
        "fpdf", "langgraph", "pypdf", "lxml", "accelerate", "together", "markdownify", "retry", "rank_bm25", "trafilatura", "pymupdf", "playwright",
        "ratelimit", "pandas", "python-dotenv", "bs4", "faiss-CPU", "google-genai>=1.0.0", "requests_html", "lxml[html_clean]", "rich",
        "fake_useragent", "nest_asyncio", "aiohttp", "beautifulsoup4", "pydantic>=2.0", "selenium", "webdriver-manager",
        "requests", "fitz", "rank_bm25", "fpdf" # Added packages based on code cells
    ]

    logging.info("Installing required packages...")
    for package in packages:
        try:
            # Use sys.executable to ensure the package is installed in the current environment
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            logging.info(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error installing {package}: {e}")
            # Optionally, handle the error or exit if a critical package fails
            # sys.exit(1)

    logging.info("Package installation complete.")

## Uncomment and run install_packages() if you need to install packages within the notebook
# install_packages()
# subprocess.run(["playwright", "install"], check=True)

# --- Import necessary modules after potential installation ---
# This assumes packages are installed in the environment where this script runs.
try:
    import nest_asyncio
    nest_asyncio.apply()
    logging.info("nest_asyncio applied.")
except ImportError:
    logging.warning("nest_asyncio not found. Ensure your environment supports nested event loops if needed.")

# Import API keys from api_keys.py
try:
    from src.api_keys import GOOGLE_API_KEY, VOYAGE_API_KEY, SERPER_API_KEY, ANTHROPIC_API_KEY, TOGETHER_API_KEY
    logging.info("Successfully imported API keys from api_keys.py")
except ImportError:
    logging.error("Could not import API keys from api_keys.py. API keys will not be available.")
    # Define dummy variables to prevent NameError later, but warn the user
    GOOGLE_API_KEY = None
    VOYAGE_API_KEY = None
    SERPER_API_KEY = None
    ANTHROPIC_API_KEY = None
    TOGETHER_API_KEY = None


# --- Global Variable Initialization ---
# Initialize any global variables or resources needed across modules
# Example: Constants for colors, timeouts, etc.
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

# User agent (can be set in config or derived dynamically)
USER_AGENT = os.environ.get('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Cache settings (can be imported from config)
try:
    from src.config import CACHE_ENABLED, CACHE_TTL
except ImportError:
    logging.warning("Could not import cache settings from config. Using defaults.")
    CACHE_ENABLED = False # Default to disabled if config is missing
    CACHE_TTL = 3600


# Placeholder for embeddings and LLM models - initialized in llm_calling.py
embeddings = None # For embedding/indexing
llm = None # For LLM Calling


# Initialize cache here if using a global cache instance
if CACHE_ENABLED:
    try:
        # Assuming SimpleCache is defined in scraper.py or utils.py
        # Import it here or define it globally if needed across modules
        class SimpleCache:
            def __init__(self, ttl: int = 3600):
                self._cache = {}
                self._ttl = ttl
                self._timestamps = {}

            def get(self, key: str):
                if key in self._cache:
                    if time.time() - self._timestamps.get(key, 0) < self._ttl:
                        return self._cache[key]
                    else:
                        self._cache.pop(key, None)
                        self._timestamps.pop(key, None)
                return None

            def set(self, key: str, value: Any):
                self._cache[key] = value
                self._timestamps[key] = time.time()

        global cache
        cache = SimpleCache(ttl=CACHE_TTL)
        logging.info("Global cache initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize global cache: {e}. Caching disabled.")
        CACHE_ENABLED = False
        cache = None
else:
    cache = None


logging.info("setup.py created with initial setup and global variables.")
