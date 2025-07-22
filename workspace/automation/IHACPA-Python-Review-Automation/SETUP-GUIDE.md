# IHACPA Python Package Review Automation - Setup Guide

## Development Environment Setup

This guide will help you set up the development environment for the IHACPA Python Package Review Automation project.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git (for version control)
- Excel-compatible software for viewing results
- Internet connection for API access

### Required Python Packages
```bash
# Install core dependencies (tested and working)
pip install openpyxl==3.1.5 requests==2.32.4 pytest==8.4.1

# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Note: If pandas has import issues, the application can work with openpyxl alone
```

## Step-by-Step Setup

### 1. Project Directory Setup
```bash
# Create main project directory
mkdir ihacpa-python-review-automation
cd ihacpa-python-review-automation

# Initialize git repository
git init

# Create directory structure
mkdir -p src config data/{input,output,backups} logs tests docs
```

### 2. Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration Files

#### Create `config/settings.yaml`:
```yaml
# Application settings
app:
  name: "IHACPA Python Package Review Automation"
  version: "1.0.0"
  log_level: "INFO"

# Processing settings
processing:
  concurrent_requests: 5
  request_timeout: 30
  retry_attempts: 3
  retry_delay: 2

# Excel settings
excel:
  backup_original: true
  preserve_formatting: true
  header_row: 3

# Output settings
output:
  generate_summary: true
  create_backups: true
  timestamp_files: true
```

#### Create `config/databases.yaml`:
```yaml
# Vulnerability database configurations
databases:
  pypi:
    base_url: "https://pypi.org/pypi"
    api_format: "{base_url}/{package}/json"
    rate_limit: 10  # requests per second
    
  nist_nvd:
    base_url: "https://services.nvd.nist.gov/rest/json/cves/2.0"
    rate_limit: 5
    requires_auth: false
    
  mitre_cve:
    base_url: "https://cve.mitre.org/cgi-bin/cvekey.cgi"
    rate_limit: 3
    requires_auth: false
    
  snyk:
    base_url: "https://security.snyk.io/package/pip"
    rate_limit: 10
    requires_auth: false
    
  exploit_db:
    base_url: "https://www.exploit-db.com/search"
    rate_limit: 5
    requires_auth: false
    
  github:
    base_url: "https://api.github.com"
    rate_limit: 60  # per hour for unauthenticated
    requires_auth: true  # for higher limits
    # token: "your_github_token_here"  # Add your token
```

#### Create `.env` file (for sensitive configurations):
```bash
# API Keys and sensitive configuration
GITHUB_TOKEN=your_github_token_here
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### 4. Requirements File

#### Create `requirements.txt`:
```txt
# Core dependencies for IHACPA Python Package Review Automation
# Tested and working versions as of 2025-07-09

# Essential Excel and data processing
openpyxl==3.1.5
requests==2.32.4

# Data analysis (optional - can work without pandas if needed)
# Note: pandas has dependency issues in some environments
# The application can work with openpyxl alone if needed
pandas>=2.0.0,<3.0.0

# Async HTTP requests for concurrent API calls
aiohttp>=3.8.0
asyncio-throttle>=1.0.0

# Configuration and environment
pyyaml>=6.0.0
python-dotenv>=0.19.0

# Development and testing dependencies
pytest==8.4.1
pytest-asyncio>=0.18.0
black>=21.0.0
flake8>=4.0.0
mypy>=0.900

# Documentation
mkdocs>=1.2.0
mkdocs-material>=8.0.0

# Additional utilities found useful during testing
python-dateutil>=2.8.0
certifi>=2025.0.0
charset-normalizer>=3.0.0
```

### 5. Basic Project Files

#### Create `src/__init__.py`:
```python
"""
IHACPA Python Package Review Automation
"""
__version__ = "1.0.0"
__author__ = "IHACPA Development Team"
```

#### Create basic logging configuration `config/logging.yaml`:
```yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  detailed:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout
    
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/app.log
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  "":  # root logger
    level: DEBUG
    handlers: [console, file]
    propagate: false
    
  aiohttp:
    level: WARNING
    handlers: [file]
    propagate: false
