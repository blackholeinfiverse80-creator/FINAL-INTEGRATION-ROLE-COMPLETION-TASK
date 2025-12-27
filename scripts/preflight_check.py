#!/usr/bin/env python3
"""
Pre-flight Checker for Core Integrator
Validates environment, dependencies, and configuration before deployment
"""

import sys
import os
import subprocess
import json
import requests
from pathlib import Path
from datetime import datetime

class PreflightChecker:
    """Comprehensive pre-flight validation"""
    
    def __init__(self):
        self.checks = []
        self.errors = []
        self.warnings = []
        
    def add_check(self, name, status, message=""):
        """Add check result"""
        self.checks.append({
            "name": name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        if not status:
            self.errors.append(f"{name}: {message}")
        
    def add_warning(self, message):
        """Add warning"""
        self.warnings.append(message)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        try:
            version = sys.version_info
            if version.major == 3 and version.minor >= 10:
                self.add_check("Python Version", True, f"Python {version.major}.{version.minor}.{version.micro}")
                return True
            else:
                self.add_check("Python Version", False, f"Python {version.major}.{version.minor} - Requires 3.10+")
                return False
        except Exception as e:
            self.add_check("Python Version", False, str(e))
            return False
    
    def check_required_packages(self):
        """Check required Python packages"""
        required_packages = [
            "flask", "requests", "pytest", "coverage"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                self.add_check(f"Package: {package}", True)
            except ImportError:
                missing_packages.append(package)
                self.add_check(f"Package: {package}", False, "Not installed")
        
        if missing_packages:
            self.add_warning(f"Install missing packages: pip install {' '.join(missing_packages)}")
        
        return len(missing_packages) == 0
    
    def check_project_structure(self):
        """Check project directory structure"""
        required_dirs = [
            "src", "tests", "config", "documentation"
        ]
        
        required_files = [
            "requirements.txt", ".env", "main.py", "creator_routing.py"
        ]
        
        all_good = True
        
        # Check directories
        for dir_name in required_dirs:
            if Path(dir_name).exists():
                self.add_check(f"Directory: {dir_name}", True)
            else:
                self.add_check(f"Directory: {dir_name}", False, "Missing")
                all_good = False
        
        # Check files
        for file_name in required_files:
            if Path(file_name).exists():
                self.add_check(f"File: {file_name}", True)
            else:
                self.add_check(f"File: {file_name}", False, "Missing")
                all_good = False
        
        return all_good
    
    def check_configuration(self):
        """Check configuration files and environment variables"""
        config_checks = []
        
        # Check .env file
        if Path(".env").exists():
            self.add_check("Configuration File", True, ".env found")
            
            # Read and validate .env
            try:
                with open(".env", "r") as f:
                    env_content = f.read()
                    
                required_vars = [
                    "INTEGRATOR_USE_NOOPUR",
                    "NOOPUR_BASE_URL", 
                    "DB_PATH"
                ]
                
                for var in required_vars:
                    if var in env_content:
                        self.add_check(f"Config: {var}", True)
                    else:
                        self.add_check(f"Config: {var}", False, "Missing from .env")
                        config_checks.append(False)
                        
            except Exception as e:
                self.add_check("Configuration Parsing", False, str(e))
                return False
        else:
            self.add_check("Configuration File", False, ".env not found")
            return False
        
        return len([c for c in config_checks if not c]) == 0
    
    def check_database_setup(self):
        """Check database directories and permissions"""
        db_dirs = ["db", "data", "reports", "logs"]
        
        all_good = True
        
        for db_dir in db_dirs:
            dir_path = Path(db_dir)
            
            if not dir_path.exists():
                try:
                    dir_path.mkdir(exist_ok=True)
                    self.add_check(f"Database Dir: {db_dir}", True, "Created")
                except Exception as e:
                    self.add_check(f"Database Dir: {db_dir}", False, f"Cannot create: {e}")
                    all_good = False
            else:
                # Check write permissions
                test_file = dir_path / "test_write.tmp"
                try:
                    test_file.write_text("test")
                    test_file.unlink()
                    self.add_check(f"Database Dir: {db_dir}", True, "Writable")
                except Exception as e:
                    self.add_check(f"Database Dir: {db_dir}", False, f"Not writable: {e}")
                    all_good = False
        
        return all_good
    
    def check_port_availability(self):
        """Check if required ports are available"""
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
                    self.add_check(f"Port {port}", False, "Already in use")
                    all_available = False
                else:
                    self.add_check(f"Port {port}", True, "Available")
                    
            except Exception as e:
                self.add_check(f"Port {port}", False, f"Check failed: {e}")
                all_available = False
        
        return all_available
    
    def check_service_connectivity(self):
        """Check if services can be reached (if running)"""
        services = [
            ("Noopur", "http://localhost:5001/history"),
            ("Mock CreatorCore", "http://localhost:5002/system/health")
        ]
        
        for service_name, url in services:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    self.add_check(f"Service: {service_name}", True, "Responding")
                else:
                    self.add_check(f"Service: {service_name}", False, f"HTTP {response.status_code}")
            except requests.exceptions.ConnectionError:
                self.add_check(f"Service: {service_name}", False, "Not running (expected)")
            except Exception as e:
                self.add_check(f"Service: {service_name}", False, str(e))
    
    def check_docker_availability(self):
        """Check if Docker is available for containerization"""
        try:
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.add_check("Docker", True, result.stdout.strip())
                
                # Check docker-compose
                compose_result = subprocess.run(["docker-compose", "--version"],
                                              capture_output=True, text=True, timeout=5)
                if compose_result.returncode == 0:
                    self.add_check("Docker Compose", True, compose_result.stdout.strip())
                else:
                    self.add_check("Docker Compose", False, "Not available")
                    
                return True
            else:
                self.add_check("Docker", False, "Command failed")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.add_check("Docker", False, "Not installed")
            return False
    
    def run_all_checks(self):
        """Run all pre-flight checks"""
        print("Core Integrator Pre-flight Check")
        print("=" * 50)
        
        # Run checks
        self.check_python_version()
        self.check_required_packages()
        self.check_project_structure()
        self.check_configuration()
        self.check_database_setup()
        self.check_port_availability()
        self.check_service_connectivity()
        self.check_docker_availability()
        
        # Generate report
        return self.generate_report()
    
    def generate_report(self):
        """Generate pre-flight report"""
        passed = len([c for c in self.checks if c["status"]])
        total = len(self.checks)
        
        print(f"\nPre-flight Check Results: {passed}/{total} passed")
        print("-" * 50)
        
        # Show results
        for check in self.checks:
            status_icon = "✓" if check["status"] else "✗"
            print(f"{status_icon} {check['name']}: {check['message']}")
        
        # Show warnings
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"⚠ {warning}")
        
        # Show errors
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                print(f"✗ {error}")
        
        # Overall status
        success = len(self.errors) == 0
        print(f"\nOverall Status: {'PASS' if success else 'FAIL'}")
        
        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_checks": total,
            "passed_checks": passed,
            "failed_checks": total - passed,
            "success": success,
            "checks": self.checks,
            "warnings": self.warnings,
            "errors": self.errors
        }
        
        # Ensure reports directory exists
        Path("reports").mkdir(exist_ok=True)
        
        with open("reports/preflight_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"Report saved: reports/preflight_report.json")
        
        return success

def main():
    """Main pre-flight check function"""
    checker = PreflightChecker()
    success = checker.run_all_checks()
    
    if success:
        print("\n🎉 Pre-flight check passed! Ready for deployment.")
        return 0
    else:
        print("\n❌ Pre-flight check failed. Please fix errors before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())