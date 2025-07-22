#!/usr/bin/env python3
"""
Check Azure OpenAI deployments using REST API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_azure_deployments():
    """Check what deployments exist in Azure OpenAI"""
    
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_KEY')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    if not endpoint or not api_key:
        print("❌ Azure OpenAI configuration missing")
        return
    
    # Remove trailing slash if present
    endpoint = endpoint.rstrip('/')
    
    # Azure OpenAI deployments API
    url = f"{endpoint}/openai/deployments?api-version={api_version}"
    
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    print("🔍 Checking Azure OpenAI deployments...")
    print(f"📍 Endpoint: {endpoint}")
    print(f"🔗 URL: {url}")
    print()
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            deployments = data.get('data', [])
            
            if deployments:
                print(f"✅ Found {len(deployments)} deployment(s):")
                print("=" * 50)
                
                for i, deployment in enumerate(deployments, 1):
                    name = deployment.get('id', 'Unknown')
                    model = deployment.get('model', 'Unknown')
                    status = deployment.get('status', 'Unknown')
                    
                    print(f"{i}. Deployment Name: '{name}'")
                    print(f"   Model: {model}")
                    print(f"   Status: {status}")
                    print()
                    
                    if status == 'succeeded':
                        print(f"💡 Try updating your .env file with:")
                        print(f"   AZURE_OPENAI_MODEL={name}")
                        print()
                
            else:
                print("❌ No deployments found!")
                print("💡 You need to create a model deployment in Azure Portal:")
                print("   1. Go to your Azure OpenAI resource")
                print("   2. Click 'Model deployments'")
                print("   3. Click 'Create new deployment'")
                print("   4. Choose a model and deployment name")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    check_azure_deployments()