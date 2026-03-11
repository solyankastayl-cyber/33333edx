#!/usr/bin/env python3
"""
PHASE 13.2 Alpha Feature Library - Backend API Tests
====================================================
Comprehensive testing for Alpha Feature Library endpoints.

Test Coverage:
- Health check
- Stats (total_features >= 300)
- Categories (8 categories)
- Transforms (16 transforms)
- Feature listing with pagination
- Individual feature retrieval
- Features by category
- Feature search
- Tags listing
- Feature creation (POST)
- Transform application (POST)
- Feature update (PUT)
- Feature dependencies
- Alpha factory stats (PHASE 13.1 compatibility)
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class AlphaFeatureLibraryTester:
    def __init__(self, base_url: str = "https://pattern-detector-10.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AlphaFeatureLibrary-Tester/1.0'
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

    def test_health_check(self):
        """Test GET /api/alpha-features/health"""
        print("\n🔍 Testing Alpha Features Health Check...")
        
        success, data, status = self.make_request('GET', 'alpha-features/health')
        
        if success and data.get('status') == 'healthy':
            self.log_test("Alpha Features Health Check", True, f"Status: {data.get('status')}")
            return True
        else:
            self.log_test("Alpha Features Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_stats_endpoint(self):
        """Test GET /api/alpha-features/stats - should show >= 300 features"""
        print("\n🔍 Testing Alpha Features Stats...")
        
        success, data, status = self.make_request('GET', 'alpha-features/stats')
        
        if success:
            registry_stats = data.get('registry', {})
            total_features = registry_stats.get('total_features', 0)
            
            if total_features >= 300:
                self.log_test("Stats - Total Features >= 300", True, f"Found {total_features} features")
            else:
                self.log_test("Stats - Total Features >= 300", False, f"Only {total_features} features found")
            
            # Check category breakdown
            categories = registry_stats.get('features_by_category', {})
            self.log_test("Stats - Category Breakdown", len(categories) > 0, f"Categories: {list(categories.keys())}")
            
            return total_features >= 300
        else:
            self.log_test("Stats Endpoint", False, f"Status: {status}, Data: {data}")
            return False

    def test_categories_endpoint(self):
        """Test GET /api/alpha-features/categories - should return 8 categories"""
        print("\n🔍 Testing Categories Endpoint...")
        
        success, data, status = self.make_request('GET', 'alpha-features/categories')
        
        if success:
            categories = data.get('categories', [])
            expected_categories = ['price', 'volatility', 'volume', 'liquidity', 'structure', 'microstructure', 'correlation', 'context']
            
            if len(categories) == 8:
                self.log_test("Categories Count = 8", True, f"Categories: {categories}")
            else:
                self.log_test("Categories Count = 8", False, f"Found {len(categories)} categories: {categories}")
            
            # Check if all expected categories are present
            missing = [cat for cat in expected_categories if cat not in categories]
            if not missing:
                self.log_test("All Expected Categories Present", True)
            else:
                self.log_test("All Expected Categories Present", False, f"Missing: {missing}")
            
            return len(categories) == 8 and not missing
        else:
            self.log_test("Categories Endpoint", False, f"Status: {status}, Data: {data}")
            return False

    def test_transforms_endpoint(self):
        """Test GET /api/alpha-features/transforms - should return 16 transforms"""
        print("\n🔍 Testing Transforms Endpoint...")
        
        success, data, status = self.make_request('GET', 'alpha-features/transforms')
        
        if success:
            transforms = data.get('transforms', [])
            count = data.get('count', 0)
            
            if count == 16:
                self.log_test("Transforms Count = 16", True, f"Transforms: {transforms}")
            else:
                self.log_test("Transforms Count = 16", False, f"Found {count} transforms: {transforms}")
            
            # Check for key transforms
            expected_transforms = ['raw', 'zscore', 'rolling_mean', 'rolling_std', 'percentile_rank', 'ema', 'sma']
            present = [t for t in expected_transforms if t in transforms]
            self.log_test("Key Transforms Present", len(present) >= 5, f"Present: {present}")
            
            return count == 16
        else:
            self.log_test("Transforms Endpoint", False, f"Status: {status}, Data: {data}")
            return False

    def test_features_listing(self):
        """Test GET /api/alpha-features - list features with pagination"""
        print("\n🔍 Testing Features Listing...")
        
        # Test basic listing
        success, data, status = self.make_request('GET', 'alpha-features?limit=50')
        
        if success:
            features = data.get('features', [])
            count = data.get('count', 0)
            
            self.log_test("Features Listing", count > 0, f"Retrieved {count} features")
            
            # Test with category filter
            success2, data2, status2 = self.make_request('GET', 'alpha-features?category=price&limit=20')
            if success2:
                price_features = data2.get('features', [])
                self.log_test("Price Category Filter", len(price_features) > 0, f"Found {len(price_features)} price features")
            
            # Test with status filter
            success3, data3, status3 = self.make_request('GET', 'alpha-features?status=active&limit=30')
            if success3:
                active_features = data3.get('features', [])
                self.log_test("Active Status Filter", len(active_features) > 0, f"Found {len(active_features)} active features")
            
            return count > 0
        else:
            self.log_test("Features Listing", False, f"Status: {status}, Data: {data}")
            return False

    def test_individual_feature_retrieval(self):
        """Test GET /api/alpha-features/{feature_id} - get volatility_compression feature"""
        print("\n🔍 Testing Individual Feature Retrieval...")
        
        # First, get a list of features to find a valid ID
        success, data, status = self.make_request('GET', 'alpha-features?category=volatility&limit=10')
        
        if success:
            features = data.get('features', [])
            
            # Look for volatility_compression or use first volatility feature
            target_feature = None
            for feature in features:
                if 'volatility_compression' in feature.get('feature_id', ''):
                    target_feature = feature
                    break
            
            if not target_feature and features:
                target_feature = features[0]
            
            if target_feature:
                feature_id = target_feature['feature_id']
                success2, data2, status2 = self.make_request('GET', f'alpha-features/{feature_id}')
                
                if success2:
                    feature_data = data2.get('feature', {})
                    dependencies = data2.get('dependencies', {})
                    
                    self.log_test("Individual Feature Retrieval", True, f"Retrieved feature: {feature_id}")
                    self.log_test("Feature Dependencies", 'dependencies' in data2, f"Dependencies: {dependencies}")
                    return True
                else:
                    self.log_test("Individual Feature Retrieval", False, f"Status: {status2}, Data: {data2}")
            else:
                self.log_test("Individual Feature Retrieval", False, "No volatility features found")
        else:
            self.log_test("Individual Feature Retrieval", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_features_by_category(self):
        """Test GET /api/alpha-features/by-category/price"""
        print("\n🔍 Testing Features by Category...")
        
        success, data, status = self.make_request('GET', 'alpha-features/by-category/price')
        
        if success:
            features = data.get('features', [])
            count = data.get('count', 0)
            category = data.get('category', '')
            
            self.log_test("Features by Category (price)", count > 0, f"Found {count} price features")
            
            # Test another category
            success2, data2, status2 = self.make_request('GET', 'alpha-features/by-category/volatility')
            if success2:
                vol_count = data2.get('count', 0)
                self.log_test("Features by Category (volatility)", vol_count > 0, f"Found {vol_count} volatility features")
            
            return count > 0
        else:
            self.log_test("Features by Category", False, f"Status: {status}, Data: {data}")
            return False

    def test_feature_search(self):
        """Test GET /api/alpha-features/search?q=momentum"""
        print("\n🔍 Testing Feature Search...")
        
        success, data, status = self.make_request('GET', 'alpha-features/search?q=momentum')
        
        if success:
            features = data.get('features', [])
            count = data.get('count', 0)
            query = data.get('query', '')
            
            self.log_test("Feature Search (momentum)", count > 0, f"Found {count} features matching 'momentum'")
            
            # Test another search
            success2, data2, status2 = self.make_request('GET', 'alpha-features/search?q=price')
            if success2:
                price_count = data2.get('count', 0)
                self.log_test("Feature Search (price)", price_count > 0, f"Found {price_count} features matching 'price'")
            
            return count > 0
        else:
            self.log_test("Feature Search", False, f"Status: {status}, Data: {data}")
            return False

    def test_tags_endpoint(self):
        """Test GET /api/alpha-features/tags"""
        print("\n🔍 Testing Tags Endpoint...")
        
        success, data, status = self.make_request('GET', 'alpha-features/tags')
        
        if success:
            tags = data.get('tags', [])
            count = data.get('count', 0)
            
            self.log_test("Tags Listing", count > 0, f"Found {count} unique tags")
            
            # Check for expected tags
            expected_tags = ['price', 'momentum', 'volatility', 'volume']
            present_tags = [tag for tag in expected_tags if tag in tags]
            self.log_test("Expected Tags Present", len(present_tags) > 0, f"Present: {present_tags}")
            
            return count > 0
        else:
            self.log_test("Tags Endpoint", False, f"Status: {status}, Data: {data}")
            return False

    def test_feature_creation(self):
        """Test POST /api/alpha-features - create new feature"""
        print("\n🔍 Testing Feature Creation...")
        
        test_feature = {
            "feature_id": f"test_feature_{int(datetime.now().timestamp())}",
            "category": "price",
            "inputs": ["close"],
            "transform": "raw",
            "params": {},
            "output_type": "numeric",
            "description": "Test feature for API testing",
            "tags": ["test", "api"],
            "depends_on": [],
            "regime_dependency": []
        }
        
        success, data, status = self.make_request('POST', 'alpha-features', test_feature, 201)
        
        if success:
            created = data.get('created', False)
            feature_id = data.get('feature_id', '')
            
            self.log_test("Feature Creation", created, f"Created feature: {feature_id}")
            
            # Verify the feature was created by retrieving it
            if created and feature_id:
                success2, data2, status2 = self.make_request('GET', f'alpha-features/{feature_id}')
                self.log_test("Created Feature Retrieval", success2, f"Retrieved created feature: {feature_id}")
            
            return created
        else:
            self.log_test("Feature Creation", False, f"Status: {status}, Data: {data}")
            return False

    def test_transform_application(self):
        """Test POST /api/alpha-features/transform - apply zscore transform"""
        print("\n🔍 Testing Transform Application...")
        
        transform_request = {
            "transform": "zscore",
            "values": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            "params": {"window": 5}
        }
        
        success, data, status = self.make_request('POST', 'alpha-features/transform', transform_request)
        
        if success:
            transform_name = data.get('transform', '')
            result = data.get('result', [])
            input_count = data.get('input_count', 0)
            output_count = data.get('output_count', 0)
            
            self.log_test("Transform Application (zscore)", len(result) > 0, f"Applied {transform_name} to {input_count} values, got {output_count} results")
            
            # Test another transform
            percentile_request = {
                "transform": "percentile_rank",
                "values": [10, 20, 30, 40, 50],
                "params": {"window": 5}
            }
            
            success2, data2, status2 = self.make_request('POST', 'alpha-features/transform', percentile_request)
            if success2:
                result2 = data2.get('result', [])
                self.log_test("Transform Application (percentile_rank)", len(result2) > 0, f"Applied percentile_rank transform")
            
            return len(result) > 0
        else:
            self.log_test("Transform Application", False, f"Status: {status}, Data: {data}")
            return False

    def test_feature_update(self):
        """Test PUT /api/alpha-features/{feature_id} - update feature"""
        print("\n🔍 Testing Feature Update...")
        
        # First create a feature to update
        test_feature = {
            "feature_id": f"update_test_{int(datetime.now().timestamp())}",
            "category": "price",
            "description": "Original description",
            "tags": ["original"]
        }
        
        success, data, status = self.make_request('POST', 'alpha-features', test_feature, 201)
        
        if success:
            feature_id = data.get('feature_id', '')
            
            # Now update the feature
            update_data = {
                "description": "Updated description",
                "tags": ["updated", "test"],
                "params": {"new_param": "value"}
            }
            
            success2, data2, status2 = self.make_request('PUT', f'alpha-features/{feature_id}', update_data)
            
            if success2:
                updated = data2.get('updated', False)
                self.log_test("Feature Update", updated, f"Updated feature: {feature_id}")
                return updated
            else:
                self.log_test("Feature Update", False, f"Status: {status2}, Data: {data2}")
        else:
            self.log_test("Feature Update", False, "Could not create feature for update test")
        
        return False

    def test_feature_dependencies(self):
        """Test GET /api/alpha-features/{feature_id}/dependencies"""
        print("\n🔍 Testing Feature Dependencies...")
        
        # Get a feature with dependencies
        success, data, status = self.make_request('GET', 'alpha-features?limit=10')
        
        if success:
            features = data.get('features', [])
            
            if features:
                feature_id = features[0]['feature_id']
                success2, data2, status2 = self.make_request('GET', f'alpha-features/{feature_id}/dependencies')
                
                if success2:
                    dependencies = data2.get('dependencies', {})
                    self.log_test("Feature Dependencies", True, f"Retrieved dependencies for {feature_id}: {dependencies}")
                    return True
                else:
                    self.log_test("Feature Dependencies", False, f"Status: {status2}, Data: {data2}")
            else:
                self.log_test("Feature Dependencies", False, "No features available for dependency test")
        else:
            self.log_test("Feature Dependencies", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_alpha_factory_stats(self):
        """Test GET /api/alpha-factory/stats - PHASE 13.1 compatibility"""
        print("\n🔍 Testing Alpha Factory Stats (PHASE 13.1)...")
        
        success, data, status = self.make_request('GET', 'alpha-factory/stats')
        
        if success:
            # Check if we have node registry stats
            total_nodes = data.get('total_nodes', 0)
            self.log_test("Alpha Factory Stats", total_nodes > 0, f"Found {total_nodes} nodes in registry")
            return total_nodes > 0
        else:
            self.log_test("Alpha Factory Stats", False, f"Status: {status}, Data: {data}")
            return False

    def run_all_tests(self):
        """Run all test cases."""
        print("=" * 80)
        print("🚀 PHASE 13.2 Alpha Feature Library - Backend API Tests")
        print("=" * 80)
        
        # Core health and stats tests
        self.test_health_check()
        self.test_stats_endpoint()
        self.test_categories_endpoint()
        self.test_transforms_endpoint()
        
        # Feature operations tests
        self.test_features_listing()
        self.test_individual_feature_retrieval()
        self.test_features_by_category()
        self.test_feature_search()
        self.test_tags_endpoint()
        
        # CRUD operations tests
        self.test_feature_creation()
        self.test_transform_application()
        self.test_feature_update()
        self.test_feature_dependencies()
        
        # Compatibility test
        self.test_alpha_factory_stats()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
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
    """Main test execution."""
    tester = AlphaFeatureLibraryTester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n💥 Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())