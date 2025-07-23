#!/usr/bin/env python3
"""
Debug script to find which CVE is missing from paramiko
"""

import sys
import os
import asyncio
import requests
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_paramiko():
    """Debug paramiko MITRE CVE scanner"""
    print("=== DEBUGGING PARAMIKO MISSING CVE ===")
    scanner = VulnerabilityScanner()
    
    try:
        # Test paramiko
        package_name = 'paramiko'
        version = '3.1.0'
        
        print(f"\nTesting: {package_name} v{version}")
        print('='*60)
        
        # Get our scanner results
        mitre_result = await scanner.scan_mitre_cve(package_name, version)
        our_cves = []
        
        vulnerabilities = mitre_result.get('vulnerabilities', [])
        print(f"\nOur scanner found {len(vulnerabilities)} CVEs:")
        for vuln in vulnerabilities:
            cve_id = vuln.get('cve_id', 'Unknown')
            our_cves.append(cve_id)
            print(f"  - {cve_id}")
        
        # Check web for comparison
        print(f"\nChecking MITRE website for comparison...")
        url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={package_name}"
        
        # Use requests with no SSL verification for testing
        try:
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                # Find all CVE IDs in the response
                cve_matches = re.findall(r'CVE-\d{4}-\d+', response.text)
                unique_web_cves = sorted(list(set(cve_matches)))
                
                print(f"\nWeb scraping found {len(unique_web_cves)} unique CVEs:")
                for cve in unique_web_cves:
                    status = "✅" if cve in our_cves else "❌ MISSING"
                    print(f"  - {cve} {status}")
                
                # Find missing CVEs
                missing_cves = [cve for cve in unique_web_cves if cve not in our_cves]
                if missing_cves:
                    print(f"\n❌ Missing CVEs: {missing_cves}")
                    
                    # Let's check why they're missing
                    print("\nChecking filtering logic for missing CVEs...")
                    for missing_cve in missing_cves:
                        # Try to find description in the HTML
                        pattern = f'{missing_cve}.*?<TD[^>]*>(.*?)</TD>'
                        match = re.search(pattern, response.text, re.DOTALL | re.IGNORECASE)
                        if match:
                            desc = re.sub('<[^>]+>', '', match.group(1)).strip()[:200]
                            print(f"\n{missing_cve} description: {desc}...")
                else:
                    print("\n✅ All web CVEs are found by our scanner!")
                
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

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    asyncio.run(debug_paramiko())