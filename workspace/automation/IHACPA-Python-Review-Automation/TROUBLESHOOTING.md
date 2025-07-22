# Troubleshooting Guide

This guide covers common issues and their solutions for the IHACPA Python Package Review Automation system v1.5.0.

## Common Issues and Solutions

### 1. Azure OpenAI Configuration Issues

#### Error: "Azure OpenAI key not configured"
```bash
2025-07-10 15:30:45 - ai_cve_analyzer - ERROR - Azure OpenAI key not configured
```

**Solution:**
1. Set environment variables:
   ```bash
   export AZURE_OPENAI_KEY="your-azure-api-key"
   export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
   export AZURE_OPENAI_MODEL="gpt-4.1"
   export AZURE_OPENAI_API_VERSION="2025-01-01-preview"
   ```

2. Or create a `.env` file:
   ```env
   AZURE_OPENAI_KEY=your-azure-api-key-here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_MODEL=gpt-4.1
   AZURE_OPENAI_API_VERSION=2025-01-01-preview
   ```

#### Error: "HTTP Request: POST ... '429 Too Many Requests'"
```bash
httpx - INFO - HTTP Request: POST ... "HTTP/1.1 429 Too Many Requests"
```

**Solution:**
- Azure OpenAI rate limit exceeded
- Wait a few minutes and retry
- Consider upgrading your Azure OpenAI pricing tier
- The system will automatically retry with exponential backoff

#### Error: "Deployment 'gpt-4.1' not found"
```bash
ai_cve_analyzer - ERROR - Deployment 'gpt-4.1' not found
```

**Solution:**
- Check your Azure OpenAI deployment name in Azure Portal
- Update the `AZURE_OPENAI_MODEL` environment variable to match your deployment name
- Common deployment names: `gpt-4`, `gpt-4-turbo`, `gpt-4.1`

### 2. Excel File Issues

#### Error: "Excel file not found"
```bash
Error: Input file not found: /path/to/file.xlsx
```

**Solution:**
- Check the file path is correct and absolute
- Ensure the Excel file exists and is accessible
- Use quotes around file paths with spaces

#### Error: "Permission denied" when saving Excel file
```bash
excel_handler - ERROR - Error saving Excel file: Permission denied
```

**Solution:**
- Close the Excel file if it's open in Excel or another application
- Check file write permissions
- Ensure the directory exists and is writable
- Run as administrator if necessary (Windows)

#### Error: "'RGB' object is not subscriptable"
```bash
excel_handler - ERROR - Error in format check: 'RGB' object is not subscriptable
```

**Solution:**
- This was fixed in v1.4.0
- Update to the latest version
- If still occurring, the Excel file may have corrupted color formatting

### 3. Network and API Issues

#### Error: "Connection timeout" for PyPI or vulnerability databases
```bash
pypi_client - ERROR - Request timeout for package 'requests'
```

**Solution:**
- Check internet connection
- Try again later (temporary network issues)
- Some packages may have network-related names causing DNS conflicts
- The system will continue with other packages

#### Error: "SSL Certificate verification failed"
```bash
aiohttp.client_exceptions.ClientConnectorSSLError: SSL
```

**Solution:**
- Update certificates: `pip install --upgrade certifi`
- Corporate firewall/proxy may be interfering
- Try running from a different network environment

### 4. Format Check Issues

#### Error: "Format check failed: No worksheet loaded"
```bash
excel_handler - ERROR - Format check failed: No worksheet loaded
```

**Solution:**
- Ensure Excel file is loaded before running format check
- Check if the Excel file is corrupted
- Try opening the file manually in Excel first

#### Warning: "Font color issues in column P"
```bash
Issues found in NIST NVD column: incorrect green colors instead of red
```

**Solution:**
- Run format check: `python main.py --input "file.xlsx" --format-check`
- This was addressed in v1.4.0 with the comprehensive format check system

### 5. Processing Issues

#### Error: "Package processing failed"
```bash
automation - ERROR - Package processing failed
```

**Solution:**
- Check the error details in the log file
- Try processing with `--dry-run` first
- Check if specific packages are causing issues
- Verify internet connectivity for API calls

#### Warning: "Could not retrieve publication date"
```bash
Could not retrieve publication date for package_name v1.0.0
```

**Solution:**
- This is expected for some packages
- The system will mark it as "Not Available"
- Not a critical error - processing continues

