# api_keys.py - API Key Access
# Simplified to import from unified config

from .config import (
    GOOGLE_API_KEY,
    TOGETHER_API_KEY, 
    SERPER_API_KEY,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    VOYAGE_API_KEY,
    GOOGLE_CSE_API_KEY,
    GOOGLE_CSE_ID
)

# Legacy support - some modules may still import these directly
GEMINI_API_KEY = GOOGLE_API_KEY  # Alias for backward compatibility
HF_TOKEN = None  # Not used in current implementation

import logging
logging.info("API keys loaded from unified configuration")