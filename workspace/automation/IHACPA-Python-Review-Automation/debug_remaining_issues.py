#!/usr/bin/env python3
"""
Debug the remaining issues with tornado and other packages
"""

import sys
import os
import asyncio
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_tornado():
    """Debug why tornado shows 0 results"""
    print("=== DEBUGGING TORNADO ISSUE ===")
    scanner = VulnerabilityScanner()
    
    try:
        # Add longer delay to avoid rate limiting
        await asyncio.sleep(2)
        
        # Test tornado specifically
        print("Testing tornado with detailed logging...")
        result = await scanner.scan_nist_nvd('tornado', '6.2')
        
        print(f"Tornado NIST NVD Results:")
        print(f"  Found vulnerabilities: {result.get('found_vulnerabilities', False)}")
        print(f"  Vulnerability count: {result.get('vulnerability_count', 0)}")
        print(f"  Summary: {result.get('summary', 'N/A')}")
        print(f"  Search URL: {result.get('search_url', 'N/A')}")
        
        # Check the raw search strategy
        search_urls = scanner._get_enhanced_search_urls(
            "https://services.nvd.nist.gov/rest/json/cves/2.0", 
            "tornado"
        )
        print(f"\nSearch URLs being used:")
        for i, url in enumerate(search_urls):
            print(f"  {i+1}. {url}")
        
        # Test with longer delays between requests
        print(f"\nTrying individual search strategies with delays...")
        await asyncio.sleep(3)
        
        for i, search_url in enumerate(search_urls[:2]):  # Test first 2 to avoid rate limits
            print(f"\nTesting search strategy {i+1}: {search_url}")
            try:
                data = await scanner._rate_limited_request('nist_nvd', search_url)
                if data:
                    total_results = data.get('totalResults', 0)
                    vulnerabilities = data.get('vulnerabilities', [])
                    print(f"  API Response: {total_results} total results, {len(vulnerabilities)} vulnerabilities returned")
                    
                    if vulnerabilities:
                        print(f"  First vulnerability:")
                        vuln = vulnerabilities[0]
                        cve_data = vuln.get('cve', {})
                        cve_id = cve_data.get('id', 'Unknown')
                        descriptions = cve_data.get('descriptions', [])
                        description = descriptions[0].get('value', '') if descriptions else ''
                        print(f"    {cve_id}: {description[:100]}...")
                        
                        # Test relevance filtering
                        is_relevant = scanner._is_python_cve_relevant_enhanced_nist(
                            'tornado', cve_id, description, cve_data
                        )
                        print(f"    Passes relevance filter: {is_relevant}")
                else:
                    print(f"  No data returned (likely rate limited)")
                    
            except Exception as e:
                print(f"  Error: {e}")
            
            # Add delay between requests
            await asyncio.sleep(5)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

async def debug_pillow_mitre():
    """Debug why Pillow MITRE shows only 9 instead of 55"""
    print("\n=== DEBUGGING PILLOW MITRE CVE ISSUE ===")
    scanner = VulnerabilityScanner()
    
    try:
        # Test Pillow MITRE CVE
        result = await scanner.scan_mitre_cve('Pillow', '9.4.0')
        
        print(f"Pillow MITRE CVE Results:")
        print(f"  Found vulnerabilities: {result.get('found_vulnerabilities', False)}")
        print(f"  Vulnerability count: {result.get('vulnerability_count', 0)}")
        print(f"  Summary: {result.get('summary', 'N/A')}")
        
        vulnerabilities = result.get('vulnerabilities', [])
        print(f"  Found {len(vulnerabilities)} vulnerabilities:")
        for i, vuln in enumerate(vulnerabilities[:10]):
            print(f"    {i+1}. {vuln.get('cve_id', 'Unknown')}: {vuln.get('description', 'No description')[:80]}...")
        
        # The difference might be due to relevance filtering
        # MITRE CVE uses different data source (NIST API) which may have different search results
        # than the MITRE website, plus our relevance filtering may be removing some
        print(f"\nNote: MITRE CVE scanner uses NIST API data with MITRE-specific filtering.")
        print(f"The difference between 9 and 55 may be due to:")
        print(f"  1. NIST API returning different results than MITRE website")
        print(f"  2. Relevance filtering removing non-Python-specific Pillow CVEs")
        print(f"  3. Rate limiting affecting search completeness")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await scanner.close()

if __name__ == "__main__":
    print("Starting debugging with delays to avoid rate limiting...")
    asyncio.run(debug_tornado())
    time.sleep(10)  # Long delay between tests
    asyncio.run(debug_pillow_mitre())