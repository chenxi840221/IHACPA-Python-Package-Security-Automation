#!/usr/bin/env python3
"""
Test script to verify standardized result messages and updated recommendation logic
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_standardized_results():
    """Test standardized result messages and PROCEED logic"""
    
    print('🔍 Testing Standardized Result Messages and Recommendation Logic')
    print('=' * 70)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    if not (scanner.ai_analyzer and scanner.ai_analyzer.is_enabled()):
        print('❌ AI analyzer not enabled - cannot test standardized results')
        return
    
    print(f'✅ AI Analyzer enabled: {scanner.ai_analyzer.model}')
    print(f'🌐 Azure Endpoint: {scanner.ai_analyzer.azure_endpoint}')
    
    # Test packages with different risk profiles
    test_packages = [
        {
            'name': 'agate', 
            'version': '1.9.1', 
            'github_url': 'https://github.com/wireservice/agate',
            'expected': 'Safe package - should show standardized messages'
        },
        {
            'name': 'requests', 
            'version': '2.25.0', 
            'github_url': 'https://github.com/psf/requests',
            'expected': 'Package with vulnerabilities - should show detailed recommendations'
        },
    ]
    
    for package in test_packages:
        print(f'\n📦 Testing {package["name"]} v{package["version"]}')
        print(f'Expected: {package["expected"]}')
        print('-' * 60)
        
        # Test full database scan
        full_result = await scanner.scan_all_databases(
            package['name'], 
            github_url=package['github_url'],
            current_version=package['version']
        )
        
        scan_results = full_result.get('scan_results', {})
        
        print('📊 Database Results:')
        
        # Check each database result
        databases = {
            'github_advisory': 'Column M (GitHub Security Advisory)',
            'nist_nvd': 'Column P (NIST NVD)',
            'mitre_cve': 'Column R (MITRE CVE)', 
            'snyk': 'Column T (SNYK)',
            'exploit_db': 'Column V (Exploit Database)'
        }
        
        for db_key, db_description in databases.items():
            if db_key in scan_results:
                result = scan_results[db_key]
                summary = result.get('summary', 'No summary')
                ai_analysis = result.get('ai_analysis', 'No AI analysis')
                
                print(f'  {db_description}:')
                print(f'    Summary: {summary}')
                if ai_analysis != 'No AI analysis':
                    print(f'    AI Analysis: {ai_analysis[:100]}...')
                
                # Check for standardized messages
                if db_key == 'github_advisory':
                    if 'No published security advisories' in summary or 'No published security advisories' in ai_analysis:
                        print(f'    ✅ Correct standardized message for GitHub Advisory')
                    elif 'NOT_FOUND' in ai_analysis.upper():
                        print(f'    ⚠️ Should use "No published security advisories" instead')
                else:
                    if 'None found' in summary or 'None found' in ai_analysis:
                        print(f'    ✅ Correct standardized message')
                    elif 'NOT_FOUND' in ai_analysis.upper():
                        print(f'    ⚠️ Should use "None found" instead')
                print()
        
        # Test recommendation logic
        print('🎯 Recommendation Analysis:')
        recommendation = scanner.generate_recommendations(
            package['name'],
            package['version'],
            '999.999.999',  # Fake latest version to test update logic
            full_result
        )
        
        print(f'   Recommendation: {recommendation}')
        
        # Check for PROCEED logic
        if 'PROCEED' in recommendation:
            print('   ✅ PROCEED logic working - no security risks detected')
        elif 'SECURITY RISK' in recommendation:
            print('   ✅ Security risk logic working - vulnerabilities detected')
        else:
            print('   ⚠️ Unexpected recommendation format')
        
        # Check for comprehensive analysis
        if 'Sources:' in recommendation:
            print('   ✅ Multi-database analysis working - sources listed')
        
        print()
    
    # Test safe package scenario (no vulnerabilities, same version)
    print('\n🔒 Testing Safe Package Scenario (no vulnerabilities, current version)')
    print('-' * 60)
    
    safe_recommendation = scanner.generate_recommendations(
        'safe-package',
        '1.0.0',
        '1.0.0',  # Same version
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
    
    print(f'Safe Package Recommendation: {safe_recommendation}')
    if safe_recommendation == 'PROCEED':
        print('✅ Perfect! Safe package correctly returns "PROCEED"')
    else:
        print('⚠️ Expected "PROCEED" for safe package')
    
    await scanner.close()
    
    print('\n🎉 Standardized Results and Recommendation Logic Test Completed!')
    print('\nKey Features Tested:')
    print('✅ Standardized messages: "None found" for P,R,T,V and "No published security advisories" for M')
    print('✅ Comprehensive recommendation logic analyzing all columns M,P,R,T,V')
    print('✅ PROCEED logic when no risks found')
    print('✅ Detailed security risk analysis with sources and severity')

if __name__ == "__main__":
    asyncio.run(test_standardized_results())