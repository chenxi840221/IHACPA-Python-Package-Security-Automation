#!/usr/bin/env python3
"""
Test SNYK scanner with packages known to have vulnerabilities
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def test_snyk_vulnerable_packages():
    """Test SNYK scanner with packages that should have vulnerabilities"""
    scanner = VulnerabilityScanner()
    
    print("🧪 TESTING SNYK SCANNER WITH KNOWN VULNERABLE PACKAGES")
    print("=" * 70)
    print()
    
    # Test packages that commonly have vulnerabilities
    test_packages = [
        {'name': 'pillow', 'version': '8.0.0'},  # Older Pillow version
        {'name': 'requests', 'version': '2.20.0'},  # Older requests
        {'name': 'urllib3', 'version': '1.24.0'},  # Older urllib3
        {'name': 'django', 'version': '2.0.0'},  # Much older Django
        {'name': 'pyyaml', 'version': '3.13'},  # Older PyYAML
    ]
    
    for pkg in test_packages:
        package_name = pkg['name']
        version = pkg['version']
        
        print(f"📊 Testing {package_name} v{version}")
        print("-" * 40)
        
        try:
            result = await scanner.scan_snyk(package_name, version)
            
            found_vulnerabilities = result.get('found_vulnerabilities', False)
            vulnerability_count = result.get('vulnerability_count', 0)
            summary = result.get('summary', 'No summary')
            search_url = result.get('search_url', '')
            
            print(f"🔍 URL: {search_url}")
            print(f"✓ Found vulnerabilities: {found_vulnerabilities}")
            print(f"✓ Vulnerability count: {vulnerability_count}")
            print(f"✓ Summary: {summary}")
            
            if vulnerability_count > 0:
                print("✅ SNYK scanner working - found vulnerabilities")
                vulnerabilities = result.get('vulnerabilities', [])
                for i, vuln in enumerate(vulnerabilities[:2], 1):  # Show first 2
                    vuln_id = vuln.get('id', vuln.get('vulnerability_id', 'Unknown'))
                    severity = vuln.get('severity', 'Unknown')
                    print(f"  {i}. {vuln_id} - {severity}")
                break  # Found working example, stop testing
            else:
                print("❌ No vulnerabilities found")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_snyk_vulnerable_packages())