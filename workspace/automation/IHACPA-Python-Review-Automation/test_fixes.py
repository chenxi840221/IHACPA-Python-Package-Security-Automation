#!/usr/bin/env python3
"""
Test the fixes for database scanner separation
Focus on the most critical issues mentioned by the user
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# Test the most critical cases from user feedback
CRITICAL_TEST_CASES = [
    # NIST NVD critical issues
    ('pywin32', '306', 'NIST NVD', 'Expected 1 CVE but found 0'),
    ('tables', '3.8.0', 'NIST NVD', 'Expected ~392 but found 23'),
    
    # SNYK critical issues  
    ('cffi', '1.15.1', 'SNYK', 'Expected 1 vulnerability but found 0'),
    
    # MITRE CVE verification (should already be working)
    ('paramiko', '3.1.0', 'MITRE CVE', 'Should find 5 CVEs'),
]

async def test_fixes():
    """Test the critical fixes"""
    print("=== TESTING CRITICAL FIXES ===")
    scanner = VulnerabilityScanner()
    
    try:
        for package_name, version, database, expected in CRITICAL_TEST_CASES:
            print(f"\n{'='*60}")
            print(f"Testing: {package_name} v{version} ({database})")
            print(f"Expected: {expected}")
            print('='*60)
            
            if database == 'NIST NVD':
                result = await scanner.scan_nist_nvd(package_name, version)
            elif database == 'MITRE CVE':
                result = await scanner.scan_mitre_cve(package_name, version)
            elif database == 'SNYK':
                result = await scanner.scan_snyk(package_name, version)
            else:
                continue
                
            # Print results
            print(f"{database} Results:")
            print(f"  Found vulnerabilities: {result.get('found_vulnerabilities', False)}")
            print(f"  Vulnerability count: {result.get('vulnerability_count', 0)}")
            print(f"  Summary: {result.get('summary', 'N/A')}")
            
            # Show first few vulnerabilities
            vulnerabilities = result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"  First 3 vulnerabilities:")
                for i, vuln in enumerate(vulnerabilities[:3]):
                    print(f"    {i+1}. {vuln.get('cve_id', vuln.get('id', 'No ID'))}: {vuln.get('title', vuln.get('description', 'No description'))[:80]}...")
            
            # Status check
            actual_count = result.get('vulnerability_count', 0)
            if package_name == 'pywin32' and actual_count > 0:
                print(f"  ✅ FIXED: pywin32 now finds {actual_count} vulnerabilities (was 0)")
            elif package_name == 'tables' and actual_count > 23:
                print(f"  ✅ IMPROVED: tables now finds {actual_count} vulnerabilities (was 23)")
            elif package_name == 'cffi' and actual_count > 0:
                print(f"  ✅ FIXED: cffi now finds {actual_count} vulnerabilities (was 0)")
            elif package_name == 'paramiko' and actual_count >= 5:
                print(f"  ✅ WORKING: paramiko finds {actual_count} vulnerabilities as expected")
            elif actual_count == 0:
                print(f"  ❌ STILL BROKEN: {package_name} finds 0 vulnerabilities")
            else:
                print(f"  ⚠️  PARTIAL: {package_name} finds {actual_count} vulnerabilities")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_fixes())