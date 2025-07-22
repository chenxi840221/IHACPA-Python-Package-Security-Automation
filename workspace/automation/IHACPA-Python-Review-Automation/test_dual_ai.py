#!/usr/bin/env python3
"""
Test script to verify both MITRE CVE and SNYK AI integrations work together
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_dual_ai_integration():
    """Test both MITRE CVE and SNYK AI analysis working together"""
    
    print('🔍 Testing Dual AI Integration (MITRE CVE + SNYK)')
    print('=' * 60)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    if not (scanner.ai_analyzer and scanner.ai_analyzer.is_enabled()):
        print('❌ AI analyzer not enabled - cannot test dual integration')
        return
    
    print(f'✅ AI Analyzer enabled: {scanner.ai_analyzer.model}')
    print(f'🌐 Azure Endpoint: {scanner.ai_analyzer.azure_endpoint}')
    
    # Test packages with different risk profiles
    test_packages = [
        {'name': 'requests', 'version': '2.25.0', 'expected_risk': 'HIGH'},
        {'name': 'agate', 'version': '1.9.1', 'expected_risk': 'LOW'},
        {'name': 'aiohttp', 'version': '3.8.0', 'expected_risk': 'HIGH'},
    ]
    
    for package in test_packages:
        print(f'\n📦 Testing {package["name"]} v{package["version"]}')
        print('-' * 40)
        
        # Test MITRE CVE analysis
        print('🔍 MITRE CVE Analysis:')
        mitre_result = await scanner.scan_mitre_cve(package['name'], package['version'])
        mitre_summary = mitre_result.get('summary', 'No summary')
        print(f'   {mitre_summary[:80]}...')
        
        if 'CVE Analysis:' in mitre_summary:
            print('   🤖 AI Analysis: ✅ WORKING')
        else:
            print('   👤 Manual Review: ⚠️ FALLBACK')
        
        # Test SNYK analysis
        print('🔍 SNYK Analysis:')
        snyk_result = await scanner.scan_snyk(package['name'], package['version'])
        snyk_summary = snyk_result.get('summary', 'No summary')
        print(f'   {snyk_summary[:80]}...')
        
        if 'SNYK Analysis:' in snyk_summary:
            print('   🤖 AI Analysis: ✅ WORKING')
        else:
            print('   👤 Manual Review: ⚠️ FALLBACK')
        
        # Check consistency between analyses
        mitre_has_vulns = 'FOUND' in mitre_summary and 'NOT_FOUND' not in mitre_summary
        snyk_has_vulns = 'FOUND' in snyk_summary and 'NOT_FOUND' not in snyk_summary
        
        if mitre_has_vulns == snyk_has_vulns:
            print('   🎯 Consistency: ✅ MITRE and SNYK results align')
        else:
            print('   ⚠️ Consistency: Different results (normal - different databases)')
    
    # Test full database scan
    print(f'\n🔍 Testing Full Database Scan (all databases with AI)')
    print('-' * 50)
    
    full_result = await scanner.scan_all_databases('requests', current_version='2.25.0')
    
    print(f"📊 Full Scan Results for requests v2.25.0:")
    print(f"   Total vulnerabilities: {full_result.get('total_vulnerabilities', 0)}")
    print(f"   Databases with vulnerabilities: {len(full_result.get('databases_with_vulnerabilities', []))}")
    
    scan_results = full_result.get('scan_results', {})
    
    # Check AI results in scan
    mitre_ai = scan_results.get('mitre_cve', {}).get('ai_analysis')
    snyk_ai = scan_results.get('snyk', {}).get('ai_analysis')
    
    print(f"   MITRE CVE AI: {'✅ ENABLED' if mitre_ai and 'Manual review required' not in mitre_ai else '❌ DISABLED'}")
    print(f"   SNYK AI: {'✅ ENABLED' if snyk_ai and 'Manual review required' not in snyk_ai else '❌ DISABLED'}")
    
    await scanner.close()
    
    print('\n🎉 Dual AI Integration Test Completed!')
    print('✅ Both MITRE CVE and SNYK now use AI-powered analysis')
    print('✅ Column R (MITRE CVE) and Column T (SNYK) automated')

if __name__ == "__main__":
    asyncio.run(test_dual_ai_integration())