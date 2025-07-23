#!/usr/bin/env python3
"""
Debug script for specific NIST NVD issues
Testing openpyxl, SQLAlchemy, tabulate packages
"""

import sys
import os
import asyncio
import json
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner
from vulnerability_verification import VulnerabilityVerification

# Test packages with known issues
TEST_PACKAGES = [
    ('openpyxl', '3.1.2'),
    ('SQLAlchemy', '2.0.19'), 
    ('tabulate', '0.9.0')
]

async def debug_nist_scanner():
    """Debug our NIST NVD scanner for specific packages"""
    print("=== DEBUGGING NIST NVD SCANNER ISSUES ===")
    scanner = VulnerabilityScanner()
    
    try:
        for package_name, version in TEST_PACKAGES:
            print(f"\n{'='*60}")
            print(f"Testing: {package_name} v{version}")
            print('='*60)
            
            print(f"\n1. Our NIST NVD Scanner Result:")
            nist_result = await scanner.scan_nist_nvd(package_name, version)
            print(f"Summary: {nist_result.get('summary', 'No summary')}")
            print(f"Found: {nist_result.get('found_vulnerabilities', False)}")
            print(f"Count: {nist_result.get('vulnerability_count', 0)}")
            print(f"Search URLs: {nist_result.get('search_urls', [])}")
            
            # Print first few vulnerabilities if any found
            vulnerabilities = nist_result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"First 3 vulnerabilities:")
                for i, vuln in enumerate(vulnerabilities[:3]):
                    print(f"  {i+1}. {vuln.get('vulnerability_id', 'No ID')}: {vuln.get('title', 'No title')}")
            else:
                print("No vulnerabilities found")
                
            print(f"\n2. Direct API Test:")
            # Test direct API call
            api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package_name}"
            print(f"API URL: {api_url}")
            
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    total_results = data.get('totalResults', 0)
                    results_per_page = data.get('resultsPerPage', 0)
                    print(f"API Response: {total_results} total results, {results_per_page} per page")
                    
                    vulnerabilities = data.get('vulnerabilities', [])
                    if vulnerabilities:
                        print(f"First API result:")
                        first_vuln = vulnerabilities[0]
                        cve_id = first_vuln.get('cve', {}).get('id', 'No ID')
                        descriptions = first_vuln.get('cve', {}).get('descriptions', [])
                        description = descriptions[0].get('value', 'No description') if descriptions else 'No description'
                        print(f"  CVE: {cve_id}")
                        print(f"  Description: {description[:200]}...")
                else:
                    print(f"API Error: Status {response.status_code}")
                    print(f"Response: {response.text[:200]}")
                    
            except Exception as e:
                print(f"API Request Error: {str(e)}")
                
    except Exception as e:
        print(f"Scanner error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

def debug_web_scraping():
    """Debug web scraping for the same packages"""
    print(f"\n\n=== DEBUGGING WEB SCRAPING ===")
    verifier = VulnerabilityVerification()
    
    try:
        verifier.setup_browser()
        
        for package_name, version in TEST_PACKAGES:
            print(f"\n{'='*60}")
            print(f"Web Scraping: {package_name} v{version}")
            print('='*60)
            
            web_count = verifier.scrape_nist_nvd(package_name)
            print(f"Web scraping result: {web_count} vulnerabilities")
            
            # Also show the URL being scraped
            web_url = f"https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&search_type=all&query={package_name}"
            print(f"Web URL: {web_url}")
            
    except Exception as e:
        print(f"Web scraping error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        verifier.cleanup_browser()

async def main():
    """Main debug function"""
    print("DEBUGGING NIST NVD SCANNER DISCREPANCIES")
    print("Testing packages: openpyxl, SQLAlchemy, tabulate")
    print("="*70)
    
    # Test our scanner
    await debug_nist_scanner()
    
    # Test web scraping
    debug_web_scraping()
    
    print("\n" + "="*70)
    print("DEBUG COMPLETED - Check results above")

if __name__ == "__main__":
    asyncio.run(main())