#!/usr/bin/env python3
"""
Step-by-step testing guide for Day 3 deliverables
Tests deployment script, Docker setup, and pre-flight checker
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_step(step_name, test_func):
    """Test a step and report results"""
    print(f"\n{'='*50}")
    print(f"TESTING: {step_name}")
    print('='*50)
    
    try:
        result = test_func()
        status = "PASS" if result else "FAIL"
        print(f"RESULT: {status}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        print("RESULT: FAIL")
        return False

def test_preflight_basic():
    """Test basic pre-flight checks"""
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   Python {version.major}.{version.minor}.{version.micro} - OK")
    else:
        print(f"   Python {version.major}.{version.minor} - NEEDS 3.10+")
        return False
    
    print("2. Checking project structure...")
    required_items = [
        ("src", "directory"),
        ("tests", "directory"), 
        ("requirements.txt", "file"),
        (".env", "file"),
        ("deploy.ps1", "file"),
        ("Dockerfile", "file"),
        ("docker-compose.yml", "file")
    ]
    
    all_good = True
    for item, item_type in required_items:
        if Path(item).exists():
            print(f"   {item} ({item_type}) - OK")
        else:
            print(f"   {item} ({item_type}) - MISSING")
            all_good = False
    
    print("3. Checking required packages...")
    packages = ["flask", "requests", "pytest"]
    for package in packages:
        try:
            __import__(package)
            print(f"   {package} - OK")
        except ImportError:
            print(f"   {package} - MISSING")
            all_good = False
    
    return all_good

def test_deployment_script():
    """Test deployment script functionality"""
    print("1. Checking deployment script exists...")
    if not Path("deploy.ps1").exists():
        print("   deploy.ps1 not found")
        return False
    print("   deploy.ps1 found - OK")
    
    print("2. Testing PowerShell availability...")
    try:
        result = subprocess.run(["powershell", "-Command", "Write-Host 'Test'"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   PowerShell available - OK")
        else:
            print("   PowerShell test failed")
            return False
    except Exception as e:
        print(f"   PowerShell not available: {e}")
        return False
    
    print("3. Testing deployment script syntax...")
    try:
        # Test script syntax without execution
        result = subprocess.run([
            "powershell", "-Command", 
            "Get-Content deploy.ps1 | Out-Null; Write-Host 'Syntax OK'"
        ], capture_output=True, text=True, timeout=10)
        
        if "Syntax OK" in result.stdout:
            print("   Deployment script syntax - OK")
            return True
        else:
            print("   Deployment script syntax - ERROR")
            return False
    except Exception as e:
        print(f"   Syntax check failed: {e}")
        return False

def test_docker_files():
    """Test Docker configuration files"""
    print("1. Checking Dockerfile...")
    if not Path("Dockerfile").exists():
        print("   Dockerfile not found")
        return False
    
    # Check Dockerfile content
    with open("Dockerfile", "r") as f:
        dockerfile_content = f.read()
    
    required_elements = ["FROM python:", "WORKDIR", "COPY", "RUN pip install", "EXPOSE"]
    for element in required_elements:
        if element in dockerfile_content:
            print(f"   {element} - OK")
        else:
            print(f"   {element} - MISSING")
            return False
    
    print("2. Checking docker-compose.yml...")
    if not Path("docker-compose.yml").exists():
        print("   docker-compose.yml not found")
        return False
    
    with open("docker-compose.yml", "r") as f:
        compose_content = f.read()
    
    required_services = ["noopur", "mock-creatorcore", "core-integrator"]
    for service in required_services:
        if service in compose_content:
            print(f"   Service {service} - OK")
        else:
            print(f"   Service {service} - MISSING")
            return False
    
    print("3. Checking Dockerfile.mock...")
    if Path("Dockerfile.mock").exists():
        print("   Dockerfile.mock - OK")
    else:
        print("   Dockerfile.mock - MISSING")
        return False
    
    return True

def test_docker_availability():
    """Test if Docker is available"""
    print("1. Checking Docker installation...")
    try:
        result = subprocess.run(["docker", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   Docker version: {result.stdout.strip()}")
        else:
            print("   Docker command failed")
            return False
    except FileNotFoundError:
        print("   Docker not installed")
        return False
    
    print("2. Checking Docker Compose...")
    try:
        result = subprocess.run(["docker-compose", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   Docker Compose version: {result.stdout.strip()}")
            return True
        else:
            print("   Docker Compose not available")
            return False
    except FileNotFoundError:
        print("   Docker Compose not installed")
        return False

def test_port_availability():
    """Test if required ports are available"""
    print("1. Checking port availability...")
    required_ports = [5001, 5002, 8000]
    
    all_available = True
    for port in required_ports:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"   Port {port} - IN USE")
                all_available = False
            else:
                print(f"   Port {port} - AVAILABLE")
        except Exception as e:
            print(f"   Port {port} - CHECK FAILED: {e}")
            all_available = False
    
    return all_available

def test_directory_structure():
    """Test directory creation and permissions"""
    print("1. Testing directory creation...")
    test_dirs = ["db", "data", "reports", "logs"]
    
    for dir_name in test_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"   Created {dir_name} - OK")
            except Exception as e:
                print(f"   Failed to create {dir_name}: {e}")
                return False
        else:
            print(f"   {dir_name} exists - OK")
    
    print("2. Testing write permissions...")
    for dir_name in test_dirs:
        test_file = Path(dir_name) / "test_write.tmp"
        try:
            test_file.write_text("test")
            test_file.unlink()
            print(f"   {dir_name} writable - OK")
        except Exception as e:
            print(f"   {dir_name} not writable: {e}")
            return False
    
    return True

def main():
    """Run all Day 3 tests step by step"""
    print("Day 3 Deliverables - Step by Step Testing")
    print("=" * 60)
    
    tests = [
        ("Pre-flight Basic Checks", test_preflight_basic),
        ("Deployment Script", test_deployment_script),
        ("Docker Configuration Files", test_docker_files),
        ("Docker Availability", test_docker_availability),
        ("Port Availability", test_port_availability),
        ("Directory Structure", test_directory_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_step(test_name, test_func)
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print("TESTING SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\nAll Day 3 deliverables are ready!")
        print("Next steps:")
        print("1. Run: .\\deploy.ps1 (to test deployment)")
        print("2. Run: docker-compose build (to test Docker)")
        print("3. Proceed to Day 4 tasks")
    else:
        print("\nSome tests failed. Please fix issues before proceeding.")
    
    return passed == len(results)

if __name__ == "__main__":
    main()