#!/usr/bin/env python3
"""
Test script to verify font color implementation in Excel output
"""

import sys
import os
sys.path.append('src')

from excel_handler import ExcelHandler
from pathlib import Path
from datetime import datetime

def test_font_colors():
    """Test that font colors are applied correctly with fill colors"""
    
    # Create a test Excel file
    test_file = "test_font_colors.xlsx"
    
    # Copy sample data
    import shutil
    source_file = "02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx"
    if Path(source_file).exists():
        shutil.copy2(source_file, test_file)
    else:
        print(f"❌ Source file not found: {source_file}")
        return
    
    # Load the test file
    handler = ExcelHandler(test_file)
    if not handler.load_workbook():
        print("❌ Failed to load Excel file")
        return
    
    print("📊 Testing Font Colors with Fill Colors")
    print("=" * 50)
    
    # Test different types of updates to see font colors
    test_updates = [
        {
            'row': 10,
            'updates': {
                'mitre_cve_result': 'CVE-2024-1234 FOUND - Critical vulnerability affecting version 1.0.0',
                'recommendation': 'SECURITY RISK: Update immediately to patch critical vulnerability',
                'date_published': 'Not Available',
            }
        },
        {
            'row': 11,
            'updates': {
                'nist_nvd_result': 'No vulnerabilities found for this package',
                'github_url': 'https://github.com/example/package',
                'latest_version': '2.0.0',
            }
        },
        {
            'row': 12,
            'updates': {
                'snyk_result': 'Manual review required - check https://security.snyk.io/vuln/pip/package',
                'development_status': 'Production/Stable',
                'requires': 'requests>=2.28.0, aiohttp>=3.8.0',
            }
        }
    ]
    
    # Apply test updates
    for test in test_updates:
        row = test['row']
        updates = test['updates']
        
        print(f"\n📝 Updating row {row}:")
        for field, value in updates.items():
            print(f"   - {field}: {value[:50]}...")
        
        handler.update_package_data(row, updates)
    
    # Save the file
    handler.save_workbook(backup=False)
    
    # Display color statistics
    print("\n📈 Color Statistics:")
    stats = handler.get_color_statistics()
    print(f"Total changes: {stats['total_changes']}")
    print("\nColor breakdown:")
    for color_type, count in stats['color_breakdown'].items():
        desc = stats['color_descriptions'].get(color_type, color_type)
        print(f"  - {color_type}: {count} cells - {desc}")
    
    print(f"\n✅ Test completed! Check '{test_file}' to see:")
    print("  - Light red cells with dark red text for security risks")
    print("  - Light green cells with dark green text for safe/new data")
    print("  - Light orange cells with dark orange text for version updates")
    print("  - Light blue cells with dark blue text for general updates")
    print("  - Red cells with white text for 'Not Available' data")
    
    handler.close()

if __name__ == "__main__":
    test_font_colors()