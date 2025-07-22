#!/usr/bin/env python3
"""
Test script to verify color coding is working correctly
"""

import sys
sys.path.append('src')

from excel_handler import ExcelHandler

def test_color_logic():
    """Test the color determination logic"""
    
    # Create Excel handler instance
    handler = ExcelHandler("dummy.xlsx")
    
    print('🎨 Testing Color Determination Logic')
    print('=' * 60)
    
    # Test cases for different field types and values
    test_cases = [
        # Security vulnerability results - should be RED
        ('github_advisory_result', 'GitHub Security Advisory Analysis: FOUND - Multiple advisories affect xlwt', None, 'security_risk'),
        ('snyk_result', 'SNYK Analysis: FOUND – SNYK reports a known vulnerability', None, 'security_risk'),
        ('mitre_cve_result', 'CVE Analysis: FOUND - xlwt 1.3.0 is affected by CVE-2023-12345', None, 'security_risk'),
        ('exploit_db_result', 'Exploit Database Analysis: FOUND - Remote code execution exploit', None, 'security_risk'),
        ('nist_nvd_result', 'Found 5 vulnerabilities in NIST NVD', None, 'security_risk'),
        
        # Safe results - should be GREEN
        ('github_advisory_result', 'No published security advisories', None, 'new_data'),
        ('snyk_result', 'None found', None, 'new_data'),
        ('mitre_cve_result', 'CVE Analysis: NOT_FOUND', None, 'new_data'),
        ('exploit_db_result', 'Exploit Database Analysis: NOT_FOUND', None, 'new_data'),
        ('nist_nvd_result', 'None found', None, 'new_data'),
        
        # Recommendations - should be RED for security risks, GREEN for PROCEED
        ('recommendation', 'SECURITY RISK: 2 vulnerabilities found | HIGH PRIORITY', None, 'security_risk'),
        ('recommendation', 'PROCEED', None, 'new_data'),
        
        # Version updates - should be ORANGE
        ('latest_version', '2.1.0', '2.0.0', 'version_update'),
        ('latest_release_date', '2025-07-10', '2025-07-09', 'version_update'),
        ('date_published', '2023-01-01', '2022-12-31', 'version_update'),
        
        # GitHub fields - should be PURPLE
        ('github_url', 'https://github.com/user/repo', None, 'github_added'),
        ('github_advisory_url', 'https://github.com/user/repo/security/advisories', None, 'github_added'),
        
        # URLs - should be GREEN
        ('pypi_latest_link', 'https://pypi.org/project/package/1.0.0/', None, 'new_data'),
        ('nist_nvd_url', 'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=package', None, 'new_data'),
        
        # General updates - should be BLUE
        ('requires', 'requests>=2.25.0', 'requests>=2.24.0', 'updated'),
        ('development_status', '5 - Production/Stable', '4 - Beta', 'updated'),
    ]
    
    print('Testing color determination for different scenarios:')
    print('-' * 60)
    
    all_passed = True
    
    for field, new_value, old_value, expected_color in test_cases:
        actual_color = handler._determine_color_type(field, new_value, old_value)
        
        status = "✅ PASS" if actual_color == expected_color else "❌ FAIL"
        if actual_color != expected_color:
            all_passed = False
            
        print(f"{status} | {field:25} | Expected: {expected_color:12} | Actual: {actual_color or 'None':12}")
        if actual_color != expected_color:
            print(f"      Value: {new_value[:50]}...")
    
    print('-' * 60)
    if all_passed:
        print('🎉 All color tests PASSED!')
    else:
        print('⚠️  Some color tests FAILED - check logic above')
    
    # Test color definitions
    print('\n🎨 Color and Font Definitions:')
    print('-' * 30)
    
    color_mappings = {
        'security_risk': ('Light red background', 'Bright red bold text'),
        'new_data': ('Light green background', 'Dark green bold text'),
        'version_update': ('Light orange background', 'Bright orange bold text'),
        'updated': ('Light blue background', 'Bright blue bold text'),
        'github_added': ('Light purple background', 'Bright purple bold text'),
        'not_available': ('Red background', 'White bold text')
    }
    
    for color_type, (bg_desc, font_desc) in color_mappings.items():
        fill_color = handler.colors[color_type]
        font_color = handler.font_colors[color_type]
        print(f"{color_type:15} | {bg_desc:25} | {font_desc}")
        print(f"                | Fill: {fill_color.start_color} | Font: {font_color.color} (Bold: {font_color.bold})")

if __name__ == "__main__":
    test_color_logic()