import requests
import json
import time

# Service URLs
MAIN_SERVICE = "http://localhost:8001"
EXTERNAL_SERVICE = "http://localhost:5001"

def test_complete_feedback_flow():
    """Test the complete generate -> feedback flow"""
    print("🧪 Testing Complete Feedback Flow")
    print("=" * 50)
    
    # Step 1: Generate content
    print("1️⃣ Generating content...")
    generate_payload = {
        "module": "creator",
        "intent": "generate",
        "user_id": "test_user_feedback",
        "data": {
            "prompt": "Write a short story about robots",
            "topic": "AI creativity"
        }
    }
    
    try:
        response = requests.post(f"{MAIN_SERVICE}/core", json=generate_payload, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
            
            # Extract generation_id
            generation_id = result.get("result", {}).get("generation_id")
            if generation_id:
                print(f"   ✅ Got generation_id: {generation_id}")
                
                # Step 2: Submit positive feedback
                print("\n2️⃣ Submitting positive feedback (+2)...")
                feedback_payload = {
                    "generation_id": generation_id,
                    "command": "+2",
                    "user_id": "test_user_feedback"
                }
                
                feedback_response = requests.post(f"{MAIN_SERVICE}/feedback", json=feedback_payload, timeout=10)
                print(f"   Status: {feedback_response.status_code}")
                print(f"   Response: {json.dumps(feedback_response.json(), indent=2)}")
                
                # Step 3: Check history to verify feedback was applied
                print("\n3️⃣ Checking history...")
                history_response = requests.get(f"{MAIN_SERVICE}/creator/history?user_id=all", timeout=10)
                print(f"   Status: {history_response.status_code}")
                history_data = history_response.json()
                print(f"   History: {json.dumps(history_data, indent=2)}")
                
                return True
            else:
                print("   ❌ No generation_id in response!")
                return False
        else:
            print(f"   ❌ Generate failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_external_service_direct():
    """Test external service directly to verify it returns generation_id"""
    print("\n🔧 Testing External Service Direct")
    print("=" * 50)
    
    try:
        # Test generate endpoint
        response = requests.post(
            f"{EXTERNAL_SERVICE}/generate",
            json={"prompt": "Test direct call"},
            timeout=10
        )
        print(f"Generate Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Generate Response: {json.dumps(result, indent=2)}")
            
            generation_id = result.get("generation_id")
            if generation_id:
                print(f"✅ External service returns generation_id: {generation_id}")
                
                # Test feedback endpoint
                feedback_response = requests.post(
                    f"{EXTERNAL_SERVICE}/feedback",
                    json={"generation_id": generation_id, "command": "+1"},
                    timeout=10
                )
                print(f"Feedback Status: {feedback_response.status_code}")
                print(f"Feedback Response: {json.dumps(feedback_response.json(), indent=2)}")
                return True
            else:
                print("❌ External service missing generation_id")
                return False
        else:
            print(f"❌ External service error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ External service error: {e}")
        return False

def check_services_running():
    """Check if both services are running"""
    print("🔍 Checking Services")
    print("=" * 50)
    
    services = [
        ("Main Service", MAIN_SERVICE),
        ("External Service", EXTERNAL_SERVICE)
    ]
    
    all_running = True
    for name, url in services:
        try:
            response = requests.get(f"{url}/", timeout=5)
            print(f"{name}: ✅ Running (Status: {response.status_code})")
        except Exception as e:
            print(f"{name}: ❌ Not running ({e})")
            all_running = False
    
    return all_running

if __name__ == "__main__":
    print("🚀 Feedback ID Mapping Test Suite")
    print("=" * 60)
    
    # Check if services are running
    if not check_services_running():
        print("\n❌ Please start both services first:")
        print("   Terminal 1: cd external/CreatorCore-Task && python app.py")
        print("   Terminal 2: python main.py")
        exit(1)
    
    # Run tests
    print("\n" + "=" * 60)
    external_works = test_external_service_direct()
    main_works = test_complete_feedback_flow()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"External Service Direct: {'✅ PASS' if external_works else '❌ FAIL'}")
    print(f"Complete Feedback Flow: {'✅ PASS' if main_works else '❌ FAIL'}")
    
    if external_works and main_works:
        print("\n🎉 ALL TESTS PASSED! Feedback ID mapping is working correctly!")
    else:
        print("\n🔧 Some tests failed. Check the output above for details.")