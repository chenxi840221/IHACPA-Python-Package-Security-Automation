#!/usr/bin/env python3
"""
Simple test to demonstrate Date Published logic for specific packages
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from excel_handler import ExcelHandler
from pypi_client import PyPIClient

def test_date_published_logic():
    """Test the Date Published logic as implemented in main.py"""
    
    # Packages to test
    packages_to_test = [
        ("PyQt5", "5.15.7"),
        ("PyQtWebEngine", "5.15.4"),
        ("ruamel.yaml", "0.17.21"),
        ("Unidecode", "1.2.0")
    ]
    
    # Initialize PyPI client
    pypi_client = PyPIClient()
    
    print("Testing Date Published Logic")
    print("=" * 60)
    print("\nThis demonstrates what the automation would do for each package:\n")
    
    for package_name, current_version in packages_to_test:
        print(f"\n📦 {package_name} (Version: {current_version})")
        print("-" * 40)
        
        # This is the logic from main.py lines 231-253
        
        # Step 1: Get PyPI information
        pypi_info = pypi_client.get_package_info(package_name)
        
        if pypi_info:
            print(f"✅ Successfully fetched PyPI info")
            
            # Step 2: Extract publication date for CURRENT version (not latest)
            current_version_date = pypi_client.extract_version_date_from_package_info(pypi_info, current_version)
            
            # Step 3: Determine what would be written to Date Published column
            if current_version_date:
                date_published_value = current_version_date
                print(f"📅 Date Published would be set to: {date_published_value}")
                print(f"   Formatted: {date_published_value.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                date_published_value = "Not Available"
                print(f"⚠️  Date Published would be set to: '{date_published_value}'")
                print(f"   (Could not retrieve publication date for version {current_version})")
        else:
            print(f"❌ Failed to fetch PyPI info")
            print(f"   Date Published would remain empty")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    print("-" * 60)
    print("The automation script has the following logic for Date Published:")
    print("1. It always tries to update the Date Published field (force_update_date_published = True)")
    print("2. It uses the CURRENT version (Column C), not the latest version")
    print("3. If PyPI returns a date for that version, it sets that date")
    print("4. If PyPI cannot provide a date, it sets 'Not Available'")
    print("\nThe Excel file shows empty/None values because the automation")
    print("hasn't been run on these packages yet. Once run, these fields")
    print("would be populated with the dates shown above.")

if __name__ == "__main__":
    test_date_published_logic()