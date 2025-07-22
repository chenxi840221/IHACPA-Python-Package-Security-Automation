#!/usr/bin/env python3
"""
Debug script to test xlwt vulnerability detection
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def debug_xlwt_detection():
    """Debug xlwt vulnerability detection logic"""
    
    print('🔍 Debugging xlwt Vulnerability Detection')
    print('=' * 50)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    # Test xlwt package
    print('\n📦 Testing xlwt package')
    print('-' * 30)
    
    full_result = await scanner.scan_all_databases(
        'xlwt', 
        current_version='1.3.0'
    )
    
    scan_results = full_result.get('scan_results', {})
    
    print('📊 Raw Database Results:')
    
    # Check each database result
    for db_name, result in scan_results.items():
        print(f'\n{db_name.upper()}:')
        print(f'  found_vulnerabilities: {result.get("found_vulnerabilities", False)}')
        print(f'  vulnerability_count: {result.get("vulnerability_count", 0)}')
        print(f'  summary: {result.get("summary", "No summary")[:100]}...')
        
        ai_analysis = result.get('ai_analysis', 'No AI analysis')
        if ai_analysis != 'No AI analysis':
            print(f'  ai_analysis: {ai_analysis[:150]}...')
        
        # Test our detection logic manually
        summary = result.get('summary', '').lower()
        ai_analysis_lower = ai_analysis.lower() if ai_analysis != 'No AI analysis' else ''
        
        vulnerability_found = False
        
        # Check explicit found_vulnerabilities flag
        if result.get('found_vulnerabilities', False):
            vulnerability_found = True
            print(f'  ✅ DETECTED via found_vulnerabilities flag')
        
        # Check for actual vulnerability count > 0
        elif result.get('vulnerability_count', 0) > 0:
            vulnerability_found = True
            print(f'  ✅ DETECTED via vulnerability_count > 0')
        
        # Check AI analysis for explicit FOUND indication (but not NOT_FOUND)
        elif ai_analysis_lower and ': found' in ai_analysis_lower and 'not_found' not in ai_analysis_lower:
            vulnerability_found = True
            print(f'  ✅ DETECTED via AI analysis ": found" pattern')
        
        # Check summary for vulnerability counts
        elif 'found' in summary and 'vulnerabilities' in summary and 'none found' not in summary and 'no published' not in summary:
            vulnerability_found = True
            print(f'  ✅ DETECTED via summary vulnerability pattern')
        
        if not vulnerability_found:
            print(f'  ❌ NOT DETECTED - no patterns matched')
            print(f'  Debug: ": found" in ai_analysis? {"Yes" if ": found" in ai_analysis_lower else "No"}')
            print(f'  Debug: "not_found" in ai_analysis? {"Yes" if "not_found" in ai_analysis_lower else "No"}')
    
    # Test recommendation logic
    print(f'\n🎯 Recommendation Logic:')
    recommendation = scanner.generate_recommendations(
        'xlwt',
        '1.3.0',
        '1.3.0',  # Same version
        full_result
    )
    
    print(f'Generated Recommendation: "{recommendation}"')
    
    if recommendation == 'PROCEED':
        print('❌ BUG: Should not be PROCEED with HIGH severity vulnerabilities!')
    else:
        print('✅ Correct: Shows security risk information')
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(debug_xlwt_detection())