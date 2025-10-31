# startup_validation.py
# Run this before starting the main application to ensure all imports work

import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate the entire environment setup."""
    
    print("\n" + "="*60)
    print("🔍 INTELLISEARCH STARTUP VALIDATION")
    print("="*60)
    
    success = True
    
    # 1. Validate Python version
    print(f"\n1. 🐍 Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        success = False
    else:
        print("✅ Python version OK")
    
    # 2. Validate virtual environment
    print(f"\n2. 🔧 Virtual Environment:")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️ No virtual environment detected (recommended)")
    
    # 3. Validate LangChain imports
    print(f"\n3. 📦 LangChain/LangGraph Imports:")
    try:
        from src.import_validator import validate_imports
        validator = validate_imports()
        
        # Check critical packages
        critical_available = True
        for module_name, status in validator.import_status.items():
            if module_name in ["langgraph.graph", "langchain_core.messages", "langchain_core.documents"]:
                if not status.available:
                    critical_available = False
                    print(f"❌ {module_name}: {status.error}")
                else:
                    print(f"✅ {module_name}")
        
        if not critical_available:
            print("❌ Critical LangChain packages missing")
            success = False
            
            missing = validator.get_missing_packages()
            if missing:
                print(f"\n💡 Install missing packages with:")
                print(f"   pip install {' '.join(missing)}")
        
    except Exception as e:
        print(f"❌ Import validation failed: {e}")
        success = False
    
    # 4. Validate configuration
    print(f"\n4. ⚙️ Configuration:")
    try:
        from src.config import validate_config, GOOGLE_API_KEY, SERPER_API_KEY
        
        if validate_config():
            print("✅ Configuration validation passed")
        else:
            print("⚠️ Configuration warnings (check logs)")
            
        # Check critical API keys
        if GOOGLE_API_KEY:
            print("✅ Google API key configured")
        else:
            print("❌ Google API key missing")
            success = False
            
        if SERPER_API_KEY:
            print("✅ Serper API key configured")
        else:
            print("⚠️ Serper API key missing (search may be limited)")
            
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        success = False
    
    # 5. Validate core modules
    print(f"\n5. 🧩 Core Modules:")
    modules_to_test = [
        ("src.config", "Configuration"),
        ("src.api_keys", "API Keys"),
        ("src.search", "Search Engine"),
        ("src.llm_utils", "LLM Utilities"),
        ("src.nodes", "Workflow Nodes"),
        ("src.graph", "LangGraph Workflow"),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}")
        except Exception as e:
            print(f"❌ {description}: {e}")
            success = False
    
    # 6. Test basic functionality
    print(f"\n6. 🧪 Basic Functionality:")
    try:
        from src.search import UnifiedSearcher
        searcher = UnifiedSearcher(max_results=1)
        print("✅ Search engine initialization")
    except Exception as e:
        print(f"❌ Search engine initialization: {e}")
        success = False
    
    try:
        from src.graph import app
        if app is not None:
            print("✅ LangGraph workflow compilation")
        else:
            print("❌ LangGraph workflow compilation failed")
            success = False
    except Exception as e:
        print(f"❌ LangGraph workflow: {e}")
        success = False
    
    # Final result
    print("\n" + "="*60)
    if success:
        print("🎉 VALIDATION PASSED - INTELLISEARCH is ready to run!")
        print("   You can now use: python app.py")
    else:
        print("💥 VALIDATION FAILED - Please fix the issues above")
        print("   Try running: run_setup_and_interactive.bat")
    print("="*60)
    
    return success

def main():
    """Main function for command line usage."""
    try:
        success = validate_environment()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()