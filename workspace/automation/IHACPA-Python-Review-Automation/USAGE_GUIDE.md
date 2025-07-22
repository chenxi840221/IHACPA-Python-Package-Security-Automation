# IHACPA Python Package Review Automation - Usage Guide

## Quick Start (Production Use)

### 1. Navigate to Source Directory
```bash
cd src
```

### 2. Test with Dry Run (Recommended)
```bash
python main.py --input "../02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx" --dry-run
```

### 3. Run for Production
```bash
python main.py --input "../02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx" --output "updated_packages.xlsx"
```

## Copy-Based Processing Logic

The system implements your requested workflow:

1. **Creates a copy** of the input Excel file as the output file
2. **Processes all 486 packages** systematically
3. **Only updates packages needing updates** (those with empty automated fields)
4. **Preserves all original data** - output has same format as input
5. **Generates comparison report** showing exactly what changed

## Date Published Logic

**Important**: Column E (Date Published) shows the publication date for the **current/installed version** (Column C), not the latest available version. This design allows you to:

- See when the version you're currently using was published
- Assess the age of your current installation
- Make informed decisions about version updates
- Understand security timeline for compliance purposes

**Special Cases**:
- If the PyPI version link is not available (404 error or missing data), the field shows **"Not Available"** with red highlighting
- When current version equals latest version, both dates will be identical (correct behavior)
- When current version differs from latest version, dates will be different

**Examples**:
- Current Version (C): `requests 2.29.0` → Date Published (E): `2023-04-26`
- Latest Version (F): `requests 2.32.4` → Latest Release Date (H): `2025-06-09`
- Non-existent Version: `PyYAML 6` → Date Published (E): `Not Available` (red background)

## Color Highlighting System

The system automatically applies color highlighting to changed cells to provide visual feedback about the type of change:

### Color Scheme
- 🔴 **Red (Bright Red Background)** - Security vulnerabilities found or data not available
  - NIST NVD, MITRE CVE, SNYK, Exploit DB results showing vulnerabilities
  - Recommendations containing security warnings
  - "Not Available" fields when PyPI version links are not accessible
  
- 🟢 **Green (Light Green Background)** - Safe results and new data
  - "No vulnerabilities found" results
  - New URLs and safe data additions
  
- 🔵 **Blue (Light Blue Background)** - General updates
  - Requirements/dependencies updates
  - General field modifications
  
- 🟠 **Orange (Light Orange Background)** - Version information
  - Latest version updates
  - Release date changes
  - Current version publication dates
  
- 🟣 **Purple (Light Purple Background)** - GitHub-related additions
  - GitHub URLs and repository information
  - GitHub security advisory data

### Color Report
Each processing run generates a color summary showing:
- Total changes by color type
- Number of affected rows
- Breakdown by field type
- Security risk indicators

## Command Line Options

### Basic Usage
```bash
python main.py --input <excel_file> [OPTIONS]
```

### Key Options

| Option | Description | Example |
|--------|-------------|---------|
| `--input, -i` | Input Excel file (required) | `--input "packages.xlsx"` |
| `--output, -o` | Output Excel file | `--output "updated.xlsx"` |
| `--dry-run` | Test mode - no changes made | `--dry-run` |
| `--verbose, -v` | Detailed logging | `--verbose` |
| `--quiet, -q` | Minimal output | `--quiet` |
| `--config, -c` | Custom configuration | `--config "settings.yaml"` |

### Testing Options (Limited Use)
| Option | Description | Warning |
|--------|-------------|---------|
| `--packages` | Process specific packages | ⚠️ Creates incomplete output |
| `--start-row` | Start from specific row | ⚠️ Creates incomplete output |
| `--end-row` | End at specific row | ⚠️ Creates incomplete output |

### Reporting Options
| Option | Description |
|--------|-------------|
| `--report-only` | Generate analysis report only |
| `--changes-only` | Generate changes comparison only |

## Expected Output

### Processing Time
- **All 486 packages**: ~1-2 minutes
- **Average per package**: ~0.16 seconds
- **Concurrent processing**: Up to 5 packages simultaneously

### Success Metrics
- **Target success rate**: 100%
- **Recent test results**: 486/486 packages processed successfully
- **Error recovery**: Automatic retry with exponential backoff

### Files Generated

#### 1. Updated Excel File
- **Location**: As specified in `--output` parameter
- **Format**: Same as input (490 rows, 23 columns)
- **Content**: All packages preserved, automated fields updated

