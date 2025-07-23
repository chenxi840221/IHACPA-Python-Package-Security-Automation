#!/usr/bin/env python3
"""
Test NIST API search to see if CVE-2023-48795 is returned for paramiko searches
"""

import asyncio
import aiohttp
from urllib.parse import quote

async def test_nist_search():
    print("=== TESTING NIST API SEARCH FOR PARAMIKO ===")
    
    search_terms = ["paramiko", "python paramiko", "python-paramiko"]
    
    async with aiohttp.ClientSession() as session:
        for term in search_terms:
            print(f"\nSearching NIST API with term: '{term}'")
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={quote(term)}"
            print(f"URL: {url}")
            
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        vulnerabilities = data.get('vulnerabilities', [])
                        print(f"Found {len(vulnerabilities)} vulnerabilities")
                        
                        # Look for CVE-2023-48795
                        found_target = False
                        for vuln in vulnerabilities:
                            cve_data = vuln.get('cve', {})
                            cve_id = cve_data.get('id', '')
                            
                            if cve_id == 'CVE-2023-48795':
                                found_target = True
                                print(f"✅ Found CVE-2023-48795!")
                                
                                descriptions = cve_data.get('descriptions', [])
                                description = descriptions[0].get('value', '') if descriptions else ''
                                print(f"Full Description: {description}")
                                print(f"Description length: {len(description)}")
                                
                                # Check if description contains "paramiko"
                                if 'paramiko' in description.lower():
                                    print("✅ Description contains 'paramiko'")
                                    # Find where paramiko appears
                                    idx = description.lower().find('paramiko')
                                    print(f"'paramiko' found at position {idx}")
                                    print(f"Context: ...{description[max(0, idx-50):idx+50]}...")
                                else:
                                    print("❌ Description does NOT contain 'paramiko'")
                                    print("This explains why it's being filtered out!")
                                    
                                # Test our filtering logic
                                print("\n--- Testing Our Filtering Logic ---")
                                cve_info = {
                                    'description': description,
                                    'cve_id': cve_id
                                }
                                
                                # Simulate our filtering
                                package_lower = 'paramiko'
                                desc_lower = description.lower()
                                
                                # Check package name in description
                                package_in_desc = package_lower in desc_lower
                                print(f"Package 'paramiko' in description: {package_in_desc}")
                                
                                # Check known package list
                                known_python_packages = [
                                    'werkzeug', 'flask', 'django', 'requests', 'urllib3', 'jinja2', 
                                    'pandas', 'numpy', 'scipy', 'matplotlib', 'pillow', 'cryptography',
                                    'click', 'pyyaml', 'lxml', 'beautifulsoup4', 'sqlalchemy', 'psycopg2',
                                    'redis', 'celery', 'gunicorn', 'uwsgi', 'tornado', 'aiohttp',
                                    'fastapi', 'starlette', 'pydantic', 'marshmallow', 'pytest',
                                    'tox', 'coverage', 'mypy', 'black', 'flake8', 'isort', 'bandit',
                                    'zipp', 'setuptools', 'wheel', 'pip', 'virtualenv', 'conda',
                                    'mistune', 'paramiko', 'pyjwt', 'jwt', 'ssh', 'markdown'
                                ]
                                is_known_package = package_lower in known_python_packages
                                print(f"Is known Python package: {is_known_package}")
                                
                                if package_in_desc and is_known_package:
                                    print("✅ Should PASS filtering (package found + known package)")
                                else:
                                    print("❌ Should FAIL filtering")
                                break
                        
                        if not found_target:
                            print("❌ CVE-2023-48795 NOT found in search results")
                            
                        # Show first few CVE IDs for reference
                        if vulnerabilities:
                            cve_ids = []
                            for vuln in vulnerabilities[:5]:
                                cve_data = vuln.get('cve', {})
                                cve_id = cve_data.get('id', '')
                                if cve_id:
                                    cve_ids.append(cve_id)
                            print(f"First 5 CVEs: {cve_ids}")
                    else:
                        print(f"API request failed: Status {response.status}")
                        
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_nist_search())