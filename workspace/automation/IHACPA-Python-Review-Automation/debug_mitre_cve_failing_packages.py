#!/usr/bin/env python3
"""
Debug script for MITRE CVE packages still failing
Focus on mistune, paramiko, and PyJWT search and filtering issues
"""

import sys
import os
import asyncio
import json
from urllib.parse import quote

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_failing_packages():
    """Debug MITRE CVE filtering for failing packages"""
    scanner = VulnerabilityScanner()
    
    print("🔍 DEBUGGING MITRE CVE FAILING PACKAGES")
    print("=" * 70)
    print()
    
    failing_packages = ['mistune', 'paramiko', 'PyJWT']
    
    for package in failing_packages:
        print(f"🔍 DEBUGGING: {package}")
        print("-" * 50)
        
        try:
            # Test enhanced MITRE CVE data retrieval
            print("📡 Testing enhanced MITRE CVE data retrieval...")
            enhanced_data = await scanner._get_enhanced_mitre_cve_data(package)
            print(f"Enhanced search found: {len(enhanced_data)} CVEs")
            
            if enhanced_data:
                print("✅ Raw CVEs found before filtering:")
                for i, vuln in enumerate(enhanced_data[:3], 1):
                    cve_id = vuln.get('cve_id', 'Unknown')
                    description = vuln.get('description', 'No description')[:150]
                    print(f"  {i}. {cve_id}: {description}...")
                    
                    # Test filtering for each CVE
                    is_relevant = scanner._is_mitre_cve_relevant_enhanced(package, vuln)
                    print(f"     Enhanced filtering result: {is_relevant}")
                    
                    if not is_relevant:
                        print(f"     🚨 CVE FILTERED OUT - checking why...")
                        # Check specific filtering reasons
                        desc_lower = description.lower()
                        package_lower = package.lower()
                        
                        # Check for hard exclusions
                        hard_exclusions = [
                            f"lib{package_lower}", f"{package_lower}.c", f"{package_lower}.exe",
                            f"rust crate", f"ruby gem", f"java library"
                        ]
                        found_exclusions = [exc for exc in hard_exclusions if exc in desc_lower]
                        if found_exclusions:
                            print(f"     Hard exclusion found: {found_exclusions}")
                            
                        # Check for Python indicators
                        python_indicators = [
                            f"python {package_lower}", f"pip install {package_lower}", 
                            f"pypi {package_lower}", f"{package_lower} python package"
                        ]
                        found_indicators = [ind for ind in python_indicators if ind in desc_lower]
                        if found_indicators:
                            print(f"     Python indicators found: {found_indicators}")
                        else:
                            print(f"     ❌ No clear Python indicators found")
                            
                            # Check if it's in known Python packages
                            known_python_packages = [
                                'mistune', 'paramiko', 'pyjwt', 'jwt', 'pillow', 'pil',
                                'werkzeug', 'flask', 'django', 'requests', 'urllib3'
                            ]
                            if package_lower in known_python_packages or any(pkg in package_lower for pkg in known_python_packages):
                                print(f"     ✅ Package IS in known Python packages list")
                            else:
                                print(f"     ⚠️  Package NOT in known Python packages list")
                        
                print()
            else:
                print("❌ No raw CVEs found - search strategy issue")
                
                # Test individual search terms
                print("🔍 Testing individual search terms...")
                search_terms = [
                    package,
                    f"python {package}",
                    f"python-{package}",
                    f"pypi {package}",
                    f"{package} python package"
                ]
                
                for term in search_terms:
                    print(f"  Testing: '{term}'")
                    try:
                        nist_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={quote(term)}"
                        data = await scanner._rate_limited_request('nist_nvd', nist_url)
                        if data and data.get('vulnerabilities'):
                            count = len(data['vulnerabilities'])
                            print(f"    ✅ Found {count} raw vulnerabilities")
                        else:
                            print(f"    ❌ No vulnerabilities found")
                        await asyncio.sleep(1)  # Rate limiting
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
                
        except Exception as e:
            print(f"❌ ERROR debugging {package}: {e}")
        
        print()
        print("=" * 70)
        print()
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(debug_failing_packages())