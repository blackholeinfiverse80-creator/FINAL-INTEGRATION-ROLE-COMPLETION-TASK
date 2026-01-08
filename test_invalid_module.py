#!/usr/bin/env python3
"""
Test the actual FastAPI endpoint with invalid module
"""

import requests
import json

def test_invalid_module_endpoint():
    """Test the /core endpoint with invalid module"""
    
    url = "http://localhost:8001/core"
    
    # Invalid module payload
    payload = {
        "module": "invalid_module",
        "intent": "generate",
        "user_id": "test_user",
        "data": {}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"Response Body: {json.dumps(data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
        if response.status_code == 422:
            print("PASS - Proper validation error returned")
            return True
        else:
            print(f"FAIL - Expected 422, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Server not running - start with: python main.py")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing invalid module validation...")
    success = test_invalid_module_endpoint()
    print(f"\nValidation test: {'PASSED' if success else 'FAILED'}")