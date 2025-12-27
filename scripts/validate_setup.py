"""
Validation script to check if Core Integrator is ready for testing.
Run this before starting the server to catch any issues.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check required packages are installed"""
    required = ['fastapi', 'uvicorn', 'pydantic', 'pytest']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages: pip install {' '.join(missing)}")
        return False
    return True

def check_directories():
    """Check required directories exist"""
    dirs = ['db', 'modules', 'agents', 'core', 'tests', 'utils']
    all_exist = True
    
    for d in dirs:
        if Path(d).exists():
            print(f"✅ {d}/ directory exists")
        else:
            print(f"❌ {d}/ directory missing")
            all_exist = False
    
    return all_exist

def check_config_files():
    """Check required config files exist"""
    files = ['config.py', 'main.py', 'requirements.txt']
    all_exist = True
    
    for f in files:
        if Path(f).exists():
            print(f"✅ {f} exists")
        else:
            print(f"❌ {f} missing")
            all_exist = False
    
    return all_exist

def check_modules():
    """Check modules directory has valid modules"""
    modules_dir = Path('modules')
    if not modules_dir.exists():
        print("❌ modules/ directory not found")
        return False
    
    modules = [d for d in modules_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
    
    if not modules:
        print("⚠️  No modules found in modules/ directory")
        return True
    
    for module in modules:
        module_py = module / 'module.py'
        config_json = module / 'config.json'
        
        if module_py.exists() and config_json.exists():
            print(f"✅ Module {module.name} has module.py and config.json")
        else:
            print(f"⚠️  Module {module.name} incomplete (missing module.py or config.json)")
    
    return True

def check_database():
    """Check if database directory is writable"""
    db_dir = Path('db')
    db_dir.mkdir(exist_ok=True)
    
    test_file = db_dir / '.test_write'
    try:
        test_file.write_text('test')
        test_file.unlink()
        print("✅ Database directory is writable")
        return True
    except Exception as e:
        print(f"❌ Database directory not writable: {e}")
        return False

def check_port():
    """Check if port 8001 is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8001))
    sock.close()
    
    if result == 0:
        print("⚠️  Port 8001 is already in use")
        return False
    else:
        print("✅ Port 8001 is available")
        return True

def main():
    print("=" * 60)
    print("Core Integrator - Setup Validation")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Config Files", check_config_files),
        ("Modules", check_modules),
        ("Database", check_database),
        ("Port Availability", check_port),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        results.append(check_func())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED - READY FOR TESTING")
        print("\nStart server with: python main.py")
        print("API docs at: http://localhost:8001/docs")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - FIX ISSUES BEFORE TESTING")
        print("\nReview errors above and fix before starting server")
        return 1

if __name__ == "__main__":
    sys.exit(main())
