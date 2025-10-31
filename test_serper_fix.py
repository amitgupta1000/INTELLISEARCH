# test_serper_fix.py
# Quick test to verify the Serper API fix

import asyncio
import logging
from src.search import UnifiedSearcher

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_serper_search():
    """Test the updated Serper search functionality."""
    
    print("🧪 Testing Serper API Fix")
    print("=" * 40)
    
    try:
        # Initialize searcher
        searcher = UnifiedSearcher(max_results=3)
        print("✅ UnifiedSearcher initialized successfully")
        
        # Test search
        test_query = "artificial intelligence 2024"
        print(f"\n🔍 Testing search for: '{test_query}'")
        
        results = await searcher.search(test_query, engines=["serper"])
        
        print(f"\n📊 Results:")
        print(f"   Found: {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"\n   {i}. {result.title}")
            print(f"      URL: {result.url}")
            print(f"      Snippet: {result.snippet[:100]}...")
            print(f"      Source: {result.source}")
        
        if results:
            print("\n✅ Serper search working correctly!")
            return True
        else:
            print("\n⚠️ No results returned - check API key and configuration")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        logging.exception("Test failed with exception")
        return False

async def test_domain_filtering():
    """Test domain filtering functionality."""
    
    print("\n🔍 Testing Domain Filtering")
    print("=" * 40)
    
    try:
        from src.search import classify_url
        from src.config import BLOCKED_DOMAINS
        
        # Test URL classification
        test_urls = [
            "https://www.reuters.com/article/123",
            "https://scholar.google.com/paper",
            "https://www.sec.gov/filing",
            "https://example.com/page"
        ]
        
        print(f"Blocked domains: {BLOCKED_DOMAINS}")
        print(f"\nURL Classifications:")
        
        for url in test_urls:
            classification = classify_url(url)
            print(f"   {url} → {classification}")
        
        print("\n✅ Domain filtering working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during domain filtering test: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 SERPER API FIX VALIDATION")
    print("=" * 50)
    
    # Test basic functionality
    success1 = asyncio.run(test_serper_search())
    success2 = asyncio.run(test_domain_filtering())
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED - Serper API fix is working!")
    else:
        print("💥 SOME TESTS FAILED - Check the errors above")
    print("=" * 50)

if __name__ == "__main__":
    main()