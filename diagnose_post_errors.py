#!/usr/bin/env python3
"""
POST Request Error Diagnostic Tool
Identifies and fixes common API POST request errors
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

def test_endpoint(endpoint: str, payload: Dict[str, Any], description: str):
    """Test an endpoint and return detailed results"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response Text: {response.text}")
        else:
            print("❌ FAILED")
            try:
                error_data = response.json()
                print(f"Error Response: {json.dumps(error_data, indent=2)}")
                
                # Provide specific fixes for common errors
                if response.status_code == 422:
                    print("\n🔧 FIX: Validation Error (422)")
                    print("- Check required fields: module, intent, user_id")
                    print("- Verify enum values:")
                    print("  - module: finance, education, creator, sample_text")
                    print("  - intent: generate, analyze, review")
                    print("- Ensure user_id is not empty")
                    
                elif response.status_code == 500:
                    print("\n🔧 FIX: Internal Server Error (500)")
                    print("- Check if the server is running")
                    print("- Verify database connectivity")
                    print("- Check agent/module implementations")
                    
            except:
                print(f"Error Text: {response.text}")
                
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR")
        print("🔧 FIX: Server not running")
        print("- Start the server: python main.py")
        print("- Check if port 8001 is available")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR")
        print("🔧 FIX: Request timed out")
        print("- Server may be overloaded")
        print("- Check server logs for errors")
        return False
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

def run_diagnostics():
    """Run comprehensive POST request diagnostics"""
    
    print("🔍 POST Request Error Diagnostic Tool")
    print("="*60)
    
    tests = [
        # Test 1: Valid core request
        {
            "endpoint": "/core",
            "payload": {
                "module": "sample_text",
                "intent": "generate",
                "user_id": "test_user",
                "data": {"input_text": "Hello world"}
            },
            "description": "Valid Core Request (sample_text)"
        },
        
        # Test 2: Valid feedback request
        {
            "endpoint": "/feedback",
            "payload": {
                "generation_id": 1,
                "command": "+1",
                "user_id": "test_user",
                "comment": "Great work!"
            },
            "description": "Valid Feedback Request"
        },
        
        # Test 3: Invalid module (should fail with 422)
        {
            "endpoint": "/core",
            "payload": {
                "module": "invalid_module",
                "intent": "generate",
                "user_id": "test_user",
                "data": {}
            },
            "description": "Invalid Module (Expected 422 Error)"
        },
        
        # Test 4: Missing required fields (should fail with 422)
        {
            "endpoint": "/core",
            "payload": {
                "data": {"input_text": "Hello"}
            },
            "description": "Missing Required Fields (Expected 422 Error)"
        },
        
        # Test 5: Creator module request
        {
            "endpoint": "/core",
            "payload": {
                "module": "creator",
                "intent": "generate",
                "user_id": "creator_user",
                "data": {
                    "topic": "AI Technology",
                    "goal": "Educational content",
                    "type": "story"
                }
            },
            "description": "Creator Module Request"
        }
    ]
    
    results = []
    for test in tests:
        success = test_endpoint(
            test["endpoint"], 
            test["payload"], 
            test["description"]
        )
        results.append((test["description"], success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DIAGNOSTIC SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed < total:
        print(f"\n🔧 COMMON FIXES:")
        print("1. Ensure server is running: python main.py")
        print("2. Check payload format matches API requirements")
        print("3. Verify all required fields are present")
        print("4. Use correct enum values for module/intent")
        print("5. Check server logs for detailed error messages")

def quick_fix_examples():
    """Show quick fix examples for common errors"""
    
    print(f"\n{'='*60}")
    print("🛠️  QUICK FIX EXAMPLES")
    print(f"{'='*60}")
    
    print("\n1. ✅ CORRECT Core Request:")
    correct_core = {
        "module": "sample_text",
        "intent": "generate", 
        "user_id": "test_user",
        "data": {"input_text": "Hello world"}
    }
    print(json.dumps(correct_core, indent=2))
    
    print("\n2. ✅ CORRECT Feedback Request:")
    correct_feedback = {
        "generation_id": 1,
        "command": "+1",
        "user_id": "test_user",
        "comment": "Great work!"
    }
    print(json.dumps(correct_feedback, indent=2))
    
    print("\n3. ❌ COMMON MISTAKES:")
    print("- Missing required fields")
    print("- Invalid module names (use: finance, education, creator, sample_text)")
    print("- Invalid intent values (use: generate, analyze, review)")
    print("- Invalid feedback commands (use: +2, +1, -1, -2)")
    print("- Empty user_id")
    print("- generation_id <= 0 in feedback requests")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        quick_fix_examples()
    else:
        run_diagnostics()
        quick_fix_examples()