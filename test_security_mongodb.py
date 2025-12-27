"""
Quick test script for SSPL Security + MongoDB
Run this after starting the server with: python main.py
"""

import requests
import time
import json
import base64
import random
from nacl.signing import SigningKey

def test_without_security():
    """Test request without security headers (should fail)."""
    print("🔓 Testing request WITHOUT security headers...")
    
    try:
        response = requests.post("http://localhost:8001/core", json={
            "module": "sample_text",
            "intent": "generate",
            "user_id": "insecure_user",
            "data": {"text": "This should fail"}
        })
        
        if response.status_code == 400:
            print("✅ GOOD: Request rejected (missing security headers)")
        else:
            print(f"❌ BAD: Request allowed without security: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_with_security():
    """Test request with proper security headers (should succeed)."""
    print("\n🔒 Testing request WITH security headers...")
    
    try:
        # Generate keypair
        signing_key = SigningKey.generate()
        verify_key = signing_key.verify_key
        
        # Create request
        body = {
            "module": "sample_text",
            "intent": "generate",
            "user_id": "secure_user",
            "data": {"text": "This should work with security"}
        }
        
        # Generate security headers
        timestamp = str(int(time.time()))
        nonce = f"test_nonce_{random.randint(1000, 9999)}"
        message = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        signature = signing_key.sign(message).signature
        
        headers = {
            "X-SSPL-Timestamp": timestamp,
            "X-SSPL-Nonce": nonce,
            "X-SSPL-Signature": base64.b64encode(signature).decode(),
            "X-SSPL-Public-Key": base64.b64encode(bytes(verify_key)).decode(),
            "Content-Type": "application/json"
        }
        
        response = requests.post("http://localhost:8001/core", json=body, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS: Secure request processed")
            print(f"   Status: {result['status']}")
            print(f"   Result: {result['result']}")
        else:
            print(f"❌ FAILED: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_mongodb_storage():
    """Test that data is stored in MongoDB."""
    print("\n💾 Testing MongoDB storage...")
    
    try:
        response = requests.get("http://localhost:8001/get-context?user_id=secure_user")
        
        if response.status_code == 200:
            context = response.json()
            print(f"✅ MongoDB working: {len(context)} entries retrieved")
        else:
            print(f"❌ MongoDB test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("SSPL Security + MongoDB Test")
    print("=" * 50)
    print("Make sure server is running: python main.py")
    print()
    
    test_without_security()
    test_with_security() 
    test_mongodb_storage()
    
    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)