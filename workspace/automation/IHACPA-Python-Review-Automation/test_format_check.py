#!/usr/bin/env python3
"""
Test script to demonstrate the format check and fix functionality
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import IHACPAAutomation
from src.config import Config

async def test_format_check():
    """Test the format check functionality"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🧪 Testing Format Check Functionality")
    print("=" * 60)
    
    # Use default config
    config = Config()
    
    # Initialize automation
    automation = IHACPAAutomation(config, dry_run=False)
    
    try:
        # Setup with source file
        input_file = "02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx"
        output_file = "format_check_test.xlsx"
        
        if not automation.setup(input_file, output_file):
            print("❌ Failed to setup automation")
            return False
        
        print(f"📊 Loaded Excel file: {input_file}")
        print(f"📊 Output file: {output_file}")
        
        # Test 1: Format check only (dry run)
        print("\n🔍 Test 1: Format check only (dry run)")
        print("-" * 40)
        
        success = automation.run_format_check(fix=False)
        if not success:
            print("❌ Format check failed")
            return False
        
        print("✅ Format check (dry run) completed successfully")
        
        # Test 2: Format check with fixes
        print("\n🔧 Test 2: Format check with fixes")
        print("-" * 40)
        
        success = automation.run_format_check(fix=True)
        if not success:
            print("❌ Format check with fixes failed")
            return False
        
        print("✅ Format check with fixes completed successfully")
        
        # Save the results
        if automation.excel_handler:
            automation.excel_handler.save_workbook(backup=True)
            print(f"💾 Results saved to: {output_file}")
        
        print("\n🎉 All format check tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during format check test: {e}")
        return False
    finally:
        await automation.cleanup()

if __name__ == "__main__":
    success = asyncio.run(test_format_check())
    sys.exit(0 if success else 1)