#!/usr/bin/env python3
"""
Debug script to trace PyJWT CVE-2024-53861 filtering step by step
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_filtering_logic():
    """Step by step debug of the filtering logic for CVE-2024-53861"""
    
    # CVE data
    package_name = "PyJWT"
    cve_info = {
        'cve_id': 'CVE-2024-53861',
        'description': 'pyjwt is a JSON Web Token implementation in Python. An incorrect string comparison is run for `iss` checking, resulting in `"acb"` being accepted for `"_abc_"`. This is a bug introduced in version 2.1'
    }
    
    print("🔍 STEP BY STEP CVE FILTERING DEBUG")
    print("=" * 60)
    print(f"Package: {package_name}")
    print(f"CVE: {cve_info['cve_id']}")
    print(f"Description: {cve_info['description']}")
    print()
    
    # Start of filtering logic
    description = cve_info.get('description', '').lower()
    package_lower = package_name.lower()
    
    print(f"✓ description (lowercase): {description}")
    print(f"✓ package_lower: {package_lower}")
    print()
    
    # Step 1: Check for explicit Python package indicators
    print("STEP 1: Check explicit Python package indicators")
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
    
    found_indicators = []
    for indicator in python_indicators:
        if indicator in description:
            found_indicators.append(indicator)
    
    print(f"Python indicators found: {found_indicators}")
    if found_indicators:
        print("✅ EARLY RETURN: Explicit Python indicators found!")
        return True
    print("❌ No explicit Python indicators found, continuing...")
    print()
    
    # Step 2: Check for hard exclusions
    print("STEP 2: Check hard exclusion patterns")
    hard_exclusions = [
        f"lib{package_lower}",
        f"{package_lower}.c",
        f"{package_lower}.h",
        f"{package_lower}.exe",
        f"{package_lower}.dll",
        f"rust crate",
        f"ruby gem",
        f"perl module",
        f"golang",
        f"node.js",
        f"npm package",
        f".NET framework",
        f"java library",
        f"android",
        f"ios"
    ]
    
    found_exclusions = []
    for exclusion in hard_exclusions:
        if exclusion in description:
            found_exclusions.append(exclusion)
    
    print(f"Hard exclusions found: {found_exclusions}")
    if found_exclusions:
        print("❌ EARLY RETURN: Hard exclusions found!")
        return False
    print("✅ No hard exclusions found, continuing...")
    print()
    
    # Step 3: Check for soft exclusions
    print("STEP 3: Check soft exclusion patterns")
    soft_exclusions = ["java", "php", "ruby", "perl", "golang", "node", "npm", ".net"]
    exclusion_found = any(excl in description for excl in soft_exclusions)
    
    print(f"Soft exclusions found: {exclusion_found}")
    if exclusion_found:
        exclusions_present = [excl for excl in soft_exclusions if excl in description]
        print(f"Specific soft exclusions: {exclusions_present}")
    print()
    
    # Step 4: Check if package name is in description
    print("STEP 4: Check if package name is in description")
    package_in_desc = package_lower in description
    print(f"'{package_lower}' in description: {package_in_desc}")
    
    if not package_in_desc:
        print("❌ RETURN FALSE: Package name not in description")
        return False
    print("✅ Package name found in description, continuing...")
    print()
    
    # Step 5: Check if it's a known Python package
    print("STEP 5: Check known Python packages")
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
    print(f"'{package_lower}' in known_python_packages: {is_known_package}")
    
    if is_known_package:
        print("✅ KNOWN PYTHON PACKAGE!")
        
        # Check exclusions with strong context for known packages
        if exclusion_found:
            print("⚠️  Soft exclusions found, checking context...")
            exclusion_context_patterns = [
                f"java {package_lower}",
                f"php {package_lower}",
                f"ruby {package_lower}",
                f"{package_lower} for java",
                f"{package_lower} for php",
                f"{package_lower} for ruby"
            ]
            
            strong_exclusion_context = []
            for pattern in exclusion_context_patterns:
                if pattern in description:
                    strong_exclusion_context.append(pattern)
            
            print(f"Strong exclusion context found: {strong_exclusion_context}")
            if strong_exclusion_context:
                print("❌ RETURN FALSE: Strong exclusion context for known package")
                return False
            else:
                print("✅ Soft exclusions without strong context - allowing")
        
        print("✅ RETURN TRUE: Known Python package, assume relevant")
        return True
    
    print("❌ Not a known Python package, checking broader context...")
    return False

if __name__ == "__main__":
    result = debug_filtering_logic()
    print()
    print(f"🎯 FINAL RESULT: {result}")