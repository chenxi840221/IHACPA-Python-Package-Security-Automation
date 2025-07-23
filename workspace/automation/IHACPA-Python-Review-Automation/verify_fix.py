#!/usr/bin/env python3
"""
Quick verification that the NIST NVD fix works correctly
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

# Test packages to verify fix doesn't break anything
VERIFY_PACKAGES = [
    ('openpyxl', '3.1.2'),      # The fixed package
    ('requests', '2.31.0'),     # Should still work
    ('flask', '2.3.2'),         # Should still work
    ('xlsxwriter', '3.1.2'),    # Another Excel package 
    ('tabulate', '0.9.0')       # Should correctly filter WordPress
]

async def verify_fix():
    """Quick verification of the fix"""
    print("=== VERIFYING NIST NVD FIX ===")
    scanner = VulnerabilityScanner()
    
    try:
        for package_name, version in VERIFY_PACKAGES:
            print(f"\n📦 {package_name} v{version}:")
            result = await scanner.scan_nist_nvd(package_name, version)
            summary = result.get('summary', 'No summary')
            count = result.get('vulnerability_count', 0)
            print(f"   Result: {summary}")
            print(f"   Count: {count}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(verify_fix())