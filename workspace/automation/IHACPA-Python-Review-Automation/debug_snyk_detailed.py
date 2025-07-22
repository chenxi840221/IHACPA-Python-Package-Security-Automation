#!/usr/bin/env python3
"""
Detailed debug script for SNYK vulnerability extraction patterns
"""

import sys
import os
import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def debug_snyk_patterns():
    """Debug SNYK vulnerability patterns in detail"""
    package_name = "cffi"
    search_url = f"https://security.snyk.io/package/pip/{package_name.lower()}"
    
    print("🔍 DETAILED SNYK PATTERN ANALYSIS")
    print("=" * 60)
    print()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    print("🧪 EXAMINING VULNERABILITY SECTIONS:")
                    print("-" * 50)
                    
                    # Find vulnerability sections
                    vuln_sections = soup.find_all(['div', 'article', 'section'], class_=re.compile(r'vuln|vulnerability|issue'))
                    
                    print(f"Found {len(vuln_sections)} potential vulnerability sections")
                    print()
                    
                    for i, section in enumerate(vuln_sections[:5], 1):  # Examine first 5
                        section_text = section.get_text().strip()
                        print(f"📋 SECTION {i}:")
                        print(f"Classes: {section.get('class', [])}")
                        print(f"Text length: {len(section_text)} characters")
                        print(f"Text preview: {section_text[:300]}...")
                        print()
                        
                        # Test current patterns
                        cve_pattern = re.compile(r'CVE-\d{4}-\d{4,}')
                        snyk_pattern = re.compile(r'SNYK-[A-Z]+-[A-Z0-9]+-\d+')
                        
                        cve_matches = cve_pattern.findall(section_text)
                        snyk_matches = snyk_pattern.findall(section_text)
                        
                        print(f"Current CVE pattern matches: {cve_matches}")
                        print(f"Current SNYK pattern matches: {snyk_matches}")
                        
                        # Look for all SNYK-like patterns
                        all_snyk_pattern = re.compile(r'SNYK-[A-Za-z0-9-]+')
                        all_snyk_matches = all_snyk_pattern.findall(section_text)
                        print(f"All SNYK-like patterns: {all_snyk_matches}")
                        
                        # Look for severity patterns
                        severity_pattern = re.compile(r'(Critical|High|Medium|Low)', re.IGNORECASE)
                        severity_matches = severity_pattern.findall(section_text)
                        print(f"Severity matches: {severity_matches}")
                        
                        print("-" * 30)
                        print()
                    
                    print("🔍 SEARCHING FULL HTML FOR SNYK PATTERNS:")
                    print("-" * 50)
                    
                    # Search for all SNYK ID patterns in the entire HTML
                    full_text = soup.get_text()
                    
                    # Different SNYK patterns to test
                    snyk_patterns = [
                        r'SNYK-[A-Z]+-[A-Z0-9]+-\d+',  # Original pattern
                        r'SNYK-[A-Za-z]+-[A-Za-z0-9]+-\d+',  # Case insensitive
                        r'SNYK-[A-Z]+-[A-Z0-9-]+-\d+',  # Allow hyphens
                        r'SNYK-\w+-\w+-\d+',  # Word characters
                        r'SNYK-[A-Za-z0-9-]+',  # Any SNYK- pattern
                    ]
                    
                    for pattern_desc, pattern in zip(['Original', 'Case insensitive', 'Allow hyphens', 'Word chars', 'Any SNYK'], snyk_patterns):
                        matches = re.findall(pattern, full_text)
                        unique_matches = list(set(matches))
                        print(f"{pattern_desc}: {len(unique_matches)} unique matches")
                        if unique_matches:
                            print(f"  Examples: {unique_matches[:3]}")
                    
                    print()
                    print("🔍 SEARCHING FOR SPECIFIC VULNERABILITY INDICATORS:")
                    print("-" * 50)
                    
                    # Look for vulnerability cards or containers
                    vuln_indicators = [
                        'div[data-testid*="vulnerability"]',
                        'div[data-testid*="vuln"]',
                        'article[data-testid*="vulnerability"]',
                        'div.vulnerability-card',
                        'div.vuln-card',
                        'tr.vulnerability-row',
                        'div[class*="vulnerability-item"]'
                    ]
                    
                    for indicator in vuln_indicators:
                        try:
                            elements = soup.select(indicator)
                            if elements:
                                print(f"✅ Found {len(elements)} elements: {indicator}")
                                # Show first element content
                                if elements:
                                    first_text = elements[0].get_text().strip()[:200]
                                    print(f"   First element: {first_text}...")
                            else:
                                print(f"❌ No elements found: {indicator}")
                        except Exception as e:
                            print(f"❌ Error with {indicator}: {e}")
                    
                    print()
                    
                else:
                    print(f"❌ Failed to fetch page: {response.status}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_snyk_patterns())