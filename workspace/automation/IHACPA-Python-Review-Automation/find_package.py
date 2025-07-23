#!/usr/bin/env python3
"""
Find packages in the spreadsheet that contain specific text
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from excel_handler import ExcelHandler

def find_packages_containing(filename, search_text):
    """Find packages containing the search text"""
    print(f"Searching for packages containing '{search_text}' in {filename}")
    
    handler = ExcelHandler(filename)
    
    # Read all packages
    packages = handler.get_all_packages()
    
    matches = []
    for package in packages:
        package_name = package.get('package_name', '').lower()
        if search_text.lower() in package_name:
            matches.append({
                'name': package.get('package_name', ''),
                'row': package.get('row_number', ''),
                'version': package.get('current_version', '')
            })
    
    if matches:
        print(f"\nFound {len(matches)} matching packages:")
        for match in matches:
            print(f"  - {match['name']} (Row {match['row']}, v{match['version']})")
    else:
        print(f"\nNo packages found containing '{search_text}'")
        
    # Show total count and some examples
    print(f"\nTotal packages in spreadsheet: {len(packages)}")
    print(f"First 10 packages in spreadsheet:")
    for i, package in enumerate(packages[:10]):
        print(f"  {i+1}. {package.get('package_name', 'Unknown')} (Row {package.get('row_number', 'Unknown')})")
        
    return matches

if __name__ == "__main__":
    # Just search for one term and show the packages
    print("=" * 60)
    find_packages_containing("2025-07-23.xlsx", "pbi")