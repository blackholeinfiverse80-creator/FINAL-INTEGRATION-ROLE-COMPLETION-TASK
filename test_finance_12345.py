#!/usr/bin/env python3
import requests
import json

def test_finance_post():
    url = "http://localhost:8001/core"
    payload = {
        "module": "finance",
        "intent": "generate", 
        "user_id": "12345",
        "data": {"report_type": "quarterly"}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS - Finance module working")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print("❌ FAILED")
            try:
                error = response.json()
                print(f"Error: {json.dumps(error, indent=2)}")
            except:
                print(f"Error text: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Server not running - start with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_finance_post()