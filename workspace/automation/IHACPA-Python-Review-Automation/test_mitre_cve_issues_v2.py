#!/usr/bin/env python3
"""
Test script for additional MITRE CVE scanner issues
Tests problematic packages: mistune, paramiko, Pillow, PyJWT
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner
import asyncio

async def test_mitre_cve_issues():
    """Test MITRE CVE scanning with newly reported problematic packages"""
    scanner = VulnerabilityScanner()
    
    print("🧪 TESTING ADDITIONAL MITRE CVE SCANNER ISSUES")
    print("=" * 80)
    print("Testing packages with known discrepancies")
    print()
    
    # Test cases with known issues
    test_cases = [
        {
            'package': 'mistune',
            'version': '2.0.5',
            'expected_website_records': 3,
            'current_result': 'None found',
            'issue': 'MITRE website shows 3 records, scanner shows None found'
        },
        {
            'package': 'paramiko',
            'version': '3.1.0',
            'expected_website_records': 5,
            'current_result': 'None found',
            'issue': 'MITRE website shows 5 records, scanner shows None found'
        },
        {
            'package': 'Pillow',
            'version': '9.4.0',
            'expected_website_records': 55,
            'current_result': 'SAFE - 9 MITRE CVEs found',
            'issue': 'MITRE website shows 55 records, scanner shows only 9 CVEs'
        },
        {
            'package': 'PyJWT',
            'version': '2.4.0',
            'expected_website_records': 3,
            'current_result': 'VULNERABLE - 1 MITRE CVEs affect',
            'issue': 'MITRE website shows 3 records, scanner shows only 1 CVE'
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
            print(f"🔍 Testing current MITRE CVE scanning for {package}...")
            result = await scanner.scan_mitre_cve(package, version)
            
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
                for j, vuln in enumerate(vulnerabilities[:5], 1):  # Show first 5
                    cve_id = vuln.get('cve_id', 'Unknown')
                    severity = vuln.get('severity', 'Unknown')
                    version_affected = vuln.get('version_affected', False)
                    description = vuln.get('description', '')[:100] + '...'
                    
                    print(f"  {j}. {cve_id} - {severity}")
                    print(f"     Version Affected: {version_affected}")
                    print(f"     Description: {description}")
                
                if len(vulnerabilities) > 5:
                    print(f"     ... and {len(vulnerabilities) - 5} more CVEs")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print()
        print("=" * 80)
        print()
    
    print("🎯 MITRE CVE TESTING SUMMARY")
    print("=" * 80)
    print("Issues to Fix:")
    print("- mistune: Should find ~3 CVEs instead of 'None found'")
    print("- paramiko: Should find ~5 CVEs instead of 'None found'")
    print("- Pillow: Should find ~55 CVEs instead of just 9")
    print("- PyJWT: Should find ~3 CVEs instead of just 1")
    print()
    print("Likely Root Causes:")
    print("- Search terms may not be comprehensive enough")
    print("- Filtering might be too restrictive for these packages")
    print("- Some packages might need special handling")
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_mitre_cve_issues())