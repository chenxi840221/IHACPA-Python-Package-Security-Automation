#!/usr/bin/env python3
"""
Simple debug script to check scanner result format
"""

import sys
import os
import asyncio
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_scanner import VulnerabilityScanner

async def simple_test():
    """Simple test to see the exact result format"""
    print("=== Simple Scanner Test ===")
    scanner = VulnerabilityScanner()
    
    try:
        print("Testing requests...")
        result = await scanner.scan_all_databases('requests', current_version='2.31.0')
        
        print("\n=== RESULT STRUCTURE ===")
        print(f"Type: {type(result)}")
        print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict):
            for db, db_result in result.items():
                if isinstance(db_result, dict):
                    print(f"\n{db}:")
                    print(f"  Type: {type(db_result)}")
                    print(f"  Keys: {list(db_result.keys())}")
                    if 'summary' in db_result:
                        print(f"  Summary: {db_result['summary']}")
                    if 'vulnerability_count' in db_result:
                        print(f"  Count: {db_result['vulnerability_count']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await scanner.close()

if __name__ == "__main__":
    asyncio.run(simple_test())