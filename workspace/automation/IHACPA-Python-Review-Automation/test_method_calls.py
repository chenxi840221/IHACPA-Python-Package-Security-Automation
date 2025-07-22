#!/usr/bin/env python3
"""
Test actual method calls used by MITRE CVE scanner
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def test_actual_method_call():
    scanner = VulnerabilityScanner()
    
    # Get the actual CVE data from the scanner
    enhanced_data = await scanner._get_enhanced_mitre_cve_data('PyJWT')
    
    # Find CVE-2024-53861
    target_cve = None
    for cve in enhanced_data:
        if cve.get('cve_id') == 'CVE-2024-53861':
            target_cve = cve
            break
    
    if target_cve:
        print('Testing actual method calls:')
        print(f"CVE: {target_cve.get('cve_id')}")
        print(f"Description: {target_cve.get('description', '')[:100]}...")
        print()
        
        # Test the method that MITRE CVE scanner actually calls
        result1 = scanner._is_mitre_cve_relevant('PyJWT', target_cve)
        print(f'_is_mitre_cve_relevant: {result1}')
        
        # Test the enhanced method directly
        result2 = scanner._is_mitre_cve_relevant_enhanced('PyJWT', target_cve)
        print(f'_is_mitre_cve_relevant_enhanced: {result2}')
        
        if result1 != result2:
            print('🚨 METHODS DISAGREE!')
        else:
            print('✅ Methods agree')
            
        print(f'Final result should be: {result1}')
    else:
        print('CVE not found')
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_actual_method_call())