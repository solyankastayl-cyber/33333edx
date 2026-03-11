#!/usr/bin/env python3
"""
PHASE 13.1 Alpha Node Registry Backend API Tests
===============================================
Comprehensive testing of all Alpha Factory endpoints.

Tests:
- Health endpoints (system, db, alpha factory)
- Node CRUD operations
- Search functionality
- Statistics and registry endpoints
- Node types and filtering
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

class AlphaNodeRegistryTester:
    def __init__(self, base_url: str = "https://pattern-detector-10.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.test_results = {}
        
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}")
        else:
            self.failed_tests.append({"test": test_name, "details": details})
            print(f"❌ {test_name} - {details}")
        
        self.test_results[test_name] = {
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            else:
                return False, {}, 0
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            return response.status_code < 400, response_data, response.status_code
            
        except Exception as e:
            return False, {"error": str(e)}, 0
    
    def test_health_endpoints(self):
        """Test all health check endpoints"""
        print("\n🔍 Testing Health Endpoints...")
        
        # 1. Main API health
        success, data, status = self.make_request('GET', '/api/health')
        if success and data.get('ok') is True:
            self.log_result("API Health Check", True)
        else:
            self.log_result("API Health Check", False, f"Status: {status}, Data: {data}")
        
        # 2. Database health
        success, data, status = self.make_request('GET', '/api/system/db-health')
        if success and data.get('connected') is True:
            self.log_result("MongoDB Health Check", True)
        else:
            self.log_result("MongoDB Health Check", False, f"Status: {status}, Connected: {data.get('connected')}")
        
        # 3. Alpha Factory health
        success, data, status = self.make_request('GET', '/api/alpha-factory/health')
        if success and data.get('status') == 'healthy':
            self.log_result("Alpha Factory Health Check", True)
        else:
            self.log_result("Alpha Factory Health Check", False, f"Status: {status}, Data: {data}")
    
    def test_statistics_endpoints(self):
        """Test statistics and registry endpoints"""
        print("\n📊 Testing Statistics Endpoints...")
        
        # 1. Alpha Factory stats - should show >= 50 nodes
        success, data, status = self.make_request('GET', '/api/alpha-factory/stats')
        if success:
            registry_stats = data.get('registry', {})
            total_nodes = registry_stats.get('total_nodes', 0)
            if total_nodes >= 50:
                self.log_result("Alpha Factory Stats (>=50 nodes)", True, f"Found {total_nodes} nodes")
            else:
                self.log_result("Alpha Factory Stats (>=50 nodes)", False, f"Only {total_nodes} nodes found")
        else:
            self.log_result("Alpha Factory Stats", False, f"Status: {status}, Data: {data}")
        
        # 2. TA Registry stats
        success, data, status = self.make_request('GET', '/api/ta/registry')
        if success and data.get('status') == 'ok':
            self.log_result("TA Registry Stats", True)
        else:
            self.log_result("TA Registry Stats", False, f"Status: {status}, Data: {data}")
        
        # 3. TA Patterns
        success, data, status = self.make_request('GET', '/api/ta/patterns')
        if success and data.get('status') == 'ok':
            alpha_count = len(data.get('alpha_patterns', []))
            structure_count = len(data.get('structure_patterns', []))
            self.log_result("TA Patterns", True, f"Alpha: {alpha_count}, Structure: {structure_count}")
        else:
            self.log_result("TA Patterns", False, f"Status: {status}, Data: {data}")
    
    def test_node_types(self):
        """Test node types endpoint - should return 9 types"""
        print("\n🏷️ Testing Node Types...")
        
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/types')
        if success:
            types = data.get('types', [])
            counts = data.get('counts', {})
            total = data.get('total', 0)
            
            if len(types) == 9:
                self.log_result("Node Types Count (9 types)", True, f"Types: {types}")
            else:
                self.log_result("Node Types Count (9 types)", False, f"Found {len(types)} types: {types}")
            
            # Check expected types
            expected_types = ['alpha', 'structure', 'liquidity', 'microstructure', 'context', 'correlation', 'portfolio', 'feature', 'factor']
            missing_types = [t for t in expected_types if t not in types]
            if not missing_types:
                self.log_result("All Expected Node Types Present", True)
            else:
                self.log_result("All Expected Node Types Present", False, f"Missing: {missing_types}")
        else:
            self.log_result("Node Types Endpoint", False, f"Status: {status}, Data: {data}")
    
    def test_node_listing(self):
        """Test node listing with various filters"""
        print("\n📋 Testing Node Listing...")
        
        # 1. List all nodes
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes')
        if success:
            count = data.get('count', 0)
            nodes = data.get('nodes', [])
            self.log_result("List All Nodes", True, f"Found {count} nodes")
            
            # Store first few node IDs for later tests
            self.sample_node_ids = [node.get('node_id') for node in nodes[:3]]
        else:
            self.log_result("List All Nodes", False, f"Status: {status}, Data: {data}")
            self.sample_node_ids = []
        
        # 2. Filter by node type (alpha)
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes', params={'node_type': 'alpha'})
        if success:
            count = data.get('count', 0)
            self.log_result("Filter by Alpha Type", True, f"Found {count} alpha nodes")
        else:
            self.log_result("Filter by Alpha Type", False, f"Status: {status}")
        
        # 3. Filter by tag
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes', params={'tag': 'trend'})
        if success:
            count = data.get('count', 0)
            self.log_result("Filter by Tag (trend)", True, f"Found {count} trend nodes")
        else:
            self.log_result("Filter by Tag (trend)", False, f"Status: {status}")
    
    def test_specific_node_retrieval(self):
        """Test retrieving specific nodes"""
        print("\n🎯 Testing Specific Node Retrieval...")
        
        # Test trend_strength node specifically mentioned in requirements
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/trend_strength')
        if success:
            node = data.get('node', {})
            node_id = node.get('node_id')
            if node_id == 'trend_strength':
                self.log_result("Get trend_strength Node", True, f"Node type: {node.get('node_type')}")
            else:
                self.log_result("Get trend_strength Node", False, f"Wrong node returned: {node_id}")
        else:
            self.log_result("Get trend_strength Node", False, f"Status: {status}, Data: {data}")
        
        # Test other sample nodes if available
        for node_id in self.sample_node_ids[:2]:
            success, data, status = self.make_request('GET', f'/api/alpha-factory/nodes/{node_id}')
            if success:
                self.log_result(f"Get Node {node_id}", True)
            else:
                self.log_result(f"Get Node {node_id}", False, f"Status: {status}")
    
    def test_node_search(self):
        """Test node search functionality"""
        print("\n🔍 Testing Node Search...")
        
        # Search for volatility nodes as specified in requirements
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/search', params={'q': 'volatility'})
        if success:
            count = data.get('count', 0)
            query = data.get('query', '')
            if count > 0:
                self.log_result("Search Volatility Nodes", True, f"Found {count} nodes for '{query}'")
            else:
                self.log_result("Search Volatility Nodes", False, f"No nodes found for '{query}'")
        else:
            self.log_result("Search Volatility Nodes", False, f"Status: {status}, Data: {data}")
        
        # Search for trend nodes
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/search', params={'q': 'trend'})
        if success:
            count = data.get('count', 0)
            self.log_result("Search Trend Nodes", True, f"Found {count} trend nodes")
        else:
            self.log_result("Search Trend Nodes", False, f"Status: {status}")
    
    def test_node_creation(self):
        """Test creating a new node"""
        print("\n➕ Testing Node Creation...")
        
        # Create a test node
        test_node = {
            "node_id": f"test_node_{int(datetime.now().timestamp())}",
            "node_type": "alpha",
            "source_module": "test_module",
            "inputs": ["price", "volume"],
            "outputs": ["test_signal"],
            "description": "Test node for API testing",
            "tags": ["test", "api"],
            "category": "test",
            "confidence_range": [0.0, 1.0]
        }
        
        success, data, status = self.make_request('POST', '/api/alpha-factory/nodes', data=test_node)
        if success and data.get('created') is True:
            created_node_id = data.get('node_id')
            self.log_result("Create New Node", True, f"Created: {created_node_id}")
            
            # Verify the created node can be retrieved
            success, data, status = self.make_request('GET', f'/api/alpha-factory/nodes/{created_node_id}')
            if success:
                self.log_result("Retrieve Created Node", True)
            else:
                self.log_result("Retrieve Created Node", False, f"Status: {status}")
        else:
            self.log_result("Create New Node", False, f"Status: {status}, Data: {data}")
    
    def test_additional_endpoints(self):
        """Test additional endpoints for completeness"""
        print("\n🔧 Testing Additional Endpoints...")
        
        # Test node categories
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/categories')
        if success:
            categories = data.get('categories', {})
            count = data.get('count', 0)
            self.log_result("Node Categories", True, f"Found {count} categories")
        else:
            self.log_result("Node Categories", False, f"Status: {status}")
        
        # Test node tags
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/tags')
        if success:
            tags = data.get('tags', [])
            count = data.get('count', 0)
            self.log_result("Node Tags", True, f"Found {count} unique tags")
        else:
            self.log_result("Node Tags", False, f"Status: {status}")
        
        # Test nodes by type endpoint
        success, data, status = self.make_request('GET', '/api/alpha-factory/nodes/by-type/feature')
        if success:
            count = data.get('count', 0)
            self.log_result("Nodes by Type (feature)", True, f"Found {count} feature nodes")
        else:
            self.log_result("Nodes by Type (feature)", False, f"Status: {status}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Alpha Node Registry API Tests")
        print(f"📡 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run test suites
        self.test_health_endpoints()
        self.test_statistics_endpoints()
        self.test_node_types()
        self.test_node_listing()
        self.test_specific_node_retrieval()
        self.test_node_search()
        self.test_node_creation()
        self.test_additional_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Failed: {len(self.failed_tests)}/{self.tests_run}")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for failure in self.failed_tests:
                print(f"  - {failure['test']}: {failure['details']}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": len(self.failed_tests),
            "success_rate": success_rate,
            "failures": self.failed_tests,
            "detailed_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = AlphaNodeRegistryTester()
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if results["failed_tests"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())