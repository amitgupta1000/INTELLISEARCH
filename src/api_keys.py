# api_keys.py
import os
import logging

# Try to load dotenv if available, otherwise use regular environment variables
try:
    from dotenv import load_dotenv, dotenv_values 
    load_dotenv() 
    logging.info("Loaded environment variables from .env file")
except ImportError:
    logging.info("dotenv not available, using system environment variables only")

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

logging.info("API keys loaded from environment (presence not guaranteed).")