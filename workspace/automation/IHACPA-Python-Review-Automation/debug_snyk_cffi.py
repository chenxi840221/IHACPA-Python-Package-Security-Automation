#!/usr/bin/env python3
"""
Debug script for SNYK cffi HTML parsing
"""

import sys
import os
import asyncio
import aiohttp
from urllib.parse import quote

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def debug_snyk_cffi():
    """Debug SNYK HTML parsing for cffi package"""
    package_name = "cffi"
    
    print("🔍 DEBUGGING SNYK HTML PARSING FOR CFFI")
    print("=" * 60)
    print(f"Package: {package_name}")
    print()
    
    # Build SNYK URL
    search_url = f"https://security.snyk.io/package/pip/{package_name.lower()}"
    print(f"📡 SNYK URL: {search_url}")
    print()
    
    # Set headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    try:
        # Fetch the SNYK page
        async with aiohttp.ClientSession() as session:
            print("🌐 Fetching SNYK page...")
            async with session.get(search_url, headers=headers, timeout=30) as response:
                print(f"📊 Response Status: {response.status}")
                print(f"📊 Content-Type: {response.headers.get('content-type', 'Unknown')}")
                print()
                
                if response.status == 200:
                    html_content = await response.text()
                    print(f"📄 HTML Content Length: {len(html_content)} characters")
                    print()
                    
                    # Show first part of HTML content
                    print("📝 HTML CONTENT PREVIEW (first 1000 chars):")
                    print("-" * 50)
                    print(html_content[:1000])
                    print("-" * 50)
                    print()
                    
                    # Check for key indicators
                    print("🔍 SEARCHING FOR KEY PATTERNS:")
                    
                    # Common vulnerability patterns
                    patterns_to_check = [
                        'vulnerability', 'vuln', 'CVE-', 'SNYK-', 
                        'security', 'issue', 'advisory', 'alert',
                        'cffi', 'severity', 'critical', 'high', 'medium', 'low'
                    ]
                    
                    found_patterns = []
                    for pattern in patterns_to_check:
                        if pattern.lower() in html_content.lower():
                            count = html_content.lower().count(pattern.lower())
                            found_patterns.append(f"{pattern}: {count}")
                    
                    if found_patterns:
                        print("✅ Found patterns:")
                        for pattern in found_patterns[:10]:  # Show first 10
                            print(f"  - {pattern}")
                    else:
                        print("❌ No vulnerability-related patterns found")
                    
                    print()
                    
                    # Test the parsing method
                    print("🧪 TESTING SNYK HTML PARSER:")
                    scanner = VulnerabilityScanner()
                    vulnerabilities = scanner._parse_snyk_html(html_content, package_name)
                    
                    print(f"📊 Parsed vulnerabilities: {len(vulnerabilities)}")
                    
                    if vulnerabilities:
                        print("✅ FOUND VULNERABILITIES:")
                        for i, vuln in enumerate(vulnerabilities, 1):
                            print(f"  {i}. {vuln}")
                    else:
                        print("❌ NO VULNERABILITIES PARSED")
                        print()
                        print("🔍 DEBUGGING PARSE METHODS:")
                        
                        # Try to debug why parsing failed
                        from bs4 import BeautifulSoup
                        import re
                        
                        soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # Check for vulnerability sections
                        vuln_sections = soup.find_all(['div', 'article', 'section'], class_=re.compile(r'vuln|vulnerability|issue'))
                        print(f"  Found {len(vuln_sections)} potential vulnerability sections")
                        
                        # Check for table rows
                        vuln_rows = soup.find_all('tr')
                        print(f"  Found {len(vuln_rows)} table rows")
                        
                        # Check for common SNYK elements
                        common_selectors = [
                            'div[class*="vulnerability"]',
                            'div[class*="vuln"]',
                            'div[class*="issue"]',
                            'div[data-testid*="vuln"]',
                            '.vulnerability',
                            '.vuln-card',
                            '.issue-card'
                        ]
                        
                        for selector in common_selectors:
                            try:
                                elements = soup.select(selector)
                                if elements:
                                    print(f"  Found {len(elements)} elements with selector: {selector}")
                            except Exception as e:
                                print(f"  Error with selector {selector}: {e}")
                    
                    await scanner.close()
                    
                else:
                    print(f"❌ Failed to fetch SNYK page: HTTP {response.status}")
                    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_snyk_cffi())