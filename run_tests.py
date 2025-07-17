#!/usr/bin/env python3
"""
Test runner script for NFC decode regression testing.

This script provides easy commands to run different test suites
for the spool-coder NFC functionality.

Usage:
    python run_tests.py [test_type]

Test types:
    all         - Run all tests (default)
    regression  - Run only regression tests  
    integration - Run only integration tests
    coverage    - Run all tests with coverage report
"""

import sys
import subprocess
import os


def run_command(cmd):
    """Run a command and return success status."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    """Main test runner function."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if test_type == "regression":
        cmd = ["python", "-m", "pytest", "tests/test_nfc_decode_regression.py", "-v"]
        
    elif test_type == "integration":
        cmd = ["python", "-m", "pytest", "tests/test_nfc_integration.py", "-v"]
        
    elif test_type == "coverage":
        cmd = ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing", "--cov-report=html"]
        
    elif test_type == "all":
        cmd = ["python", "-m", "pytest", "tests/", "-v"]
        
    else:
        print(f"Unknown test type: {test_type}")
        print(__doc__)
        return False
    
    success = run_command(cmd)
    
    if success:
        print(f"\n✅ {test_type.capitalize()} tests passed!")
        if test_type == "coverage":
            print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print(f"\n❌ {test_type.capitalize()} tests failed!")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)