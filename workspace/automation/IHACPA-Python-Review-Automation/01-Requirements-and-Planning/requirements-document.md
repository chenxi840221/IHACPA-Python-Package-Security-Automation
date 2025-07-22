# IHACPA Python Package Review Automation
## Software Requirements Document

**Version:** 1.0  
**Date:** July 9, 2025  
**Project:** Automation of Python Package Cybersecurity Vulnerability Review Process

---

## 1. Executive Summary

This document outlines the requirements for automating the IHACPA (Independent Health and Aged Care Pricing Authority) Python package review process. The system will automatically update PyPI package information, check for vulnerabilities across multiple cybersecurity databases, and generate comprehensive reports with recommendations.

## 2. Project Background

Based on the meeting transcription and current Excel-based manual process, the team is currently:
- Manually reviewing **486 Python packages** (confirmed from Excel analysis 2025-07-09)
- Checking PyPI for version information and release dates
- Looking up vulnerabilities in multiple security databases
- Recording findings and recommendations in an Excel spreadsheet with **23 columns**
- Taking approximately 6+ hours per day with manual processes

## 3. Current State Analysis

### 3.1 Existing Data Structure ✅ **VERIFIED 2025-07-09**
The current Excel file contains the following columns (confirmed structure):
- **Column A:** # (Package Index)
- **Column B:** Package Name
- **Column C:** Version (Currently Installed)
- **Column D:** PyPI Links (installed version)
- **Column E:** Date Published
- **Column F:** Latest Version
- **Column G:** PyPI Links (latest version)
- **Column H:** Latest Version Release Date
- **Column I:** Requires (Dependencies)
- **Column J:** Development Status
- **Column K:** GitHub URL
- **Column L:** GitHub Mirror Security Advisory Lookup URL
- **Column M:** GitHub Security Advisory Result
- **Column N:** Notes
- **Column O:** NIST NVD Lookup URL
- **Column P:** NIST NVD Lookup Result
- **Column Q:** MITRE CVE Lookup URL
- **Column R:** MITRE CVE Lookup Result
- **Column S:** SNYK Vulnerability Lookup URL
- **Column T:** SNYK Vulnerability Lookup Result
- **Column U:** Exploit Database Lookup URL
- **Column V:** Exploit Database Lookup Result
- **Column W:** Recommendation

**Excel File Details:**
- **File Path:** `02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx`
- **Total Rows:** 490 (Header at row 3, data starts at row 4)
- **Total Columns:** 23 (A through W)
- **Total Packages:** 486 active packages
- **Sheet Names:** Sheet1 (primary), Sheet2, Sheet3
- **Sample Packages:** agate v1.9.1, aiobotocore v2.4.2, aiofiles v22.1.0

### 3.2 Current Manual Process
1. Open PyPI.org for each package
2. Check current version information and publication date
3. Identify if newer versions are available
4. Update PyPI links for latest versions
5. Extract package requirements and development status
6. Find GitHub repository URLs
7. Check security advisories across multiple databases
8. Document findings and generate recommendations

## 4. Functional Requirements

### 4.1 Core Automation Features

#### 4.1.1 PyPI Information Retrieval
- **FR-001:** Automatically fetch package information from PyPI API
- **FR-002:** Extract current version, publication date, and metadata
- **FR-003:** Identify latest available version and release date
- **FR-004:** Generate correct PyPI URLs for both current and latest versions
- **FR-005:** Extract package dependencies (Requires field)
- **FR-006:** Capture development status information
- **FR-007:** Identify and extract GitHub repository URLs

#### 4.1.2 Vulnerability Database Integration
- **FR-008:** Integrate with NIST NVD (National Vulnerability Database)
- **FR-009:** Integrate with MITRE CVE database
- **FR-010:** Integrate with SNYK Vulnerability Database
- **FR-011:** Generate appropriate lookup URLs for each database
- **FR-012:** Perform automated vulnerability searches
- **FR-013:** Parse and extract vulnerability information
- **FR-014:** Identify severity levels and CVSS scores

#### 4.1.3 GitHub Security Advisory Integration
- **FR-015:** Generate GitHub security advisory URLs
- **FR-016:** Check for published security advisories
- **FR-017:** Extract advisory details and severity information