```

## Database API Setup

### 1. NIST NVD
- **No authentication required** for basic usage
- **Rate limit:** 5 requests per 30 seconds
- **Enhanced access:** Register for API key at https://nvd.nist.gov/developers/request-an-api-key

### 2. MITRE CVE
- **No authentication required**
- **Rate limit:** Reasonable usage (2-3 requests per second)
- **Access method:** Web scraping with respectful delays

### 3. SNYK
- **Free tier available** with limited access
- **API access:** Register at https://snyk.io/
- **Rate limit:** Varies by plan

### 4. Exploit Database
- **No authentication required** for basic searches
- **Rate limit:** Reasonable usage
- **Access method:** Web scraping

### 5. GitHub Security Advisories
- **Authentication recommended** for higher rate limits
- **Setup:** Create personal access token at https://github.com/settings/tokens
- **Permissions needed:** `public_repo` (for public repositories)

## Testing Setup

### 1. Create Test Data
```bash
# Create sample test files
mkdir -p tests/data
cp "data/input/sample_packages.xlsx" "tests/data/test_packages.xlsx"
```

### 2. Basic Test Structure
```bash
# Create test files
touch tests/__init__.py
touch tests/test_excel_handler.py
touch tests/test_pypi_client.py
touch tests/test_vulnerability_scanner.py
```

### 3. Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

## Verification Steps

### 1. Test PyPI Access
```python
import requests
response = requests.get("https://pypi.org/pypi/requests/json")
print(f"PyPI API Status: {response.status_code}")
```

### 2. Test Excel Reading
```python
import pandas as pd
df = pd.read_excel("data/input/your_excel_file.xlsx")
print(f"Excel loaded: {len(df)} rows")
```

### 3. Test Configuration Loading
```python
import yaml
with open("config/settings.yaml", 'r') as f:
    config = yaml.safe_load(f)
print(f"Config loaded: {config['app']['name']}")
```

### 4. Test Excel File Analysis (Verified Working)
```python
# Run the provided test script
python simple_excel_test.py

# Expected output (verified 2025-07-09):
# 📊 IHACPA Excel File Analysis
# Sheet names: ['Sheet1', 'Sheet3', 'Sheet2']
# Total rows: 490
# Total columns: 23
# Total packages found: 486
# Header row: 3
# All expected columns: ✅ Present
```

### 5. Test PyPI API Connectivity (Verified Working)
```python
# Quick test
python -c "import requests; r = requests.get('https://pypi.org/pypi/agate/json'); print(f'PyPI API Status: {r.status_code}'); print(f'Package: {r.json()[\"info\"][\"name\"]} v{r.json()[\"info\"][\"version\"]}')"

# Expected output:
# PyPI API Status: 200
# Package: agate v1.13.0
```

## Common Issues and Solutions

### Issue: Pandas Import Errors
```bash
# Problem: "ModuleNotFoundError: No module named 'pandas.util'"
# Solution 1: Use openpyxl-only mode (recommended)
# The application is designed to work without pandas

# Solution 2: Install compatible pandas version
pip install "pandas>=2.0.0,<3.0.0"

# Solution 3: Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Issue: SSL Certificate Errors
```bash
# Solution: Update certificates or add SSL verification
pip install --upgrade certifi
```

### Issue: Excel File Permissions
```bash
# Solution: Ensure Excel file is not open in other applications
# Create backup before processing
```

### Issue: API Rate Limiting
```bash
# Solution: Implement proper delays and retry logic
# Use async processing with throttling
```

### Issue: Memory Usage with Large Files
```bash
# Solution: Process data in chunks
# Use pandas chunk processing for large datasets
```

## Development Workflow

### 1. Daily Setup
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Update dependencies if needed
pip install -r requirements.txt

# Run tests
pytest tests/
```

### 2. Before Committing
```bash
# Format code
black src/

# Run linting
flake8 src/

# Run tests
pytest tests/

# Commit changes
git add .
git commit -m "Your commit message"
```

## Security Considerations

### 1. API Keys
- Store in `.env` file (never commit to git)
- Use environment variables in production
- Rotate keys regularly

### 2. Data Handling
- Backup original Excel files before processing
- Store sensitive vulnerability data securely
- Log access for audit purposes

### 3. Network Security
- Use HTTPS for all API calls
- Verify SSL certificates
- Implement proper error handling for network issues

## Performance Optimization

### 1. Async Processing
```python
# Use asyncio for concurrent API calls
import asyncio
import aiohttp

# Implement rate limiting
from asyncio_throttle import Throttler
```

### 2. Caching
```python
# Cache API responses to avoid repeated calls
import functools
import time

@functools.lru_cache(maxsize=1000)
def cached_api_call(package_name):
    # Implementation
    pass
```

### 3. Memory Management
```python
# Process large files in chunks
chunk_size = 100
for chunk in pd.read_excel(file, chunksize=chunk_size):
    process_chunk(chunk)
```

---

**Setup Complete!** You're now ready to begin development. Refer to the implementation roadmap for the next steps.