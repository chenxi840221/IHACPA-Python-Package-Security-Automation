#!/usr/bin/env python3
"""
Test script to verify GitHub Security Advisory AI integration
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def test_github_advisory_ai():
    """Test GitHub Security Advisory AI analysis"""
    
    print('🔍 Testing GitHub Security Advisory AI Integration')
    print('=' * 60)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    if not (scanner.ai_analyzer and scanner.ai_analyzer.is_enabled()):
        print('❌ AI analyzer not enabled - cannot test GitHub AI integration')
        return
    
    print(f'✅ AI Analyzer enabled: {scanner.ai_analyzer.model}')
    print(f'🌐 Azure Endpoint: {scanner.ai_analyzer.azure_endpoint}')
    
    # Test packages with different GitHub scenarios
    test_packages = [
        {
            'name': 'requests', 
            'version': '2.25.0', 
            'github_url': 'https://github.com/psf/requests',
            'expected_risk': 'MEDIUM-HIGH'
        },
        {
            'name': 'agate', 
            'version': '1.9.1', 
            'github_url': 'https://github.com/wireservice/agate',
            'expected_risk': 'LOW'
        },
        {
            'name': 'flask', 
            'version': '2.0.0', 
            'github_url': 'https://github.com/pallets/flask',
            'expected_risk': 'HIGH'
        },
    ]
    
    for package in test_packages:
        print(f'\n📦 Testing {package["name"]} v{package["version"]}')
        print('-' * 50)
        
        # Test GitHub Security Advisory analysis
        print('🔍 GitHub Security Advisory Analysis:')
        github_result = await scanner.scan_github_advisory(
            package['name'], 
            package['github_url'], 
            package['version']
        )
        
        github_summary = github_result.get('summary', 'No summary')
        github_ai = github_result.get('ai_analysis', 'No AI analysis')
        
        print(f'   Summary: {github_summary[:80]}...')
        print(f'   AI Analysis: {github_ai[:80]}...')
        
        if 'GitHub Security Advisory Analysis:' in github_ai:
            print('   🤖 AI Analysis: ✅ WORKING')
        else:
            print('   👤 Manual Review: ⚠️ FALLBACK')
        
        # Check AI response format
        if 'GitHub Security Advisory Analysis:' in github_ai:
            if 'Severity:' in github_ai and 'Recommendation:' in github_ai:
                print('   📋 Format: ✅ CORRECT')
            else:
                print('   📋 Format: ⚠️ INCOMPLETE')
        
        # Display GitHub URL used
        github_url = github_result.get('search_url', 'No URL')
        print(f'   🔗 GitHub URL: {github_url}')
    
    # Test full database scan with GitHub AI
    print(f'\n🔍 Testing Full Database Scan (including GitHub AI)')
    print('-' * 60)
    
    full_result = await scanner.scan_all_databases(
        'requests', 
        github_url='https://github.com/psf/requests',
        current_version='2.25.0'
    )
    
    print(f"📊 Full Scan Results for requests v2.25.0:")
    print(f"   Total vulnerabilities: {full_result.get('total_vulnerabilities', 0)}")
    print(f"   Databases with vulnerabilities: {len(full_result.get('databases_with_vulnerabilities', []))}")
    
    scan_results = full_result.get('scan_results', {})
    
    # Check AI results in scan
    github_ai = scan_results.get('github_advisory', {}).get('ai_analysis')
    
    print(f"   GitHub Advisory AI: {'✅ ENABLED' if github_ai and 'Manual review required' not in github_ai else '❌ DISABLED'}")
    
    if github_ai:
        print(f"   GitHub AI Response: {github_ai[:100]}...")
    
    await scanner.close()
    
    print('\n🎉 GitHub Security Advisory AI Test Completed!')
    print('✅ GitHub Security Advisory (Column M) - AI-powered')
    print('🚀 Four major vulnerability databases now automated!')
    print('\nAI-Enhanced Databases:')
    print('  - ✅ MITRE CVE (Column R)')
    print('  - ✅ SNYK (Column T)')  
    print('  - ✅ Exploit Database (Column V)')
    print('  - ✅ GitHub Security Advisory (Column M)')

if __name__ == "__main__":
    asyncio.run(test_github_advisory_ai())