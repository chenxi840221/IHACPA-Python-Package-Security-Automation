#!/usr/bin/env python3
"""
Debug NIST NVD discrepancies for specific packages
Investigates why our results differ significantly from manual website searches
"""

import sys
import os
import asyncio
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# Packages with reported discrepancies
TEST_PACKAGES = [
    # (package_name, version, expected_website_count, our_result_description)
    ('lxml', '4.9.2', 12, 'Manual review required - 10 CVEs found'),
    ('Markdown', '3.4.4', 264, 'None found'), 
    ('tables', '3.4.1', 392, 'SAFE - 1 CVEs found'),
    ('SQLAlchemy', '1.4.39', 7, 'None found'),
    ('tabulate', '0.9.0', 7, 'None found'),
    ('tornado', '6.2', 14, 'None found')
]

async def debug_nist_package(scanner, package_name, version, expected_count, our_result):
    """Debug a specific package's NIST NVD results"""
    print(f"\n{'='*80}")
    print(f"🔍 DEBUGGING: {package_name} v{version}")
    print(f"📊 Expected (website): {expected_count} CVE Records")
    print(f"🤖 Our result: {our_result}")
    print('='*80)
    
    try:
        # Test 1: Check search URLs being generated
        base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        search_urls = scanner._get_enhanced_search_urls(base_url, package_name)
        
        print(f"\n📋 SEARCH URLS BEING USED:")
        for i, url in enumerate(search_urls, 1):
            print(f"  {i}. {url}")
        
        # Test 2: Check raw API responses for each search URL
        print(f"\n🔍 RAW API RESPONSES:")
        total_found_across_searches = 0
        all_cve_ids = set()
        
        for i, search_url in enumerate(search_urls, 1):
            print(f"\n  Search {i}: {search_url}")
            try:
                await asyncio.sleep(2)  # Rate limiting
                data = await scanner._rate_limited_request('nist_nvd', search_url)
                
                if data:
                    total_results = data.get('totalResults', 0)
                    vulnerabilities = data.get('vulnerabilities', [])
                    print(f"    ✅ API Response: {total_results} total results, {len(vulnerabilities)} returned")
                    
                    # Count unique CVEs
                    for vuln in vulnerabilities:
                        cve_id = vuln.get('cve', {}).get('id', '')
                        if cve_id:
                            all_cve_ids.add(cve_id)
                    
                    total_found_across_searches += total_results
                    
                    # Show first few CVEs
                    if vulnerabilities:
                        print(f"    First 3 CVEs found:")
                        for j, vuln in enumerate(vulnerabilities[:3]):
                            cve_data = vuln.get('cve', {})
                            cve_id = cve_data.get('id', 'Unknown')
                            descriptions = cve_data.get('descriptions', [])
                            description = descriptions[0].get('value', '') if descriptions else ''
                            print(f"      {j+1}. {cve_id}: {description[:100]}...")
                else:
                    print(f"    ❌ No data returned (likely rate limited or error)")
                    
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        print(f"\n📊 SEARCH SUMMARY:")
        print(f"  Total CVEs found across all searches: {total_found_across_searches}")
        print(f"  Unique CVE IDs: {len(all_cve_ids)}")
        print(f"  Website shows: {expected_count}")
        print(f"  Discrepancy: {expected_count - len(all_cve_ids)} CVEs missing")
        
        # Test 3: Full scan with our logic
        print(f"\n🧪 FULL SCAN TEST:")
        result = await scanner.scan_nist_nvd(package_name, version)
        
        found_vulnerabilities = result.get('found_vulnerabilities', False)
        vulnerability_count = result.get('vulnerability_count', 0)
        summary = result.get('summary', 'N/A')
        vulnerabilities = result.get('vulnerabilities', [])
        
        print(f"  Found vulnerabilities: {found_vulnerabilities}")
        print(f"  Vulnerability count: {vulnerability_count}")
        print(f"  Summary: {summary}")
        
        if vulnerabilities:
            print(f"  Vulnerabilities after filtering:")
            for i, vuln in enumerate(vulnerabilities[:5]):
                cve_id = vuln.get('cve_id', 'Unknown')
                description = vuln.get('description', 'No description')
                severity = vuln.get('severity', 'Unknown')
                print(f"    {i+1}. {cve_id} ({severity}): {description[:80]}...")
        
        # Test 4: Manual website URL for comparison
        website_url = f"https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query={package_name}&search_type=all&isCpeNameSearch=false"
        print(f"\n🌐 MANUAL WEBSITE URL: {website_url}")
        
        # Analysis
        print(f"\n📋 ANALYSIS:")
        if vulnerability_count == 0 and expected_count > 0:
            print(f"  ❌ MAJOR ISSUE: We found 0 CVEs but website shows {expected_count}")
            print(f"  🔍 Possible causes:")
            print(f"    1. API search terms don't match website search")
            print(f"    2. Relevance filtering too aggressive")
            print(f"    3. Rate limiting blocking requests")
            print(f"    4. API vs website use different data/algorithms")
        elif vulnerability_count < expected_count * 0.8:  # Less than 80% of expected
            print(f"  ⚠️  PARTIAL ISSUE: We found {vulnerability_count} CVEs but website shows {expected_count}")
            print(f"  🔍 Likely causes:")
            print(f"    1. Different search scope between API and website")
            print(f"    2. Some CVEs filtered out by relevance logic")
            print(f"    3. Limited search strategies")
        else:
            print(f"  ✅ REASONABLE MATCH: {vulnerability_count} vs {expected_count} expected")
        
        return {
            'package': package_name,
            'expected': expected_count,
            'found': vulnerability_count,
            'discrepancy': expected_count - vulnerability_count,
            'success': vulnerability_count > 0
        }
        
    except Exception as e:
        print(f"❌ Debug failed for {package_name}: {e}")
        import traceback
        traceback.print_exc()
        return {
            'package': package_name,
            'expected': expected_count,
            'found': 0,
            'discrepancy': expected_count,
            'success': False,
            'error': str(e)
        }

