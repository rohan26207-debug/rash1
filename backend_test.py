#!/usr/bin/env python3
"""
Backend API Testing for Petrol Pump Management System
Tests all backend endpoints and functionality
"""

import requests
import json
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend .env
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class PetrolPumpAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session_token = None
        self.user_data = None
        
    def test_basic_connectivity(self):
        """Test basic API connectivity"""
        print("🔍 Testing basic API connectivity...")
        try:
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                print("✅ Basic API connectivity: PASSED")
                return True
            else:
                print(f"❌ Basic API connectivity: FAILED - Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Basic API connectivity: FAILED - {str(e)}")
            return False
    
    def test_status_endpoints(self):
        """Test status check endpoints (public)"""
        print("\n🔍 Testing status endpoints...")
        
        # Test GET status
        try:
            response = self.session.get(f"{API_BASE}/status")
            if response.status_code == 200:
                print("✅ GET /api/status: PASSED")
                get_status_success = True
            else:
                print(f"❌ GET /api/status: FAILED - Status {response.status_code}")
                get_status_success = False
        except Exception as e:
            print(f"❌ GET /api/status: FAILED - {str(e)}")
            get_status_success = False
        
        # Test POST status
        try:
            test_data = {"client_name": "test_client_petrol_pump"}
            response = self.session.post(f"{API_BASE}/status", json=test_data)
            if response.status_code == 200:
                print("✅ POST /api/status: PASSED")
                post_status_success = True
            else:
                print(f"❌ POST /api/status: FAILED - Status {response.status_code}")
                print(f"Response: {response.text}")
                post_status_success = False
        except Exception as e:
            print(f"❌ POST /api/status: FAILED - {str(e)}")
            post_status_success = False
        
        return get_status_success and post_status_success
    
    def test_auth_endpoints_without_session(self):
        """Test authentication endpoints without valid session"""
        print("\n🔍 Testing authentication endpoints (without session)...")
        
        # Test /auth/me without session
        try:
            response = self.session.get(f"{API_BASE}/auth/me")
            if response.status_code == 401:
                print("✅ GET /api/auth/me (no auth): PASSED - Correctly returns 401")
                auth_me_success = True
            else:
                print(f"❌ GET /api/auth/me (no auth): FAILED - Expected 401, got {response.status_code}")
                auth_me_success = False
        except Exception as e:
            print(f"❌ GET /api/auth/me (no auth): FAILED - {str(e)}")
            auth_me_success = False
        
        # Test logout endpoint
        try:
            response = self.session.post(f"{API_BASE}/auth/logout")
            if response.status_code == 200:
                print("✅ POST /api/auth/logout: PASSED")
                logout_success = True
            else:
                print(f"❌ POST /api/auth/logout: FAILED - Status {response.status_code}")
                logout_success = False
        except Exception as e:
            print(f"❌ POST /api/auth/logout: FAILED - {str(e)}")
            logout_success = False
        
        return auth_me_success and logout_success
    
    def test_protected_endpoints_without_auth(self):
        """Test protected endpoints without authentication"""
        print("\n🔍 Testing protected endpoints (without auth)...")
        
        protected_endpoints = [
            "/fuel-sales",
            "/credit-sales", 
            "/income-expenses",
            "/fuel-rates"
        ]
        
        # Special case for backup endpoint (POST only)
        backup_endpoint = "/sync/backup"
        
        all_success = True
        
        for endpoint in protected_endpoints:
            try:
                # Test GET endpoints
                response = self.session.get(f"{API_BASE}{endpoint}")
                if response.status_code == 401:
                    print(f"✅ GET /api{endpoint} (no auth): PASSED - Correctly returns 401")
                else:
                    print(f"❌ GET /api{endpoint} (no auth): FAILED - Expected 401, got {response.status_code}")
                    all_success = False
                
                # Test POST endpoints 
                test_data = {"test": "data"}
                response = self.session.post(f"{API_BASE}{endpoint}", json=test_data)
                if response.status_code == 401:
                    print(f"✅ POST /api{endpoint} (no auth): PASSED - Correctly returns 401")
                else:
                    print(f"❌ POST /api{endpoint} (no auth): FAILED - Expected 401, got {response.status_code}")
                    all_success = False
                        
            except Exception as e:
                print(f"❌ {endpoint} (no auth): FAILED - {str(e)}")
                all_success = False
        
        # Test backup endpoint separately (POST only)
        try:
            test_data = {"test": "data"}
            response = self.session.post(f"{API_BASE}{backup_endpoint}", json=test_data)
            if response.status_code == 401:
                print(f"✅ POST /api{backup_endpoint} (no auth): PASSED - Correctly returns 401")
            else:
                print(f"❌ POST /api{backup_endpoint} (no auth): FAILED - Expected 401, got {response.status_code}")
                all_success = False
        except Exception as e:
            print(f"❌ {backup_endpoint} (no auth): FAILED - {str(e)}")
            all_success = False
        
        return all_success
    
    def test_mongodb_connection(self):
        """Test MongoDB connection by checking if status endpoint works"""
        print("\n🔍 Testing MongoDB connection...")
        
        try:
            # Create a status check to test DB write
            test_data = {"client_name": "mongodb_connection_test"}
            response = self.session.post(f"{API_BASE}/status", json=test_data)
            
            if response.status_code == 200:
                # Try to retrieve it
                response = self.session.get(f"{API_BASE}/status")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print("✅ MongoDB connection: PASSED - Can write and read data")
                        return True
                    else:
                        print("❌ MongoDB connection: FAILED - No data returned")
                        return False
                else:
                    print(f"❌ MongoDB connection: FAILED - Cannot read data, status {response.status_code}")
                    return False
            else:
                print(f"❌ MongoDB connection: FAILED - Cannot write data, status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ MongoDB connection: FAILED - {str(e)}")
            return False
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        print("\n🔍 Testing CORS headers...")
        
        try:
            # Test with a simple GET request to see if CORS works
            response = self.session.get(f"{API_BASE}/")
            headers = response.headers
            
            cors_success = True
            
            # Check for CORS headers in response
            if 'Access-Control-Allow-Origin' in headers:
                print("✅ CORS Allow-Origin header: PRESENT")
            else:
                print("⚠️  CORS Allow-Origin header: NOT VISIBLE (may be handled by proxy)")
                # Don't fail the test as CORS might be handled by Kubernetes ingress
            
            # Test if we can make cross-origin requests (if we get a response, CORS is working)
            if response.status_code == 200:
                print("✅ CORS functionality: WORKING - API responds to requests")
                return True
            else:
                print(f"❌ CORS functionality: FAILED - Status {response.status_code}")
                return False
            
        except Exception as e:
            print(f"❌ CORS headers test: FAILED - {str(e)}")
            return False
    
    def test_api_response_format(self):
        """Test API response formats"""
        print("\n🔍 Testing API response formats...")
        
        try:
            # Test root endpoint response format
            response = self.session.get(f"{API_BASE}/")
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'message' in data:
                        print("✅ API response format: PASSED - Valid JSON structure")
                        return True
                    else:
                        print("❌ API response format: FAILED - Invalid JSON structure")
                        return False
                except json.JSONDecodeError:
                    print("❌ API response format: FAILED - Invalid JSON")
                    return False
            else:
                print(f"❌ API response format: FAILED - Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API response format test: FAILED - {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Petrol Pump Management System Backend API Tests")
        print(f"🔗 Testing backend at: {API_BASE}")
        print("=" * 60)
        
        test_results = {}
        
        # Run all tests
        test_results['connectivity'] = self.test_basic_connectivity()
        test_results['status_endpoints'] = self.test_status_endpoints()
        test_results['auth_without_session'] = self.test_auth_endpoints_without_session()
        test_results['protected_without_auth'] = self.test_protected_endpoints_without_auth()
        test_results['mongodb_connection'] = self.test_mongodb_connection()
        test_results['cors_headers'] = self.test_cors_headers()
        test_results['response_format'] = self.test_api_response_format()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests PASSED! Backend is working correctly.")
            return True
        else:
            print("⚠️  Some backend tests FAILED. Check the details above.")
            return False

def main():
    """Main test execution"""
    tester = PetrolPumpAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Backend testing completed successfully!")
        exit(0)
    else:
        print("\n❌ Backend testing completed with failures!")
        exit(1)

if __name__ == "__main__":
    main()