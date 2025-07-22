#!/usr/bin/env python3
"""
Test script to find the correct Azure OpenAI deployment name
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv not installed")

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.ai_cve_analyzer import AICVEAnalyzer

async def test_deployment_name(deployment_name):
    """Test a specific deployment name"""
    print(f"🧪 Testing deployment name: {deployment_name}")
    
    try:
        analyzer = AICVEAnalyzer(
            api_key=os.getenv('AZURE_OPENAI_KEY'),
            model=deployment_name,
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
        )
        
        if not analyzer.is_enabled():
            print(f"❌ Analyzer not enabled for {deployment_name}")
            return False
            
        # Try a simple test
        result = await analyzer.analyze_cve_result(
            package_name="test",
            current_version="1.0.0",
            cve_lookup_url="https://test.com"
        )
        
        if "AI analysis failed" not in result:
            print(f"✅ SUCCESS! Deployment name '{deployment_name}' works!")
            print(f"📝 Test result: {result[:100]}...")
            return True
        else:
            print(f"❌ Failed for {deployment_name}: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error with {deployment_name}: {str(e)[:100]}...")
        return False

async def find_deployment_name():
    """Try common deployment names"""
    common_names = [
        "gpt-4o",
        "gpt4o", 
        "gpt-4o-mini",
        "gpt4o-mini",
        "chat",
        "chatgpt",
        "openai",
        "gpt-4",
        "gpt4",
        "deployment",
        "default"
    ]
    
    print("🔍 Searching for correct Azure OpenAI deployment name...")
    print("=" * 60)
    
    for name in common_names:
        success = await test_deployment_name(name)
        if success:
            return name
        print()
    
    print("❌ No working deployment name found.")
    print("💡 Please check your Azure Portal for the exact deployment name.")
    return None

if __name__ == "__main__":
    import asyncio
    
    print("AZURE OPENAI DEPLOYMENT NAME FINDER")
    print("=" * 60)
    
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    key = os.getenv('AZURE_OPENAI_KEY')
    
    if not endpoint or not key:
        print("❌ Azure OpenAI configuration missing")
        print("   Make sure AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY are set")
    else:
        print(f"✅ Endpoint: {endpoint}")
        print(f"✅ Key: {key[:10]}...")
        print()
        
        try:
            result = asyncio.run(find_deployment_name())
            if result:
                print(f"\n🎉 FOUND IT! Your deployment name is: '{result}'")
                print(f"💡 Update your .env file with:")
                print(f"   AZURE_OPENAI_MODEL={result}")
        except Exception as e:
            print(f"💥 Error: {e}")