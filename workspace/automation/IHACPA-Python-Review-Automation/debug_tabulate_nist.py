#!/usr/bin/env python3
"""
Debug script for tabulate NIST NVD issue
Check what CVE the website shows and how our filtering handles it
"""

import sys
import os
import asyncio
import json
from urllib.parse import quote

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_tabulate_nist():
    """Debug tabulate NIST NVD filtering"""
    scanner = VulnerabilityScanner()
    
    print("🔍 DEBUGGING TABULATE NIST NVD ISSUE")
    print("=" * 70)
    print()
    
    # Make direct API call to see raw data
    print("📡 Making direct NIST NVD API call for 'tabulate'...")
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    search_url = f"{base_url}?keywordSearch={quote('tabulate')}"
    
    try:
        data = await scanner._rate_limited_request('nist_nvd', search_url)
        
        if data and data.get('vulnerabilities'):
            print(f"✅ Found {len(data['vulnerabilities'])} raw vulnerabilities")
            print(f"📊 Total results: {data.get('totalResults', 'Unknown')}")
            print()
            
            for i, vuln in enumerate(data['vulnerabilities'], 1):
                cve_data = vuln.get('cve', {})
                cve_id = cve_data.get('id', 'Unknown')
                
                descriptions = cve_data.get('descriptions', [])
                description = descriptions[0].get('value', '') if descriptions else ''
                
                print(f"🔍 CVE #{i}: {cve_id}")
                print(f"📝 Description: {description[:300]}...")
                print()
                
                # Test both filtering methods
                print("🧪 TESTING FILTERING METHODS:")
                
                # Original method
                original_relevant = scanner._is_python_cve_relevant('tabulate', cve_id, description, cve_data)
                print(f"  📊 Original filtering: {original_relevant}")
                
                # Enhanced method
                enhanced_relevant = scanner._is_python_cve_relevant_enhanced_nist('tabulate', cve_id, description, cve_data)
                print(f"  🧠 Enhanced filtering: {enhanced_relevant}")
                
                if original_relevant != enhanced_relevant:
                    print(f"  🎯 FILTERING DIFFERENCE FOUND!")
                    if not enhanced_relevant:
                        print(f"  ✅ Enhanced filtering correctly filtered out false positive")
                    else:
                        print(f"  ⚠️  Enhanced filtering may be too strict")
                else:
                    print(f"  ↔️  Both methods agree: {original_relevant}")
                
                # Check for specific WordPress indicators
                desc_lower = description.lower()
                wordpress_indicators = [
                    "wordpress plugin", "wordpress theme", "wp plugin", "wp theme",
                    "drupal module", "joomla extension", "php plugin"
                ]
                
                found_cms_indicators = [ind for ind in wordpress_indicators if ind in desc_lower]
                if found_cms_indicators:
                    print(f"  🚨 CMS indicators found: {found_cms_indicators}")
                    print(f"  ✅ Likely a legitimate false positive (WordPress/CMS plugin)")
                
                print("-" * 70)
        else:
            print("❌ No vulnerabilities found in API response")
            print(f"📊 API Response: {data}")
    
    except Exception as e:
        print(f"❌ Error making API call: {e}")
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(debug_tabulate_nist())