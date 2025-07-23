#!/usr/bin/env python3
"""
Debug why CVE-2023-48795 is missing from paramiko results
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_specific_cve():
    """Debug why CVE-2023-48795 is missing"""
    print("=== DEBUGGING CVE-2023-48795 (MISSING FROM PARAMIKO) ===")
    scanner = VulnerabilityScanner()
    
    try:
        # First, let's check if searching for different terms finds it
        search_terms = ['paramiko', 'ssh', 'python ssh', 'python paramiko', 'CVE-2023-48795']
        
        for term in search_terms:
            print(f"\nSearching MITRE with term: '{term}'")
            url = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={term}"
            
            # Use internal method to search
            data = await scanner._rate_limited_request('mitre_cve', url)
            if data:
                # Check if CVE-2023-48795 is in the results
                if 'CVE-2023-48795' in data:
                    print(f"  ✅ Found CVE-2023-48795 with search term '{term}'")
                    # Extract description
                    import re
                    pattern = r'CVE-2023-48795.*?<TD[^>]*>(.*?)</TD>'
                    match = re.search(pattern, data, re.DOTALL | re.IGNORECASE)
                    if match:
                        desc = re.sub('<[^>]+>', '', match.group(1)).strip()
                        print(f"  Description: {desc[:150]}...")
                        
                        # Check if it would pass our relevance filter
                        # Get the filtering method
                        is_relevant = scanner._is_mitre_cve_relevant_enhanced(
                            'paramiko', 'CVE-2023-48795', desc, {}
                        )
                        print(f"  Would pass relevance filter: {is_relevant}")
                        if not is_relevant:
                            print("  ❌ Being filtered out by relevance check!")
                else:
                    print(f"  ❌ CVE-2023-48795 NOT found with search term '{term}'")
            else:
                print(f"  ⚠️  No data returned for search term '{term}'")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(debug_specific_cve())