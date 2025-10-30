# config.py

USE_PERSISTENCE = False        # Toggle ChromaDB disk usage
MAX_RESULTS = 15               # Search results per query
CACHE_TTL = 86400              # Time-to-live for cached results (24 hours)
CACHE_ENABLED = True
EMBEDDING_MODEL = "voyage-3"   # Options: "voyage-3", "google-genai", etc.
REPORT_FORMAT = "both"          # Options: "pdf", "txt", or "both"
REPORT_FILENAME_PDF = "Crystal_DeepSearch.pdf"
REPORT_FILENAME_TEXT = "Crystal_DeepSearch.txt"

# Performance tuning
MAX_SEARCH_QUERIES = 15
MAX_CONCURRENT_SCRAPES = 5     # Parallel scraping limit
MAX_SEARCH_RETRIES = 3        # Retry attempts per engine
MAX_AI_ITERATIONS = 6             # Max refinement loops during extraction
MAX_USER_QUERY_LOOPS = 3

# Scraping behavior
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)

DEFAULT_REFERER = "https://www.google.com/"
URL_TIMEOUT = 60
SKIP_EXTENSIONS = []
BLOCKED_DOMAINS = ["youtube.com", "youtu.be", "nsearchives.nseindia.com"]  # Domains to skip during search and extraction

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Gemini Model Configuration
gemini1 = "gemini-2.0-flash-lite"
gemini2 = "gemini-2.0-flash"
gemini_model =  gemini1
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash-lite"

MAX_RETRIES = 5
BASE_DELAY = 1
MAX_CONCURRENT_CALLS = 10
MAX_CALLS_PER_SECOND = 30

DEFAULT_LLM_MODEL_NAME = DEFAULT_GEMINI_MODEL # Or another model name

# Default parameters for LLM calls
DEFAULT_LLM_TIMEOUT = 120 # seconds
DEFAULT_MAX_TOKENS = 20000
DEFAULT_TEMPERATURE = 0.1


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

import logging
logging.info("config.py loaded successfully")

