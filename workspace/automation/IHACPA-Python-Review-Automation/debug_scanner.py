#!/usr/bin/env python3
"""
Debug script to investigate scanner accuracy issues
"""

import sys
import os
import asyncio
import logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner, SynchronousVulnerabilityScanner

# Configure logging
logging.basicConfig(level=logging.DEBUG)

async def debug_async_scanner():
    """Debug the async scanner directly"""
    print("=== Testing Async Scanner ===")
    scanner = VulnerabilityScanner()
    
    try:
        print("\n1. Testing NIST NVD for 'requests'...")
        nist_result = await scanner.scan_nist_nvd('requests', '2.31.0')
        print(f"NIST Result: {nist_result}")
        
        print("\n2. Testing MITRE CVE for 'requests'...")  
        mitre_result = await scanner.scan_mitre_cve('requests', '2.31.0')
        print(f"MITRE Result: {mitre_result}")
        
        print("\n3. Testing SNYK for 'requests'...")
        snyk_result = await scanner.scan_snyk('requests', '2.31.0')
        print(f"SNYK Result: {snyk_result}")
        
        print("\n4. Testing scan_all_databases for 'requests'...")
        all_result = await scanner.scan_all_databases('requests', current_version='2.31.0')
        print(f"All Databases Result: {all_result}")
        
    except Exception as e:
        print(f"Async scanner error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

def debug_sync_scanner():
    """Debug the synchronous scanner"""
    print("\n=== Testing Synchronous Scanner ===")
    scanner = SynchronousVulnerabilityScanner()
    
    try:
        print("\n1. Testing scan_package for 'requests'...")
        result = scanner.scan_package('requests', current_version='2.31.0')
        print(f"Sync Scanner Result: {result}")
        
        # Extract individual scanner results
        if isinstance(result, dict):
            print(f"\nNIST NVD: {result.get('nist_nvd', 'Not found')}")
            print(f"MITRE CVE: {result.get('mitre_cve', 'Not found')}")
            print(f"SNYK: {result.get('snyk', 'Not found')}")
            print(f"Exploit DB: {result.get('exploit_db', 'Not found')}")
            print(f"GitHub Advisory: {result.get('github_advisory', 'Not found')}")
        
    except Exception as e:
        print(f"Sync scanner error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        scanner.close()

async def main():
    """Main debug function"""
    print("DEBUG: Investigating Scanner Accuracy Issues")
    print("=" * 60)
    
    # Test async scanner
    await debug_async_scanner()
    
    # Test sync scanner  
    debug_sync_scanner()
    
    print("\nDEBUG COMPLETED")

if __name__ == "__main__":
    asyncio.run(main())