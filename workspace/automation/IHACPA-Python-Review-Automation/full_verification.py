#!/usr/bin/env python3
"""
Full verification script for all 30 test packages
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vulnerability_verification import VulnerabilityVerification
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    """Run full verification"""
    print("Starting comprehensive vulnerability scanner verification...")
    print("Testing 30 packages (10 per database)")
    print("This may take several minutes...")
    print("="*70)
    
    verifier = VulnerabilityVerification()
    
    try:
        verifier.run_full_verification()
        
        # Generate and save report
        report_file = verifier.save_report("comprehensive_verification_report.txt")
        print(f"\nFull report saved to: {report_file}")
        
        # Print summary
        report = verifier.generate_report()
        summary_section = report.split("DETAILED RESULTS:")[0]
        
        print("\n" + "="*70)
        print("COMPREHENSIVE VERIFICATION SUMMARY")
        print("="*70)
        print(summary_section)
        
        # Print discrepancies count
        discrepancies = [r for r in verifier.results if not (r.nist_match and r.mitre_match and r.snyk_match)]
        print(f"\nTotal packages with discrepancies: {len(discrepancies)}/{len(verifier.results)}")
        
        if discrepancies:
            print("\nPackages with significant discrepancies:")
            for result in discrepancies[:5]:  # Show first 5
                print(f"  {result.package_name}: {result.notes}")
        
        print(f"\nDetailed report available in: {report_file}")
        
    except Exception as e:
        print(f"Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()