# config.py - Unified Configuration System
# All configuration values loaded from environment variables (.env file)

import os
import logging
from typing import List, Optional, Union

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Loaded environment variables from .env file")
except ImportError:
    logging.warning("dotenv not available, using system environment variables only")

def get_env_bool(key: str, default: bool = False) -> bool:
    """Convert environment variable to boolean."""
    return os.getenv(key, str(default)).lower() in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int) -> int:
    """Convert environment variable to integer."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        logging.warning(f"Invalid integer value for {key}, using default: {default}")
        return default

def get_env_float(key: str, default: float) -> float:
    """Convert environment variable to float."""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        logging.warning(f"Invalid float value for {key}, using default: {default}")
        return default

def get_env_list(key: str, default: List[str] = None, separator: str = ',') -> List[str]:
    """Convert environment variable to list."""
    if default is None:
        default = []
    value = os.getenv(key, '')
    if not value:
        return default
    return [item.strip() for item in value.split(separator) if item.strip()]

# =============================================================================
# API CONFIGURATION
# =============================================================================

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
GOOGLE_CSE_API_KEY = os.getenv("GOOGLE_CSE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# =============================================================================
# LLM CONFIGURATION
# =============================================================================

PRIMARY_LLM_PROVIDER = os.getenv("PRIMARY_LLM_PROVIDER", "google")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Embedding Configuration
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "google")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")

# LLM Settings
LLM_TEMPERATURE = get_env_float("LLM_TEMPERATURE", 0.1)
MAX_TOKENS = get_env_int("MAX_TOKENS", 30000)
DEFAULT_LLM_TIMEOUT = get_env_int("DEFAULT_LLM_TIMEOUT", 120)

# Legacy support for old variable names
DEFAULT_GEMINI_MODEL = GOOGLE_MODEL
gemini_model = GOOGLE_MODEL
gemini1 = "gemini-2.0-flash-lite"
gemini2 = "gemini-2.0-flash"
DEFAULT_LLM_MODEL_NAME = GOOGLE_MODEL
DEFAULT_MAX_TOKENS = MAX_TOKENS
DEFAULT_TEMPERATURE = LLM_TEMPERATURE

# =============================================================================
# SEARCH AND PROCESSING CONFIGURATION
# =============================================================================

# Search limits
MAX_SEARCH_QUERIES = get_env_int("MAX_SEARCH_QUERIES", 15)
MAX_SEARCH_RESULTS = get_env_int("MAX_SEARCH_RESULTS", 10)
MAX_CONCURRENT_SCRAPES = get_env_int("MAX_CONCURRENT_SCRAPES", 4)
MAX_SEARCH_RETRIES = get_env_int("MAX_SEARCH_RETRIES", 2)

# AI iteration limits
MAX_AI_ITERATIONS = get_env_int("MAX_AI_ITERATIONS", 3)
MAX_USER_QUERY_LOOPS = get_env_int("MAX_USER_QUERY_LOOPS", 3)

# Content processing
CHUNK_SIZE = get_env_int("CHUNK_SIZE", 1000)
CHUNK_OVERLAP = get_env_int("CHUNK_OVERLAP", 100)
MAX_CONTENT_LENGTH = get_env_int("MAX_CONTENT_LENGTH", 10000)
URL_TIMEOUT = get_env_int("URL_TIMEOUT", 30)

# Legacy support
MAX_RESULTS = MAX_SEARCH_RESULTS  # Backward compatibility
MAX_RETRIES = MAX_SEARCH_RETRIES

# =============================================================================
# REPORT CONFIGURATION
# =============================================================================

REPORT_FORMAT = os.getenv("REPORT_FORMAT", "md")
DEFAULT_REPORT_TYPE = os.getenv("DEFAULT_REPORT_TYPE", "detailed")
REPORT_FILENAME_TEXT = os.getenv("REPORT_FILENAME_TEXT", "IntelliSearchReport.txt")
REPORT_FILENAME_PDF = os.getenv("REPORT_FILENAME_PDF", "IntelliSearchReport.pdf")

# Legacy support
REPORT_FILENAME_PDF = os.getenv("REPORT_FILENAME_PDF", "Crystal_DeepSearch.pdf")
REPORT_FILENAME_TEXT = os.getenv("REPORT_FILENAME_TEXT", "Crystal_DeepSearch.txt")

# =============================================================================
# WEB SCRAPING CONFIGURATION
# =============================================================================

USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
DEFAULT_USER_AGENT = USER_AGENT  # Legacy support
REQUEST_TIMEOUT = get_env_int("REQUEST_TIMEOUT", 30)
REQUEST_DELAY = get_env_int("REQUEST_DELAY", 1)
DEFAULT_REFERER = "https://www.google.com/"

# Blocked domains and extensions
BLOCKED_DOMAINS = get_env_list("BLOCKED_DOMAINS", [
    "facebook.com", "twitter.com", "instagram.com", "linkedin.com/posts", 
    "reddit.com/r/", "youtube.com/watch", "youtu.be", "nsearchives.nseindia.com", 
    "bseindia.com", "sebi.gov.in"
])
SKIP_EXTENSIONS = get_env_list("SKIP_EXTENSIONS", [
    ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3", ".zip", 
    ".exe", ".dmg", ".rar", ".7z"
])

# =============================================================================
# CACHING AND PERFORMANCE
# =============================================================================

CACHE_ENABLED = get_env_bool("CACHE_ENABLED", True)
CACHE_TTL = get_env_int("CACHE_TTL", 86400)

# Rate limiting
MAX_CONCURRENT_CALLS = get_env_int("MAX_CONCURRENT_CALLS", 10)
MAX_CALLS_PER_SECOND = get_env_int("MAX_CALLS_PER_SECOND", 30)
BASE_DELAY = get_env_int("BASE_DELAY", 1)
API_REQUESTS_PER_MINUTE = get_env_int("API_REQUESTS_PER_MINUTE", 30)
SCRAPING_REQUESTS_PER_MINUTE = get_env_int("SCRAPING_REQUESTS_PER_MINUTE", 30)

# =============================================================================
# AUTOMATION SETTINGS
# =============================================================================

DEFAULT_AUTOMATION_MODE = os.getenv("DEFAULT_AUTOMATION_MODE", "none")
AUTO_APPROVE_QUERIES = get_env_bool("AUTO_APPROVE_QUERIES", False)
AUTO_REPORT_TYPE = os.getenv("AUTO_REPORT_TYPE", "detailed")

# =============================================================================
# LOGGING AND DEBUGGING
# =============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
DEBUG_MODE = get_env_bool("DEBUG_MODE", False)
VERBOSE = get_env_bool("VERBOSE", False)

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

SSL_VERIFY = get_env_bool("SSL_VERIFY", True)

# =============================================================================
# LEGACY SUPPORT AND COLORS
# =============================================================================

# Color constants for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

# Legacy persistence setting
USE_PERSISTENCE = get_env_bool("USE_PERSISTENCE", False)

# =============================================================================
# VALIDATION
# =============================================================================

def validate_config():
    """Validate critical configuration values."""
    errors = []
    warnings = []
    
    # Check API keys
    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY is required")
    if not SERPER_API_KEY:
        warnings.append("SERPER_API_KEY not set - search functionality may be limited")
    
    # Check numeric limits
    if MAX_SEARCH_QUERIES <= 0:
        errors.append("MAX_SEARCH_QUERIES must be positive")
    if CACHE_TTL <= 0:
        warnings.append("CACHE_TTL should be positive for effective caching")
    
    # Log results
    if errors:
        for error in errors:
            logging.error(f"Configuration error: {error}")
    if warnings:
        for warning in warnings:
            logging.warning(f"Configuration warning: {warning}")
    
    return len(errors) == 0

# Validate configuration on import
config_valid = validate_config()

logging.info("config.py loaded successfully with unified environment-based configuration")

# Export commonly used values for backward compatibility
__all__ = [
    # API Keys
    'GOOGLE_API_KEY', 'TOGETHER_API_KEY', 'SERPER_API_KEY', 'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY', 'VOYAGE_API_KEY',
    
    # LLM Configuration  
    'PRIMARY_LLM_PROVIDER', 'GOOGLE_MODEL', 'OPENAI_MODEL', 'EMBEDDING_MODEL',
    'LLM_TEMPERATURE', 'MAX_TOKENS',
    
    # Search and Processing
    'MAX_SEARCH_QUERIES', 'MAX_SEARCH_RESULTS', 'MAX_CONCURRENT_SCRAPES',
    'MAX_AI_ITERATIONS', 'CHUNK_SIZE', 'CHUNK_OVERLAP',
    
    # Reports
    'REPORT_FORMAT', 'REPORT_FILENAME_TEXT', 'REPORT_FILENAME_PDF',
    
    # Web Scraping
    'USER_AGENT', 'BLOCKED_DOMAINS', 'SKIP_EXTENSIONS', 'REQUEST_TIMEOUT',
    
    # Caching
    'CACHE_ENABLED', 'CACHE_TTL',
    
    # Colors
    'RED', 'GREEN', 'BLUE', 'YELLOW', 'ENDC',
    
    # Legacy support
    'MAX_RESULTS', 'DEFAULT_USER_AGENT', 'DEFAULT_GEMINI_MODEL'
]

