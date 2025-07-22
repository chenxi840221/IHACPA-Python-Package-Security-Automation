#!/usr/bin/env python3
"""
Debug test for Date Published logic
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from pypi_client import PyPIClient

def test_single_package(package_name, current_version):
    """Test a single package with detailed output"""
    print(f"\n{'='*60}")
    print(f"Testing: {package_name} v{current_version}")
    print(f"{'='*60}")
    
    client = PyPIClient()
    
    # Step 1: Test basic package info retrieval
    print("\n1. Testing get_package_info()...")
    try:
        pypi_info = client.get_package_info(package_name)
        if pypi_info:
            print(f"✅ Package info retrieved successfully")
            print(f"   Name: {pypi_info.get('name')}")
            print(f"   Latest version: {pypi_info.get('latest_version')}")
            print(f"   Has releases data: {'releases' in pypi_info}")
            
            # Step 2: Test version date extraction
            print(f"\n2. Testing extract_version_date_from_package_info() for v{current_version}...")
            version_date = client.extract_version_date_from_package_info(pypi_info, current_version)
            if version_date:
                print(f"✅ Date extracted: {version_date}")
            else:
                print(f"❌ Could not extract date")
                
                # Check if version exists in releases
                releases = pypi_info.get('releases', {})
                if current_version in releases:
                    print(f"   Version {current_version} exists in releases")
                    print(f"   Release files: {len(releases[current_version])}")
                else:
                    print(f"   Version {current_version} NOT found in releases")
                    print(f"   Available versions (first 5): {list(releases.keys())[:5]}")
        else:
            print(f"❌ Failed to retrieve package info")
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 3: Test direct version API
    print(f"\n3. Testing get_version_publication_date() directly...")
    try:
        direct_date = client.get_version_publication_date(package_name, current_version)
        if direct_date:
            print(f"✅ Direct API returned: {direct_date}")
        else:
            print(f"❌ Direct API returned None")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    packages = [
        ("PyQt5", "5.15.7"),
        ("Unidecode", "1.2.0")
    ]
    
    for package_name, version in packages:
        test_single_package(package_name, version)

if __name__ == "__main__":
    main()