#!/usr/bin/env python3
"""
PHASE 13.7 Alpha Deployment - Backend API Tests (Local)
=======================================================
Testing Alpha Deployment endpoints locally since external routing isn't configured.

Test Coverage:
- Health check
- Deployment statistics  
- Active deployments (should be 5)
- Shadow deployments (should be 18)
- Signal generation from factor values
- Signal summary for BTCUSDT
- Safety scan functionality
- Deployment snapshots
- Deployment history

Expected State: 23 factors deployed (5 active, 18 shadow)
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

class AlphaDeploymentLocalTester:
    """PHASE 13.7 Alpha Deployment Local API Tests"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AlphaDeployment-Tester/1.0'
        })

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result."""
        self.tests_run += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {name}")
        if details:
            print(f"     {details}")
        
        if success:
            self.tests_passed += 1
        else:
            self.failed_tests.append({"test": name, "details": details})

    def make_request(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)."""
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=10)
            else:
                return False, {}, 0
            
            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            return success, response_data, response.status_code
            
        except Exception as e:
            return False, {"error": str(e)}, 0

    def run_all_tests(self):
        """Run all Alpha Deployment test cases."""
        print("=" * 80)
        print("🚀 PHASE 13.7 Alpha Deployment - Backend API Tests (Local)")
        print("=" * 80)
        print("Expected State: 23 factors deployed (5 active, 18 shadow)")
        print("=" * 80)
        
        # Test 1: Health Check
        print("\n🔍 Testing Alpha Deployment Health Check...")
        success, data, status = self.make_request('GET', 'alpha-deployment/health')
        
        if success and data.get('status') == 'healthy':
            module = data.get('module', '')
            version = data.get('version', '')
            active_count = data.get('active_count', 0)
            shadow_count = data.get('shadow_count', 0)
            
            self.log_test("Alpha Deployment Health Check", True, 
                         f"Status: {data.get('status')}, Module: {module}, Version: {version}")
            self.log_test("Health - Active Count = 5", active_count == 5, f"Active deployments: {active_count}")
            self.log_test("Health - Shadow Count = 18", shadow_count == 18, f"Shadow deployments: {shadow_count}")
        else:
            self.log_test("Alpha Deployment Health Check", False, f"Status: {status}, Data: {data}")

        # Test 2: Deployment Stats
        print("\n🔍 Testing Deployment Statistics...")
        success, data, status = self.make_request('GET', 'alpha-deployment/stats')
        
        if success:
            summary = data.get('summary', {})
            registry = data.get('registry', {})
            signal_engine = data.get('signal_engine', {})
            safety = data.get('safety', {})
            
            # Check summary stats
            total_deployed = summary.get('total_deployed', 0)
            active = summary.get('active', 0)
            shadow = summary.get('shadow', 0)
            
            self.log_test("Stats - Summary Present", len(summary) > 0, 
                         f"Total: {total_deployed}, Active: {active}, Shadow: {shadow}")
            self.log_test("Stats - Active = 5", active == 5, f"Active: {active}")
            self.log_test("Stats - Shadow = 18", shadow == 18, f"Shadow: {shadow}")
            self.log_test("Stats - Total = 23", total_deployed == 23, f"Total: {total_deployed}")
        else:
            self.log_test("Deployment Stats", False, f"Status: {status}, Data: {data}")

        # Test 3: Active Deployments
        print("\n🔍 Testing Active Deployments...")
        success, data, status = self.make_request('GET', 'alpha-deployment/active')
        
        if success:
            deployments = data.get('deployments', [])
            count = data.get('count', 0)
            
            self.log_test("Active Deployments Count = 5", count == 5, f"Found {count} active deployments")
            
            if deployments:
                deployment = deployments[0]
                required_fields = ['deployment_id', 'factor_id', 'status', 'deployment_mode']
                present_fields = [field for field in required_fields if field in deployment]
                self.log_test("Active Deployment Structure", len(present_fields) >= 3, 
                             f"Present fields: {present_fields}")
        else:
            self.log_test("Active Deployments", False, f"Status: {status}, Data: {data}")

        # Test 4: Shadow Deployments
        print("\n🔍 Testing Shadow Deployments...")
        success, data, status = self.make_request('GET', 'alpha-deployment/shadow')
        
        if success:
            deployments = data.get('deployments', [])
            count = data.get('count', 0)
            
            self.log_test("Shadow Deployments Count = 18", count == 18, f"Found {count} shadow deployments")
            
            if deployments:
                deployment = deployments[0]
                required_fields = ['deployment_id', 'factor_id', 'status', 'shadow_mode']
                present_fields = [field for field in required_fields if field in deployment]
                self.log_test("Shadow Deployment Structure", len(present_fields) >= 3, 
                             f"Present fields: {present_fields}")
        else:
            self.log_test("Shadow Deployments", False, f"Status: {status}, Data: {data}")

        # Test 5: Signal Generation
        print("\n🔍 Testing Signal Generation...")
        signal_request = {
            "factor_values": {
                "momentum_factor_001": 0.65,
                "breakout_factor_002": -0.45,
                "trend_factor_003": 0.23,
                "volatility_factor_004": 0.78,
                "regime_factor_005": -0.12
            },
            "symbol": "BTCUSDT",
            "regime": "TRENDING", 
            "regime_confidence": 0.75
        }
        
        success, data, status = self.make_request('POST', 'alpha-deployment/signals/generate', signal_request)
        
        if success:
            symbol = data.get('symbol', '')
            signals_generated = data.get('signals_generated', 0)
            signals = data.get('signals', [])
            aggregated = data.get('aggregated', {})
            
            self.log_test("Signal Generation", signals_generated >= 0, 
                         f"Generated {signals_generated} signals for {symbol}")
            
            if signals:
                signal = signals[0]
                required_fields = ['signal_id', 'deployment_id', 'direction', 'strength', 'confidence']
                present_fields = [field for field in required_fields if field in signal]
                self.log_test("Signal Structure", len(present_fields) >= 4, 
                             f"Present fields: {present_fields}")
            
            # Check aggregated signal
            agg_direction = aggregated.get('direction')
            self.log_test("Aggregated Signal", agg_direction is not None, 
                         f"Direction: {agg_direction}")
        else:
            self.log_test("Signal Generation", False, f"Status: {status}, Data: {data}")

        # Test 6: Signal Summary
        print("\n🔍 Testing Signal Summary...")
        success, data, status = self.make_request('GET', 'alpha-deployment/signals/BTCUSDT/summary')
        
        if success:
            symbol = data.get('symbol', '')
            active_signals = data.get('active_signals', 0)
            direction = data.get('direction', '')
            
            self.log_test("Signal Summary for BTCUSDT", symbol == 'BTCUSDT', 
                         f"Symbol: {symbol}, Active signals: {active_signals}")
            self.log_test("Summary Direction", direction in ['long', 'short', 'neutral'], 
                         f"Direction: {direction}")
        else:
            self.log_test("Signal Summary", False, f"Status: {status}, Data: {data}")

        # Test 7: Safety Scan
        print("\n🔍 Testing Safety Scan...")
        success, data, status = self.make_request('GET', 'alpha-deployment/safety/scan')
        
        if success:
            scan_id = data.get('scan_id')
            scanned_deployments = data.get('scanned_deployments', 0)
            
            self.log_test("Safety Scan Execution", scan_id is not None or scanned_deployments >= 0, 
                         f"Scanned: {scanned_deployments}")
        else:
            self.log_test("Safety Scan", False, f"Status: {status}, Data: {data}")

        # Test 8: Deployment Snapshot
        print("\n🔍 Testing Deployment Snapshot...")
        success, data, status = self.make_request('POST', 'alpha-deployment/snapshot')
        
        if success:
            snapshot_id = data.get('snapshot_id')
            total_deployed = data.get('total_deployed', 0)
            active_count = data.get('active_count', 0)
            shadow_count = data.get('shadow_count', 0)
            
            self.log_test("Snapshot Creation", snapshot_id is not None, 
                         f"Snapshot ID: {snapshot_id}")
            self.log_test("Snapshot - Total Deployed = 23", total_deployed == 23, 
                         f"Total deployed: {total_deployed}")
            self.log_test("Snapshot - Active/Shadow Counts", 
                         active_count == 5 and shadow_count == 18, 
                         f"Active: {active_count}, Shadow: {shadow_count}")
        else:
            self.log_test("Deployment Snapshot", False, f"Status: {status}, Data: {data}")

        # Test 9: Deployment History
        print("\n🔍 Testing Deployment History...")
        success, data, status = self.make_request('GET', 'alpha-deployment/history?limit=50')
        
        if success:
            history = data.get('history', [])
            count = data.get('count', 0)
            
            self.log_test("Deployment History", count >= 0, 
                         f"Found {count} history entries")
            
            if history:
                entry = history[0]
                expected_fields = ['action', 'decided_at']
                present_fields = [field for field in expected_fields if field in entry]
                self.log_test("History Entry Structure", len(present_fields) >= 1, 
                             f"Present fields: {present_fields}")
        else:
            self.log_test("Deployment History", False, f"Status: {status}, Data: {data}")

        # Print summary
        print("\n" + "=" * 80)
        print("📊 ALPHA DEPLOYMENT TEST SUMMARY")
        print("=" * 80)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"{i}. {failure['test']}")
                if failure['details']:
                    print(f"   {failure['details']}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    print("🔧 Starting PHASE 13.7 Alpha Deployment Local API Tests...")
    
    tester = AlphaDeploymentLocalTester()
    success = tester.run_all_tests()
    
    print(f"\n🏁 Testing completed. Success: {success}")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())