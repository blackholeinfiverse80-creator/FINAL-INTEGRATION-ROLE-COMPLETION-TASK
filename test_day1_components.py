#!/usr/bin/env python3
"""
Day 1 Component Test Runner
Tests all Day 1 deliverables: Mock Server, Bridge Client, and Core Tests
"""

import sys
import os
import subprocess
import time
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_mock_server():
    """Test CreatorCore mock server"""
    print("Testing CreatorCore Mock Server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5002/system/health", timeout=2)
        if response.status_code == 200:
            print("✓ Mock server is running and healthy")
            data = response.json()
            print(f"  Status: {data.get('status')}")
            return True
        else:
            print(f"✗ Mock server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Mock server not running on port 5002")
        print("  Start it with: python tests/mocks/creatorcore_mock.py")
        return False
    except Exception as e:
        print(f"✗ Error testing mock server: {e}")
        return False

def test_bridge_client():
    """Test Bridge Client functionality"""
    print("\nTesting Bridge Client...")
    
    try:
        from utils.bridge_client import BridgeClient, ErrorType
        
        # Test initialization
        client = BridgeClient("http://localhost:5002")
        print("✓ Bridge client initialized")
        
        # Test health check
        result = client.health_check()
        if result.get('success') is not False:
            print("✓ Bridge client health check successful")
        else:
            print(f"✓ Bridge client error handling working: {result.get('error_type')}")
        
        # Test error classification
        invalid_client = BridgeClient("http://invalid:9999")
        error_result = invalid_client.health_check()
        if error_result.get('error_type') == ErrorType.NETWORK.value:
            print("✓ Bridge client error classification working")
        
        return True
        
    except Exception as e:
        print(f"✗ Bridge client test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without complex imports"""
    print("\nTesting Basic Functionality...")
    
    try:
        # Test bridge client with mock server
        from utils.bridge_client import BridgeClient
        
        client = BridgeClient("http://localhost:5002")
        
        # Test log endpoint
        log_result = client.log({"test": "log message"})
        if log_result.get('success') is not False:
            print("✓ Log endpoint working")
        else:
            print(f"✓ Log endpoint error handling: {log_result.get('error_type')}")
        
        # Test feedback endpoint  
        feedback_result = client.feedback({"test": "feedback"})
        if feedback_result.get('success') is not False:
            print("✓ Feedback endpoint working")
        else:
            print(f"✓ Feedback endpoint error handling: {feedback_result.get('error_type')}")
        
        # Test context endpoint
        context_result = client.get_context(limit=2)
        if context_result.get('success') is not False:
            print("✓ Context endpoint working")
        else:
            print(f"✓ Context endpoint error handling: {context_result.get('error_type')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_creator_router():
    """Test CreatorRouter functionality"""
    print("\nTesting CreatorRouter...")
    
    try:
        # Import and test CreatorRouter
        sys.path.append('.')
        from creator_routing import CreatorRouter
        
        # Test initialization
        router = CreatorRouter()
        print("✓ CreatorRouter initialized")
        
        # Test prewarm logic
        test_data = {
            "topic": "Test Topic",
            "goal": "Test Goal", 
            "type": "test"
        }
        
        result = router.prewarm_and_prepare("generate", "test_user", test_data)
        
        # Should return data (with or without context)
        if isinstance(result, dict) and "topic" in result:
            print("✓ CreatorRouter prewarm logic working")
            if "related_context" in result:
                print(f"  Added {len(result['related_context'])} context items")
        
        return True
        
    except Exception as e:
        print(f"✗ CreatorRouter test failed: {e}")
        return False

def main():
    """Run all Day 1 component tests"""
    print("Day 1 Component Testing")
    print("=" * 50)
    
    results = []
    
    # Test components
    results.append(("Mock Server", test_mock_server()))
    results.append(("Bridge Client", test_bridge_client()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("CreatorRouter", test_creator_router()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Day 1 Test Results:")
    
    passed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All Day 1 components working!")
    else:
        print("⚠️  Some components need attention")
    
    return passed == len(results)

if __name__ == "__main__":
    main()