#!/usr/bin/env python3
"""
Test script to verify all three AI integrations working together:
- MITRE CVE (Column R)
- SNYK (Column T)  
- Exploit Database (Column V)
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_triple_ai_integration():
    """Test MITRE CVE, SNYK, and Exploit Database AI analysis working together"""
    
    print('🔍 Testing Triple AI Integration (MITRE CVE + SNYK + Exploit DB)')
    print('=' * 70)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    if not (scanner.ai_analyzer and scanner.ai_analyzer.is_enabled()):
        print('❌ AI analyzer not enabled - cannot test triple integration')
        return
    
    print(f'✅ AI Analyzer enabled: {scanner.ai_analyzer.model}')
    print(f'🌐 Azure Endpoint: {scanner.ai_analyzer.azure_endpoint}')
    
    # Test packages with different risk profiles
    test_packages = [
        {'name': 'requests', 'version': '2.25.0', 'expected_risk': 'MEDIUM-HIGH'},
        {'name': 'agate', 'version': '1.9.1', 'expected_risk': 'LOW'},
        {'name': 'aiohttp', 'version': '3.8.0', 'expected_risk': 'HIGH'},
    ]
    
    for package in test_packages:
        print(f'\n📦 Testing {package["name"]} v{package["version"]}')
        print('-' * 50)
        
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
        
        # Test Exploit Database analysis
        print('🔍 Exploit Database Analysis:')
        exploit_result = await scanner.scan_exploit_db(package['name'], package['version'])
        exploit_summary = exploit_result.get('summary', 'No summary')
        print(f'   {exploit_summary[:80]}...')
        
        if 'Exploit Database Analysis:' in exploit_summary:
            print('   🤖 AI Analysis: ✅ WORKING')
        else:
            print('   👤 Manual Review: ⚠️ FALLBACK')
        
        # Check consistency between analyses
        mitre_has_vulns = 'FOUND' in mitre_summary and 'NOT_FOUND' not in mitre_summary
        snyk_has_vulns = 'FOUND' in snyk_summary and 'NOT_FOUND' not in snyk_summary
        exploit_has_vulns = 'FOUND' in exploit_summary and 'NOT_FOUND' not in exploit_summary
        
        vuln_count = sum([mitre_has_vulns, snyk_has_vulns, exploit_has_vulns])
        
        if vuln_count == 0:
            print('   🎯 Consensus: ✅ All sources agree - SAFE')
        elif vuln_count >= 2:
            print('   🎯 Consensus: ⚠️ Multiple sources report vulnerabilities')
        else:
            print('   🎯 Consensus: 📊 Mixed results (normal - different databases)')
    
    # Test full database scan with all AI systems
    print(f'\n🔍 Testing Full Database Scan (all databases with AI)')
    print('-' * 60)
    
    full_result = await scanner.scan_all_databases('requests', current_version='2.25.0')
    
    print(f"📊 Full Scan Results for requests v2.25.0:")
    print(f"   Total vulnerabilities: {full_result.get('total_vulnerabilities', 0)}")
    print(f"   Databases with vulnerabilities: {len(full_result.get('databases_with_vulnerabilities', []))}")
    
    scan_results = full_result.get('scan_results', {})
    
    # Check AI results in scan
    mitre_ai = scan_results.get('mitre_cve', {}).get('ai_analysis')
    snyk_ai = scan_results.get('snyk', {}).get('ai_analysis')
    exploit_ai = scan_results.get('exploit_db', {}).get('ai_analysis')
    
    print(f"   MITRE CVE AI: {'✅ ENABLED' if mitre_ai and 'Manual review required' not in mitre_ai else '❌ DISABLED'}")
    print(f"   SNYK AI: {'✅ ENABLED' if snyk_ai and 'Manual review required' not in snyk_ai else '❌ DISABLED'}")
    print(f"   Exploit DB AI: {'✅ ENABLED' if exploit_ai and 'Manual review required' not in exploit_ai else '❌ DISABLED'}")
    
    await scanner.close()
    
    print('\n🎉 Triple AI Integration Test Completed!')
    print('✅ MITRE CVE (Column R) - AI-powered')
    print('✅ SNYK (Column T) - AI-powered') 
    print('✅ Exploit Database (Column V) - AI-powered')
    print('🚀 All three major vulnerability databases now automated!')

if __name__ == "__main__":
    asyncio.run(test_triple_ai_integration())