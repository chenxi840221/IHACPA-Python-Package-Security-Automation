# API Reference

Complete API documentation for the IHACPA Python Package Review Automation system.

## Overview

The system is built using a modular architecture with the following main components:

- **ExcelHandler**: Excel file operations and formatting
- **PyPIClient**: PyPI API integration
- **VulnerabilityScanner**: Multi-database vulnerability scanning
- **AICVEAnalyzer**: AI-powered vulnerability analysis
- **IHACPAAutomation**: Main automation orchestrator

## Core Classes

### ExcelHandler

Handles Excel file operations, formatting, and data management.

#### Constructor
```python
ExcelHandler(file_path: str)
```

**Parameters:**
- `file_path` (str): Path to the Excel file

#### Methods

##### load_workbook()
```python
def load_workbook() -> bool
```
Load Excel workbook and get active worksheet.

**Returns:**
- `bool`: True if successful, False otherwise

##### get_package_count()
```python
def get_package_count() -> int
```
Get total number of packages in the Excel file.

**Returns:**
- `int`: Number of packages

##### get_packages_by_range()
```python
def get_packages_by_range(start_row: int, end_row: int) -> List[Dict[str, Any]]
```
Get packages within a specific row range.

**Parameters:**
- `start_row` (int): Starting row number
- `end_row` (int): Ending row number

**Returns:**
- `List[Dict[str, Any]]`: List of package dictionaries

##### update_package_data()
```python
def update_package_data(row_number: int, data: Dict[str, Any]) -> bool
```
Update a package row with new data and apply color highlighting.

**Parameters:**
- `row_number` (int): Row number to update
- `data` (Dict[str, Any]): Data to update

**Returns:**
- `bool`: True if successful, False otherwise

##### check_and_fix_formatting()
```python
def check_and_fix_formatting(dry_run: bool = False) -> Dict[str, Any]
```
Check for formatting issues and optionally fix them.

**Parameters:**
- `dry_run` (bool): If True, only report issues without fixing

**Returns:**
- `Dict[str, Any]`: Results with issues found and fixes applied

##### save_workbook()
```python
def save_workbook(backup: bool = True) -> bool
```
Save the Excel workbook with optional backup.

**Parameters:**
- `backup` (bool): Create backup before saving

**Returns:**
- `bool`: True if successful, False otherwise

#### Color Coding System

The ExcelHandler uses a comprehensive color coding system:

```python
colors = {
    'updated': PatternFill(...),        # Light blue - General updates
    'new_data': PatternFill(...),       # Light green - New safe data
    'security_risk': PatternFill(...),  # Light red - Security vulnerabilities
    'version_update': PatternFill(...), # Light orange - Version updates
    'github_added': PatternFill(...),   # Light purple - GitHub data
    'not_available': PatternFill(...)   # Red - Not available data
}
```

### PyPIClient

Handles PyPI API integration for package information retrieval.

#### Constructor
```python
PyPIClient(session: Optional[aiohttp.ClientSession] = None)
```

**Parameters:**
- `session` (aiohttp.ClientSession, optional): HTTP session for requests

#### Methods

##### get_package_info()
```python
async def get_package_info(package_name: str) -> Optional[Dict[str, Any]]
```
Get comprehensive package information from PyPI.

**Parameters:**
- `package_name` (str): Name of the package

**Returns:**
- `Optional[Dict[str, Any]]`: Package information or None if failed

**Response Format:**
```python
{
    'latest_version': str,
    'latest_release_date': str,
    'pypi_latest_url': str,
    'dependencies': List[str],
    'classifiers': List[str],
    'github_url': str
}
```

##### extract_version_date_from_package_info()
```python
def extract_version_date_from_package_info(package_info: Dict, target_version: str) -> Optional[str]
```
Extract publication date for a specific version.

**Parameters:**
- `package_info` (Dict): Package information from PyPI
- `target_version` (str): Target version to find date for

**Returns:**
- `Optional[str]`: Publication date or None if not found

### VulnerabilityScanner

Handles multi-database vulnerability scanning with AI integration.

#### Constructor
```python
VulnerabilityScanner(ai_analyzer: Optional[AICVEAnalyzer] = None)
```

**Parameters:**
- `ai_analyzer` (AICVEAnalyzer, optional): AI analyzer for enhanced analysis

#### Methods

##### scan_all_databases()
```python
async def scan_all_databases(
    package_name: str,
    github_url: Optional[str] = None,
    current_version: Optional[str] = None
) -> Dict[str, Any]
```
Scan all vulnerability databases for a package.

**Parameters:**
- `package_name` (str): Package name to scan
- `github_url` (str, optional): GitHub URL for advisory scanning
- `current_version` (str, optional): Current version for AI analysis

