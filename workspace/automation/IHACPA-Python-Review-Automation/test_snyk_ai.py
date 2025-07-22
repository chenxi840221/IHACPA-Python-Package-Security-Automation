#!/usr/bin/env python3
"""
Test script to verify SNYK AI integration
"""

import sys
import asyncio
sys.path.append('src')

from ai_cve_analyzer import AICVEAnalyzer
from vulnerability_scanner import VulnerabilityScanner

async def test_snyk_ai():
    """Test SNYK AI analysis functionality"""
    
    print('🔍 Testing SNYK AI Integration')
    print('=' * 50)
    
    # Test AI CVE Analyzer directly
    print('\n📋 Testing AI CVE Analyzer SNYK method...')
    analyzer = AICVEAnalyzer()
    
    if analyzer.is_enabled():
        print(f'✅ AI Analyzer enabled: {analyzer.model}')
        
        # Test SNYK analysis
        result = await analyzer.analyze_snyk_result(
            package_name='requests',
            current_version='2.25.0',
            snyk_lookup_url='https://security.snyk.io/vuln/pip/requests'
        )
        
        print(f'📝 SNYK AI Analysis Result:')
        print(f'   {result}')
        
        # Test another package
        result2 = await analyzer.analyze_snyk_result(
            package_name='aiohttp',
            current_version='3.8.0',
            snyk_lookup_url='https://security.snyk.io/vuln/pip/aiohttp'
        )
        
        print(f'📝 SNYK AI Analysis Result (aiohttp):')
        print(f'   {result2}')
        
    else:
        print('❌ AI analyzer not enabled')
        return
    
    # Test Vulnerability Scanner integration
    print('\n🔧 Testing Vulnerability Scanner SNYK integration...')
    scanner = VulnerabilityScanner()
    
    if scanner.ai_analyzer and scanner.ai_analyzer.is_enabled():
        print('✅ Scanner AI integration enabled')
        
        # Test SNYK scan with AI
        snyk_result = await scanner.scan_snyk('requests', '2.25.0')
        
        print(f'📊 SNYK Scanner Result:')
        print(f'   Database: {snyk_result.get("database")}')
        print(f'   Package: {snyk_result.get("package_name")} v{snyk_result.get("current_version")}')
        print(f'   URL: {snyk_result.get("search_url")}')
        print(f'   Summary: {snyk_result.get("summary", "No summary")[:100]}...')
        print(f'   AI Analysis: {snyk_result.get("ai_analysis", "No AI analysis")[:100]}...')
        
        await scanner.close()
    else:
        print('❌ Scanner AI integration not enabled')
    
    print('\n🎉 SNYK AI Integration Test Completed!')

if __name__ == "__main__":
    asyncio.run(test_snyk_ai())