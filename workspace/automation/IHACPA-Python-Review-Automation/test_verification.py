#!/usr/bin/env python3
"""
Quick test script for vulnerability verification system
Tests a few packages to verify the automation works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_verification import VulnerabilityVerification
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_verification():
    """Test verification with a small set of packages"""
    verifier = VulnerabilityVerification()
    
    # Override test packages with just a few for quick testing
    verifier.test_packages = {
        'nist_nvd': [
            ('requests', '2.31.0'),
            ('flask', '2.3.2'),
        ],
        'mitre_cve': [
            ('django', '4.2.3'),
            ('requests', '2.31.0'),
        ],
        'snyk': [
            ('pyyaml', '6.0'),
            ('click', '8.1.6'),
        ]
    }
    
    print("Starting verification test...")
    try:
        verifier.setup_browser()
        print(f"Browser setup: {'Success' if verifier.driver else 'Fallback to requests'}")
        
        # Test a few packages
        packages_to_test = [
            ('requests', '2.31.0', 'test'),
            ('flask', '2.3.2', 'test'),
        ]
        
        for package_name, version, scanner_type in packages_to_test:
            print(f"\nTesting {package_name} v{version}...")
            result = verifier.verify_package(package_name, version, scanner_type)
            print(f"Results: NIST={result.nist_match}, MITRE={result.mitre_match}, SNYK={result.snyk_match}")
            if result.notes:
                print(f"Notes: {result.notes}")
                
        # Generate and print report
        report = verifier.generate_report()
        print("\n" + "="*80)
        print("TEST VERIFICATION REPORT")
        print("="*80)
        print(report.split("DETAILED RESULTS:")[0])
        
        # Save report
        filename = verifier.save_report("test_verification_report.txt")
        print(f"\nFull report saved to: {filename}")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        verifier.cleanup_browser()
        print("Test completed!")

if __name__ == "__main__":
    test_verification()