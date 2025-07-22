#!/usr/bin/env python3
"""
Test script for NIST NVD scanner issues
Tests problematic packages: lxml and tabulate
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner
import asyncio

async def test_nist_nvd_issues():
    """Test NIST NVD scanning with problematic packages"""
    scanner = VulnerabilityScanner()
    
    print("🧪 TESTING NIST NVD SCANNER ISSUES")
    print("=" * 80)
    print("Testing packages with known discrepancies")
    print()
    
    # Test cases with known issues
    test_cases = [
        {
            'package': 'lxml',
            'version': '4.9.3',
            'expected_website_records': 14,
            'current_result': 'None found',
            'issue': 'NIST NVD website shows 14 records, scanner shows None found'
        },
        {
            'package': 'tabulate',
            'version': '0.9.0', 
            'expected_website_records': 1,
            'current_result': 'None found',
            'issue': 'NIST NVD website shows 1 record, scanner shows None found'
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
            print(f"🔍 Testing current NIST NVD scanning for {package}...")
            result = await scanner.scan_nist_nvd(package, version)
            
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
                if vulnerability_count >= (test_case['expected_website_records'] * 0.5):
                    print("✅ REASONABLE: CVE count is in expected range")
                else:
                    print("⚠️  LOW: Scanner finding fewer CVEs than expected")
            else:
                print("❌ ISSUE PERSISTS: Still showing 'None found'")
                print("🔍 NEED TO INVESTIGATE: Search strategy or relevance filtering")
            
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
    
    print("🎯 NIST NVD TESTING SUMMARY")
    print("=" * 80)
    print("Expected Issues to Fix:")
    print("- lxml: Should find CVEs instead of 'None found'")
    print("- tabulate: Should find CVEs instead of 'None found'")
    print()
    print("Likely Root Causes (similar to MITRE CVE issues):")
    print("- Overly strict relevance filtering")
    print("- Missing known Python packages recognition")
    print("- Search strategy limitations")
    print("- Need for enhanced Python context detection")
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_nist_nvd_issues())