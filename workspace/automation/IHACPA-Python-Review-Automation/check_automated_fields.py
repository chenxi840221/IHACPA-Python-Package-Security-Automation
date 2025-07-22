import pandas as pd
import os

# Read the Excel file
file_path = '/mnt/c/workspace/IHACPA-Python-Review-Automation-Complete/IHACPA-Python-Review-Automation-Complete/02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx'
df = pd.read_excel(file_path)

# Packages to check with their row numbers (Excel rows, so subtract 1 for 0-based index)
packages_to_check = {
    'PyQt5': 322,  # Row 323 in Excel
    'PyQtWebEngine': 324,  # Row 325 in Excel
    'ruamel.yaml': 376,  # Row 377 in Excel
    'Unidecode': 453  # Row 454 in Excel
}

# Automated columns (E through W)
automated_columns = [
    'date_published',
    'latest_version',
    'pypi_latest_link',
    'latest_release_date',
    'requires',
    'development_status',
    'github_url',
    'github_advisory_url',
    'github_advisory_result',
    'nist_nvd_url',
    'nist_nvd_result',
    'mitre_cve_url',
    'mitre_cve_result',
    'snyk_url',
    'snyk_result',
    'exploit_db_url',
    'exploit_db_result',
    'recommendation'
]

print("Checking automated fields for specified packages:\n")
print("=" * 80)

for package_name, excel_row in packages_to_check.items():
    print(f"\nPackage: {package_name} (Excel Row {excel_row + 1})")
    print("-" * 40)
    
    # Get the row data
    row_idx = excel_row
    if row_idx < len(df):
        row_data = df.iloc[row_idx]
        
        # Check if package name matches
        actual_package = row_data.get('package_name', 'N/A')
        if pd.notna(actual_package):
            print(f"Actual package in row: {actual_package}")
        
        # Check each automated field
        populated_fields = []
        empty_fields = []
        
        for col in automated_columns:
            if col in df.columns:
                value = row_data.get(col)
                if pd.notna(value) and str(value).strip() != '':
                    populated_fields.append(f"{col}: {value}")
                else:
                    empty_fields.append(col)
            else:
                empty_fields.append(f"{col} (column not found)")
        
        if populated_fields:
            print("\nPopulated fields:")
            for field in populated_fields:
                print(f"  - {field}")
        else:
            print("\nNo populated automated fields found.")
        
        if empty_fields:
            print(f"\nEmpty fields: {', '.join(empty_fields)}")
    else:
        print(f"Row index {row_idx} is out of range for the dataframe.")

print("\n" + "=" * 80)
print("\nSummary:")
print(f"Total rows in Excel: {len(df)}")
print(f"Columns in Excel: {list(df.columns)}")