# llm_utils.py
#===================

import logging, os, random, asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import nest_asyncio
nest_asyncio.apply()

# Try importing LangChain components with error handling
try:
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    LANGCHAIN_GOOGLE_AVAILABLE = True
except ImportError as e:
    logging.error(f"Could not import langchain_google_genai: {e}")
    LANGCHAIN_GOOGLE_AVAILABLE = False

try:
    from langchain_voyageai import VoyageAIEmbeddings
    VOYAGE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import langchain_voyageai: {e}")
    VOYAGE_AVAILABLE = False

try:
    from langchain_together import ChatTogether
    TOGETHER_LANGCHAIN_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import langchain_together: {e}")
    TOGETHER_LANGCHAIN_AVAILABLE = False

try:
    from together import Together, AsyncTogether
    TOGETHER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import together: {e}")
    TOGETHER_AVAILABLE = False

try:
    from ratelimit import limits, sleep_and_retry
    RATELIMIT_AVAILABLE = True
except ImportError:
    try:
        from ratelimiter import RateLimiter
        RATELIMIT_AVAILABLE = True
    except ImportError as e:
        logging.warning(f"Could not import rate limiting: {e}")
        RATELIMIT_AVAILABLE = False

try:
    from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
    LANGCHAIN_CORE_AVAILABLE = True
except ImportError as e:
    logging.error(f"Could not import langchain_core.messages: {e}")
    LANGCHAIN_CORE_AVAILABLE = False

try:
    from google import genai
    from google.genai.types import Content, Part
    GOOGLE_GENAI_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Could not import google.genai: {e}")
    GOOGLE_GENAI_AVAILABLE = False


# Import API keys from api_keys.py
try:
    from .api_keys import GOOGLE_API_KEY, VOYAGE_API_KEY, TOGETHER_API_KEY, GEMINI_API_KEY
except ImportError:
    logging.error("Could not import API keys from api_keys.py. LLMs and embeddings may not initialize.")
    GOOGLE_API_KEY = None
    VOYAGE_API_KEY = None
    TOGETHER_API_KEY = None
    GEMINI_API_KEY = None

# Import configuration
try: 
    from .config import (
        DEFAULT_GEMINI_MODEL,
        MAX_RETRIES,
        BASE_DELAY,
        MAX_CONCURRENT_CALLS,
        MAX_CALLS_PER_SECOND,
    )
except ImportError:
    logging.error("Could not import config paramters from config.py. LLMs and embeddings may not initialize.")
    DEFAULT_GEMINI_MODEL = None
    MAX_RETRIES = None
    BASE_DELAY = None
    MAX_CONCURRENT_CALLS = None
    MAX_CALLS_PER_SECOND = None

# --- Embedding Model Initialization ---

embeddings = None # The primary embeddings model

# For embedding/indexing
try:
    if GOOGLE_API_KEY and LANGCHAIN_GOOGLE_AVAILABLE:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
        logging.info("Initialized GoogleGenerativeAIEmbeddings with models/text-embedding-004.")
    elif VOYAGE_API_KEY and VOYAGE_AVAILABLE:
        embeddings = VoyageAIEmbeddings(api_key=VOYAGE_API_KEY, model="voyage-3")
        logging.info("Initialized VoyageAIEmbeddings with voyage-3")
    else:
         embeddings = None
         if not LANGCHAIN_GOOGLE_AVAILABLE and not VOYAGE_AVAILABLE:
             logging.error("No embedding packages available (langchain_google_genai or langchain_voyageai).")
         else:
             logging.error("No API key available for initializing embeddings (Google or VoyageAI).")

except Exception as e:
    embeddings = None
    logging.error(f"Failed to initialize embeddings model: {e}")

# --- LLM Model Initialization --- 

# Consolidate LLM initialization into a single 'llm' variable
llm = None # The primary LLM for most tasks

# --- Configuration ---
# Together API calling
together1 = "openai/gpt-oss-20b"
TOGETHER_API_KEY = TOGETHER_API_KEY
TOGETHER_MODEL = together1

# --- Role-Based Message Serialization ---
def serialize_messages(messages: List[Any]) -> List[Dict[str, Any]]:
    """Convert LangChain-style messages to Together API-compatible dicts."""
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

    serialized = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            serialized.append({"role": "system", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            serialized.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            serialized.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, ToolMessage):
            serialized.append({
                "role": "tool",
                "content": msg.content,
                "tool_call_id": msg.tool_call_id,
            })
        else:
            logging.warning(f"Unknown message type: {type(msg)} — skipping.")
    return serialized

# --- Async Together Invocation ---
async def llm_call_async_old(messages: List[Any], model: Optional[str] = None) -> str:
    """Call Together API asynchronously and return assistant's reply."""
    if TOGETHER_API_KEY is None:
        logging.error("TOGETHER_API_KEY is not set.")
        return ""

    try:
        client = AsyncTogether(api_key=TOGETHER_API_KEY)
        payload = serialize_messages(messages)

        response = await client.chat.completions.create(
            model=model or TOGETHER_MODEL,
            messages=payload,
            max_tokens=20000,
            temperature=0.2,
        )

        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Together API call failed: {e}")
        return ""


#=========================
# LLM calling with langchain chat client
try:
    if  GOOGLE_API_KEY:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0, google_api_key=GOOGLE_API_KEY)
        logging.info("Initialized ChatGoogleGenerativeAI (llm) with gemini-1.5-flash")
    elif TOGETHER_API_KEY:
        llm = ChatTogether(model=TOGETHER_MODEL, temperature=0.2, max_tokens=20000, timeout=None, max_retries=4, together_api_key=TOGETHER_API_KEY)
        logging.info(f"Initialized ChatTogether (llm) with {TOGETHER_MODEL}")
    else:
         logging.error("No API key available for initializing llm (Together, Anthropic, or Google).")

