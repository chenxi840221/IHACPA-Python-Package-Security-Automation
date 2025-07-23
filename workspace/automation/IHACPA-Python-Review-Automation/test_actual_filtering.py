#!/usr/bin/env python3
"""
Test our actual filtering method with the exact data structure
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def test_filtering():
    print("=== TESTING ACTUAL FILTERING METHOD ===")
    scanner = VulnerabilityScanner()
    
    try:
        # Get the actual CVE data from NIST API
        results = await scanner._get_enhanced_mitre_cve_data('paramiko')
        
        print(f"Found {len(results)} CVEs from NIST API")
        
        # Look for CVE-2023-48795
        target_cve = None
        for cve_info in results:
            if cve_info.get('cve_id') == 'CVE-2023-48795':
                target_cve = cve_info
                break
        
        if target_cve:
            print(f"✅ Found CVE-2023-48795 in API results")
            print(f"Description length: {len(target_cve.get('description', ''))}")
            print(f"Description preview: {target_cve.get('description', '')[:200]}...")
            
            # Test the actual filtering method
            print("\n--- Testing Actual Filtering Method ---")
            is_relevant = scanner._is_mitre_cve_relevant_enhanced('paramiko', target_cve)
            print(f"Filter result: {is_relevant}")
            
            if is_relevant:
                print("✅ CVE passes filtering - should be included")
            else:
                print("❌ CVE fails filtering - this is the bug!")
                
                # Debug the filtering step by step
                print("\n--- Debugging Filtering Logic ---")
                description = target_cve.get('description', '').lower()
                package_lower = 'paramiko'
                
                print(f"Package name: {package_lower}")
                print(f"Package in description: {'paramiko' in description}")
                
                # Check python indicators
                python_indicators = [
                    f"python {package_lower}",
                    f"pip install {package_lower}",
                    f"pypi {package_lower}",
                    f"{package_lower} python package",
                    f"{package_lower} python library",
                    f"python's {package_lower}",
                    f"python-{package_lower}",
                    f"the {package_lower} package for python",
                    f"the {package_lower} library for python"
                ]
                
                found_python_indicator = False
                for indicator in python_indicators:
                    if indicator in description:
                        print(f"✅ Found Python indicator: '{indicator}'")
                        found_python_indicator = True
                        
                if not found_python_indicator:
                    print("❌ No Python indicators found")
                    
                # Check hard exclusions
                hard_exclusions = [
                    f"lib{package_lower}",      # C libraries
                    f"{package_lower}.c",       # C source files
                    f"{package_lower}.h",       # C header files
                    f"{package_lower}.exe",     # Windows executables
                    f"{package_lower}.dll",     # Windows libraries
                    f"rust crate",              # Rust crates
                    f"ruby gem",               # Ruby gems
                    f"perl module",            # Perl modules
                    f"golang",                 # Go packages
                    f"node.js",                # Node.js specific
                    f"npm package",            # npm packages
                    f".NET framework",         # .NET libraries
                    f"java library",           # Java libraries
                    f"android app",            # Android specific
                    f"android application",    # Android specific 
                    f"ios app",                # iOS specific
                    f"ios application"         # iOS specific
                ]
                
                found_hard_exclusion = False
                for exclusion in hard_exclusions:
                    if exclusion in description:
                        print(f"❌ Found hard exclusion: '{exclusion}'")
                        found_hard_exclusion = True
                        
                if not found_hard_exclusion:
                    print("✅ No hard exclusions found")
                    
                # Check known packages logic
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
                
                is_known = package_lower in known_python_packages
                print(f"Is known Python package: {is_known}")
                
        else:
            print("❌ CVE-2023-48795 NOT found in API results")
            print("Available CVEs:")
            for cve_info in results[:5]:
                print(f"  - {cve_info.get('cve_id', 'Unknown')}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(test_filtering())