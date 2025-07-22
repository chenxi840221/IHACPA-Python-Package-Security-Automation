#!/usr/bin/env python3
"""
Test direct Azure OpenAI API call with exact endpoint
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_direct_azure_call():
    """Test the exact endpoint you provided"""
    
    # Your Azure OpenAI configuration (replace with your actual values)
    api_key = os.getenv("AZURE_OPENAI_KEY", "your-azure-openai-key-here")
    endpoint = f"https://your-resource-name.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview"
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a cybersecurity expert. Provide brief CVE analysis."
            },
            {
                "role": "user", 
                "content": "Analyze CVE risks for Python package 'requests' version 2.25.0. Be very brief."
            }
        ],
        "max_tokens": 100,
        "temperature": 0.1
    }
    
    print("🔍 Testing Direct Azure OpenAI API Call")
    print("=" * 50)
    print(f"🔗 Endpoint: {endpoint}")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")
    print()
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and data['choices']:
                content = data['choices'][0]['message']['content']
                print(f"✅ SUCCESS! AI Response:")
                print(f"📝 {content}")
                return True
            else:
                print(f"❌ Empty response: {data}")
                return False
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False

def test_openai_library():
    """Test using OpenAI library with exact configuration"""
    print("\n🤖 Testing OpenAI Library with Azure")
    print("=" * 40)
    
    try:
        import openai
        
        client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY", "your-azure-openai-key-here"),
            api_version="2025-01-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource-name.openai.azure.com/")
        )
        
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a cybersecurity expert. Provide brief CVE analysis."
                },
                {
                    "role": "user", 
                    "content": "Analyze CVE risks for Python package 'requests' version 2.25.0. Be very brief."
                }
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        if response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            print(f"✅ SUCCESS! OpenAI Library Response:")
            print(f"📝 {content}")
            return True
        else:
            print(f"❌ Empty response from OpenAI library")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI library error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 DIRECT AZURE OPENAI API TEST")
    print("=" * 60)
    
    # Test direct API call
    direct_success = test_direct_azure_call()
    
    # Test OpenAI library
    library_success = test_openai_library()
    
    print(f"\n📊 RESULTS:")
    print(f"{'✅' if direct_success else '❌'} Direct API Call: {'SUCCESS' if direct_success else 'FAILED'}")
    print(f"{'✅' if library_success else '❌'} OpenAI Library: {'SUCCESS' if library_success else 'FAILED'}")
    
    if direct_success or library_success:
        print("\n🎉 Azure OpenAI is working!")
    else:
        print("\n⚠️ Both methods failed - check configuration")