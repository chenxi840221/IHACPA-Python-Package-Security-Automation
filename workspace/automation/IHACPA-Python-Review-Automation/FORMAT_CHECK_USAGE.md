# Format Check and Fix Functionality

The IHACPA Python Review Automation now includes comprehensive format checking and fixing capabilities to ensure consistent Excel formatting across all vulnerability results.

## Overview

The format check functionality automatically detects and fixes formatting issues in security-related columns (M, P, R, T, V) to ensure:
- Proper color coding (red for security risks, green for safe results)
- Consistent font styling (bold text with correct colors)
- Preserved alignment and wrap text settings

## Usage

### Command Line Options

#### 1. Format Check Only (Dry Run)
```bash
python src/main.py --input "your_file.xlsx" --format-check-only
```
- Reports formatting issues without making changes
- Generates detailed report showing what needs fixing
- Safe to run anytime

#### 2. Format Check with Fixes
```bash
python src/main.py --input "your_file.xlsx" --format-check
```
- Detects and fixes formatting issues
- Creates backup before making changes
- Saves corrected file

#### 3. Format Check During Processing
```bash
python src/main.py --input "your_file.xlsx" --format-check
```
- Runs format check after processing packages
- Ensures all new and existing data has correct formatting
- Recommended for production runs

### Python API

```python
# Initialize automation
automation = IHACPAAutomation(config, dry_run=False)
automation.setup("input.xlsx", "output.xlsx")

# Run format check only (dry run)
results = automation.run_format_check(fix=False)

# Run format check with fixes
results = automation.run_format_check(fix=True)
```

## What Gets Checked

### Security Fields
- **Column M**: GitHub Security Advisory Result
- **Column P**: NIST NVD Lookup Result  
- **Column R**: MITRE CVE Lookup Result
- **Column T**: SNYK Vulnerability Lookup Result
- **Column V**: Exploit Database Lookup Result

### Formatting Rules

#### Security Risk (Red)
- **When**: Contains vulnerability keywords ("found", "security risk", "severity: high", etc.)
- **Fill Color**: Light red (#FFE6E6)
- **Font Color**: Dark red (#CC0000)
- **Font**: Bold

#### Safe Results (Green)
- **When**: Contains safe keywords ("none found", "no vulnerabilities", etc.)
- **Fill Color**: Light green (#E6FFE6)
- **Font Color**: Dark green (#006600)
- **Font**: Bold

#### General Updates (Blue)
- **When**: General content updates
- **Fill Color**: Light blue (#E6F3FF)
- **Font Color**: Dark blue (#0066CC)
- **Font**: Bold

## Common Issues Fixed

### 1. NIST NVD Column P Issues
- **Problem**: Packages with vulnerability text showing green instead of red
- **Fix**: Automatically detects "Found X vulnerabilities" and applies red security risk formatting

### 2. Font Color Problems
- **Problem**: Incorrect font colors (green instead of red for security risks)
- **Fix**: Applies correct font colors based on content analysis

### 3. Missing Bold Formatting
- **Problem**: Security results not showing as bold text
- **Fix**: Ensures all security-related content is properly bolded

### 4. Alignment Issues
- **Problem**: Lost wrap text or center alignment
- **Fix**: Preserves existing alignment while updating colors and fonts

## Reports Generated

### 1. Format Check Report
```
IHACPA FORMAT CHECK REPORT
==========================================================
Generated: 2025-07-10 15:30:45
Excel file: /path/to/your/file.xlsx

SUMMARY:
------------------------------
Total packages checked: 486
Formatting issues found: 16
Fixes applied: 16

ISSUES BY COLUMN:
------------------------------
nist_nvd_result: 16 issues

DETAILED FIXES BY PACKAGE:
------------------------------
📦 psutil (Row 289):
  🔧 nist_nvd_result - FIXED
     Value: Found 2 vulnerabilities in NIST NVD
     Expected format: security_risk
     Issues: fill_color: 000000 → FFE6E6, font_color: 006100 → CC0000, bold: False → True
```

### 2. Log Output
```
2025-07-10 15:30:45 - main - INFO - 🔍 Running format check...
2025-07-10 15:30:45 - excel_handler - INFO - Format check completed: 486 packages checked, 16 issues found, 16 fixes applied
2025-07-10 15:30:45 - main - INFO - 📊 Format check completed:
2025-07-10 15:30:45 - main - INFO -    Packages checked: 486
2025-07-10 15:30:45 - main - INFO -    Issues found: 16
2025-07-10 15:30:45 - main - INFO -    Fixes applied: 16
2025-07-10 15:30:45 - main - INFO -    Issues by column:
2025-07-10 15:30:45 - main - INFO -      nist_nvd_result: 16 issues
2025-07-10 15:30:45 - main - INFO -    Detailed report: data/output/format_check_report_20250710_153045.txt
```

## Best Practices

### 1. Regular Format Checks
- Run format check after any manual Excel modifications
- Include format check in automated processing workflows

### 2. Backup Strategy
- Format check with fixes automatically creates backups
- Keep backup files for recovery if needed

### 3. Validation
- Always run format check only (dry run) first on important files
- Review the report before applying fixes

### 4. Integration
- Use `--format-check` flag in production automation runs
- Ensures consistent formatting across all processing

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Ensure Excel file is not open in another application
   - Check file permissions

2. **Memory Issues**
   - Large files may require more memory
   - Close other applications if needed

3. **Format Detection**
   - Review content keywords if format detection seems incorrect
   - Check logs for specific field analysis

### Debug Mode
```bash
python src/main.py --input "your_file.xlsx" --format-check-only --verbose
```

## Examples

### Example 1: Check Specific Issues
```bash
# Check for formatting issues without fixing
python src/main.py --input "packages.xlsx" --format-check-only
```

### Example 2: Fix Known Issues
```bash
# Fix the NIST NVD column P issues we identified
python src/main.py --input "packages.xlsx" --format-check
```

### Example 3: Full Processing with Format Check
```bash
# Process packages and ensure proper formatting
python src/main.py --input "packages.xlsx" --output "updated_packages.xlsx" --format-check
```

## Technical Details

### Format Detection Logic
1. **Content Analysis**: Scans cell values for security keywords
2. **Current Formatting**: Reads existing font colors, fill colors, and bold settings
3. **Comparison**: Compares current vs expected formatting
4. **Fix Application**: Applies correct formatting while preserving alignment

### Supported Formats
- **Excel 2007+** (.xlsx files)
- **openpyxl** library for Excel manipulation
- **Color formats**: RGB hex codes
- **Font properties**: Color, bold, size, name
- **Alignment**: Wrap text, horizontal, vertical

This format check functionality ensures consistent, professional appearance of your vulnerability analysis results while maintaining data integrity and readability.