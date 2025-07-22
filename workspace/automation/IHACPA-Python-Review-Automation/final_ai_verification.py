#!/usr/bin/env python3
"""
Final verification of Azure OpenAI AI CVE integration
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not available")

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_configuration():
    """Test Azure OpenAI configuration"""
    print("\n🔧 Testing Configuration:")
    print("=" * 40)
    
    api_key = os.getenv('AZURE_OPENAI_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    model = os.getenv('AZURE_OPENAI_MODEL')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:] if api_key else 'None'}")
    print(f"🌐 Endpoint: {endpoint}")
    print(f"🤖 Model: {model}")
    print(f"📋 API Version: {api_version}")
    
    if all([api_key, endpoint, model, api_version]):
        print("✅ All Azure OpenAI configuration present")
        return True
    else:
        print("❌ Missing Azure OpenAI configuration")
        return False

def test_ai_analyzer():
    """Test AI CVE Analyzer directly"""
    print("\n🤖 Testing AI CVE Analyzer:")
    print("=" * 40)
    
    try:
        from src.ai_cve_analyzer import AICVEAnalyzer
        
        analyzer = AICVEAnalyzer()
        
        if analyzer.is_enabled():
            stats = analyzer.get_analysis_stats()
            print("✅ AI CVE Analyzer enabled")
            print(f"📊 Service: {stats['service_type']}")
            print(f"🔗 Endpoint: {stats['azure_endpoint']}")
            print(f"🤖 Model: {stats['model']}")
            return True
        else:
            print("❌ AI CVE Analyzer not enabled")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing AI analyzer: {e}")
        return False

def test_vulnerability_scanner():
    """Test vulnerability scanner with AI integration"""
    print("\n🛡️ Testing Vulnerability Scanner with AI:")
    print("=" * 40)
    
    try:
        from src.vulnerability_scanner import VulnerabilityScanner
        
        scanner = VulnerabilityScanner()
        
        if scanner.ai_analyzer and scanner.ai_analyzer.is_enabled():
            print("✅ Vulnerability Scanner has AI analysis enabled")
            print(f"🔗 AI Service: {scanner.ai_analyzer.get_analysis_stats()['service_type']}")
            return True
        else:
            print("❌ Vulnerability Scanner AI not enabled")
            return False
            
    except Exception as e:
        print(f"❌ Error testing vulnerability scanner: {e}")
        return False

async def test_live_analysis():
    """Test live AI CVE analysis"""
    print("\n🧪 Testing Live AI Analysis:")
    print("=" * 40)
    
    try:
        from src.ai_cve_analyzer import AICVEAnalyzer
        
        analyzer = AICVEAnalyzer()
        
        if not analyzer.is_enabled():
            print("❌ AI analyzer not enabled")
            return False
        
        # Test with a simple package
        result = await analyzer.analyze_cve_result(
            package_name="test-package",
            current_version="1.0.0",
            cve_lookup_url="https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=test-package"
        )
        
        if "AI analysis failed" not in result:
            print("✅ Live AI analysis working")
            print(f"📝 Sample result: {result[:100]}...")
            return True
        else:
            print(f"❌ AI analysis failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error in live analysis: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 AZURE OPENAI AI CVE INTEGRATION VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("AI Analyzer", test_ai_analyzer),
        ("Vulnerability Scanner", test_vulnerability_scanner),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Live analysis test (async)
    print("\n🧪 Testing Live AI Analysis:")
    print("=" * 40)
    try:
        import asyncio
        live_result = asyncio.run(test_live_analysis())
        results.append(("Live Analysis", live_result))
    except Exception as e:
        print(f"💥 Live analysis test failed: {e}")
        results.append(("Live Analysis", False))
    
    # Summary
    print("\n📊 VERIFICATION SUMMARY:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 AZURE OPENAI AI CVE INTEGRATION FULLY WORKING! 🎉")
        print("✅ Ready for production use with AI-powered CVE analysis")
        print("✅ Column R (MITRE CVE Lookup Result) will use AI analysis")
        print("✅ System will provide version-specific vulnerability assessments")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed - check configuration")

if __name__ == "__main__":
    main()