# Configuration Reference

Complete reference for configuring the IHACPA Python Package Review Automation system.

## Overview

The system supports multiple configuration methods:
1. **Environment Variables** (recommended for sensitive data)
2. **Configuration Files** (YAML format)
3. **Command Line Arguments**
4. **Default Values** (built-in fallbacks)

## Environment Variables

### Azure OpenAI Configuration (Recommended)

```bash
# Required for AI-powered vulnerability analysis
export AZURE_OPENAI_KEY="your-azure-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_MODEL="gpt-4.1"  # Your deployment name
export AZURE_OPENAI_API_VERSION="2025-01-01-preview"
```

### Standard OpenAI Configuration (Alternative)

```bash
# Alternative to Azure OpenAI
export OPENAI_API_KEY="sk-your-openai-key-here"
```

### .env File (Recommended)

Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration (Production)
AZURE_OPENAI_KEY=your-azure-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Alternative: Standard OpenAI
# OPENAI_API_KEY=sk-your-openai-key-here

# Optional: Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs

# Optional: Processing Configuration
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
```

## Configuration File Format (config.yaml)

The system accepts YAML configuration files for advanced settings:

```yaml
# config.yaml
ai:
  # Azure OpenAI Settings (Primary)
  azure_openai:
    api_key: "${AZURE_OPENAI_KEY}"  # Reference environment variable
    endpoint: "${AZURE_OPENAI_ENDPOINT}"
    model: "${AZURE_OPENAI_MODEL}"
    api_version: "${AZURE_OPENAI_API_VERSION}"
    
  # Standard OpenAI Settings (Fallback)
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
    
  # AI Analysis Settings
  analysis:
    enable_ai: true
    max_retries: 3
    timeout: 60
    
processing:
  # Concurrency Settings
  max_concurrent: 10
  batch_size: 50
  
  # Timeout Settings
  request_timeout: 30
  pypi_timeout: 10
  vulnerability_timeout: 20
  
  # Retry Settings
  max_retries: 3
  retry_delay: 1
  backoff_factor: 2
  
output:
  # Report Generation
  create_reports: true
  create_backups: true
  timestamp_files: true
  
  # Excel Settings
  preserve_formatting: true
  auto_color_coding: true
  format_check_enabled: true
  
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  directory: "logs"
  max_file_size: "10MB"
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
security:
  # Data Handling
  mask_sensitive_data: true
  log_api_responses: false
  sanitize_urls: true
```

## Command Line Arguments

### Basic Usage
```bash
python main.py [OPTIONS]
```

### Required Arguments
```bash
--input, -i PATH          # Path to input Excel file (required)
```

### Optional Arguments

#### File Operations
```bash
--output, -o PATH         # Path to output Excel file (default: overwrites input with backup)
--config, -c PATH         # Path to configuration file
```

#### Processing Control
```bash
--start-row NUMBER        # Start processing from this row number
--end-row NUMBER          # End processing at this row number  
--packages PACKAGE ...    # Process specific packages by name (space-separated)
```

#### Operation Modes
```bash
--dry-run                 # Process without making changes (test mode)
--report-only             # Generate report only, do not process packages
--changes-only            # Generate changes report only
--format-check            # Run format check and apply fixes
--format-check-only       # Run format check without fixing (dry run)
```

### Example Commands

#### Production Usage
```bash
# Full processing with all features
python main.py --input "packages.xlsx" --output "updated.xlsx" --format-check

# Test run before production
python main.py --input "packages.xlsx" --dry-run

# Process specific packages for testing
python main.py --input "packages.xlsx" --packages requests pandas numpy --dry-run
```

#### Format Management
```bash
# Check formatting issues without fixing
python main.py --input "packages.xlsx" --format-check-only

# Fix formatting issues
python main.py --input "packages.xlsx" --format-check

# Combined processing and format check
python main.py --input "packages.xlsx" --output "updated.xlsx" --format-check
```

#### Report Generation
```bash
# Generate report only
python main.py --input "packages.xlsx" --report-only

# Generate changes comparison
python main.py --input "packages.xlsx" --changes-only
```

## Default Configuration Values

The system uses these defaults when no configuration is provided:

```python
# Default AI Configuration
AI_ENABLED = True
AI_MAX_RETRIES = 3
AI_TIMEOUT = 60

# Default Processing Configuration
MAX_CONCURRENT_REQUESTS = 10
REQUEST_TIMEOUT = 30
BATCH_SIZE = 50

# Default Logging Configuration
LOG_LEVEL = "INFO"
LOG_DIRECTORY = "logs"

