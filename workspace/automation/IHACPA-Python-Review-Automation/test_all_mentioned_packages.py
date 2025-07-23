#!/usr/bin/env python3
"""
Test ALL packages mentioned by the user in the last chat to verify fixes
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# ALL packages mentioned by the user with their specific issues
ALL_MENTIONED_PACKAGES = [
    # NIST NVD issues (Column P)
    ('PyJWT', '2.8.0', 'NIST NVD', 'has 3 CVE Records but our result is "None found"'),
    ('pywin32', '306', 'NIST NVD', 'has 1 CVE Record but our result is "None found"'),
    ('tables', '3.8.0', 'NIST NVD', 'has 392 matching records but our result is "SAFE - 1 CVEs found but v3.8.0 not affected"'),
    ('transformers', '2.1.1', 'NIST NVD', 'has 9 matching records but our result is "SAFE - 1 CVEs found but v2.1.1 not affected"'),
    ('tornado', '6.2', 'NIST NVD', 'has 14 matching records but our result is "SAFE - 2 CVEs found but v6.2 not affected"'),
    
    # MITRE CVE issues (Column R)
    ('paramiko', '3.1.0', 'MITRE CVE', 'has 5 CVE Records but our result is "None found"'),
    ('Pillow', '9.4.0', 'MITRE CVE', 'has 55 CVE Records but our result is "SAFE - 9 MITRE CVEs found but v9.4.0 not affected"'),
    ('PyJWT', '2.8.0', 'MITRE CVE', 'has 3 matching records but our result is "None found"'),
    
    # SNYK issues (Column T)
    ('cffi', '1.15.1', 'SNYK', 'has 1 VULNERABILITY Record but our result is "None found"'),
]

async def comprehensive_test():
    """Test all mentioned packages across all relevant databases"""
    print("=== COMPREHENSIVE TEST OF ALL MENTIONED PACKAGES ===")
    scanner = VulnerabilityScanner()
    
    results_summary = {
        'NIST NVD': {'fixed': 0, 'improved': 0, 'still_broken': 0, 'working': 0},
        'MITRE CVE': {'fixed': 0, 'improved': 0, 'still_broken': 0, 'working': 0},
        'SNYK': {'fixed': 0, 'improved': 0, 'still_broken': 0, 'working': 0}
    }
    
    try:
        for package_name, version, database, original_issue in ALL_MENTIONED_PACKAGES:
            print(f"\n{'='*80}")
            print(f"Testing: {package_name} v{version} ({database})")
            print(f"Original Issue: {original_issue}")
            print('='*80)
            
            if database == 'NIST NVD':
                result = await scanner.scan_nist_nvd(package_name, version)
            elif database == 'MITRE CVE':
                result = await scanner.scan_mitre_cve(package_name, version)
            elif database == 'SNYK':
                result = await scanner.scan_snyk(package_name, version)
            else:
                continue
                
            # Extract results
            found_vulnerabilities = result.get('found_vulnerabilities', False)
            vulnerability_count = result.get('vulnerability_count', 0)
            summary = result.get('summary', 'N/A')
            
            print(f"\n{database} Results for {package_name}:")
            print(f"  Search URL: {result.get('search_url', 'N/A')}")
            print(f"  Found vulnerabilities: {found_vulnerabilities}")
            print(f"  Vulnerability count: {vulnerability_count}")
            print(f"  Summary: {summary}")
            
            # Show vulnerabilities found
            vulnerabilities = result.get('vulnerabilities', [])
            if vulnerabilities:
                print(f"  Vulnerabilities found:")
                for i, vuln in enumerate(vulnerabilities[:5]):  # Show first 5
                    vuln_id = vuln.get('cve_id', vuln.get('id', 'No ID'))
                    description = vuln.get('title', vuln.get('description', 'No description'))
                    print(f"    {i+1}. {vuln_id}: {description[:80]}...")
            
            # Analyze the fix status
            status = analyze_fix_status(package_name, database, original_issue, vulnerability_count, found_vulnerabilities)
            print(f"\n  📊 FIX STATUS: {status}")
            
            # Update summary
            if 'FIXED' in status:
                results_summary[database]['fixed'] += 1
            elif 'IMPROVED' in status:
                results_summary[database]['improved'] += 1
            elif 'WORKING' in status:
                results_summary[database]['working'] += 1
            else:
                results_summary[database]['still_broken'] += 1
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print("COMPREHENSIVE RESULTS SUMMARY")
    print('='*80)
    
    for database, stats in results_summary.items():
        total = sum(stats.values())
        if total > 0:
            print(f"\n{database} ({total} packages tested):")
            print(f"  ✅ FIXED: {stats['fixed']} packages")
            print(f"  ⬆️  IMPROVED: {stats['improved']} packages") 
            print(f"  ✅ WORKING: {stats['working']} packages")
            print(f"  ❌ STILL BROKEN: {stats['still_broken']} packages")
            
            success_rate = ((stats['fixed'] + stats['improved'] + stats['working']) / total) * 100
            print(f"  🎯 SUCCESS RATE: {success_rate:.1f}%")

def analyze_fix_status(package_name, database, original_issue, count, found_vulnerabilities):
    """Analyze whether the package issue was fixed"""
    
    # Extract expected count from original issue
    expected_count = extract_expected_count(original_issue)
    
    # Determine status based on original issue and current results
    if '"None found"' in original_issue and found_vulnerabilities:
        if count >= expected_count:
            return f"✅ FULLY FIXED - Now finds {count} vulnerabilities (was 'None found')"
        else:
            return f"✅ PARTIALLY FIXED - Now finds {count} vulnerabilities (was 'None found', expected ~{expected_count})"
    
    elif 'SAFE' in original_issue and count > expected_count:
        return f"⬆️ IMPROVED - Now finds {count} vulnerabilities (was {expected_count})"
    
    elif found_vulnerabilities and count >= expected_count:
        return f"✅ WORKING CORRECTLY - Finds {count} vulnerabilities as expected"
    
    elif not found_vulnerabilities and expected_count > 0:
        return f"❌ STILL BROKEN - Still shows 'None found' (expected {expected_count})"
    
    else:
        return f"⚠️ PARTIAL - Finds {count} vulnerabilities (expected ~{expected_count})"

def extract_expected_count(original_issue):
    """Extract expected vulnerability count from original issue description"""
    import re
    
    # Look for numbers in the issue description
    numbers = re.findall(r'(\d+)', original_issue)
    
    if 'has 3 CVE Records' in original_issue or 'has 3 matching records' in original_issue:
        return 3
    elif 'has 1 CVE Record' in original_issue or 'has 1 VULNERABILITY Record' in original_issue:
        return 1
    elif 'has 5 CVE Records' in original_issue:
        return 5
    elif 'has 55 CVE Records' in original_issue:
        return 55
    elif 'has 392 matching records' in original_issue:
        return 392
    elif 'has 9 matching records' in original_issue:
        return 9
    elif 'has 14 matching records' in original_issue:
        return 14
    elif numbers:
        return int(numbers[0])
    else:
        return 1

if __name__ == "__main__":
    asyncio.run(comprehensive_test())