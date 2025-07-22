#!/usr/bin/env python3
"""
Test script to verify PROCEED logic works for safe packages
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_proceed_logic():
    """Test that PROCEED logic works correctly"""
    
    print('🔍 Testing PROCEED Logic')
    print('=' * 50)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    # Test with simulated safe package results
    print('\n🧪 Testing with simulated safe package results:')
    
    # Create fake "safe" results
    fake_safe_results = {
        'scan_results': {
            'github_advisory': {
                'found_vulnerabilities': False,
                'vulnerability_count': 0,
                'summary': 'No published security advisories',
                'ai_analysis': 'GitHub Security Advisory Analysis: NOT_FOUND'
            },
            'nist_nvd': {
                'found_vulnerabilities': False,
                'vulnerability_count': 0,
                'summary': 'None found',
                'ai_analysis': 'No AI analysis available'
            },
            'mitre_cve': {
                'found_vulnerabilities': False,
                'vulnerability_count': 0,
                'summary': 'None found',
                'ai_analysis': 'CVE Analysis: NOT_FOUND'
            },
            'snyk': {
                'found_vulnerabilities': False,
                'vulnerability_count': 0,
                'summary': 'None found',
                'ai_analysis': 'SNYK Analysis: NOT_FOUND'
            },
            'exploit_db': {
                'found_vulnerabilities': False,
                'vulnerability_count': 0,
                'summary': 'None found',
                'ai_analysis': 'Exploit Database Analysis: NOT_FOUND'
            }
        }
    }
    
    # Test recommendation generation
    recommendation = scanner.generate_recommendations(
        'safe-package',
        '1.0.0',
        '1.0.0',  # Same version
        fake_safe_results
    )
    
    print(f'Generated Recommendation: "{recommendation}"')
    
    if recommendation == 'PROCEED':
        print('✅ Correct: Shows PROCEED for safe package')
    else:
        print('❌ Issue: Should show PROCEED but shows:', recommendation)
    
    # Test with version update but no security issues
    print('\n🧪 Testing with version update but no security issues:')
    
    recommendation_with_update = scanner.generate_recommendations(
        'safe-package',
        '1.0.0',
        '2.0.0',  # Different version
        fake_safe_results
    )
    
    print(f'Generated Recommendation (with version update): "{recommendation_with_update}"')
    
    if recommendation_with_update == 'PROCEED':
        print('✅ Correct: Shows PROCEED for safe package (ignores version updates)')
    else:
        print('❌ Issue: Should show PROCEED but shows:', recommendation_with_update)
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_proceed_logic())