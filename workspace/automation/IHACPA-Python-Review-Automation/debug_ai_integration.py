#!/usr/bin/env python3
"""
Debug script to check AI integration in the main workflow
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️ python-dotenv not available")

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def check_environment():
    """Check environment variables"""
    print("\n🔍 Environment Variables:")
    print("=" * 40)
    
    vars_to_check = [
        'AZURE_OPENAI_KEY',
        'AZURE_OPENAI_ENDPOINT', 
        'AZURE_OPENAI_MODEL',
        'AZURE_OPENAI_API_VERSION'
    ]
    
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            if 'KEY' in var:
                print(f"✅ {var}: {value[:10]}...{value[-10:]}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

def test_vulnerability_scanner_integration():
    """Test if vulnerability scanner properly initializes AI"""
    print("\n🛡️ Testing Vulnerability Scanner AI Integration:")
    print("=" * 50)
    
    try:
        from src.vulnerability_scanner import VulnerabilityScanner
        
        # Initialize scanner with current environment
        scanner = VulnerabilityScanner()
        
        if scanner.ai_analyzer:
            print("✅ AI analyzer initialized in vulnerability scanner")
            if scanner.ai_analyzer.is_enabled():
                print("✅ AI analyzer is enabled")
                stats = scanner.ai_analyzer.get_analysis_stats()
                print(f"📊 Service: {stats['service_type']}")
                print(f"🔗 Endpoint: {stats['azure_endpoint']}")
                print(f"🤖 Model: {stats['model']}")
                print(f"📋 API Version: {stats['api_version']}")
                return True
            else:
                print("❌ AI analyzer is disabled")
                return False
        else:
            print("❌ AI analyzer not initialized")
            return False
            
    except Exception as e:
        print(f"❌ Error testing vulnerability scanner: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mitre_scan():
    """Test MITRE CVE scan with AI"""
    print("\n🔍 Testing MITRE CVE Scan with AI:")
    print("=" * 40)
    
    try:
        from src.vulnerability_scanner import VulnerabilityScanner
        
        scanner = VulnerabilityScanner()
        
        if not scanner.ai_analyzer or not scanner.ai_analyzer.is_enabled():
            print("❌ AI analyzer not available for testing")
            return False
        
        # Test with a real package
        result = await scanner.scan_mitre_cve("requests", "2.25.0")
        
        print(f"📝 Result Summary: {result['summary'][:100]}...")
        print(f"📋 Note: {result['note'][:100]}...")
        
        if 'ai_analysis' in result and result['ai_analysis']:
            print(f"🤖 AI Analysis: {result['ai_analysis'][:100]}...")
            
        if "Manual review required" not in result['summary']:
            print("✅ AI analysis working in MITRE scan")
            return True
        else:
            print("❌ Still showing manual review required")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MITRE scan: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all debug tests"""
    print("🔧 DEBUGGING AI INTEGRATION IN MAIN WORKFLOW")
    print("=" * 60)
    
    # Check environment
    check_environment()
    
    # Test vulnerability scanner
    scanner_ok = test_vulnerability_scanner_integration()
    
    # Test MITRE scan
    if scanner_ok:
        mitre_ok = await test_mitre_scan()
    else:
        mitre_ok = False
    
    print("\n📊 DEBUG SUMMARY:")
    print("=" * 30)
    print(f"✅ Environment: OK")
    print(f"{'✅' if scanner_ok else '❌'} Scanner AI: {'OK' if scanner_ok else 'FAILED'}")
    print(f"{'✅' if mitre_ok else '❌'} MITRE AI: {'OK' if mitre_ok else 'FAILED'}")
    
    if scanner_ok and mitre_ok:
        print("\n🎉 AI integration should work in main workflow!")
    else:
        print("\n⚠️ Issues found - AI integration may not work properly")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())