# Default Output Configuration
CREATE_REPORTS = True
CREATE_BACKUPS = True
TIMESTAMP_FILES = True
```

## Azure OpenAI Setup Guide

### 1. Create Azure OpenAI Resource
1. Go to Azure Portal → Create Resource → Azure OpenAI
2. Configure region, pricing tier, and resource group
3. Wait for deployment completion

### 2. Deploy GPT-4 Model
1. Go to Azure OpenAI Studio
2. Navigate to Deployments
3. Create new deployment with GPT-4 model
4. Note the deployment name (e.g., "gpt-4.1")

### 3. Get Configuration Values
```bash
# From Azure Portal → Your OpenAI Resource
ENDPOINT: https://your-resource-name.openai.azure.com/
KEY: Available in "Keys and Endpoint" section
MODEL: Your deployment name from step 2
API_VERSION: 2025-01-01-preview (current recommended)
```

### 4. Test Configuration
```bash
python test_triple_ai.py
```

## Configuration Hierarchy

The system loads configuration in this order (later values override earlier ones):

1. **Built-in defaults**
2. **Configuration file** (if provided)
3. **Environment variables**
4. **Command line arguments**

## Environment-Specific Configurations

### Development Environment
```yaml
# config-dev.yaml
ai:
  analysis:
    enable_ai: false  # Skip AI for faster testing
    
processing:
  max_concurrent: 5  # Lower concurrency for development

logging:
  level: "DEBUG"  # Verbose logging
  
output:
  create_backups: false  # Skip backups in development
```

### Production Environment
```yaml
# config-prod.yaml
ai:
  analysis:
    enable_ai: true
    max_retries: 5  # More retries for stability
    
processing:
  max_concurrent: 20  # Higher throughput
  
logging:
  level: "INFO"  # Standard logging
  
security:
  mask_sensitive_data: true  # Enhanced security
  log_api_responses: false
```

### Testing Environment
```yaml
# config-test.yaml
ai:
  analysis:
    enable_ai: true
    timeout: 10  # Faster timeouts for testing
    
processing:
  max_concurrent: 3
  batch_size: 10  # Smaller batches
  
output:
  create_backups: false
  timestamp_files: false
```

## Security Considerations

### Sensitive Data
- Store API keys in environment variables or secure key management
- Never commit API keys to version control
- Use Azure Key Vault or similar for production environments

### Network Security
- Configure firewall rules for Azure OpenAI endpoints
- Use VPN or private endpoints in enterprise environments
- Monitor API usage and set spending limits

### Data Handling
- Vulnerability data is sensitive - ensure proper access controls
- Consider data retention policies
- Implement audit logging for compliance

## Validation and Testing

### Configuration Validation
```bash
# Test configuration loading
python -c "from src.config import Config; print(Config().to_dict())"

# Test Azure OpenAI connection
python -c "from src.ai_cve_analyzer import AICVEAnalyzer; import asyncio; asyncio.run(AICVEAnalyzer().verify_deployment())"
```

### Performance Testing
```bash
# Test with small dataset
python main.py --input "test.xlsx" --packages requests --dry-run

# Benchmark processing speed
time python main.py --input "packages.xlsx" --start-row 1 --end-row 10 --dry-run
```

## Troubleshooting Configuration

### Common Issues

1. **API Key Not Found**
   - Check environment variable names
   - Verify .env file location
   - Ensure proper quoting in shell

2. **Azure OpenAI Authentication Failed**
   - Verify endpoint URL format
   - Check API version compatibility
   - Confirm deployment name

3. **Configuration File Not Loaded**
   - Check file path and permissions
   - Verify YAML syntax
   - Ensure file encoding is UTF-8

### Debug Configuration
```bash
# Show current configuration
python main.py --input "test.xlsx" --dry-run --verbose

# Test specific configuration
export LOG_LEVEL=DEBUG
python main.py --input "test.xlsx" --packages requests --dry-run
```

## Best Practices

### Configuration Management
- Use environment variables for sensitive data
- Keep configuration files in version control (without secrets)
- Document environment-specific settings
- Use configuration validation in CI/CD

### Performance Optimization
- Adjust concurrency based on system resources
- Monitor API rate limits and costs
- Use appropriate timeout values
- Consider caching strategies

### Security
- Regularly rotate API keys
- Monitor API usage and costs
- Implement proper access controls
- Use least-privilege principles

### Monitoring
- Set up logging and monitoring
- Track processing metrics
- Monitor API response times
- Alert on error rates