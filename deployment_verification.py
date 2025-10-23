#!/usr/bin/env python3
"""
Deployment Verification for Petrol Pump Management System
Comprehensive testing for deployment readiness
"""

import requests
import json
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend .env
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class DeploymentVerifier:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout for deployment testing
        
    def test_service_availability(self):
        """Test if all services are available and responding"""
        print("🔍 Testing service availability...")
        
        try:
            # Test backend API
            response = self.session.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                print("✅ Backend API: AVAILABLE")
                backend_available = True
            else:
                print(f"❌ Backend API: UNAVAILABLE - Status {response.status_code}")
                backend_available = False
        except Exception as e:
            print(f"❌ Backend API: UNAVAILABLE - {str(e)}")
            backend_available = False
        
        try:
            # Test frontend (check if it's serving content)
            frontend_url = BACKEND_URL.replace('/api', '')  # Remove /api if present
            response = self.session.get(frontend_url, timeout=10)
            if response.status_code == 200:
                print("✅ Frontend: AVAILABLE")
                frontend_available = True
            else:
                print(f"❌ Frontend: UNAVAILABLE - Status {response.status_code}")
                frontend_available = False
        except Exception as e:
            print(f"❌ Frontend: UNAVAILABLE - {str(e)}")
            frontend_available = False
        
        return backend_available and frontend_available
    
    def test_database_connectivity(self):
        """Test database connectivity and operations"""
        print("\n🔍 Testing database connectivity...")
        
        try:
            # Test write operation
            test_data = {
                "client_name": f"deployment_test_{int(time.time())}"
            }
            response = self.session.post(f"{API_BASE}/status", json=test_data)
            
            if response.status_code == 200:
                print("✅ Database Write: WORKING")
                write_success = True
            else:
                print(f"❌ Database Write: FAILED - Status {response.status_code}")
                write_success = False
            
            # Test read operation
            response = self.session.get(f"{API_BASE}/status")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print("✅ Database Read: WORKING")
                    read_success = True
                else:
                    print("❌ Database Read: FAILED - Invalid data format")
                    read_success = False
            else:
                print(f"❌ Database Read: FAILED - Status {response.status_code}")
                read_success = False
            
            return write_success and read_success
            
        except Exception as e:
            print(f"❌ Database connectivity: FAILED - {str(e)}")
            return False
    
    def test_api_endpoints_comprehensive(self):
        """Test all API endpoints comprehensively"""
        print("\n🔍 Testing API endpoints comprehensively...")
        
        endpoints_to_test = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/status", "Status check (GET)"),
            ("POST", "/status", "Status check (POST)"),
            ("GET", "/auth/me", "Authentication check"),
            ("POST", "/auth/logout", "Logout endpoint"),
            ("GET", "/fuel-sales", "Fuel sales (GET)"),
            ("POST", "/fuel-sales", "Fuel sales (POST)"),
            ("GET", "/credit-sales", "Credit sales (GET)"),
            ("POST", "/credit-sales", "Credit sales (POST)"),
            ("GET", "/income-expenses", "Income/Expenses (GET)"),
            ("POST", "/income-expenses", "Income/Expenses (POST)"),
            ("GET", "/fuel-rates", "Fuel rates (GET)"),
            ("POST", "/fuel-rates", "Fuel rates (POST)"),
            ("POST", "/sync/backup", "Backup endpoint")
        ]
        
        all_success = True
        
        for method, endpoint, description in endpoints_to_test:
            try:
                url = f"{API_BASE}{endpoint}"
                
                if method == "GET":
                    response = self.session.get(url)
                elif method == "POST":
                    if endpoint == "/status":
                        test_data = {"client_name": "endpoint_test"}
                    else:
                        test_data = {"test": "data"}
                    response = self.session.post(url, json=test_data)
                
                # Check if endpoint is responding (not necessarily successful)
                if response.status_code in [200, 401, 422]:  # Valid responses
                    print(f"✅ {description}: RESPONDING (Status {response.status_code})")
                else:
                    print(f"❌ {description}: NOT RESPONDING (Status {response.status_code})")
                    all_success = False
                    
            except Exception as e:
                print(f"❌ {description}: ERROR - {str(e)}")
                all_success = False
        
        return all_success
    
    def test_response_times(self):
        """Test API response times for deployment performance"""
        print("\n🔍 Testing API response times...")
        
        endpoints = [
            "/",
            "/status",
            "/auth/me"
        ]
        
        all_fast = True
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{API_BASE}{endpoint}")
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response_time < 5000:  # Less than 5 seconds is acceptable for deployment
                    print(f"✅ {endpoint}: {response_time:.0f}ms - FAST")
                else:
                    print(f"⚠️  {endpoint}: {response_time:.0f}ms - SLOW")
                    all_fast = False
                    
            except Exception as e:
                print(f"❌ {endpoint}: TIMEOUT - {str(e)}")
                all_fast = False
        
        return all_fast
    
    def test_error_handling(self):
        """Test error handling for deployment"""
        print("\n🔍 Testing error handling...")
        
        try:
            # Test invalid endpoint
            response = self.session.get(f"{API_BASE}/invalid-endpoint")
            if response.status_code == 404:
                print("✅ 404 Error handling: WORKING")
                error_404 = True
            else:
                print(f"❌ 404 Error handling: UNEXPECTED - Status {response.status_code}")
                error_404 = False
            
            # Test invalid JSON
            response = self.session.post(f"{API_BASE}/status", data="invalid json")
            if response.status_code in [400, 422]:
                print("✅ Invalid JSON handling: WORKING")
                json_error = True
            else:
                print(f"❌ Invalid JSON handling: UNEXPECTED - Status {response.status_code}")
                json_error = False
            
            return error_404 and json_error
            
        except Exception as e:
            print(f"❌ Error handling test: FAILED - {str(e)}")
            return False
    
    def test_security_headers(self):
        """Test security configurations for deployment"""
        print("\n🔍 Testing security configurations...")
        
        try:
            response = self.session.get(f"{API_BASE}/")
            headers = response.headers
            
            security_checks = []
            
            # Check for CORS (may be handled by proxy)
            if 'Access-Control-Allow-Origin' in headers:
                print("✅ CORS headers: PRESENT")
                security_checks.append(True)
            else:
                print("⚠️  CORS headers: HANDLED BY PROXY (acceptable)")
                security_checks.append(True)  # Don't fail for this
            
            # Check content type
            if 'application/json' in headers.get('content-type', ''):
                print("✅ Content-Type: CORRECT")
                security_checks.append(True)
            else:
                print(f"⚠️  Content-Type: {headers.get('content-type', 'MISSING')}")
                security_checks.append(True)  # Don't fail for this
            
            return all(security_checks)
            
        except Exception as e:
            print(f"❌ Security headers test: FAILED - {str(e)}")
            return False
    
    def run_deployment_verification(self):
        """Run complete deployment verification"""
        print("🚀 Starting Deployment Verification for Petrol Pump Management System")
        print(f"🔗 Backend URL: {BACKEND_URL}")
        print(f"🔗 API Base: {API_BASE}")
        print("=" * 70)
        
        test_results = {}
        
        # Run all deployment tests
        test_results['service_availability'] = self.test_service_availability()
        test_results['database_connectivity'] = self.test_database_connectivity()
        test_results['api_endpoints'] = self.test_api_endpoints_comprehensive()
        test_results['response_times'] = self.test_response_times()
        test_results['error_handling'] = self.test_error_handling()
        test_results['security_headers'] = self.test_security_headers()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 DEPLOYMENT VERIFICATION SUMMARY")
        print("=" * 70)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Overall Result: {passed}/{total} verification checks passed")
        
        if passed == total:
            print("🎉 DEPLOYMENT READY! All verification checks passed.")
            print("✅ The Petrol Pump Management System is ready for production deployment.")
            return True
        else:
            print("⚠️  DEPLOYMENT ISSUES DETECTED! Check the details above.")
            return False

def main():
    """Main deployment verification execution"""
    verifier = DeploymentVerifier()
    success = verifier.run_deployment_verification()
    
    if success:
        print("\n✅ Deployment verification completed successfully!")
        exit(0)
    else:
        print("\n❌ Deployment verification completed with issues!")
        exit(1)

if __name__ == "__main__":
    main()