async def comprehensive_nist_debug():
    """Run comprehensive debugging of NIST NVD issues"""
    print("=" * 80)
    print("🔍 NIST NVD DISCREPANCY INVESTIGATION")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(TEST_PACKAGES)} packages with known discrepancies")
    
    scanner = VulnerabilityScanner()
    results = []
    
    try:
        for package_name, version, expected_count, our_result in TEST_PACKAGES:
            result = await debug_nist_package(scanner, package_name, version, expected_count, our_result)
            results.append(result)
            
            # Long delay between packages to avoid rate limiting
            await asyncio.sleep(5)
        
        # Final summary
        print(f"\n{'='*80}")
        print("📊 FINAL SUMMARY")
        print('='*80)
        
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        print(f"✅ Packages finding some CVEs: {len(successful)}/{len(results)}")
        print(f"❌ Packages finding zero CVEs: {len(failed)}/{len(results)}")
        
        total_expected = sum(r['expected'] for r in results)
        total_found = sum(r['found'] for r in results)
        total_discrepancy = sum(r['discrepancy'] for r in results)
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"  Expected total CVEs: {total_expected}")
        print(f"  Found total CVEs: {total_found}")
        print(f"  Total discrepancy: {total_discrepancy}")
        print(f"  Detection rate: {(total_found/total_expected)*100:.1f}%")
        
        print(f"\n🔍 PACKAGES WITH MAJOR ISSUES (0 CVEs found):")
        for result in failed:
            print(f"  ❌ {result['package']}: Expected {result['expected']}, Found 0")
        
        print(f"\n⚠️  PACKAGES WITH PARTIAL ISSUES:")
        for result in successful:
            if result['discrepancy'] > result['expected'] * 0.2:  # More than 20% missing
                print(f"  ⚠️  {result['package']}: Expected {result['expected']}, Found {result['found']} (missing {result['discrepancy']})")
        
        print(f"\n💡 RECOMMENDED FIXES:")
        if len(failed) > 0:
            print(f"  1. Enhance search URL strategies for broader coverage")
            print(f"  2. Reduce relevance filtering restrictions") 
            print(f"  3. Add fallback search methods")
            print(f"  4. Implement website scraping as backup")
        
        if total_discrepancy > total_expected * 0.3:
            print(f"  5. Consider alternative NIST NVD access methods")
            print(f"  6. Investigate API vs website differences")
        
    except Exception as e:
        print(f"❌ Comprehensive debug failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(comprehensive_nist_debug())