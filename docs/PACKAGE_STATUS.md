# INTELLISEARCH Package Dependencies Guide

## Package Status for Python 3.13

### ✅ **Core Packages (Required)**
These are essential for INTELLISEARCH to function:

| Package | Status | Notes |
|---------|--------|-------|
| `requests` | ✅ Excellent | HTTP requests |
| `python-dotenv` | ✅ Excellent | Environment variables |
| `pydantic` | ⚠️ Good | Use v2.8+ for Python 3.13 |
| `langchain` | ✅ Good | Core LLM framework |
| `langgraph` | ✅ Good | Workflow engine |
| `beautifulsoup4` | ✅ Excellent | HTML parsing |
| `aiohttp` | ✅ Good | Async HTTP |
| `nest_asyncio` | ✅ Excellent | Async compatibility |
| `rich` | ✅ Excellent | Terminal formatting |

### 🔧 **Document Processing**
| Package | Status | Notes |
|---------|--------|-------|
| `pymupdf` | ✅ Good | PDF processing |
| `trafilatura` | ✅ Good | Web content extraction |
| `fpdf2` | ✅ Good | PDF generation |
| `lxml` | ⚠️ Fair | May need binary wheel |

### 🤖 **LLM Provider SDKs**
These connect to different AI services:

| Package | Python 3.13 Status | Purpose | Import Statement |
|---------|-------------------|---------|------------------|
| `google-genai` | ✅ **Good** | Google Gemini API | `from google import genai` |
| `langchain-google-genai` | ✅ **Good** | LangChain + Google integration | `import langchain_google_genai` |
| `anthropic` | ✅ **Excellent** | Claude API | `import anthropic` |
| `together` | ✅ **Good** | Together AI API | `import together` |
| `voyageai` | ✅ **Good** | Voyage embeddings | `import voyageai` |

### 🗃️ **Vector Databases & Search**
| Package | Python 3.13 Status | Notes |
|---------|-------------------|-------|
| `chromadb` | ❌ **Problematic** | No Python 3.13 wheels yet |
| `faiss-cpu` | ⚠️ **Conditional** | Use conda or binary wheels |
| `rank_bm25` | ✅ **Excellent** | Text ranking |

## 🚀 **Installation Recommendations**

### **Option 1: Use the Python 3.13 Setup (Recommended)**
```cmd
python313_setup.bat
```
This handles all compatibility issues automatically.

### **Option 2: Manual Installation**
```cmd
# Core packages (always install these)
pip install requests python-dotenv "pydantic>=2.8.0" langchain langgraph

# LLM providers (install what you need)
pip install "google-genai>=1" anthropic together voyageai
pip install langchain-google-genai

# Document processing
pip install pymupdf trafilatura fpdf2
pip install "lxml>=5.0.0" --prefer-binary

# Vector databases (problematic on Python 3.13)
pip install "chromadb>=0.4.0" --prefer-binary  # May fail
conda install -c conda-forge faiss-cpu  # Better via conda
```

### **Option 3: Use Python 3.11 Instead**
If you need all packages working perfectly:
```cmd
# Install Python 3.11 from python.org
# Then create venv with specific version
C:\Python311\python.exe -m venv .venv
```

## 🔍 **Which Packages Do You Actually Need?**

### **Minimal Setup (Core functionality)**
```
requests, python-dotenv, pydantic, langchain, langgraph
beautifulsoup4, aiohttp, pymupdf, rich
```

### **+ Google AI**
```
+ google-genai, langchain-google-genai
```
**Import:** `from google import genai`

### **+ Anthropic Claude**
```
+ anthropic
```

### **+ Vector Search**
```
+ chromadb (if working) OR faiss-cpu (via conda)
+ rank_bm25
```

### **+ Advanced Document Processing**
```
+ trafilatura, fpdf2, lxml
```

## ⚠️ **Known Issues & Solutions**

### **ChromaDB on Python 3.13**
- **Issue**: No pre-compiled wheels available
- **Solution 1**: Use conda instead of pip
- **Solution 2**: Wait for ChromaDB to release Python 3.13 wheels
- **Solution 3**: Use alternative vector DB like Weaviate or Pinecone

### **FAISS on Windows**
- **Issue**: Complex compilation requirements
- **Solution**: Use conda: `conda install -c conda-forge faiss-cpu`

### **Google GenAI Package Name**
- **Correct package**: `google-genai>=1` (not google-generativeai)
- **Import**: `from google import genai` 
- **Installation**: `pip install "google-genai>=1"`

## 🎯 **Recommendation for Your Setup**

Since you're using Python 3.13, I recommend:

1. **Run `python313_setup.bat`** - handles everything automatically
2. **Core packages will install fine** - langchain, langgraph, pydantic all work
3. **LLM providers will mostly work** - Google, Anthropic, Together all good
4. **Vector DB may need alternatives** - ChromaDB problematic, use conda for FAISS
5. **Consider staying with Python 3.11** if you need 100% compatibility

The application will work with just the core packages - the optional ones enhance functionality but aren't strictly required for basic operation.