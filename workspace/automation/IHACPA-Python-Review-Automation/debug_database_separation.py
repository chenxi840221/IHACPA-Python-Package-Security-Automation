#!/usr/bin/env python3
"""
Debug script to test individual database scanners and identify cross-contamination issues
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# Test cases mentioned by the user
TEST_CASES = [
    # NIST NVD issues
    ('PyJWT', '2.8.0', 'NIST NVD', 'has 3 CVE Records but our result is "None found"'),
    ('pywin32', '306', 'NIST NVD', 'has 1 CVE Record but our result is "None found"'),
    ('tables', '3.8.0', 'NIST NVD', 'has 392 matching records but our result is "SAFE"'),
    ('transformers', '2.1.1', 'NIST NVD', 'has 9 matching records but our result is "SAFE"'),
    ('tornado', '6.2', 'NIST NVD', 'has 14 matching records but our result is "SAFE"'),
    
    # MITRE CVE issues
    ('paramiko', '3.1.0', 'MITRE CVE', 'has 5 CVE Records but our result is "None found"'),
    ('Pillow', '9.4.0', 'MITRE CVE', 'has 55 CVE Records but our result is "SAFE"'),
    ('PyJWT', '2.8.0', 'MITRE CVE', 'has 3 matching records but our result is "None found"'),
    
    # SNYK issues
    ('cffi', '1.15.1', 'SNYK', 'has 1 VULNERABILITY Record but our result is "None found"'),
]

async def test_individual_databases():
    """Test each database scanner individually"""
    print("=== DEBUGGING INDIVIDUAL DATABASE SCANNERS ===")
    scanner = VulnerabilityScanner()
    
    try:
        for package_name, version, database, issue_description in TEST_CASES:
            print(f"\n{'='*80}")
            print(f"Testing: {package_name} v{version} ({database})")
            print(f"Issue: {issue_description}")
            print('='*80)
            
            if database == 'NIST NVD':
                result = await scanner.scan_nist_nvd(package_name, version)
            elif database == 'MITRE CVE':
                result = await scanner.scan_mitre_cve(package_name, version)
            elif database == 'SNYK':
                result = await scanner.scan_snyk(package_name, version)
            else:
                continue
                
            # Print detailed results
            print(f"\n{database} Results for {package_name}:")
            print(f"  Search URL: {result.get('search_url', 'N/A')}")
            print(f"  Found vulnerabilities: {result.get('found_vulnerabilities', False)}")
            print(f"  Vulnerability count: {result.get('vulnerability_count', 0)}")
            print(f"  Summary: {result.get('summary', 'N/A')}")
            
            # Show first few vulnerabilities if any
            vulnerabilities = result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"  First 3 vulnerabilities:")
                for i, vuln in enumerate(vulnerabilities[:3]):
                    print(f"    {i+1}. {vuln.get('cve_id', 'No ID')}: {vuln.get('title', vuln.get('description', 'No description'))[:100]}...")
            else:
                print(f"  ❌ No vulnerabilities found by our scanner")
                
            # Check if result makes sense
            expected_count = 0
            if 'has 3 CVE Records' in issue_description:
                expected_count = 3
            elif 'has 1 CVE Record' in issue_description:
                expected_count = 1
            elif 'has 5 CVE Records' in issue_description:
                expected_count = 5
            elif 'has 55 CVE Records' in issue_description:
                expected_count = 55
            elif 'has 392 matching records' in issue_description:
                expected_count = 392
            elif 'has 9 matching records' in issue_description:
                expected_count = 9
            elif 'has 14 matching records' in issue_description:
                expected_count = 14
            elif 'has 1 VULNERABILITY Record' in issue_description:
                expected_count = 1
                
            actual_count = result.get('vulnerability_count', 0)
            if expected_count > 0:
                if actual_count == 0:
                    print(f"  🚨 ISSUE CONFIRMED: Expected ~{expected_count} but found {actual_count}")
                elif actual_count < expected_count / 2:  # Less than half expected
                    print(f"  ⚠️  POTENTIAL ISSUE: Expected ~{expected_count} but found {actual_count}")
                else:
                    print(f"  ✅ LOOKS OK: Expected ~{expected_count}, found {actual_count}")
                    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_individual_databases())