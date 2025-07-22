#!/usr/bin/env python3
"""
Analyze which fields are getting green (NEW_DATA) color and why
"""

import sys
sys.path.append('src')

from excel_handler import ExcelHandler

def analyze_green_usage():
    """Analyze which fields get green color and in what scenarios"""
    
    print('🔍 Analyzing Green (NEW_DATA) Color Usage')
    print('=' * 60)
    
    # Create Excel handler instance
    handler = ExcelHandler("dummy.xlsx")
    
    # Test different field types with various values
    fields_to_test = [
        # Security fields with safe results
        ('github_advisory_result', 'No published security advisories'),
        ('snyk_result', 'None found'),
        ('mitre_cve_result', 'CVE Analysis: NOT_FOUND'),
        ('exploit_db_result', 'Exploit Database Analysis: NOT_FOUND'),
        ('nist_nvd_result', 'None found'),
        
        # Recommendation field with safe result
        ('recommendation', 'PROCEED'),
        
        # URL fields (these also get green)
        ('pypi_latest_link', 'https://pypi.org/project/package/1.0.0/'),
        ('nist_nvd_url', 'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=package'),
        ('mitre_cve_url', 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=package'),
        ('snyk_url', 'https://security.snyk.io/vuln/pip/package'),
        ('exploit_db_url', 'https://www.exploit-db.com/search?text=package'),
        
        # GitHub fields (should be purple, not green)
        ('github_url', 'https://github.com/user/repo'),
        ('github_advisory_url', 'https://github.com/user/repo/security/advisories'),
        
        # Version fields (should be orange)
        ('latest_version', '2.1.0'),
        ('date_published', '2023-01-01'),
        
        # Other fields (should be blue)
        ('requires', 'requests>=2.25.0'),
        ('development_status', '5 - Production/Stable'),
    ]
    
    green_fields = []
    other_colors = {'security_risk': [], 'version_update': [], 'updated': [], 'github_added': []}
    
    print('Field Analysis:')
    print('-' * 60)
    
    for field, value in fields_to_test:
        color = handler._determine_color_type(field, value, None)
        
        if color == 'new_data':
            green_fields.append((field, value))
            print(f"🟢 GREEN    | {field:25} | {value[:50]}...")
        elif color in other_colors:
            other_colors[color].append((field, value))
            color_emoji = {'security_risk': '🔴', 'version_update': '🟠', 'updated': '🔵', 'github_added': '🟣'}
            print(f"{color_emoji.get(color, '⚪')} {color.upper():10} | {field:25} | {value[:50]}...")
    
    print('\n' + '=' * 60)
    print('🔍 ANALYSIS RESULTS:')
    print('=' * 60)
    
    print(f'\n🟢 GREEN (NEW_DATA) - {len(green_fields)} fields:')
    print('Used for:')
    
    # Categorize green usage
    safe_security_results = []
    url_fields = []
    safe_recommendations = []
    
    for field, value in green_fields:
        if field in ['github_advisory_result', 'snyk_result', 'mitre_cve_result', 'exploit_db_result', 'nist_nvd_result']:
            safe_security_results.append(field)
        elif field == 'recommendation' and 'proceed' in value.lower():
            safe_recommendations.append(field)
        elif 'url' in field or 'link' in field:
            url_fields.append(field)
    
    if safe_security_results:
        print(f'  • Safe security results ({len(safe_security_results)}): {", ".join(safe_security_results)}')
    if safe_recommendations:
        print(f'  • Safe recommendations ({len(safe_recommendations)}): PROCEED')
    if url_fields:
        print(f'  • URL fields ({len(url_fields)}): {", ".join(url_fields)}')
    
    print('\n🤔 POTENTIAL ISSUES:')
    print('-' * 30)
    
    if url_fields and safe_security_results:
        print('⚠️  SEMANTIC CONFUSION: Green is used for two different meanings:')
        print('   1. "Safe/No Risk" (security results, PROCEED recommendations)')
        print('   2. "New URLs Added" (pypi_latest_link, nist_nvd_url, etc.)')
        print('   This creates ambiguity - green means both "safe" and "new URL"')
        
    print('\n💡 RECOMMENDATIONS:')
    print('-' * 20)
    print('Consider splitting green into two distinct colors:')
    print('🟢 SAFE_RESULT: Security results with no vulnerabilities, PROCEED recommendations')
    print('🔗 URL_ADDED: New URLs and links added to the spreadsheet')
    print('This would make the color coding more semantically clear.')

if __name__ == "__main__":
    analyze_green_usage()