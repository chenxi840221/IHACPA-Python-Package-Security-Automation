#!/usr/bin/env python3
"""
Debug script for MITRE CVE issues
Testing paramiko, Pillow, PyJWT packages
"""

import sys
import os
import asyncio
import json
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# Test packages with known issues
TEST_PACKAGES = [
    ('paramiko', '3.1.0'),      # Shows None found vs 5 CVEs
    ('Pillow', '9.4.0'),        # Shows 9 vs 55 CVEs  
    ('PyJWT', '2.8.0')          # Shows None found vs 3 CVEs
]

async def debug_mitre_scanner():
    """Debug our MITRE CVE scanner for specific packages"""
    print("=== DEBUGGING MITRE CVE SCANNER ISSUES ===")
    scanner = VulnerabilityScanner()
    
    try:
        for package_name, version in TEST_PACKAGES:
            print(f"\n{'='*60}")
            print(f"Testing: {package_name} v{version}")
            print('='*60)
            
            print(f"\n1. Our MITRE CVE Scanner Result:")
            mitre_result = await scanner.scan_mitre_cve(package_name, version)
            print(f"Summary: {mitre_result.get('summary', 'No summary')}")
            print(f"Found: {mitre_result.get('found_vulnerabilities', False)}")
            print(f"Count: {mitre_result.get('vulnerability_count', 0)}")
            print(f"Search URLs: {mitre_result.get('search_urls', [])}")
            
            # Print first few vulnerabilities if any found
            vulnerabilities = mitre_result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"First 3 vulnerabilities:")
                for i, vuln in enumerate(vulnerabilities[:3]):
                    print(f"  {i+1}. {vuln.get('cve_id', 'No ID')}: {vuln.get('title', 'No title')}")
            else:
                print("No vulnerabilities found by our scanner")
                
            print(f"\n2. Direct Web Check:")
            # Check MITRE website directly
            url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={package_name}"
            print(f"URL: {url}")
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Count CVE matches in the HTML
                    import re
                    cve_matches = re.findall(r'CVE-\d{4}-\d+', response.text)
                    unique_cves = list(set(cve_matches))
                    print(f"Web scraping found: {len(unique_cves)} unique CVEs")
                    if unique_cves:
                        print(f"First 5 CVEs from web: {unique_cves[:5]}")
                else:
                    print(f"Web request failed: Status {response.status_code}")
                    
            except Exception as e:
                print(f"Web request error: {str(e)}")
                
    except Exception as e:
        print(f"Scanner error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

async def main():
    """Main debug function"""
    print("DEBUGGING MITRE CVE SCANNER DISCREPANCIES")
    print("Testing packages: paramiko, Pillow, PyJWT")
    print("="*70)
    
    # Test our scanner
    await debug_mitre_scanner()
    
    print("\n" + "="*70)
    print("DEBUG COMPLETED - Check results above")

if __name__ == "__main__":
    asyncio.run(main())