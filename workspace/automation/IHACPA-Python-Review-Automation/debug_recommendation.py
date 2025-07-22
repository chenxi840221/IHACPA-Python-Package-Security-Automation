#!/usr/bin/env python3
"""
Debug script to trace recommendation logic step by step
"""

import sys
import asyncio
sys.path.append('src')

from vulnerability_scanner import VulnerabilityScanner

async def debug_recommendation_logic():
    """Debug the recommendation generation step by step"""
    
    print('🔍 Debugging Recommendation Logic for xlwt')
    print('=' * 60)
    
    # Create vulnerability scanner
    scanner = VulnerabilityScanner()
    
    # Test xlwt package
    full_result = await scanner.scan_all_databases(
        'xlwt', 
        current_version='1.3.0'
    )
    
    scan_results = full_result.get('scan_results', {})
    
    print('\n📊 Step-by-step Database Analysis:')
    
    # Simulate the recommendation logic step by step
    database_findings = {
        'github_advisory': {'found': False, 'count': 0, 'severity': 'NONE'},
        'nist_nvd': {'found': False, 'count': 0, 'severity': 'NONE'},
        'mitre_cve': {'found': False, 'count': 0, 'severity': 'NONE'},
        'snyk': {'found': False, 'count': 0, 'severity': 'NONE'},
        'exploit_db': {'found': False, 'count': 0, 'severity': 'NONE'}
    }
    
    # Parse results from each database
    for db_name, result in scan_results.items():
        if db_name in database_findings:
            print(f'\n--- {db_name.upper()} Analysis ---')
            
            summary = result.get('summary', '').lower()
            ai_analysis = result.get('ai_analysis', '').lower()
            
            print(f'Summary: {result.get("summary", "No summary")[:80]}...')
            if result.get('ai_analysis'):
                print(f'AI Analysis: {result.get("ai_analysis", "No AI analysis")[:80]}...')
            
            # Check if vulnerabilities were found - step by step
            vulnerability_found = False
            detection_method = "None"
            
            # Check explicit found_vulnerabilities flag
            if result.get('found_vulnerabilities', False):
                vulnerability_found = True
                detection_method = "found_vulnerabilities flag"
            
            # Check for actual vulnerability count > 0
            elif result.get('vulnerability_count', 0) > 0:
                vulnerability_found = True
                detection_method = "vulnerability_count > 0"
            
            # Check AI analysis for explicit FOUND indication (but not NOT_FOUND)
            elif ai_analysis and ': found' in ai_analysis and 'not_found' not in ai_analysis:
                vulnerability_found = True
                detection_method = "AI analysis ': found' pattern"
            
            # Check summary for vulnerability counts
            elif 'found' in summary and 'vulnerabilities' in summary and 'none found' not in summary and 'no published' not in summary:
                vulnerability_found = True
                detection_method = "summary vulnerability pattern"
            
            print(f'Vulnerability Found: {vulnerability_found}')
            print(f'Detection Method: {detection_method}')
            print(f'found_vulnerabilities flag: {result.get("found_vulnerabilities", False)}')
            print(f'vulnerability_count: {result.get("vulnerability_count", 0)}')
            print(f'Contains ": found": {": found" in ai_analysis if ai_analysis else False}')
            print(f'Contains "not_found": {"not_found" in ai_analysis if ai_analysis else False}')
            
            if vulnerability_found:
                database_findings[db_name]['found'] = True
                # Ensure count is at least 1 when vulnerabilities are found
                vuln_count = result.get('vulnerability_count', 0)
                database_findings[db_name]['count'] = max(vuln_count, 1)
                
                # Extract severity from AI analysis
                if 'severity: critical' in ai_analysis:
                    database_findings[db_name]['severity'] = 'CRITICAL'
                elif 'severity: high' in ai_analysis:
                    database_findings[db_name]['severity'] = 'HIGH'
                elif 'severity: medium' in ai_analysis:
                    database_findings[db_name]['severity'] = 'MEDIUM'
                elif 'severity: low' in ai_analysis:
                    database_findings[db_name]['severity'] = 'LOW'
                
                print(f'Assigned Severity: {database_findings[db_name]["severity"]}')
    
    print(f'\n🎯 Final Database Findings:')
    for db, data in database_findings.items():
        if data['found']:
            print(f'  {db}: FOUND - Count: {data["count"]}, Severity: {data["severity"]}')
        else:
            print(f'  {db}: NOT FOUND')
    
    # Calculate totals
    total_vulnerabilities = sum(db['count'] for db in database_findings.values() if db['found'])
    databases_with_findings = [db for db, data in database_findings.items() if data['found']]
    
    print(f'\n📈 Summary:')
    print(f'Total Vulnerabilities: {total_vulnerabilities}')
    print(f'Databases with Findings: {databases_with_findings}')
    
    # Test the actual recommendation generation
    recommendation = scanner.generate_recommendations(
        'xlwt',
        '1.3.0',
        '1.3.0',  # Same version
        full_result
    )
    
    print(f'\n🎯 Final Recommendation: "{recommendation}"')
    
    # Determine what should happen
    if total_vulnerabilities > 0:
        print('✅ Expected: Security risk warning')
        if recommendation == 'PROCEED':
            print('❌ BUG: Should show security risks, not PROCEED!')
        else:
            print('✅ Correct: Shows security information')
    else:
        print('✅ Expected: PROCEED')
        if recommendation == 'PROCEED':
            print('✅ Correct: Shows PROCEED')
        else:
            print('❌ Issue: Should show PROCEED but shows security warning')
    
    await scanner.close()

if __name__ == "__main__":
    asyncio.run(debug_recommendation_logic())