#### 2. Changes Report
- **Location**: `data/output/changes_report_TIMESTAMP.txt`
- **Content**: Detailed before/after comparison
- **Example**: Shows 78 packages modified with 86 field changes

#### 3. Processing Logs
- **Location**: `logs/ihacpa_automation_TIMESTAMP.log`
- **Content**: Real-time progress, errors, performance metrics

#### 4. Backup Files
- **Location**: `data/backups/`
- **Format**: Timestamped backup of original file

## Troubleshooting

### Common Issues

#### 1. Excel File Cannot Be Opened
**Symptoms**: Output file is corrupted or very small
**Solution**: Ensure timezone compatibility is working
```bash
# Check if fix is applied in excel_handler.py
grep "replace(tzinfo=None)" src/excel_handler.py
```

#### 2. Processing Stops/Fails
**Symptoms**: Processing hangs or errors out
**Solutions**:
- Check internet connection
- Verify Excel file is not open in another program
- Run with `--verbose` for detailed error information

#### 3. Rate Limiting Errors
**Symptoms**: HTTP 429 errors in logs
**Solutions**:
- System automatically handles rate limiting
- Processing may take longer but will complete
- Reduce concurrent requests in configuration if needed

#### 4. Package Not Found
**Symptoms**: Some packages fail to process
**Solutions**:
- Packages may be unlisted on PyPI
- Check package name spelling in Excel file
- Review error logs for specific failures

### Performance Optimization

#### For Faster Processing
```bash
# Use more concurrent requests (be careful with rate limits)
python main.py --input "packages.xlsx" --config "fast_config.yaml"
```

#### For Safer Processing
```bash
# Use slower, more reliable settings
python main.py --input "packages.xlsx" --verbose
```

## Production Workflow

### Recommended Steps

1. **Backup Original File**
   ```bash
   cp "original.xlsx" "backup_$(date +%Y%m%d_%H%M%S).xlsx"
   ```

2. **Test with Dry Run**
   ```bash
   cd src
   python main.py --input "../02-Source-Data/original.xlsx" --dry-run --verbose
   ```

3. **Review Dry Run Output**
   - Check logs for any errors
   - Verify expected number of packages to be processed
   - Confirm no critical issues

4. **Run Production Process**
   ```bash
   python main.py --input "../02-Source-Data/original.xlsx" --output "updated_$(date +%Y%m%d_%H%M%S).xlsx"
   ```

5. **Verify Results**
   - Check output file opens correctly in Excel
   - Review changes report
   - Verify all 486+ packages are present
   - Spot-check a few updated packages

6. **Archive Files**
   ```bash
   # Move files to archive location
   mv updated_*.xlsx /path/to/archive/
   mv data/output/changes_report_*.txt /path/to/archive/
   ```

## Configuration

### Default Configuration
The system uses built-in defaults optimized for 486 packages:
- **Batch size**: 50 packages
- **Concurrent requests**: 5
- **Rate limit delay**: 1-2 seconds
- **Retry attempts**: 3
- **Request timeout**: 30 seconds

### Custom Configuration
Create `config/settings.yaml`:
```yaml
processing:
  batch_size: 50
  concurrent_requests: 5
  rate_limit_delay: 1.5
  retry_attempts: 3
  request_timeout: 30

logging:
  level: "INFO"
  max_file_size: "10MB"
  backup_count: 5

output:
  create_reports: true
  backup_files: true
```

## Security Considerations

### Data Handling
- Input files may contain sensitive package information
- Vulnerability data includes security details
- Ensure proper access controls on output files

### API Usage
- System makes requests to public APIs (PyPI, NIST NVD, etc.)
- Rate limiting is automatically applied
- No authentication tokens required for basic usage

### Network Requirements
- Internet connection required for API access
- HTTPS connections to security databases
- May be blocked by restrictive firewalls

## Support and Maintenance

### Log Analysis
```bash
# View recent processing logs
tail -f logs/ihacpa_automation_*.log

# Search for errors
grep -i error logs/ihacpa_automation_*.log

# Check processing statistics
grep -i "success rate" logs/ihacpa_automation_*.log
```

### Performance Monitoring
```bash
# Check processing times
grep -i "processing time" logs/ihacpa_automation_*.log

# Monitor memory usage during processing
top -p $(pgrep -f "python main.py")
```

### Regular Maintenance
- Archive old log files monthly
- Clean up backup files after verification
- Update dependencies quarterly
- Monitor API endpoints for changes

---

**Last Updated**: July 9, 2025  
**Tested Version**: 1.0  
**Test Results**: 486/486 packages processed successfully (100% success rate)