**Returns:**
- `Dict[str, Any]`: Comprehensive scan results

**Response Format:**
```python
{
    'scan_results': {
        'nist_nvd': {
            'search_url': str,
            'summary': str,
            'vulnerability_count': int
        },
        'mitre_cve': {...},
        'snyk': {...},
        'exploit_db': {...},
        'github_advisory': {...}
    },
    'total_vulnerabilities': int,
    'highest_severity': str,
    'recommendation': str
}
```

##### scan_nist_nvd()
```python
async def scan_nist_nvd(package_name: str) -> Dict[str, Any]
```
Scan NIST NVD database for vulnerabilities.

##### scan_mitre_cve()
```python
async def scan_mitre_cve(package_name: str, current_version: Optional[str] = None) -> Dict[str, Any]
```
Scan MITRE CVE database with AI analysis.

##### scan_snyk()
```python
async def scan_snyk(package_name: str, current_version: Optional[str] = None) -> Dict[str, Any]
```
Scan SNYK database with AI analysis.

##### scan_exploit_db()
```python
async def scan_exploit_db(package_name: str, current_version: Optional[str] = None) -> Dict[str, Any]
```
Scan Exploit Database with AI analysis.

##### scan_github_advisory()
```python
async def scan_github_advisory(
    package_name: str,
    github_url: Optional[str] = None,
    current_version: Optional[str] = None
) -> Dict[str, Any]
```
Scan GitHub Security Advisory with AI analysis.

### AICVEAnalyzer

Provides AI-powered vulnerability analysis using Azure OpenAI.

#### Constructor
```python
AICVEAnalyzer()
```

#### Methods

##### verify_deployment()
```python
async def verify_deployment() -> bool
```
Verify Azure OpenAI deployment and connectivity.

**Returns:**
- `bool`: True if verification successful

##### analyze_mitre_cve_result()
```python
async def analyze_mitre_cve_result(
    package_name: str,
    current_version: str,
    mitre_cve_url: str,
    raw_mitre_data: str = None
) -> str
```
Analyze MITRE CVE results using AI.

**Parameters:**
- `package_name` (str): Package name
- `current_version` (str): Current version
- `mitre_cve_url` (str): MITRE CVE search URL
- `raw_mitre_data` (str, optional): Raw vulnerability data

**Returns:**
- `str`: AI analysis result

##### analyze_snyk_result()
```python
async def analyze_snyk_result(
    package_name: str,
    current_version: str,
    snyk_url: str,
    raw_snyk_data: str = None
) -> str
```
Analyze SNYK results using AI.

##### analyze_exploit_db_result()
```python
async def analyze_exploit_db_result(
    package_name: str,
    current_version: str,
    exploit_db_url: str,
    raw_exploit_data: str = None
) -> str
```
Analyze Exploit Database results using AI.

##### analyze_github_advisory_result()
```python
async def analyze_github_advisory_result(
    package_name: str,
    current_version: str,
    github_advisory_url: str,
    raw_github_data: str = None
) -> str
```
Analyze GitHub Security Advisory results using AI.

### IHACPAAutomation

Main automation orchestrator that coordinates all components.

#### Constructor
```python
IHACPAAutomation(config: Config, dry_run: bool = False)
```

**Parameters:**
- `config` (Config): Configuration object
- `dry_run` (bool): If True, run in test mode without saving changes

#### Methods

##### setup()
```python
def setup(input_file: str, output_file: Optional[str] = None) -> bool
```
Initialize automation components and load Excel file.

**Parameters:**
- `input_file` (str): Path to input Excel file
- `output_file` (str, optional): Path to output Excel file

**Returns:**
- `bool`: True if setup successful

##### process_packages()
```python
async def process_packages(
    start_row: Optional[int] = None,
    end_row: Optional[int] = None,
    package_names: Optional[List[str]] = None
) -> bool
```
Process packages for vulnerability analysis and updates.

**Parameters:**
- `start_row` (int, optional): Starting row number
- `end_row` (int, optional): Ending row number
- `package_names` (List[str], optional): Specific package names to process

**Returns:**
- `bool`: True if processing successful

##### run_format_check()
```python
def run_format_check(fix: bool = True) -> bool
```
Run format check and optionally fix formatting issues.

**Parameters:**
- `fix` (bool): If True, apply fixes. If False, only report issues.

**Returns:**
- `bool`: True if successful

##### generate_report()
```python
def generate_report(output_path: Optional[str] = None) -> bool
```
Generate processing summary report.

##### generate_changes_report()
```python
def generate_changes_report(output_path: Optional[str] = None) -> bool
```
Generate detailed changes comparison report.

