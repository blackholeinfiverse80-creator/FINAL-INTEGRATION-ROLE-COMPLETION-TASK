#!/usr/bin/env python3
"""
Example of correct POST request format for the Core API
"""

import requests
import json

# Correct POST request format
def test_core_endpoint():
    url = "http://localhost:8001/core"
    
    # ✅ CORRECT - All required fields present with valid values
    correct_payload = {
        "module": "sample_text",  # Must be: finance, education, creator, sample_text
        "intent": "generate",     # Must be: generate, analyze, review
        "user_id": "test_user",   # Required, min_length=1
        "data": {                 # Optional dict
            "input_text": "Hello world"
        }
    }
    
    try:
        response = requests.post(url, json=correct_payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Common mistakes that cause 422 errors
def common_mistakes():
    url = "http://localhost:8001/core"
    
    # ❌ WRONG - Missing required fields
    wrong_payload_1 = {
        "data": {"input_text": "Hello"}
        # Missing: module, intent, user_id
    }
    
    # ❌ WRONG - Invalid module value
    wrong_payload_2 = {
        "module": "invalid_module",  # Not in allowed list
        "intent": "generate",
        "user_id": "test_user",
        "data": {}
    }
    
    # ❌ WRONG - Invalid intent value
    wrong_payload_3 = {
        "module": "sample_text",
        "intent": "invalid_intent",  # Not in allowed list
        "user_id": "test_user",
        "data": {}
    }
    
    # ❌ WRONG - Empty user_id
    wrong_payload_4 = {
        "module": "sample_text",
        "intent": "generate",
        "user_id": "",  # min_length=1 validation fails
        "data": {}
    }
    
    print("These payloads will cause 422 validation errors:")
    for i, payload in enumerate([wrong_payload_1, wrong_payload_2, wrong_payload_3, wrong_payload_4], 1):
        print(f"Wrong payload {i}: {payload}")

if __name__ == "__main__":
    print("Testing correct POST request...")
    success = test_core_endpoint()
    print(f"Test {'PASSED' if success else 'FAILED'}")
    
    print("\n" + "="*50)
    common_mistakes()