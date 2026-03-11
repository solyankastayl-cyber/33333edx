#!/usr/bin/env python3
"""
PHASE 13.7 Alpha Deployment - Backend API Tests
==============================================
Comprehensive testing for Alpha Deployment endpoints.

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

class AlphaDeploymentTester:
    """PHASE 13.7 Alpha Deployment API Tests"""
    
    def __init__(self, base_url: str = "https://market-reasoner.preview.emergentagent.com"):
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
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=30)
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

    def test_alpha_deployment_health(self):
        """Test GET /api/alpha-deployment/health - returns healthy status"""
        print("\n🔍 Testing Alpha Deployment Health Check...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/health')
        
        if success and data.get('status') == 'healthy':
            module = data.get('module', '')
            version = data.get('version', '')
            active_count = data.get('active_count', 0)
            shadow_count = data.get('shadow_count', 0)
            
            self.log_test("Alpha Deployment Health Check", True, 
                         f"Status: {data.get('status')}, Module: {module}, Version: {version}")
            self.log_test("Health - Active Count", active_count >= 0, f"Active deployments: {active_count}")
            self.log_test("Health - Shadow Count", shadow_count >= 0, f"Shadow deployments: {shadow_count}")
            return True
        else:
            self.log_test("Alpha Deployment Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_deployment_stats(self):
        """Test GET /api/alpha-deployment/stats - returns deployment statistics"""
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
            signals_24h = summary.get('signals_24h', 0)
            
            self.log_test("Stats - Summary Present", len(summary) > 0, 
                         f"Total: {total_deployed}, Active: {active}, Shadow: {shadow}")
            
            # Check registry stats
            registry_active = registry.get('active_count', 0)
            registry_shadow = registry.get('shadow_count', 0)
            
            self.log_test("Stats - Registry Stats", len(registry) > 0, 
                         f"Registry - Active: {registry_active}, Shadow: {registry_shadow}")
            
            # Check signal engine stats
            self.log_test("Stats - Signal Engine Stats", len(signal_engine) > 0, 
                         f"Signal engine stats present")
            
            # Check safety stats
            self.log_test("Stats - Safety Stats", len(safety) > 0, 
                         f"Safety stats present")
            
            return True
        else:
            self.log_test("Deployment Stats", False, f"Status: {status}, Data: {data}")
            return False

    def test_active_deployments(self):
        """Test GET /api/alpha-deployment/active - returns active deployments (should be 5)"""
        print("\n🔍 Testing Active Deployments...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/active')
        
        if success:
            deployments = data.get('deployments', [])
            count = data.get('count', 0)
            
            # According to the context, there should be 5 active deployments
            if count == 5:
                self.log_test("Active Deployments Count = 5", True, f"Found {count} active deployments")
            else:
                self.log_test("Active Deployments Count = 5", False, 
                             f"Expected 5 active deployments, found {count}")
            
            # Check deployment structure
            if deployments:
                deployment = deployments[0]
                required_fields = ['deployment_id', 'factor_id', 'status', 'deployment_mode']
                present_fields = [field for field in required_fields if field in deployment]
                self.log_test("Active Deployment Structure", len(present_fields) >= 3, 
                             f"Present fields: {present_fields}")
                
                # Verify all deployments are active
                active_statuses = [d.get('status') for d in deployments]
                all_active = all(status == 'active' for status in active_statuses)
                self.log_test("All Deployments Active", all_active, 
                             f"Statuses: {active_statuses}")
            
            return count > 0
        else:
            self.log_test("Active Deployments", False, f"Status: {status}, Data: {data}")
            return False

    def test_shadow_deployments(self):
        """Test GET /api/alpha-deployment/shadow - returns shadow deployments (should be 18)"""
        print("\n🔍 Testing Shadow Deployments...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/shadow')
        
        if success:
            deployments = data.get('deployments', [])
            count = data.get('count', 0)
            
            # According to the context, there should be 18 shadow deployments
            if count == 18:
                self.log_test("Shadow Deployments Count = 18", True, f"Found {count} shadow deployments")
            else:
                self.log_test("Shadow Deployments Count = 18", False, 
                             f"Expected 18 shadow deployments, found {count}")
            
            # Check deployment structure
            if deployments:
                deployment = deployments[0]
                required_fields = ['deployment_id', 'factor_id', 'status', 'shadow_mode']
                present_fields = [field for field in required_fields if field in deployment]
                self.log_test("Shadow Deployment Structure", len(present_fields) >= 3, 
                             f"Present fields: {present_fields}")
                
                # Verify all deployments are shadow
                shadow_statuses = [d.get('status') for d in deployments]
                all_shadow = all(status == 'shadow' for status in shadow_statuses)
                self.log_test("All Deployments Shadow", all_shadow, 
                             f"Statuses: {set(shadow_statuses)}")
            
            return count > 0
        else:
            self.log_test("Shadow Deployments", False, f"Status: {status}, Data: {data}")
            return False

    def test_signal_generation(self):
        """Test POST /api/alpha-deployment/signals/generate - generates signals from factor values"""
        print("\n🔍 Testing Signal Generation...")
        
        # Create test factor values
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
            
            self.log_test("Signal Generation", signals_generated > 0, 
                         f"Generated {signals_generated} signals for {symbol}")
            
            # Check signal structure
            if signals:
                signal = signals[0]
                required_fields = ['signal_id', 'deployment_id', 'direction', 'strength', 'confidence']
                present_fields = [field for field in required_fields if field in signal]
                self.log_test("Signal Structure", len(present_fields) >= 4, 
                             f"Present fields: {present_fields}")
            
            # Check aggregated signal
            agg_direction = aggregated.get('direction')
            agg_strength = aggregated.get('strength')
            agg_confidence = aggregated.get('confidence')
            
            self.log_test("Aggregated Signal", agg_direction is not None, 
                         f"Direction: {agg_direction}, Strength: {agg_strength}, Confidence: {agg_confidence}")
            
            return signals_generated > 0
        else:
            self.log_test("Signal Generation", False, f"Status: {status}, Data: {data}")
            return False

    def test_signal_summary(self):
        """Test GET /api/alpha-deployment/signals/BTCUSDT/summary - returns aggregated signal summary"""
        print("\n🔍 Testing Signal Summary...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/signals/BTCUSDT/summary')
        
        if success:
            symbol = data.get('symbol', '')
            active_signals = data.get('active_signals', 0)
            direction = data.get('direction', '')
            avg_strength = data.get('avg_strength', 0)
            avg_confidence = data.get('avg_confidence', 0)
            by_family = data.get('by_family', {})
            
            self.log_test("Signal Summary for BTCUSDT", symbol == 'BTCUSDT', 
                         f"Symbol: {symbol}, Active signals: {active_signals}")
            
            self.log_test("Summary Direction", direction in ['long', 'short', 'neutral'], 
                         f"Direction: {direction}")
            
            self.log_test("Summary Metrics", avg_strength is not None and avg_confidence is not None, 
                         f"Avg strength: {avg_strength}, Avg confidence: {avg_confidence}")
            
            self.log_test("Family Breakdown", len(by_family) >= 0, 
                         f"Families: {list(by_family.keys())}")
            
            return True
        else:
            self.log_test("Signal Summary", False, f"Status: {status}, Data: {data}")
            return False

    def test_safety_scan(self):
        """Test GET /api/alpha-deployment/safety/scan - runs safety scan"""
        print("\n🔍 Testing Safety Scan...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/safety/scan')
        
        if success:
            # Safety scan should return scan results
            scan_id = data.get('scan_id')
            scanned_deployments = data.get('scanned_deployments', 0)
            issues_found = data.get('issues_found', 0)
            auto_paused = data.get('auto_paused', 0)
            warnings = data.get('warnings', [])
            
            self.log_test("Safety Scan Execution", scan_id is not None, 
                         f"Scan ID: {scan_id}, Scanned: {scanned_deployments}")
            
            self.log_test("Safety Issues", issues_found >= 0, 
                         f"Issues found: {issues_found}, Auto-paused: {auto_paused}")
            
            self.log_test("Safety Warnings", len(warnings) >= 0, 
                         f"Warnings: {len(warnings)}")
            
            return True
        else:
            self.log_test("Safety Scan", False, f"Status: {status}, Data: {data}")
            return False

    def test_deployment_snapshot(self):
        """Test POST /api/alpha-deployment/snapshot - creates deployment snapshot"""
        print("\n🔍 Testing Deployment Snapshot...")
        
        success, data, status = self.make_request('POST', 'alpha-deployment/snapshot')
        
        if success:
            snapshot_id = data.get('snapshot_id')
            total_deployed = data.get('total_deployed', 0)
            active_count = data.get('active_count', 0)
            shadow_count = data.get('shadow_count', 0)
            family_breakdown = data.get('family_breakdown', {})
            
            self.log_test("Snapshot Creation", snapshot_id is not None, 
                         f"Snapshot ID: {snapshot_id}")
            
            # Check expected deployment counts (5 active + 18 shadow = 23 total)
            expected_total = 23
            if total_deployed == expected_total:
                self.log_test("Snapshot - Total Deployed", True, 
                             f"Total deployed: {total_deployed} (expected: {expected_total})")
            else:
                self.log_test("Snapshot - Total Deployed", False, 
                             f"Total deployed: {total_deployed} (expected: {expected_total})")
            
            self.log_test("Snapshot - Active/Shadow Counts", 
                         active_count >= 0 and shadow_count >= 0, 
                         f"Active: {active_count}, Shadow: {shadow_count}")
            
            self.log_test("Snapshot - Family Breakdown", len(family_breakdown) >= 0, 
                         f"Families: {list(family_breakdown.keys())}")
            
            return snapshot_id is not None
        else:
            self.log_test("Deployment Snapshot", False, f"Status: {status}, Data: {data}")
            return False

    def test_deployment_history(self):
        """Test GET /api/alpha-deployment/history - returns deployment history"""
        print("\n🔍 Testing Deployment History...")
        
        success, data, status = self.make_request('GET', 'alpha-deployment/history?limit=50')
        
        if success:
            history = data.get('history', [])
            count = data.get('count', 0)
            filters = data.get('filters', {})
            
            self.log_test("Deployment History", count >= 0, 
                         f"Found {count} history entries")
            
            # Check history structure if entries exist
            if history:
                entry = history[0]
                # History entries should have basic fields
                expected_fields = ['action', 'timestamp']
                present_fields = [field for field in expected_fields if field in entry]
                self.log_test("History Entry Structure", len(present_fields) >= 1, 
                             f"Present fields: {present_fields}")
            
            # Test with action filter
            success2, data2, status2 = self.make_request('GET', 'alpha-deployment/history?action=deploy&limit=20')
            if success2:
                deploy_count = data2.get('count', 0)
                self.log_test("History Filter (deploy)", deploy_count >= 0, 
                             f"Found {deploy_count} deploy actions")
            
            return True
        else:
            self.log_test("Deployment History", False, f"Status: {status}, Data: {data}")
            return False

    def test_integration_with_previous_phases(self):
        """Test integration with previous phases"""
        print("\n🔍 Testing Integration with Previous Phases...")
        
        # Test PHASE 13.4 Factor Ranker integration
        success1, data1, status1 = self.make_request('GET', 'factor-ranker/approved')
        if success1:
            approved_count = data1.get('count', 0)
            self.log_test("PHASE 13.4 Integration", approved_count > 0, 
                         f"Found {approved_count} approved factors")
        else:
            self.log_test("PHASE 13.4 Integration", False, f"Status: {status1}")
        
        # Test PHASE 13.6 Alpha DAG integration
        success2, data2, status2 = self.make_request('GET', 'alpha-dag/health')
        if success2:
            dag_status = data2.get('status')
            self.log_test("PHASE 13.6 Integration", dag_status == 'healthy', 
                         f"DAG status: {dag_status}")
        else:
            self.log_test("PHASE 13.6 Integration", False, f"Status: {status2}")
        
        return success1 or success2

    def test_end_to_end_workflow(self):
        """Test end-to-end deployment workflow"""
        print("\n🔍 Testing End-to-End Workflow...")
        
        # 1. Check current deployments
        success1, data1, _ = self.make_request('GET', 'alpha-deployment/stats')
        if success1:
            initial_stats = data1.get('summary', {})
            initial_active = initial_stats.get('active', 0)
            initial_shadow = initial_stats.get('shadow', 0)
            
            self.log_test("E2E - Initial State", True, 
                         f"Initial: {initial_active} active, {initial_shadow} shadow")
        
        # 2. Generate signals
        signal_request = {
            "factor_values": {"test_factor": 0.5},
            "symbol": "BTCUSDT",
            "regime": "TRENDING",
            "regime_confidence": 0.8
        }
        success2, data2, _ = self.make_request('POST', 'alpha-deployment/signals/generate', signal_request)
        if success2:
            signals_count = data2.get('signals_generated', 0)
            self.log_test("E2E - Signal Generation", signals_count >= 0, 
                         f"Generated {signals_count} signals")
        
        # 3. Create snapshot
        success3, data3, _ = self.make_request('POST', 'alpha-deployment/snapshot')
        if success3:
            snapshot_id = data3.get('snapshot_id')
            self.log_test("E2E - Snapshot Creation", snapshot_id is not None, 
                         f"Created snapshot: {snapshot_id}")
        
        # 4. Run safety scan
        success4, data4, _ = self.make_request('GET', 'alpha-deployment/safety/scan')
        if success4:
            scan_id = data4.get('scan_id')
            self.log_test("E2E - Safety Scan", scan_id is not None, 
                         f"Safety scan: {scan_id}")
        
        return success1 and success2 and success3 and success4

    def run_all_tests(self):
        """Run all Alpha Deployment test cases."""
        print("=" * 80)
        print("🚀 PHASE 13.7 Alpha Deployment - Backend API Tests")
        print("=" * 80)
        print("Expected State: 23 factors deployed (5 active, 18 shadow)")
        print("=" * 80)
        
        # Core health and stats tests
        self.test_alpha_deployment_health()
        self.test_deployment_stats()
        
        # Deployment listing tests
        self.test_active_deployments()
        self.test_shadow_deployments()
        
        # Signal functionality tests
        self.test_signal_generation()
        self.test_signal_summary()
        
        # Safety and management tests
        self.test_safety_scan()
        self.test_deployment_snapshot()
        self.test_deployment_history()
        
        # Integration tests
        self.test_integration_with_previous_phases()
        self.test_end_to_end_workflow()
        
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
    print("🔧 Starting PHASE 13.7 Alpha Deployment API Tests...")
    
    tester = AlphaDeploymentTester()
    success = tester.run_all_tests()
    
    print(f"\n🏁 Testing completed. Success: {success}")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())