#### 4.1.4 Data Processing and Analysis
- **FR-018:** Compare current vs. latest versions
- **FR-019:** Identify packages with significant version gaps
- **FR-020:** Flag packages with known vulnerabilities
- **FR-021:** Generate risk assessments based on:
  - Age of current version
  - Availability of updates
  - Number and severity of vulnerabilities
  - Package criticality and usage

#### 4.1.5 Reporting and Recommendations
- **FR-022:** Generate automated recommendations based on findings
- **FR-023:** Prioritize packages requiring immediate attention
- **FR-024:** Create summary reports by risk level
- **FR-025:** Export results back to Excel format
- **FR-026:** Generate executive summary reports

### 4.2 Data Management Requirements

#### 4.2.1 Input Processing
- **FR-027:** Read existing Excel file with current package inventory
- **FR-028:** Parse package names and current versions
- **FR-029:** Preserve existing manual notes and overrides
- **FR-030:** Handle various package name formats and edge cases

#### 4.2.2 Output Generation
- **FR-031:** Update Excel file with new information while preserving structure
- **FR-032:** Maintain data integrity and formatting
- **FR-033:** Create backup of original data before updates
- **FR-034:** Generate separate reports for different stakeholders

### 4.3 Performance Requirements

#### 4.3.1 Processing Speed ✅ **UPDATED WITH ACTUAL DATA**
- **FR-035:** Process all **486 packages** within 2 hours
- **FR-036:** Implement concurrent API calls with rate limiting
- **FR-037:** Provide progress indicators and status updates
- **FR-038:** Support resume functionality for interrupted processes

#### 4.3.2 Reliability
- **FR-039:** Handle API failures gracefully with retry mechanisms
- **FR-040:** Continue processing even if some databases are unavailable
- **FR-041:** Log all errors and issues for manual review
- **FR-042:** Validate data quality and completeness

## 5. Non-Functional Requirements

### 5.1 Usability Requirements
- **NFR-001:** Simple command-line interface for technical users
- **NFR-002:** Clear progress indicators and status messages
- **NFR-003:** Comprehensive error messages and troubleshooting guidance
- **NFR-004:** Configurable settings for different scan types

### 5.2 Compatibility Requirements
- **NFR-005:** Support Python 3.8+ environments
- **NFR-006:** Compatible with Windows, macOS, and Linux
- **NFR-007:** Work with Excel files (.xlsx format)
- **NFR-008:** Support for proxy environments if needed

### 5.3 Security Requirements
- **NFR-009:** Secure API key management for services requiring authentication
- **NFR-010:** No storage of sensitive data in logs
- **NFR-011:** Validate all external API responses
- **NFR-012:** Implement secure HTTP requests with proper SSL verification

### 5.4 Maintainability Requirements
- **NFR-013:** Modular design for easy addition of new vulnerability databases
- **NFR-014:** Comprehensive logging for debugging and auditing
- **NFR-015:** Configuration files for easy customization
- **NFR-016:** Clear documentation and code comments

## 6. Technical Architecture

### 6.1 System Components

#### 6.1.1 Core Modules
1. **Excel Reader/Writer Module**
   - Read existing Excel files
   - Preserve formatting and structure
   - Write updated data back to Excel

2. **PyPI Integration Module**
   - Interface with PyPI API
   - Parse package metadata
   - Handle API rate limiting

3. **Vulnerability Scanner Module**
   - NIST NVD integration
   - MITRE CVE integration
   - SNYK database integration
   - GitHub security advisory integration

4. **Analysis Engine**
   - Risk assessment algorithms
   - Recommendation generation
   - Data validation and quality checks

5. **Reporting Module**
   - Generate summary reports
   - Create executive dashboards
   - Export various formats

#### 6.1.2 External Dependencies
- **PyPI API:** For package information
- **NIST NVD API:** For vulnerability data
- **MITRE CVE API:** For CVE information
- **SNYK API:** For vulnerability intelligence
- **GitHub API:** For security advisories

### 6.2 Data Flow
1. **Input:** Read Excel file with package list
2. **Processing:** For each package:
   - Fetch PyPI information
   - Check vulnerability databases
   - Analyze findings
   - Generate recommendations
3. **Output:** Update Excel file and generate reports

## 7. Implementation Phases

### 7.1 Phase 1: Core Infrastructure (Week 1)
- Excel file reading/writing capabilities
- PyPI API integration
- Basic data validation
- Command-line interface

