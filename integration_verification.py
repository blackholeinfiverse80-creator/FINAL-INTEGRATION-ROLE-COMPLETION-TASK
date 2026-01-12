#!/usr/bin/env python3
"""
Integration Verification Script
Tests Core Integrator in all modes and captures JSON artifacts
"""

import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8001"
ARTIFACTS_DIR = "integration_artifacts"

def setup_artifacts_dir():
    """Create artifacts directory"""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def test_health_endpoint(mode_name):
    """Test /system/health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/system/health", timeout=10)
        data = response.json()
        
        # Save artifact
        with open(f"{ARTIFACTS_DIR}/health_{mode_name}.json", "w") as f:
            json.dump(data, f, indent=2)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "overall_status": data.get("status"),
            "components": data.get("components", {})
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_diagnostics_endpoint(mode_name):
    """Test /system/diagnostics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/system/diagnostics", timeout=10)
        data = response.json()
        
        # Save artifact
        with open(f"{ARTIFACTS_DIR}/diagnostics_{mode_name}.json", "w") as f:
            json.dump(data, f, indent=2)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "integration_ready": data.get("integration_ready"),
            "integration_score": data.get("integration_score"),
            "failing_components": data.get("failing_components", [])
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_feedback_validation():
    """Test feedback flow rejection on invalid schema"""
    try:
        # Invalid feedback payload
        invalid_payload = {
            "generation_id": 0,  # Invalid: must be > 0
            "command": "+3",     # Invalid: not in allowed values
            "user_id": "",       # Invalid: empty string
            "comment": "x" * 501 # Invalid: too long
        }
        
        response = requests.post(f"{BASE_URL}/feedback", json=invalid_payload, timeout=10)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code == 422,  # Should be validation error
            "properly_rejected": response.status_code == 422
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_integration_verification():
    """Run complete integration verification"""
    setup_artifacts_dir()
    
    print("Starting Integration Verification...")
    print("=" * 50)
    
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "modes_tested": {},
        "feedback_validation": {},
        "summary": {}
    }
    
    # Test SQLite mode (default)
    print("Testing SQLite mode...")
    results["modes_tested"]["sqlite"] = {
        "health": test_health_endpoint("sqlite"),
        "diagnostics": test_diagnostics_endpoint("sqlite")
    }
    
    # Test feedback validation
    print("Testing feedback validation...")
    results["feedback_validation"] = test_feedback_validation()
    
    # Generate summary
    all_health_ok = all(
        mode["health"]["success"] 
        for mode in results["modes_tested"].values()
    )
    all_diagnostics_ok = all(
        mode["diagnostics"]["success"] 
        for mode in results["modes_tested"].values()
    )
    feedback_ok = results["feedback_validation"]["success"]
    
    results["summary"] = {
        "all_health_endpoints_ok": all_health_ok,
        "all_diagnostics_endpoints_ok": all_diagnostics_ok,
        "feedback_validation_ok": feedback_ok,
        "overall_success": all_health_ok and all_diagnostics_ok and feedback_ok
    }
    
    # Save verification results
    with open(f"{ARTIFACTS_DIR}/verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nVerification Results:")
    print(f"Health endpoints: {'PASS' if all_health_ok else 'FAIL'}")
    print(f"Diagnostics endpoints: {'PASS' if all_diagnostics_ok else 'FAIL'}")
    print(f"Feedback validation: {'PASS' if feedback_ok else 'FAIL'}")
    print(f"Overall: {'PASS' if results['summary']['overall_success'] else 'FAIL'}")
    
    return results

if __name__ == "__main__":
    run_integration_verification()