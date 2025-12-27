"""
Security client for testing SSPL Phase III with MongoDB
"""

import time
import json
import base64
import random
import requests
from nacl.signing import SigningKey

class SSPLClient:
    """Client for making signed requests to Core Integrator with SSPL security."""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        # Generate keypair for this session
        self.signing_key = SigningKey.generate()
        self.verify_key = self.signing_key.verify_key
        print(f"Generated keypair for session")
    
    def create_signed_request(self, body_data):
        """Create signed request with all required SSPL headers."""
        # Auto-generate security data
        timestamp = str(int(time.time()))
        nonce = f"nonce_{random.randint(1000, 9999)}_{int(time.time())}"
        
        # Create canonical message
        message = json.dumps(body_data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        
        # Sign message
        signature = self.signing_key.sign(message).signature
        
        # Create headers (ALL AUTOMATIC)
        headers = {
            "X-SSPL-Timestamp": timestamp,
            "X-SSPL-Nonce": nonce,
            "X-SSPL-Signature": base64.b64encode(signature).decode(),
            "X-SSPL-Public-Key": base64.b64encode(bytes(self.verify_key)).decode(),
            "Content-Type": "application/json"
        }
        
        return headers, body_data
    
    def make_request(self, endpoint, body_data):
        """Make a signed request to the Core Integrator."""
        headers, body = self.create_signed_request(body_data)
        
        print(f"Making signed request to {endpoint}")
        print(f"   Timestamp: {headers['X-SSPL-Timestamp']}")
        print(f"   Nonce: {headers['X-SSPL-Nonce']}")
        print(f"   Signature: {headers['X-SSPL-Signature'][:20]}...")
        
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=body, headers=headers)
        
        return response

def test_security_with_mongodb():
    """Test SSPL security with MongoDB backend."""
    print("=" * 60)
    print("SSPL Security + MongoDB Integration Test")
    print("=" * 60)
    
    client = SSPLClient()
    
    # Test 1: Sample Text Module
    print("\nTest 1: Sample Text Module")
    body = {
        "module": "sample_text",
        "intent": "generate",
        "user_id": "secure_user_001",
        "data": {"text": "Testing SSPL security with MongoDB Atlas"}
    }
    
    try:
        response = client.make_request("/core", body)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['status']}")
            print(f"   Result: {result['result']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Finance Module
    print("\nTest 2: Finance Module")
    body = {
        "module": "finance", 
        "intent": "generate",
        "user_id": "secure_user_001",
        "data": {"report_type": "quarterly", "period": "Q4 2024"}
    }
    
    try:
        response = client.make_request("/core", body)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['status']}")
            print(f"   Result: {result['result']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Context Retrieval (should work with previous requests)
    print("\nTest 3: Context Retrieval")
    try:
        response = requests.get(f"{client.base_url}/get-context?user_id=secure_user_001")
        if response.status_code == 200:
            context = response.json()
            print(f"✅ Retrieved {len(context)} context entries from MongoDB")
            for i, entry in enumerate(context):
                print(f"   {i+1}. {entry['module']} - {entry['timestamp']}")
        else:
            print(f"❌ Context retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Security + MongoDB Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_security_with_mongodb()