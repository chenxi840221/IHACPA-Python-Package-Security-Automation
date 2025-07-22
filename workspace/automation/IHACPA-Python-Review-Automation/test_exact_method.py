#!/usr/bin/env python3
"""
Test exact copy of the enhanced method
"""

def _is_mitre_cve_relevant_enhanced_exact(package_name: str, cve_info: dict) -> bool:
    """Exact copy of enhanced relevance check for MITRE CVE data with improved filtering"""
    description = cve_info.get('description', '').lower()
    package_lower = package_name.lower()
    
    # First, check for explicit Python package indicators (high confidence)
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
    
    if any(indicator in description for indicator in python_indicators):
        return True
    
    # Check for hard exclusion patterns - these definitely indicate it's NOT the Python package
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
        f"android",                # Android specific
        f"ios"                     # iOS specific
    ]
    
    # If any hard exclusion is found, definitely not the Python package
    if any(pattern in description for pattern in hard_exclusions):
        return False
    
    # Soft exclusions - check with more context
    soft_exclusions = ["java", "php", "ruby", "perl", "golang", "node", "npm", ".net"]
    exclusion_found = any(excl in description for excl in soft_exclusions)
    
    # For package name mentions, apply different logic based on package type
    if package_lower in description:
        # For very common words that often appear in non-Python contexts, require explicit Python context
        very_common_words = ['regex', 'json', 'xml', 'html', 'http', 'url', 'file', 'time', 'date', 'math', 'test', 'mock']
        
        if package_lower == 'zipp':
            # Special zipp handling...
            return True  # Simplified for this test
        
        elif package_lower in very_common_words:
            # Would call _has_explicit_python_context, but we'll return False for this test
            print(f"⚠️  {package_lower} is in very_common_words - would check explicit Python context")
            return False
        
        # For known Python packages, be more permissive (unless hard exclusions apply)
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
        
        if package_lower in known_python_packages:
            print(f"✓ {package_lower} found in known_python_packages")
            # For known Python packages, only exclude if soft exclusions with strong context
            if exclusion_found:
                print("⚠️  Exclusions found, checking context...")
                # Check if the exclusion has strong context (not just a passing mention)
                exclusion_context_patterns = [
                    f"java {package_lower}",
                    f"php {package_lower}",
                    f"ruby {package_lower}",
                    f"{package_lower} for java",
                    f"{package_lower} for php",
                    f"{package_lower} for ruby"
                ]
                if any(pattern in description for pattern in exclusion_context_patterns):
                    print("❌ Strong exclusion context found")
                    return False
            print("✅ Returning True for known Python package")
            # For known Python packages, assume relevant unless hard exclusions
            return True
        
        print(f"⚠️  {package_lower} not in known_python_packages, checking broader context...")
        # Continue with broader context logic...
        
    print("❌ Returning False - end of method")
    return False

if __name__ == "__main__":
    cve_info = {
        'cve_id': 'CVE-2024-53861',
        'description': 'pyjwt is a JSON Web Token implementation in Python. An incorrect string comparison is run for iss checking, resulting in acb being accepted for _abc_. This is a bug introduced in version 2.1'
    }
    
    print("Testing exact method copy:")
    result = _is_mitre_cve_relevant_enhanced_exact('PyJWT', cve_info)
    print(f"\nFinal result: {result}")