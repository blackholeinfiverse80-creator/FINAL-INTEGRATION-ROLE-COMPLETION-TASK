#!/usr/bin/env python3
"""
Fix for Feedback POST request validation errors
"""

import requests
import json

def test_feedback_endpoint():
    """Test the /feedback endpoint with correct format"""
    url = "http://localhost:8001/feedback"
    
    # ✅ CORRECT - All required fields with valid values
    correct_payload = {
        "generation_id": 1,           # Required, must be > 0
        "command": "+1",              # Required, must be: +2, +1, -1, -2
        "user_id": "test_user",       # Required, min_length=1
        "comment": "Great work!"      # Optional, max_length=500
    }
    
    try:
        response = requests.post(url, json=correct_payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def feedback_common_mistakes():
    """Common mistakes that cause 422 validation errors"""
    
    # ❌ WRONG - Invalid command value
    wrong_payload_1 = {
        "generation_id": 1,
        "command": "+3",              # Invalid! Must be +2, +1, -1, -2
        "user_id": "test_user"
    }
    
    # ❌ WRONG - generation_id <= 0
    wrong_payload_2 = {
        "generation_id": 0,           # Invalid! Must be > 0
        "command": "+1",
        "user_id": "test_user"
    }
    
    # ❌ WRONG - Missing required fields
    wrong_payload_3 = {
        "comment": "Nice work"
        # Missing: generation_id, command, user_id
    }
    
    # ❌ WRONG - Empty user_id
    wrong_payload_4 = {
        "generation_id": 1,
        "command": "+1",
        "user_id": ""                 # Invalid! min_length=1
    }
    
    # ❌ WRONG - Comment too long
    wrong_payload_5 = {
        "generation_id": 1,
        "command": "+1",
        "user_id": "test_user",
        "comment": "x" * 501          # Invalid! max_length=500
    }
    
    print("These feedback payloads will cause 422 validation errors:")
    for i, payload in enumerate([wrong_payload_1, wrong_payload_2, wrong_payload_3, wrong_payload_4, wrong_payload_5], 1):
        print(f"Wrong payload {i}: {payload}")

def test_core_feedback_via_creator():
    """Alternative: Submit feedback via /core endpoint with creator module"""
    url = "http://localhost:8001/core"
    
    # ✅ CORRECT - Feedback via creator module
    correct_payload = {
        "module": "creator",
        "intent": "feedback",
        "user_id": "test_user",
        "data": {
            "generation_id": 1,
            "command": "+1",
            "user_id": "test_user",
            "comment": "Great work!"
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

if __name__ == "__main__":
    print("Testing feedback endpoint...")
    success1 = test_feedback_endpoint()
    print(f"Direct feedback test {'PASSED' if success1 else 'FAILED'}")
    
    print("\nTesting feedback via creator module...")
    success2 = test_core_feedback_via_creator()
    print(f"Creator feedback test {'PASSED' if success2 else 'FAILED'}")
    
    print("\n" + "="*50)
    feedback_common_mistakes()