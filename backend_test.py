#!/usr/bin/env python3
"""
PHASE 13.3 Factor Generator - Backend API Tests
===============================================
Comprehensive testing for Factor Generator endpoints.

Test Coverage:
- PHASE 13.3 Factor Generator (NEW):
  * Health check
  * Stats (total_factors >= 1000)
  * Families (12 families)
  * Templates (8 templates)
  * Factor generation (POST /run)
  * Factor listing with filters
  * Factor search
  * Individual factor retrieval
  * Generation runs history
- PHASE 13.2 Alpha Feature Library:
  * Health check
  * Stats (total_features >= 300)
  * Categories (8 categories)
  * Transforms (16 transforms)
  * Feature listing with pagination
  * Individual feature retrieval
  * Features by category
  * Feature search
  * Tags listing
  * Feature creation (POST)
  * Transform application (POST)
  * Feature update (PUT)
  * Feature dependencies
- PHASE 13.1 Alpha Factory compatibility
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

class FactorGeneratorTester:
    """PHASE 13.3 Factor Generator API Tests"""
    
    def __init__(self, base_url: str = "https://pattern-detector-10.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'FactorGenerator-Tester/1.0'
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

    def test_factor_generator_health(self):
        """Test GET /api/factor-generator/health - status=healthy"""
        print("\n🔍 Testing Factor Generator Health Check...")
        
        success, data, status = self.make_request('GET', 'factor-generator/health')
        
        if success and data.get('status') == 'healthy':
            self.log_test("Factor Generator Health Check", True, f"Status: {data.get('status')}")
            return True
        else:
            self.log_test("Factor Generator Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_generator_stats(self):
        """Test GET /api/factor-generator/stats - total_factors >= 1000"""
        print("\n🔍 Testing Factor Generator Stats...")
        
        success, data, status = self.make_request('GET', 'factor-generator/stats')
        
        if success:
            generator_stats = data.get('generator', {})
            repository_stats = data.get('repository', {})
            
            total_factors = repository_stats.get('total_factors', 0)
            
            if total_factors >= 1000:
                self.log_test("Stats - Total Factors >= 1000", True, f"Found {total_factors} factors")
            else:
                self.log_test("Stats - Total Factors >= 1000", False, f"Only {total_factors} factors found")
            
            # Check family breakdown
            family_counts = repository_stats.get('family_counts', {})
            self.log_test("Stats - Family Breakdown", len(family_counts) > 0, f"Families: {list(family_counts.keys())}")
            
            # Check template breakdown
            template_counts = repository_stats.get('template_counts', {})
            self.log_test("Stats - Template Breakdown", len(template_counts) > 0, f"Templates: {list(template_counts.keys())}")
            
            return total_factors >= 1000
        else:
            self.log_test("Factor Generator Stats", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_families(self):
        """Test GET /api/factor-generator/families - 12 families available"""
        print("\n🔍 Testing Factor Families...")
        
        success, data, status = self.make_request('GET', 'factor-generator/families')
        
        if success:
            families = data.get('families', [])
            counts = data.get('counts', {})
            total = data.get('total', 0)
            
            if len(families) >= 12:
                self.log_test("Families Count >= 12", True, f"Found {len(families)} families: {families}")
            else:
                self.log_test("Families Count >= 12", False, f"Only {len(families)} families found: {families}")
            
            # Check for expected families
            expected_families = ['momentum', 'breakout', 'trend', 'volatility', 'regime']
            present_families = [f for f in expected_families if f in families]
            self.log_test("Expected Families Present", len(present_families) > 0, f"Present: {present_families}")
            
            # Check family counts
            self.log_test("Family Counts Available", len(counts) > 0, f"Family counts: {counts}")
            
            return len(families) >= 12
        else:
            self.log_test("Factor Families", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_templates(self):
        """Test GET /api/factor-generator/templates - 8 templates available"""
        print("\n🔍 Testing Factor Templates...")
        
        success, data, status = self.make_request('GET', 'factor-generator/templates')
        
        if success:
            templates = data.get('templates', [])
            counts = data.get('counts', {})
            
            if len(templates) >= 8:
                self.log_test("Templates Count >= 8", True, f"Found {len(templates)} templates: {templates}")
            else:
                self.log_test("Templates Count >= 8", False, f"Only {len(templates)} templates found: {templates}")
            
            # Check for expected templates
            expected_templates = ['single_feature', 'pair_feature', 'triple_feature', 'ratio_feature', 'difference_feature', 'interaction_feature', 'regime_conditioned']
            present_templates = [t for t in expected_templates if t in templates]
            self.log_test("Expected Templates Present", len(present_templates) >= 6, f"Present: {present_templates}")
            
            return len(templates) >= 8
        else:
            self.log_test("Factor Templates", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_generation(self):
        """Test POST /api/factor-generator/run - генерация факторов работает"""
        print("\n🔍 Testing Factor Generation...")
        
        # Test with default configuration
        generation_config = {
            "max_total": 100,  # Smaller batch for testing
            "max_single": 10,
            "max_pair": 20,
            "max_triple": 15,
            "max_ratio": 15,
            "max_diff": 10,
            "max_interaction": 15,
            "max_regime": 15,
            "clear_existing": False
        }
        
        success, data, status = self.make_request('POST', 'factor-generator/run', generation_config)
        
        if success:
            run_status = data.get('status', '')
            run_data = data.get('run', {})
            features_used = data.get('features_used', 0)
            
            if run_status == 'completed':
                generated_count = run_data.get('generated_count', 0)
                accepted_count = run_data.get('accepted_count', 0)
                
                self.log_test("Factor Generation", True, f"Generated {generated_count} factors, accepted {accepted_count}, used {features_used} features")
                
                # Check family and template counts
                family_counts = run_data.get('family_counts', {})
                template_counts = run_data.get('template_counts', {})
                
                self.log_test("Generation Family Distribution", len(family_counts) > 0, f"Families: {family_counts}")
                self.log_test("Generation Template Distribution", len(template_counts) > 0, f"Templates: {template_counts}")
                
                return True
            else:
                self.log_test("Factor Generation", False, f"Generation failed with status: {run_status}")
        else:
            self.log_test("Factor Generation", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_factor_listing(self):
        """Test GET /api/factor-generator/factors - список факторов с фильтрами"""
        print("\n🔍 Testing Factor Listing...")
        
        # Test basic listing
        success, data, status = self.make_request('GET', 'factor-generator/factors?limit=50')
        
        if success:
            factors = data.get('factors', [])
            count = data.get('count', 0)
            
            self.log_test("Factor Listing", count > 0, f"Retrieved {count} factors")
            
            # Test with family filter
            success2, data2, status2 = self.make_request('GET', 'factor-generator/factors?family=momentum&limit=20')
            if success2:
                momentum_factors = data2.get('factors', [])
                self.log_test("Momentum Family Filter", len(momentum_factors) >= 0, f"Found {len(momentum_factors)} momentum factors")
            
            # Test with template filter
            success3, data3, status3 = self.make_request('GET', 'factor-generator/factors?template=pair_feature&limit=20')
            if success3:
                pair_factors = data3.get('factors', [])
                self.log_test("Pair Template Filter", len(pair_factors) >= 0, f"Found {len(pair_factors)} pair factors")
            
            return count > 0
        else:
            self.log_test("Factor Listing", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_search(self):
        """Test GET /api/factor-generator/factors/search?q=breakout - поиск факторов"""
        print("\n🔍 Testing Factor Search...")
        
        success, data, status = self.make_request('GET', 'factor-generator/factors/search?q=breakout')
        
        if success:
            factors = data.get('factors', [])
            count = data.get('count', 0)
            query = data.get('query', '')
            
            self.log_test("Factor Search (breakout)", count >= 0, f"Found {count} factors matching 'breakout'")
            
            # Test another search
            success2, data2, status2 = self.make_request('GET', 'factor-generator/factors/search?q=momentum')
            if success2:
                momentum_count = data2.get('count', 0)
                self.log_test("Factor Search (momentum)", momentum_count >= 0, f"Found {momentum_count} factors matching 'momentum'")
            
            return True  # Search can return 0 results and still be successful
        else:
            self.log_test("Factor Search", False, f"Status: {status}, Data: {data}")
            return False

    def test_individual_factor_retrieval(self):
        """Test GET /api/factor-generator/{factor_id} - получение конкретного фактора"""
        print("\n🔍 Testing Individual Factor Retrieval...")
        
        # First, get a list of factors to find a valid ID
        success, data, status = self.make_request('GET', 'factor-generator/factors?limit=10')
        
        if success:
            factors = data.get('factors', [])
            
            if factors:
                factor_id = factors[0]['factor_id']
                success2, data2, status2 = self.make_request('GET', f'factor-generator/{factor_id}')
                
                if success2:
                    factor_data = data2.get('factor', {})
                    
                    self.log_test("Individual Factor Retrieval", True, f"Retrieved factor: {factor_id}")
                    
                    # Check factor structure
                    required_fields = ['factor_id', 'name', 'family', 'template', 'inputs']
                    present_fields = [field for field in required_fields if field in factor_data]
                    self.log_test("Factor Structure", len(present_fields) >= 4, f"Present fields: {present_fields}")
                    
                    return True
                else:
                    self.log_test("Individual Factor Retrieval", False, f"Status: {status2}, Data: {data2}")
            else:
                self.log_test("Individual Factor Retrieval", False, "No factors found for retrieval test")
        else:
            self.log_test("Individual Factor Retrieval", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_generation_runs(self):
        """Test GET /api/factor-generator/runs - история генераций"""
        print("\n🔍 Testing Generation Runs History...")
        
        success, data, status = self.make_request('GET', 'factor-generator/runs?limit=10')
        
        if success:
            runs = data.get('runs', [])
            count = data.get('count', 0)
            
            self.log_test("Generation Runs History", count >= 0, f"Found {count} generation runs")
            
            # Check run structure if runs exist
            if runs:
                run = runs[0]
                required_fields = ['run_id', 'status', 'generated_count', 'accepted_count']
                present_fields = [field for field in required_fields if field in run]
                self.log_test("Run Structure", len(present_fields) >= 3, f"Present fields: {present_fields}")
            
            return True
        else:
            self.log_test("Generation Runs History", False, f"Status: {status}, Data: {data}")
            return False

    def test_phase_integration(self):
        """Test integration with previous phases"""
        print("\n🔍 Testing Phase Integration...")
        
        # Test PHASE 13.1 Node Registry
        success1, data1, status1 = self.make_request('GET', 'alpha-factory/stats')
        if success1:
            total_nodes = data1.get('total_nodes', 0)
            self.log_test("PHASE 13.1 Node Registry", total_nodes > 0, f"Found {total_nodes} nodes")
        else:
            self.log_test("PHASE 13.1 Node Registry", False, f"Status: {status1}")
        
        # Test PHASE 13.2 Feature Library
        success2, data2, status2 = self.make_request('GET', 'alpha-features/stats')
        if success2:
            registry_stats = data2.get('registry', {})
            total_features = registry_stats.get('total_features', 0)
            self.log_test("PHASE 13.2 Feature Library", total_features > 0, f"Found {total_features} features")
        else:
            self.log_test("PHASE 13.2 Feature Library", False, f"Status: {status2}")
        
        return success1 and success2

    def run_all_tests(self):
        """Run all Factor Generator test cases."""
        print("=" * 80)
        print("🚀 PHASE 13.3 Factor Generator - Backend API Tests")
        print("=" * 80)
        
        # Core health and stats tests
        self.test_factor_generator_health()
        self.test_factor_generator_stats()
        self.test_factor_families()
        self.test_factor_templates()
        
        # Generation tests
        self.test_factor_generation()
        
        # Factor operations tests
        self.test_factor_listing()
        self.test_factor_search()
        self.test_individual_factor_retrieval()
        self.test_generation_runs()
        
        # Integration tests
        self.test_phase_integration()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 FACTOR GENERATOR TEST SUMMARY")
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
    print("🔥 Starting Comprehensive Backend API Testing")
    print("=" * 80)
    
    # Test PHASE 13.3 Factor Generator
    factor_tester = FactorGeneratorTester()
    factor_success = factor_tester.run_all_tests()
    
    print("\n" + "=" * 80)
    
    # Test PHASE 13.2 Feature Library (for completeness)
    feature_tester = AlphaFeatureLibraryTester()
    feature_success = feature_tester.run_all_tests()
    
    # Overall summary
    print("\n" + "=" * 80)
    print("🏁 OVERALL TEST SUMMARY")
    print("=" * 80)
    print(f"Factor Generator Tests: {'✅ PASS' if factor_success else '❌ FAIL'}")
    print(f"Feature Library Tests: {'✅ PASS' if feature_success else '❌ FAIL'}")
    
    total_tests = factor_tester.tests_run + feature_tester.tests_run
    total_passed = factor_tester.tests_passed + feature_tester.tests_passed
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Total Passed: {total_passed}")
    print(f"Overall Success Rate: {(total_passed/total_tests*100):.1f}%")
    
    return 0 if (factor_success and feature_success) else 1

if __name__ == "__main__":
    sys.exit(main())