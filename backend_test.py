#!/usr/bin/env python3
"""
PHASE 13.4 Factor Ranker - Backend API Tests
============================================
Comprehensive testing for Factor Ranker endpoints.

Test Coverage:
- PHASE 13.4 Factor Ranker (NEW):
  * Health check
  * Stats (total_rankings >= 1000, approved_count >= 50)
  * Ranking execution (POST /run)
  * Rankings listing with filters
  * Verdict filtering (PROMISING, STRONG, etc.)
  * Approved factors filtering
  * Top factors retrieval
  * Approved factors count >= 100
  * Verdicts breakdown
  * Ranking runs history
  * Individual factor ranking retrieval
  * Single factor evaluation
- PHASE 13.3 Factor Generator:
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

class FactorRankerTester:
    """PHASE 13.4 Factor Ranker API Tests"""
    
    def __init__(self, base_url: str = "https://pattern-detector-10.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'FactorRanker-Tester/1.0'
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

    def test_factor_ranker_health(self):
        """Test GET /api/factor-ranker/health - status=healthy"""
        print("\n🔍 Testing Factor Ranker Health Check...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/health')
        
        if success and data.get('status') == 'healthy':
            self.log_test("Factor Ranker Health Check", True, f"Status: {data.get('status')}")
            return True
        else:
            self.log_test("Factor Ranker Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_factor_ranker_stats(self):
        """Test GET /api/factor-ranker/stats - total_rankings >= 1000, approved_count >= 50"""
        print("\n🔍 Testing Factor Ranker Stats...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/stats')
        
        if success:
            ranker_stats = data.get('ranker', {})
            repository_stats = ranker_stats.get('repository', {})
            
            total_rankings = repository_stats.get('total_rankings', 0)
            approved_count = repository_stats.get('approved_count', 0)
            
            # Check total rankings >= 1000
            if total_rankings >= 1000:
                self.log_test("Stats - Total Rankings >= 1000", True, f"Found {total_rankings} rankings")
            else:
                self.log_test("Stats - Total Rankings >= 1000", False, f"Only {total_rankings} rankings found")
            
            # Check approved count >= 50
            if approved_count >= 50:
                self.log_test("Stats - Approved Count >= 50", True, f"Found {approved_count} approved factors")
            else:
                self.log_test("Stats - Approved Count >= 50", False, f"Only {approved_count} approved factors found")
            
            # Check verdict breakdown
            verdict_counts = repository_stats.get('verdict_counts', {})
            self.log_test("Stats - Verdict Breakdown", len(verdict_counts) > 0, f"Verdicts: {verdict_counts}")
            
            # Check last run info
            last_run = ranker_stats.get('last_run')
            if last_run:
                run_status = last_run.get('status', 'unknown')
                self.log_test("Stats - Last Run Info", run_status == 'completed', f"Last run status: {run_status}")
            
            return total_rankings >= 1000 and approved_count >= 50
        else:
            self.log_test("Factor Ranker Stats", False, f"Status: {status}, Data: {data}")
            return False

    def test_ranking_execution(self):
        """Test POST /api/factor-ranker/run - запуск ranking работает"""
        print("\n🔍 Testing Ranking Execution...")
        
        # Test with smaller batch for testing
        ranking_config = {
            "max_approved": 150,
            "clear_existing": False,
            "seed": 42
        }
        
        success, data, status = self.make_request('POST', 'factor-ranker/run', ranking_config)
        
        if success:
            run_status = data.get('status', '')
            run_data = data.get('run', {})
            
            if run_status == 'completed':
                total_evaluated = run_data.get('total_evaluated', 0)
                approved_count = run_data.get('approved_count', 0)
                verdicts = run_data.get('verdicts', {})
                
                self.log_test("Ranking Execution", True, f"Evaluated {total_evaluated} factors, approved {approved_count}")
                self.log_test("Ranking Verdicts", len(verdicts) > 0, f"Verdicts: {verdicts}")
                
                # Check family distribution
                family_approved = run_data.get('family_approved', {})
                self.log_test("Family Distribution", len(family_approved) > 0, f"Family approved: {family_approved}")
                
                return True
            else:
                error_msg = run_data.get('error_message', 'Unknown error')
                self.log_test("Ranking Execution", False, f"Ranking failed: {error_msg}")
        else:
            self.log_test("Ranking Execution", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_rankings_listing(self):
        """Test GET /api/factor-ranker/rankings - список rankings с фильтрами"""
        print("\n🔍 Testing Rankings Listing...")
        
        # Test basic listing
        success, data, status = self.make_request('GET', 'factor-ranker/rankings?limit=50')
        
        if success:
            rankings = data.get('rankings', [])
            count = data.get('count', 0)
            
            self.log_test("Rankings Listing", count > 0, f"Retrieved {count} rankings")
            
            # Check ranking structure
            if rankings:
                ranking = rankings[0]
                required_fields = ['factor_id', 'verdict', 'composite_score', 'ic', 'sharpe']
                present_fields = [field for field in required_fields if field in ranking]
                self.log_test("Ranking Structure", len(present_fields) >= 4, f"Present fields: {present_fields}")
            
            return count > 0
        else:
            self.log_test("Rankings Listing", False, f"Status: {status}, Data: {data}")
            return False

    def test_verdict_filtering(self):
        """Test GET /api/factor-ranker/rankings?verdict=PROMISING - фильтр по verdict"""
        print("\n🔍 Testing Verdict Filtering...")
        
        # Test PROMISING filter
        success, data, status = self.make_request('GET', 'factor-ranker/rankings?verdict=PROMISING&limit=30')
        
        if success:
            rankings = data.get('rankings', [])
            count = data.get('count', 0)
            filters = data.get('filters', {})
            
            self.log_test("Verdict Filter (PROMISING)", count >= 0, f"Found {count} PROMISING factors")
            
            # Verify all returned rankings have PROMISING verdict
            if rankings:
                promising_count = sum(1 for r in rankings if r.get('verdict') == 'PROMISING')
                self.log_test("PROMISING Verdict Consistency", promising_count == len(rankings), 
                            f"{promising_count}/{len(rankings)} have PROMISING verdict")
            
            # Test STRONG filter
            success2, data2, status2 = self.make_request('GET', 'factor-ranker/rankings?verdict=STRONG&limit=20')
            if success2:
                strong_count = data2.get('count', 0)
                self.log_test("Verdict Filter (STRONG)", strong_count >= 0, f"Found {strong_count} STRONG factors")
            
            # Test ELITE filter
            success3, data3, status3 = self.make_request('GET', 'factor-ranker/rankings?verdict=ELITE&limit=10')
            if success3:
                elite_count = data3.get('count', 0)
                self.log_test("Verdict Filter (ELITE)", elite_count >= 0, f"Found {elite_count} ELITE factors")
            
            return True
        else:
            self.log_test("Verdict Filtering", False, f"Status: {status}, Data: {data}")
            return False

    def test_approved_filtering(self):
        """Test GET /api/factor-ranker/rankings?approved_only=true - только approved"""
        print("\n🔍 Testing Approved Filtering...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/rankings?approved_only=true&limit=100')
        
        if success:
            rankings = data.get('rankings', [])
            count = data.get('count', 0)
            filters = data.get('filters', {})
            
            self.log_test("Approved Only Filter", count > 0, f"Found {count} approved factors")
            
            # Verify all returned rankings are approved
            if rankings:
                approved_count = sum(1 for r in rankings if r.get('approved', False))
                self.log_test("Approved Consistency", approved_count == len(rankings), 
                            f"{approved_count}/{len(rankings)} are approved")
            
            return count > 0
        else:
            self.log_test("Approved Filtering", False, f"Status: {status}, Data: {data}")
            return False

    def test_top_factors(self):
        """Test GET /api/factor-ranker/top?n=20 - top factors"""
        print("\n🔍 Testing Top Factors...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/top?n=20')
        
        if success:
            top_factors = data.get('top_factors', [])
            count = data.get('count', 0)
            
            self.log_test("Top Factors (n=20)", count > 0, f"Retrieved {count} top factors")
            
            # Check if factors are sorted by composite score (descending)
            if len(top_factors) >= 2:
                scores = [f.get('composite_score', 0) for f in top_factors]
                is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
                self.log_test("Top Factors Sorted", is_sorted, f"Scores: {scores[:5]}...")
            
            # Test different n values
            success2, data2, status2 = self.make_request('GET', 'factor-ranker/top?n=10')
            if success2:
                top_10_count = data2.get('count', 0)
                self.log_test("Top Factors (n=10)", top_10_count > 0, f"Retrieved {top_10_count} top factors")
            
            return count > 0
        else:
            self.log_test("Top Factors", False, f"Status: {status}, Data: {data}")
            return False

    def test_approved_factors(self):
        """Test GET /api/factor-ranker/approved - все approved factors >= 100"""
        print("\n🔍 Testing Approved Factors...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/approved')
        
        if success:
            approved_factors = data.get('approved_factors', [])
            count = data.get('count', 0)
            
            if count >= 100:
                self.log_test("Approved Factors >= 100", True, f"Found {count} approved factors")
            else:
                self.log_test("Approved Factors >= 100", False, f"Only {count} approved factors found")
            
            # Check that all returned factors are approved
            if approved_factors:
                approved_count = sum(1 for f in approved_factors if f.get('approved', False))
                self.log_test("All Factors Approved", approved_count == len(approved_factors), 
                            f"{approved_count}/{len(approved_factors)} are approved")
            
            return count >= 100
        else:
            self.log_test("Approved Factors", False, f"Status: {status}, Data: {data}")
            return False

    def test_verdicts_breakdown(self):
        """Test GET /api/factor-ranker/verdicts - breakdown по verdicts"""
        print("\n🔍 Testing Verdicts Breakdown...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/verdicts')
        
        if success:
            verdicts = data.get('verdicts', [])
            counts = data.get('counts', {})
            total = data.get('total', 0)
            
            expected_verdicts = ["ELITE", "STRONG", "PROMISING", "WEAK", "REJECTED"]
            
            self.log_test("Verdicts List", set(expected_verdicts).issubset(set(verdicts)), 
                         f"Verdicts: {verdicts}")
            
            self.log_test("Verdict Counts", len(counts) > 0, f"Counts: {counts}")
            
            # Check that counts sum to total
            if counts:
                sum_counts = sum(counts.values())
                self.log_test("Counts Sum Consistency", sum_counts == total, 
                            f"Sum: {sum_counts}, Total: {total}")
            
            # Check for expected distribution (based on agent context)
            strong_count = counts.get('STRONG', 0)
            promising_count = counts.get('PROMISING', 0)
            
            self.log_test("Expected Distribution", strong_count >= 4 and promising_count >= 100, 
                         f"STRONG: {strong_count}, PROMISING: {promising_count}")
            
            return len(counts) > 0 and total > 0
        else:
            self.log_test("Verdicts Breakdown", False, f"Status: {status}, Data: {data}")
            return False

    def test_ranking_runs(self):
        """Test GET /api/factor-ranker/runs - история ranking runs"""
        print("\n🔍 Testing Ranking Runs History...")
        
        success, data, status = self.make_request('GET', 'factor-ranker/runs?limit=10')
        
        if success:
            runs = data.get('runs', [])
            count = data.get('count', 0)
            
            self.log_test("Ranking Runs History", count >= 0, f"Found {count} ranking runs")
            
            # Check run structure if runs exist
            if runs:
                run = runs[0]
                required_fields = ['run_id', 'status', 'total_evaluated', 'approved_count']
                present_fields = [field for field in required_fields if field in run]
                self.log_test("Run Structure", len(present_fields) >= 3, f"Present fields: {present_fields}")
                
                # Check for completed runs
                completed_runs = [r for r in runs if r.get('status') == 'completed']
                self.log_test("Completed Runs", len(completed_runs) > 0, 
                            f"{len(completed_runs)}/{len(runs)} completed")
            
            return True
        else:
            self.log_test("Ranking Runs History", False, f"Status: {status}, Data: {data}")
            return False

    def test_individual_factor_ranking(self):
        """Test GET /api/factor-ranker/{factor_id} - получение ranking конкретного фактора"""
        print("\n🔍 Testing Individual Factor Ranking...")
        
        # First, get a list of rankings to find a valid factor ID
        success, data, status = self.make_request('GET', 'factor-ranker/rankings?limit=10')
        
        if success:
            rankings = data.get('rankings', [])
            
            if rankings:
                factor_id = rankings[0]['factor_id']
                success2, data2, status2 = self.make_request('GET', f'factor-ranker/{factor_id}')
                
                if success2:
                    ranking_data = data2.get('ranking', {})
                    
                    self.log_test("Individual Factor Ranking", True, f"Retrieved ranking for: {factor_id}")
                    
                    # Check ranking structure
                    required_fields = ['factor_id', 'verdict', 'composite_score', 'ic', 'sharpe', 'stability']
                    present_fields = [field for field in required_fields if field in ranking_data]
                    self.log_test("Ranking Structure", len(present_fields) >= 5, f"Present fields: {present_fields}")
                    
                    return True
                else:
                    self.log_test("Individual Factor Ranking", False, f"Status: {status2}, Data: {data2}")
            else:
                self.log_test("Individual Factor Ranking", False, "No rankings found for retrieval test")
        else:
            self.log_test("Individual Factor Ranking", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_single_factor_evaluation(self):
        """Test POST /api/factor-ranker/evaluate/{factor_id} - оценка одного фактора"""
        print("\n🔍 Testing Single Factor Evaluation...")
        
        # First, get a factor ID from the generator
        success, data, status = self.make_request('GET', 'factor-generator/factors?limit=5')
        
        if success:
            factors = data.get('factors', [])
            
            if factors:
                factor_id = factors[0]['factor_id']
                success2, data2, status2 = self.make_request('POST', f'factor-ranker/evaluate/{factor_id}')
                
                if success2:
                    metrics = data2.get('metrics', {})
                    evaluated_factor_id = data2.get('factor_id', '')
                    
                    self.log_test("Single Factor Evaluation", True, f"Evaluated factor: {evaluated_factor_id}")
                    
                    # Check metrics structure
                    required_metrics = ['ic', 'sharpe', 'stability', 'composite_score', 'verdict']
                    present_metrics = [metric for metric in required_metrics if metric in metrics]
                    self.log_test("Metrics Structure", len(present_metrics) >= 4, f"Present metrics: {present_metrics}")
                    
                    return True
                else:
                    self.log_test("Single Factor Evaluation", False, f"Status: {status2}, Data: {data2}")
            else:
                self.log_test("Single Factor Evaluation", False, "No factors found for evaluation test")
        else:
            self.log_test("Single Factor Evaluation", False, f"Status: {status}, Data: {data}")
        
        return False

    def test_phase_integration(self):
        """Test integration with previous phases"""
        print("\n🔍 Testing Phase Integration...")
        
        # Test PHASE 13.3 Factor Generator
        success1, data1, status1 = self.make_request('GET', 'factor-generator/stats')
        if success1:
            generator_stats = data1.get('generator', {})
            repository_stats = data1.get('repository', {})
            total_factors = repository_stats.get('total_factors', 0)
            self.log_test("PHASE 13.3 Factor Generator", total_factors >= 1000, f"Found {total_factors} factors")
        else:
            self.log_test("PHASE 13.3 Factor Generator", False, f"Status: {status1}")
        
        # Test PHASE 13.2 Feature Library
        success2, data2, status2 = self.make_request('GET', 'alpha-features/stats')
        if success2:
            registry_stats = data2.get('registry', {})
            total_features = registry_stats.get('total_features', 0)
            self.log_test("PHASE 13.2 Feature Library", total_features >= 300, f"Found {total_features} features")
        else:
            self.log_test("PHASE 13.2 Feature Library", False, f"Status: {status2}")
        
        return success1 and success2

    def run_all_tests(self):
        """Run all Factor Ranker test cases."""
        print("=" * 80)
        print("🚀 PHASE 13.4 Factor Ranker - Backend API Tests")
        print("=" * 80)
        
        # Core health and stats tests
        self.test_factor_ranker_health()
        self.test_factor_ranker_stats()
        
        # Ranking execution test
        self.test_ranking_execution()
        
        # Rankings retrieval tests
        self.test_rankings_listing()
        self.test_verdict_filtering()
        self.test_approved_filtering()
        self.test_top_factors()
        self.test_approved_factors()
        self.test_verdicts_breakdown()
        self.test_ranking_runs()
        
        # Individual operations tests
        self.test_individual_factor_ranking()
        self.test_single_factor_evaluation()
        
        # Integration tests
        self.test_phase_integration()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 FACTOR RANKER TEST SUMMARY")
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
            registry_stats = data1.get('registry', {})
            total_nodes = registry_stats.get('total_nodes', 0)
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
            registry_stats = data.get('registry', {})
            total_nodes = registry_stats.get('total_nodes', 0)
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
    
    # Test PHASE 13.4 Factor Ranker (NEW)
    ranker_tester = FactorRankerTester()
    ranker_success = ranker_tester.run_all_tests()
    
    print("\n" + "=" * 80)
    
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
    print(f"Factor Ranker Tests: {'✅ PASS' if ranker_success else '❌ FAIL'}")
    print(f"Factor Generator Tests: {'✅ PASS' if factor_success else '❌ FAIL'}")
    print(f"Feature Library Tests: {'✅ PASS' if feature_success else '❌ FAIL'}")
    
    total_tests = ranker_tester.tests_run + factor_tester.tests_run + feature_tester.tests_run
    total_passed = ranker_tester.tests_passed + factor_tester.tests_passed + feature_tester.tests_passed
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Total Passed: {total_passed}")
    print(f"Overall Success Rate: {(total_passed/total_tests*100):.1f}%")
    
    return 0 if (ranker_success and factor_success and feature_success) else 1

if __name__ == "__main__":
    sys.exit(main())