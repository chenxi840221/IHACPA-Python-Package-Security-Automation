#!/usr/bin/env python3
"""
Investigate font bold/color inconsistencies in Excel formatting
"""

import sys
sys.path.append('src')

from excel_handler import ExcelHandler
from openpyxl.styles import Font

def investigate_font_inconsistencies():
    """Investigate potential font bold/color issues"""
    
    print('🔍 Investigating Font Inconsistencies')
    print('=' * 60)
    
    # Create Excel handler instance
    handler = ExcelHandler("dummy.xlsx")
    
    print('Current Font Definitions:')
    print('-' * 30)
    
    for color_type, font in handler.font_colors.items():
        print(f"{color_type:15} | Color: {font.color} | Bold: {font.bold}")
        
        # Check if font color is actually being set correctly
        if hasattr(font.color, 'rgb'):
            rgb_value = font.color.rgb
        else:
            rgb_value = str(font.color)
        print(f"                | RGB: {rgb_value}")
        print()
    
    print('🔍 POTENTIAL ISSUES:')
    print('-' * 20)
    
    # Check for potential font issues
    issues_found = []
    
    # Issue 1: Check if new_data font is actually dark green instead of bright green
    new_data_font = handler.font_colors['new_data']
    if hasattr(new_data_font.color, 'rgb'):
        rgb = new_data_font.color.rgb
        if rgb and '008000' in str(rgb):  # Dark green
            issues_found.append("new_data font is dark green (008000) instead of bright green")
    
    # Issue 2: Check for bold consistency
    bold_statuses = {}
    for color_type, font in handler.font_colors.items():
        if color_type != 'default':
            bold_statuses[color_type] = font.bold
    
    # Issue 3: Test actual font application
    print('\n🧪 Testing Font Application:')
    print('-' * 30)
    
    test_scenarios = [
        ('new_data', 'pypi_latest_link', 'https://pypi.org/project/test/'),
        ('new_data', 'snyk_result', 'None found'),
        ('new_data', 'recommendation', 'PROCEED'),
        ('security_risk', 'snyk_result', 'SNYK Analysis: FOUND - vulnerability'),
        ('version_update', 'latest_version', '2.1.0'),
    ]
    
    for expected_color, field, value in test_scenarios:
        color_result = handler._determine_color_type(field, value, None)
        expected_font = handler.font_colors.get(color_result, handler.font_colors['default'])
        
        font_rgb = expected_font.color.rgb if hasattr(expected_font.color, 'rgb') else str(expected_font.color)
        
        print(f"{field:20} | Expected: {expected_color:12} | Actual: {color_result or 'None':12}")
        print(f"                     | Font RGB: {font_rgb} | Bold: {expected_font.bold}")
        
        if color_result == 'new_data':
            # Check if this specific new_data usage might have font issues
            if field in ['pypi_latest_link', 'nist_nvd_url', 'mitre_cve_url', 'snyk_url', 'exploit_db_url']:
                print(f"                     | ⚠️  URL field using NEW_DATA color")
            elif field in ['snyk_result', 'mitre_cve_result', 'github_advisory_result', 'exploit_db_result', 'nist_nvd_result']:
                print(f"                     | ✅ Security safe result using NEW_DATA color")
            elif field == 'recommendation':
                print(f"                     | ✅ PROCEED recommendation using NEW_DATA color")
        print()
    
    print('🔍 FONT INHERITANCE CHECK:')
    print('-' * 30)
    print('Potential issues:')
    print('1. Original Excel file may have existing font formatting')
    print('2. Bold fonts might not be applied consistently')
    print('3. Dark green (008000) vs Bright green color confusion')
    print('4. Font inheritance from original cells')
    
    print('\n💡 DIAGNOSIS:')
    print('-' * 15)
    
    if '008000' in str(handler.font_colors['new_data'].color):
        print('🔴 FOUND ISSUE: new_data font is using DARK GREEN (008000)')
        print('   This might appear differently than expected in Excel')
        print('   Dark green on light green background has poor contrast')
        
    print('\n📋 RECOMMENDATIONS:')
    print('-' * 20)
    print('1. Consider making new_data font color brighter for better contrast')
    print('2. Ensure consistent bold application across all color types')
    print('3. Test with actual Excel file to see visual differences')
    print('4. Consider different font colors for URL vs Safe Result semantics')

if __name__ == "__main__":
    investigate_font_inconsistencies()