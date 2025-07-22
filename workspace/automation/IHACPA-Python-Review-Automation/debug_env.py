#!/usr/bin/env python3
"""
Debug script to check .env file loading
"""

import os
from pathlib import Path

print("=== ENV DEBUG ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {Path(__file__).parent}")

# Check if .env file exists
env_file = Path(__file__).parent / '.env'
print(f".env file path: {env_file}")
print(f".env file exists: {env_file.exists()}")

if env_file.exists():
    print("\n.env file contents:")
    with open(env_file, 'r') as f:
        content = f.read()
        print(repr(content))

# Try to load dotenv
try:
    from dotenv import load_dotenv
    print(f"\npython-dotenv imported successfully")
    
    # Load the .env file
    result = load_dotenv(env_file)
    print(f"load_dotenv result: {result}")
    
    # Check environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"OPENAI_API_KEY from environment: {api_key[:10] + '...' if api_key else 'None'}")
    
except ImportError as e:
    print(f"Failed to import dotenv: {e}")
except Exception as e:
    print(f"Error loading dotenv: {e}")