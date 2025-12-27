#!/usr/bin/env python3
"""
Test runner for Noopur integration tests.
"""

import os
import sys
import subprocess

def run_unit_tests():
    """Run unit tests for Noopur client."""
    print("Running Noopur unit tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_noopur_integration.py", "-v"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def run_live_test():
    """Run live integration test."""
    print("\nRunning live integration test...")
    
    # Temporarily enable Noopur for testing
    os.environ["INTEGRATOR_USE_NOOPUR"] = "true"
    
    result = subprocess.run([
        sys.executable, "test_noopur_live.py"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def main():
    """Main test runner."""
    print("Noopur Integration Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unit_success = run_unit_tests()
    
    # Run live tests
    live_success = run_live_test()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Unit Tests: {'PASSED' if unit_success else 'FAILED'}")
    print(f"Live Tests: {'PASSED' if live_success else 'FAILED'}")
    
    if unit_success and live_success:
        print("\nAll tests passed!")
        return 0
    else:
        print("\nSome tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())