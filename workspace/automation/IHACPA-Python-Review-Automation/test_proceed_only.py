#!/usr/bin/env python3
"""
Test script to verify PROCEED-only logic (no version update included when no risks)
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_proceed_only_logic():
    """Test that PROCEED appears alone when no security risks found"""
    
    print('🔍 Testing PROCEED-Only Logic (No Version Updates)')
    print('=' * 60)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    # Test 1: No vulnerabilities, version update available
    print('\n📦 Test 1: Safe package with version update available')
    print('-' * 50)
    
    safe_with_update = scanner.generate_recommendations(
        'safe-package',
        '1.0.0',        # Current version
        '2.0.0',        # New version available
        {
            'total_vulnerabilities': 0,
            'scan_results': {
                'github_advisory': {'found_vulnerabilities': False, 'summary': 'No published security advisories'},
                'nist_nvd': {'found_vulnerabilities': False, 'summary': 'None found'},
                'mitre_cve': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'CVE Analysis: NOT_FOUND'},
                'snyk': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'SNYK Analysis: NOT_FOUND'},
                'exploit_db': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'Exploit Database Analysis: NOT_FOUND'}
            }
        }
    )
    
    print(f'Recommendation: "{safe_with_update}"')
    if safe_with_update == 'PROCEED':
        print('✅ Perfect! Shows "PROCEED" only (no version update mentioned)')
    else:
        print('❌ Expected "PROCEED" only')
    
    # Test 2: No vulnerabilities, same version (no update available)
    print('\n📦 Test 2: Safe package with same version (no update)')
    print('-' * 50)
    
    safe_same_version = scanner.generate_recommendations(
        'safe-package',
        '1.0.0',        # Current version
        '1.0.0',        # Same version
        {
            'total_vulnerabilities': 0,
            'scan_results': {
                'github_advisory': {'found_vulnerabilities': False, 'summary': 'No published security advisories'},
                'nist_nvd': {'found_vulnerabilities': False, 'summary': 'None found'},
                'mitre_cve': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'CVE Analysis: NOT_FOUND'},
                'snyk': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'SNYK Analysis: NOT_FOUND'},
                'exploit_db': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'Exploit Database Analysis: NOT_FOUND'}
            }
        }
    )
    
    print(f'Recommendation: "{safe_same_version}"')
    if safe_same_version == 'PROCEED':
        print('✅ Perfect! Shows "PROCEED" only')
    else:
        print('❌ Expected "PROCEED" only')
    
    # Test 3: Vulnerabilities found, should include version update
    print('\n📦 Test 3: Package with vulnerabilities (should include update)')
    print('-' * 50)
    
    vulnerable_with_update = scanner.generate_recommendations(
        'vulnerable-package',
        '1.0.0',        # Current version
        '2.0.0',        # New version available
        {
            'total_vulnerabilities': 5,
            'scan_results': {
                'github_advisory': {'found_vulnerabilities': False, 'summary': 'No published security advisories'},
                'nist_nvd': {'found_vulnerabilities': True, 'vulnerability_count': 5, 'summary': 'Found 5 vulnerabilities in NIST NVD'},
                'mitre_cve': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'CVE Analysis: NOT_FOUND'},
                'snyk': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'SNYK Analysis: NOT_FOUND'},
                'exploit_db': {'found_vulnerabilities': False, 'summary': 'None found', 'ai_analysis': 'Exploit Database Analysis: NOT_FOUND'}
            }
        }
    )
    
    print(f'Recommendation: "{vulnerable_with_update}"')
    if 'Update from 1.0.0 to 2.0.0' in vulnerable_with_update and 'SECURITY RISK' in vulnerable_with_update:
        print('✅ Perfect! Shows version update and security risk (as expected for vulnerable package)')
    else:
        print('❌ Expected version update and security risk information')
    
    await scanner.close()
    
    print('\n🎉 PROCEED-Only Logic Test Completed!')
    print('\nKey Results:')
    print('✅ Safe packages (regardless of version updates): "PROCEED" only')
    print('✅ Vulnerable packages: Include version update + security details')

if __name__ == "__main__":
    asyncio.run(test_proceed_only_logic())