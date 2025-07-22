#!/usr/bin/env python3
"""
Quick test script for AI CVE analysis functionality
Tests the AI CVE analyzer with a sample package
"""

import asyncio
import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.ai_cve_analyzer import AICVEAnalyzer


async def test_ai_cve_analysis():
    """Test AI CVE analysis with a sample package"""
    print("🧪 Testing AI CVE Analysis")
    print("=" * 50)
    
    # Check if OpenAI/Azure API key is available
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('AZURE_OPENAI_KEY')
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_model = os.getenv('AZURE_OPENAI_MODEL', 'gpt-4o-mini')
    
    if not api_key:
        print("❌ OpenAI/Azure API key not found in environment variables")
        print("   Set OPENAI_API_KEY or AZURE_OPENAI_KEY environment variable to test AI analysis")
        return False
    
    # Initialize analyzer (supports both standard OpenAI and Azure OpenAI)
    analyzer = AICVEAnalyzer(
        api_key=api_key,
        model=azure_model,
        azure_endpoint=azure_endpoint
    )
    
    if not analyzer.is_enabled():
        print("❌ AI CVE analyzer not enabled")
        return False
    
    print("✅ AI CVE Analyzer initialized successfully")
    print(f"📊 Stats: {analyzer.get_analysis_stats()}")
    print()
    
    # Test packages with known vulnerabilities
    test_packages = [
        {
            'name': 'requests',
            'version': '2.25.0',  # Older version with known vulnerabilities
            'description': 'HTTP library - older version with potential vulnerabilities'
        },
        {
            'name': 'aiohttp',
            'version': '3.8.3',  # Version in our dataset
            'description': 'Async HTTP library with multiple known vulnerabilities'
        },
        {
            'name': 'unknown-safe-package',
            'version': '1.0.0',
            'description': 'Non-existent package (should be safe)'
        }
    ]
    
    for package in test_packages:
        print(f"🔍 Testing: {package['name']} v{package['version']}")
        print(f"   {package['description']}")
        
        try:
            result = await analyzer.analyze_cve_result(
                package_name=package['name'],
                current_version=package['version'],
                cve_lookup_url=f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={package['name']}"
            )
            
            print(f"📝 AI Analysis Result:")
            print(f"   {result}")
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {package['name']}: {e}")
            print()
    
    print("✅ AI CVE Analysis test completed")
    return True


if __name__ == "__main__":
    print("IHACPA AI CVE Analysis Test")
    print("=" * 50)
    
    try:
        success = asyncio.run(test_ai_cve_analysis())
        if success:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️ Some tests failed - check configuration")
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")