#!/usr/bin/env python3
"""
Test Pydantic validation for invalid module names
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.models import CoreRequest
from pydantic import ValidationError

def test_pydantic_validation():
    """Test that Pydantic properly validates module names"""
    
    print("Testing Pydantic validation...")
    
    # Valid request
    try:
        valid_request = CoreRequest(
            module="finance",
            intent="generate", 
            user_id="test_user",
            data={}
        )
        print("PASS - Valid request accepted")
    except ValidationError as e:
        print(f"FAIL - Valid request rejected: {e}")
        return False
    
    # Invalid module
    try:
        invalid_request = CoreRequest(
            module="invalid_module",
            intent="generate",
            user_id="test_user", 
            data={}
        )
        print("FAIL - Invalid module accepted (should be rejected)")
        return False
    except ValidationError as e:
        print("PASS - Invalid module properly rejected")
        print(f"Validation error: {e}")
        return True

if __name__ == "__main__":
    success = test_pydantic_validation()
    print(f"\nPydantic validation: {'WORKING' if success else 'BROKEN'}")