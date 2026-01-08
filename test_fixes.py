#!/usr/bin/env python3
"""
Quick test to verify fixes for failing tests
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.gateway import Gateway
from src.db.memory import ContextMemory

def test_memory_storage():
    """Test that memory storage works"""
    print("Testing memory storage...")
    
    # Test the gateway's memory directly
    gateway = Gateway()
    
    # Store a test interaction via gateway
    response = gateway.process_request(
        module="finance",
        intent="generate", 
        user_id="memory_test_user",
        data={"report_type": "quarterly"}
    )
    
    print(f"Gateway response: {response}")
    
    # Get history via gateway's memory
    history = gateway.memory.get_user_history("memory_test_user")
    print(f"History length: {len(history)}")
    
    if len(history) >= 1:
        print("PASS - Memory storage working")
        return True
    else:
        print("FAIL - Memory storage failed")
        print(f"Memory adapter type: {type(gateway.memory)}")
        return False

def test_gateway_processing():
    """Test gateway processing"""
    print("\nTesting gateway processing...")
    
    gateway = Gateway()
    
    # Test finance module
    response = gateway.process_request(
        module="finance",
        intent="generate",
        user_id="test_user",
        data={"report_type": "quarterly"}
    )
    
    print(f"Finance response: {response}")
    
    if response.get("status") == "success":
        print("PASS - Finance module working")
        finance_ok = True
    else:
        print("FAIL - Finance module failed")
        finance_ok = False
    
    # Test sample_text module
    response = gateway.process_request(
        module="sample_text", 
        intent="generate",
        user_id="test_user",
        data={"input_text": "Hello world"}
    )
    
    print(f"Sample text response: {response}")
    
    if response.get("status") == "success":
        print("PASS - Sample text module working")
        sample_ok = True
    else:
        print("FAIL - Sample text module failed")
        sample_ok = False
    
    return finance_ok and sample_ok

def test_module_interface():
    """Test module interface compatibility"""
    print("\nTesting module interfaces...")
    
    from src.modules.sample_text.module import SampleTextModule
    
    module = SampleTextModule()
    
    # Test if it has handle_request method
    has_handle_request = hasattr(module, 'handle_request')
    print(f"SampleTextModule has handle_request: {has_handle_request}")
    
    if has_handle_request:
        print("PASS - Module interface fixed")
        return True
    else:
        print("FAIL - Module interface still broken")
        return False

if __name__ == "__main__":
    print("Running quick tests to verify fixes...\n")
    
    memory_ok = test_memory_storage()
    gateway_ok = test_gateway_processing() 
    interface_ok = test_module_interface()
    
    print(f"\n{'='*50}")
    print("SUMMARY:")
    print(f"Memory storage: {'PASS' if memory_ok else 'FAIL'}")
    print(f"Gateway processing: {'PASS' if gateway_ok else 'FAIL'}")
    print(f"Module interface: {'PASS' if interface_ok else 'FAIL'}")
    
    if all([memory_ok, gateway_ok, interface_ok]):
        print("\nAll fixes working!")
    else:
        print("\nSome issues remain")