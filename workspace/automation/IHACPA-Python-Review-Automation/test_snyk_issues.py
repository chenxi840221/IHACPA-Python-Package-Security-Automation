#!/usr/bin/env python3
"""
Test script for SNYK vulnerability scanner issues
Tests problematic packages: cffi
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner
import asyncio

async def test_snyk_issues():
    """Test SNYK vulnerability scanning with problematic packages"""
    scanner = VulnerabilityScanner()
    
    print("🧪 TESTING SNYK VULNERABILITY SCANNER ISSUES")
    print("=" * 80)
    print("Testing packages with known discrepancies")
    print()
    
    # Test cases with known issues
    test_cases = [
        {
            'package': 'cffi',
            'version': '1.16.0',
            'expected_website_records': 1,
            'current_result': 'None found',
            'issue': 'SNYK website shows 1 record, scanner shows None found'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        package = test_case['package']
        version = test_case['version']
        
        print(f"📊 TEST CASE {i}: {package} v{version}")
        print("-" * 70)
        print(f"💡 Issue: {test_case['issue']}")
        print(f"🌐 Expected Website Records: {test_case['expected_website_records']}")
        print(f"🔧 Current Scanner Result: {test_case['current_result']}")
        print()
        
        try:
            print(f"🔍 Testing current SNYK scanning for {package}...")
            result = await scanner.scan_snyk(package, version)
            
            # Extract key information
            found_vulnerabilities = result.get('found_vulnerabilities', False)
            vulnerability_count = result.get('vulnerability_count', 0)
            summary = result.get('summary', 'No summary available')
            search_url = result.get('search_url', '')
            
            print(f"✓ Search URL: {search_url}")
            print(f"✓ Vulnerabilities Found: {found_vulnerabilities}")
            print(f"✓ CVE Count: {vulnerability_count}")
            print(f"✓ Summary: {summary}")
            
            # Analysis
            print()
            print("📈 ANALYSIS:")
            
            if vulnerability_count > 0:
                print(f"✅ FOUND CVEs: {vulnerability_count} CVEs detected")
                print(f"🎯 Expected ~{test_case['expected_website_records']} records from website")
                
                ratio = vulnerability_count / test_case['expected_website_records']
                if ratio >= 0.8:
                    print("✅ GOOD: Finding most CVEs")
                elif ratio >= 0.5:
                    print("⚠️  MODERATE: Finding some but missing many CVEs")
                else:
                    print("❌ POOR: Missing most CVEs")
                    
            else:
                print("❌ ISSUE CONFIRMED: Still showing 'None found'")
                print("🔍 NEED TO INVESTIGATE: Search strategy or filtering may be too restrictive")
            
            # Show individual CVEs if found
            if vulnerability_count > 0:
                vulnerabilities = result.get('vulnerabilities', [])
                print()
                print(f"🔍 FOUND CVEs ({len(vulnerabilities)}):")
                for j, vuln in enumerate(vulnerabilities[:3], 1):  # Show first 3
                    cve_id = vuln.get('cve_id', vuln.get('vulnerability_id', 'Unknown'))
                    severity = vuln.get('severity', 'Unknown')
                    version_affected = vuln.get('version_affected', False)
                    description = vuln.get('description', '')[:100] + '...'
                    
                    print(f"  {j}. {cve_id} - {severity}")
                    print(f"     Version Affected: {version_affected}")
                    print(f"     Description: {description}")
                
                if len(vulnerabilities) > 3:
                    print(f"     ... and {len(vulnerabilities) - 3} more CVEs")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print()
        print("=" * 80)
        print()
    
    print("🎯 SNYK TESTING SUMMARY")
    print("=" * 80)
    print("Issues to Fix:")
    print("- cffi: Should find ~1 CVE instead of 'None found'")
    print()
    print("Likely Root Causes:")
    print("- SNYK web scraping may not be working correctly")
    print("- Package name matching issues")
    print("- Filtering might be too restrictive")
    print("- HTML parsing issues with SNYK website")
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_snyk_issues())