except Exception as e:
    llm = None
    logging.error(f"Failed to initialize llm model: {e}")

#=================================================
from google import genai
import asyncio
import time
from ratelimit import limits, RateLimitException, sleep_and_retry # Import rate limiting decorators
import logging
from langchain_core.messages import (
    AnyMessage,
    AIMessage,
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

# Configure the generative AI library with the API key
gemini_api_key = GOOGLE_API_KEY
if not gemini_api_key:
    gemini_api_key = GEMINI_API_KEY  # Fallback to GEMINI_API_KEY if GOOGLE_API_KEY not set

if not gemini_api_key:
    logging.error("Neither GOOGLE_API_KEY nor GEMINI_API_KEY found in environment.")
    # Handle this case, perhaps skip Gemini initialization or raise an error
else:
    logging.info("Gemini API configured successfully.")


## GEMINI Model Calling
gemini1 = "gemini-2.0-flash-lite"
gemini2 = "gemini-2.0-flash"
gemini_model =  gemini1

from google import genai
from google.genai import types
from google.genai.types import (
    CreateBatchJobConfig,
    CreateCachedContentConfig,
    EmbedContentConfig,
    FunctionDeclaration,
    GenerateContentConfig,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    SafetySetting,
    Tool,
)


MAX_RETRIES = 5 # Increased retries for robustness
BASE_DELAY = 1 # seconds
MAX_CONCURRENT_CALLS = 10 # Limit the number of concurrent calls
MAX_CALLS_PER_SECOND = 30 # Define the maximum calls per second (adjusted slightly)

# Create a global semaphore to limit concurrent calls
semaphore = asyncio.Semaphore(MAX_CONCURRENT_CALLS)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1) # Apply rate limits
async def llm_call_async(messages: List[AnyMessage], max_tokens: int = None): # Change parameter to accept a list of AnyMessage and added max_tokens
    """
    Asynchronously call the Gemini API with the provided Langchain messages.
    Returns the content of the assistant's reply.
    Includes retry logic and rate limiting.
    Allows setting max_output_tokens.
    """

    if not gemini_api_key:
        logging.error("Gemini API key not available. Skipping API call.")
        return None

    client = None # Initialize client to None outside the try block
    try:
        client = genai.Client(api_key=gemini_api_key) # Use genai.Client

        gemini_contents = []
        for message in messages:
            if isinstance(message, SystemMessage):
                 if gemini_contents and gemini_contents[0].role == 'user':
                     gemini_contents[0].parts[0].text = f"System Instruction: {message.content}\n\n" + gemini_contents[0].parts[0].text
                 else:
                     gemini_contents.insert(0, genai.types.Content(role='user', parts=[genai.types.Part(text=f"System Instruction: {message.content}\n\n")]))

            elif isinstance(message, HumanMessage):
                gemini_contents.append(genai.types.Content(role='user', parts=[genai.types.Part(text=message.content)]))
            elif isinstance(message, AIMessage):
                 gemini_contents.append(genai.types.Content(role='model', parts=[genai.types.Part(text=message.content)]))

        if not gemini_contents:
            logging.warning("No valid messages to send to Gemini API.")
            if client: await client.close() # Close client before returning
            return None

        for attempt in range(MAX_RETRIES):
            try:
                async with semaphore:
                    response = await client.aio.models.generate_content(
                                      model=gemini_model,
                                      contents=gemini_contents,
                                      config=types.GenerateContentConfig(
                                          temperature=0.1,
                                          max_output_tokens=30000
                                      )
                                  )

                    logging.info(f"Successfully called Gemini API on attempt {attempt + 1}")
                    return response.text # Return the text of the response

            except RateLimitException as e:
                logging.warning(f"Rate limit hit on attempt {attempt + 1}. Waiting before retrying...")
                await asyncio.sleep(e.period) # Wait for the duration specified by the rate limit decorator
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed calling GEMINI Inference API: {e}")
                if attempt < MAX_RETRIES - 1:
                    wait_time = BASE_DELAY * (2 ** attempt) + random.uniform(0, 1) # Exponential backoff with jitter
                    logging.info(f"Retrying in {wait_time:.2f} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error("Max retries reached. Failed to call GEMINI Inference API.")
                    if client: client.close() # Close client before returning
                    return None # Return None after max retries

    except Exception as e:
        logging.error(f"An error occurred before attempting API calls: {e}")
        #if client: client.close() # Close client before returning
        return None