### 6. Memory and Performance Issues

#### Error: "MemoryError" or system runs slowly
```bash
MemoryError: Unable to allocate array
```

**Solution:**
- Close other applications to free memory
- Process packages in smaller batches using `--start-row` and `--end-row`
- Increase virtual memory/swap space
- Consider running on a machine with more RAM

#### Performance: Processing takes too long
**Solution:**
- Use `--packages` to test specific packages first
- Check internet connection speed
- Azure OpenAI calls add processing time but provide valuable analysis
- Consider processing during off-peak hours

### 7. Command Line Issues

#### Error: "Command not found: python"
```bash
bash: python: command not found
```

**Solution:**
- Try `python3` instead of `python`
- Ensure Python is installed and in PATH
- On Windows, try `py` command

#### Error: "No module named 'src'"
```bash
ModuleNotFoundError: No module named 'src'
```

**Solution:**
- Navigate to the `src` directory first: `cd src`
- Or run from project root: `python -m src.main`
- Ensure you're in the correct directory

### 8. Configuration Issues

#### Error: "Configuration file not found"
```bash
config - ERROR - Configuration file not found: config.yaml
```

**Solution:**
- Configuration file is optional
- The system uses default configuration if none provided
- Create a custom config file if needed (see CONFIGURATION_REFERENCE.md)

### 9. Dependency Issues

#### Error: "ModuleNotFoundError: No module named 'openpyxl'"
```bash
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution:**
- Install dependencies: `pip install -r requirements.txt`
- Or install specific package: `pip install openpyxl==3.1.5`
- Use virtual environment to avoid conflicts

## Diagnostic Commands

### Check System Status
```bash
# Test AI integration
python test_format_check.py

# Test with dry run
python main.py --input "file.xlsx" --dry-run --packages requests

# Check specific functionality
python main.py --input "file.xlsx" --format-check-only
```

### Debug Mode
```bash
# Run with verbose logging
python main.py --input "file.xlsx" --verbose

# Check logs
tail -f logs/ihacpa_automation_$(date +%Y%m%d).log
```

## Log File Locations

- **Application Logs**: `logs/ihacpa_automation_YYYYMMDD.log`
- **Error Logs**: Included in main log file with ERROR level
- **Reports**: `data/output/`
- **Backups**: Created in same directory as output file

## Performance Benchmarks

### Expected Processing Times
- **Single Package**: 2-5 seconds (with AI analysis)
- **10 Packages**: 30-60 seconds
- **100 Packages**: 5-10 minutes
- **All 486 Packages**: 20-40 minutes (depending on network and AI response times)

### Memory Usage
- **Typical Usage**: 100-200 MB RAM
- **Peak Usage**: 500 MB RAM (large Excel files)
- **Recommended**: 2+ GB available RAM

## When to Contact Support

Contact support if you encounter:
- Persistent Azure OpenAI authentication issues
- Consistent processing failures across multiple packages
- Data corruption or loss
- Security-related concerns

## Version-Specific Issues

### v1.4.0+
- Format check functionality added
- Improved color extraction methods
- Enhanced error handling

### v1.3.0+
- Quad AI integration completed
- Enhanced font color system
- Comprehensive vulnerability analysis

### Earlier Versions
- Consider upgrading to latest version for bug fixes and new features

## Quick Fixes Checklist

When encountering issues, try these steps in order:

1. ✅ **Check file paths** - Ensure input file exists and is accessible
2. ✅ **Verify dependencies** - Run `pip install -r requirements.txt`
3. ✅ **Test network** - Check internet connectivity
4. ✅ **Check Azure OpenAI** - Verify API key and endpoint configuration
5. ✅ **Close Excel** - Ensure Excel file isn't open in another application
6. ✅ **Check permissions** - Verify file read/write permissions
7. ✅ **Try dry run** - Test with `--dry-run` first
8. ✅ **Check logs** - Review log files for detailed error messages
9. ✅ **Restart** - Try restarting the application
10. ✅ **Update** - Ensure you're using the latest version

## Getting Help

- **Documentation**: Check README.md and other documentation files
- **Logs**: Always include relevant log entries when reporting issues
- **Test Cases**: Provide specific package names or scenarios that fail
- **Environment**: Include Python version, OS, and dependency versions