## Configuration Classes

### Config

Main configuration class that handles all system settings.

#### Constructor
```python
Config(config_file: Optional[str] = None)
```

**Parameters:**
- `config_file` (str, optional): Path to YAML configuration file

#### Methods

##### load_from_env()
```python
def load_from_env(self)
```
Load configuration from environment variables.

##### to_dict()
```python
def to_dict(self) -> Dict[str, Any]
```
Convert configuration to dictionary format.

**Returns:**
- `Dict[str, Any]`: Configuration as dictionary

## Error Handling

### Exception Classes

#### VulnerabilityAnalysisError
```python
class VulnerabilityAnalysisError(Exception):
    """Raised when vulnerability analysis fails"""
    pass
```

#### ExcelProcessingError
```python
class ExcelProcessingError(Exception):
    """Raised when Excel processing fails"""
    pass
```

#### ConfigurationError
```python
class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass
```

### Error Handling Patterns

```python
try:
    result = await vulnerability_scanner.scan_all_databases(package_name)
except VulnerabilityAnalysisError as e:
    logger.error(f"Vulnerability analysis failed: {e}")
    # Fallback to manual review
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # General error handling
```

## Data Structures

### Package Data Format

```python
package_data = {
    'package_name': str,          # Package name
    'current_version': str,       # Currently installed version
    'latest_version': str,        # Latest available version
    'date_published': str,        # Publication date of current version
    'latest_release_date': str,   # Latest version release date
    'requires': str,              # Dependencies
    'development_status': str,    # Development status
    'github_url': str,            # GitHub repository URL
    'github_advisory_url': str,   # GitHub security advisory URL
    'github_advisory_result': str, # AI analysis result
    'nist_nvd_url': str,         # NIST NVD search URL
    'nist_nvd_result': str,      # NIST NVD scan result
    'mitre_cve_url': str,        # MITRE CVE search URL
    'mitre_cve_result': str,     # AI analysis result
    'snyk_url': str,             # SNYK search URL
    'snyk_result': str,          # AI analysis result
    'exploit_db_url': str,       # Exploit DB search URL
    'exploit_db_result': str,    # AI analysis result
    'recommendation': str,        # Final recommendation
    'row_number': int            # Excel row number
}
```

### Vulnerability Scan Result Format

```python
scan_result = {
    'search_url': str,           # Database search URL
    'summary': str,              # Human-readable summary
    'vulnerability_count': int,  # Number of vulnerabilities found
    'severity': str,             # Highest severity level
    'ai_analysis': str,          # AI analysis (if available)
    'raw_data': str             # Raw response data
}
```

## Usage Examples

### Basic Package Processing

```python
from src.main import IHACPAAutomation
from src.config import Config

# Initialize
config = Config()
automation = IHACPAAutomation(config)

# Setup
await automation.setup("input.xlsx", "output.xlsx")

# Process all packages
await automation.process_packages()

# Generate reports
automation.generate_report()
automation.generate_changes_report()

# Cleanup
await automation.cleanup()
```

### Specific Package Analysis

```python
# Process specific packages
await automation.process_packages(
    package_names=["requests", "pandas", "numpy"]
)
```

### Format Check Only

```python
# Check formatting without fixes
automation.run_format_check(fix=False)

# Check and fix formatting
automation.run_format_check(fix=True)
```

### Direct Component Usage

```python
from src.vulnerability_scanner import VulnerabilityScanner
from src.ai_cve_analyzer import AICVEAnalyzer

# Initialize components
ai_analyzer = AICVEAnalyzer()
scanner = VulnerabilityScanner(ai_analyzer)

# Scan specific package
result = await scanner.scan_all_databases(
    "requests", 
    current_version="2.29.0"
)

print(f"Total vulnerabilities: {result['total_vulnerabilities']}")
print(f"Recommendation: {result['recommendation']}")
```

## Performance Considerations

### Async Operations
- All network operations are asynchronous
- Use proper async/await patterns
- Handle connection pooling for HTTP requests

### Memory Management
- Excel files are loaded into memory
- Large files may require streaming operations
- Consider batch processing for large datasets

### Rate Limiting
- Azure OpenAI has rate limits
- Implement exponential backoff for retries
- Monitor API usage and costs

## Security Best Practices

### API Key Management
- Store API keys in environment variables
- Never log API keys or responses
- Use secure key management systems in production

### Data Handling
- Vulnerability data is sensitive
- Implement proper access controls
- Consider data retention policies

### Network Security
- Use HTTPS for all external requests
- Validate SSL certificates
- Consider using VPNs or private endpoints