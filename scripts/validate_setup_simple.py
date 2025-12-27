"""
Simple validation script for Windows compatibility
"""

import sys
import os
from pathlib import Path

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] Python 3.8+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    required = ['fastapi', 'uvicorn', 'pydantic', 'pytest']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package} installed")
        except ImportError:
            print(f"[ERROR] {package} missing")
            missing.append(package)
    
    if missing:
        print(f"[WARNING] Install missing packages: pip install {' '.join(missing)}")
        return False
    return True

def check_directories():
    dirs = ['db', 'modules', 'agents', 'core', 'tests', 'utils']
    all_exist = True
    
    for d in dirs:
        if Path(d).exists():
            print(f"[OK] {d}/ directory exists")
        else:
            print(f"[ERROR] {d}/ directory missing")
            all_exist = False
    
    return all_exist

def check_database():
    db_dir = Path('db')
    db_dir.mkdir(exist_ok=True)
    
    test_file = db_dir / '.test_write'
    try:
        test_file.write_text('test')
        test_file.unlink()
        print("[OK] Database directory is writable")
        return True
    except Exception as e:
        print(f"[ERROR] Database directory not writable: {e}")
        return False

def main():
    print("=" * 60)
    print("Core Integrator - Setup Validation")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Database", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        results.append(check_func())
    
    print("\n" + "=" * 60)
    if all(results):
        print("[SUCCESS] ALL CHECKS PASSED - READY FOR TESTING")
        return 0
    else:
        print("[FAILED] SOME CHECKS FAILED - FIX ISSUES BEFORE TESTING")
        return 1

if __name__ == "__main__":
    sys.exit(main())