"""
Simple security test for SSPL Phase III
"""

import time
import json
import base64
import random
import requests
from nacl.signing import SigningKey

def test_security():
    """Test if security is working"""
    
    # Generate keypair
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    
    # Create request data
    body_data = {
        "module": "sample_text",
        "intent": "generate", 
        "user_id": "test_user",
        "data": {"text": "Security test"}
    }
    
    # Create security headers
    timestamp = str(int(time.time()))
    nonce = f"test_nonce_{random.randint(1000, 9999)}"
    message = json.dumps(body_data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signature = signing_key.sign(message).signature
    
    headers = {
        "X-SSPL-Timestamp": timestamp,
        "X-SSPL-Nonce": nonce,
        "X-SSPL-Signature": base64.b64encode(signature).decode(),
        "X-SSPL-Public-Key": base64.b64encode(bytes(verify_key)).decode(),
        "Content-Type": "application/json"
    }
    
    print("Testing security...")
    print(f"Timestamp: {timestamp}")
    print(f"Nonce: {nonce}")
    
    try:
        response = requests.post("http://localhost:8001/core", json=body_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Security is working!")
            print(f"Response: {response.json()}")
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_security()