### 7.2 Phase 2: Vulnerability Integration (Week 2)
- NIST NVD integration
- MITRE CVE integration
- SNYK database integration
- Error handling and retry logic

### 7.3 Phase 3: Analysis and Reporting (Week 3)
- Risk assessment algorithms
- Recommendation engine
- Report generation
- GitHub security advisory integration

### 7.4 Phase 4: Optimization and Testing (Week 4)
- Performance optimization
- Comprehensive testing
- Documentation
- User training materials

## 8. Success Criteria

### 8.1 Primary Objectives ✅ **UPDATED WITH VERIFIED DATA**
- **Reduce manual effort from 6+ hours to 30 minutes of supervision**
- **Process all 486 packages automatically** (confirmed count)
- **Achieve 95%+ accuracy in vulnerability detection**
- **Generate actionable recommendations for 100% of packages**

### 8.2 Quality Metrics
- **Data Accuracy:** 99%+ match with manual verification on sample set
- **Processing Speed:** Complete full scan in under 2 hours
- **Reliability:** 95%+ success rate for API calls
- **Usability:** Non-technical staff can run with minimal training

## 9. Risk Assessment

### 9.1 Technical Risks
- **API Rate Limiting:** Mitigation through throttling and retry logic
- **Data Quality:** Mitigation through validation and manual review flags
- **Service Availability:** Mitigation through graceful degradation

### 9.2 Operational Risks
- **False Positives:** Mitigation through confidence scoring
- **Missed Vulnerabilities:** Mitigation through multiple database checks
- **Data Loss:** Mitigation through backup and version control

## 10. Acceptance Criteria

### 10.1 Functional Acceptance
- [ ] Successfully processes complete package list
- [ ] Updates all required Excel columns automatically
- [ ] Integrates with all specified vulnerability databases
- [ ] Generates accurate recommendations
- [ ] Preserves existing manual data and formatting

### 10.2 Performance Acceptance
- [ ] Completes full scan within 2-hour timeframe
- [ ] Handles network failures gracefully
- [ ] Provides clear progress indicators
- [ ] Generates comprehensive logs for audit

### 10.3 Usability Acceptance
- [ ] Simple command-line operation
- [ ] Clear error messages and guidance
- [ ] Configurable scan options
- [ ] Resume capability for interrupted scans

---

## 11. Appendices

### 11.1 Sample Package Entry
```
Package: agate
Current Version: 1.9.1
Latest Version: 1.13.0
Risk Assessment: MEDIUM (significant version gap)
Recommendation: Update recommended - no critical vulnerabilities found
```

### 11.2 API Endpoints
- **PyPI API:** `https://pypi.org/pypi/{package}/json`
- **NIST NVD:** `https://services.nvd.nist.gov/rest/json/cves/2.0`
- **MITRE CVE:** `https://cve.mitre.org/cgi-bin/cvekey.cgi`
- **SNYK:** `https://security.snyk.io/package/pip/{package}`

### 11.3 Configuration Options
- Scan depth (quick vs. comprehensive)
- Database selection (enable/disable specific sources)
- Output format preferences
- Concurrency limits
- Timeout settings

### 11.4 Testing Results ✅ **VERIFIED 2025-07-09**
```
📊 Excel File Analysis Results:
✅ File successfully read: 02-Source-Data/2025-07-09 IHACPA Review of ALL existing PYTHON Packages.xlsx
✅ Total packages: 486 (out of 490 rows)
✅ Column structure: 23 columns (A through W) - matches requirements
✅ Header row: 3 (confirmed)
✅ Data rows: 4 to 490
✅ All expected columns present: Package Name, Version, PyPI Links, etc.

📊 PyPI API Testing Results:
✅ API Status: 200 (working)
✅ Example: agate package v1.9.1 (installed) → v1.13.0 (latest)
✅ Version gap detection: Working correctly

📊 Dependencies Status:
✅ openpyxl==3.1.5: Working
✅ requests==2.32.4: Working  
✅ pytest==8.4.1: Working
⚠️  pandas: Has import issues, application designed to work without it
```

---

**Document Prepared By:** AI Assistant  
**Review Required By:** Doug McFarlane, Linda Aney, Sean Chen  
**Last Updated:** 2025-07-09 (Excel analysis completed)  
**Next Steps:** Technical design document and implementation planning