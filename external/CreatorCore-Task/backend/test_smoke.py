import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_generate_endpoint():
    """Test the /generate endpoint"""
    print("Testing /generate endpoint...")
    payload = {
        "topic": "Test Topic",
        "goal": "Test Goal",
        "type": "story"
    }
    try:
        response = requests.post(f"{BASE_URL}/generate", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✓ Generate endpoint working")
            print(f"  Response keys: {list(data.keys())}")
            if "related_context" in data:
                print(f"  Related context found: {len(data['related_context'])} items")
            return data.get("id")
        else:
            print(f"✗ Generate endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Generate endpoint error: {e}")
        return None

def test_feedback_endpoint(generation_id):
    """Test the /feedback endpoint"""
    print("Testing /feedback endpoint...")
    if not generation_id:
        print("✗ No generation ID to test feedback")
        return

    payload = {
        "id": generation_id,
        "feedback": "This is great work, I love it!"
    }
    try:
        response = requests.post(f"{BASE_URL}/feedback", json=payload)
        if response.status_code == 200:
            print("✓ Feedback endpoint working")
        else:
            print(f"✗ Feedback endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Feedback endpoint error: {e}")

def test_history_endpoint():
    """Test the /history/<topic> endpoint"""
    print("Testing /history endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/history/Test Topic")
        if response.status_code == 200:
            data = response.json()
            print("✓ History endpoint working")
            print(f"  History data keys: {list(data.keys()) if data else 'None'}")
        elif response.status_code == 404:
            print("✓ History endpoint working (no data found)")
        else:
            print(f"✗ History endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ History endpoint error: {e}")

def run_smoke_tests():
    """Run all smoke tests"""
    print("Starting smoke tests for CreatorCore Backend...")
    print("=" * 50)

    # Start Flask app in background (assuming it's not running)
    # Note: In real testing, you'd start the app programmatically

    generation_id = test_generate_endpoint()
    time.sleep(1)  # Brief pause

    test_feedback_endpoint(generation_id)
    time.sleep(1)

    test_history_endpoint()

    print("=" * 50)
    print("Smoke tests completed!")

if __name__ == "__main__":
    run_smoke_tests()