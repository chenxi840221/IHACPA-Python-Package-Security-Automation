#!/usr/bin/env python3
"""
Test if we can determine what's wrong with Azure configuration
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_azure_access():
    """Test basic Azure OpenAI access"""
    
    endpoint = "https://automation-seanchen.openai.azure.com/"
    api_key = os.getenv('AZURE_OPENAI_KEY')
    
    # Test basic connectivity
    print("🔍 Testing Azure OpenAI Resource Access")
    print("=" * 50)
    print(f"📍 Endpoint: {endpoint}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else api_key}")
    print()
    
    # Try different API versions and endpoints
    test_configs = [
        {"version": "2023-05-15", "path": "openai/deployments"},
        {"version": "2023-12-01-preview", "path": "openai/deployments"}, 
        {"version": "2024-02-15-preview", "path": "openai/deployments"},
        {"version": "2023-05-15", "path": "openai/models"},
    ]
    
    for config in test_configs:
        url = f"{endpoint.rstrip('/')}/{config['path']}?api-version={config['version']}"
        
        headers = {
            'api-key': api_key,
            'Content-Type': 'application/json'
        }
        
        print(f"🧪 Testing: {config['path']} (API v{config['version']})")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS!")
                data = response.json()
                if 'data' in data:
                    items = data['data']
                    print(f"   📊 Found {len(items)} items")
                    for item in items[:3]:  # Show first 3 items
                        if 'id' in item:
                            print(f"      - {item['id']}")
                else:
                    print(f"   📋 Response: {str(data)[:100]}...")
                print()
                return True
            elif response.status_code == 401:
                print(f"   ❌ Authentication failed - wrong API key")
            elif response.status_code == 404:
                print(f"   ❌ Not found - {response.text[:100]}...")
            else:
                print(f"   ❌ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   💥 Exception: {str(e)[:100]}...")
        
        print()
    
    return False

if __name__ == "__main__":
    test_azure_access()