#!/usr/bin/env python3
"""
Test script to fix NIST NVD color formatting for specific packages
"""

import sys
import shutil
sys.path.append('src')

from excel_handler import ExcelHandler

def test_nist_nvd_color_fix():
    """Test fixing NIST NVD color formatting for problematic packages"""
    
    print('🔧 Testing NIST NVD Color Fix')
    print('=' * 60)
    
    # Create a copy of the source file for testing
    source_file = "02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx"
    test_file = "test_nist_nvd_color_fix.xlsx"
    
    try:
        shutil.copy2(source_file, test_file)
        print(f'📋 Created test file: {test_file}')
        
        # Load the test file
        handler = ExcelHandler(test_file)
        if not handler.load_workbook():
            print("❌ Failed to load test file")
            return
        
        # Problematic packages that need color fixing
        problematic_packages = ['psutil', 'py', 'pyarrow', 'requests', 'rope', 'sas7bdat', 'seaborn', 'shap', 'sip', 'Sphinx', 'sqlparse', 'tabulate', 'TBB', 'toml', 'tomli', 'zstandard']
        
        print(f'🔍 Finding and fixing problematic packages...')
        
        packages_fixed = []
        
        # Get all packages and find the problematic ones
        packages = handler.get_all_packages()
        
        for package in packages:
            package_name = package.get('package_name', '')
            
            if package_name in problematic_packages:
                row_number = package.get('row_number', 0)
                current_nist_result = package.get('nist_nvd_result', '')
                
                if current_nist_result and 'found' in current_nist_result.lower() and 'vulnerabilities' in current_nist_result.lower():
                    print(f'🔧 Fixing {package_name} (Row {row_number}): {current_nist_result[:50]}...')
                    
                    # "Re-update" the cell with the same value to trigger color formatting
                    updates = {
                        'nist_nvd_result': current_nist_result
                    }
                    
                    success = handler.update_package_data(row_number, updates)
                    if success:
                        packages_fixed.append(package_name)
                        print(f'   ✅ Successfully applied color formatting')
                    else:
                        print(f'   ❌ Failed to apply color formatting')
                else:
                    print(f'🔍 Skipping {package_name} (Row {row_number}): No vulnerability result found')
        
        # Save the file
        if packages_fixed:
            handler.save_workbook(backup=False)
            print(f'\n📊 Summary:')
            print(f'   • Packages fixed: {len(packages_fixed)}')
            print(f'   • Fixed packages: {", ".join(packages_fixed)}')
            
            # Get color statistics
            stats = handler.get_color_statistics()
            print(f'   • Total changes applied: {stats["total_changes"]}')
            print(f'   • Security risk cells: {stats["color_breakdown"].get("security_risk", 0)}')
            
            print(f'\n✅ Test completed! Check {test_file} for corrected formatting.')
            print('Expected changes:')
            print('   • Fill Color: Light red background (FFE6E6)')
            print('   • Font Color: Dark red text (CC0000)')
            print('   • Font Bold: True')
            print('   • Wrap Text: Preserved')
            print('   • Alignment: Center (preserved)')
            
        else:
            print('\n⚠️  No packages were fixed. Check if the NIST NVD results contain the expected text.')
        
        handler.close()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_nist_nvd_color_fix()