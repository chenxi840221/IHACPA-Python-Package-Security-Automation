#!/usr/bin/env python3
"""
Show all packages in the spreadsheet
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd

def show_all_packages(filename):
    """Show all packages in the spreadsheet"""
    print(f"Reading packages from {filename}")
    
    try:
        # Read the Excel file
        df = pd.read_excel(filename, sheet_name=0)
        
        # Look for package name column (usually column B)
        package_columns = ['Package Name', 'package_name', 'Package', 'B']
        package_col = None
        
        for col in package_columns:
            if col in df.columns:
                package_col = col
                break
        
        if package_col is None:
            # Try by position (column B = index 1)
            if len(df.columns) > 1:
                package_col = df.columns[1]
        
        if package_col is None:
            print("Could not find package name column")
            print(f"Available columns: {list(df.columns)}")
            return
        
        print(f"Using column: {package_col}")
        
        # Get all package names
        packages = df[package_col].dropna().tolist()
        
        print(f"\nTotal packages: {len(packages)}")
        print("\nAll packages:")
        
        for i, pkg in enumerate(packages):
            print(f"  {i+1:3d}. {pkg}")
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    show_all_packages("2025-07-23.xlsx")