#!/usr/bin/env python3
"""
Comprehensive Test Runner for ECU Diagnostic Tool
Runs all tests in organized categories and provides detailed reporting
"""

try:
    import usys as sys
    import utime as time
except ImportError:
    import sys
    import time
import os

# Add paths
sys.path.append('src')
sys.path.append('test')

def run_test_file(test_file_path, test_name):
    """Run a single test file and return results"""
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print(f"{'='*60}")
    
    try:
        # Import and run the test
        if test_file_path.endswith('.py'):
            # Remove .py extension and convert path to module name
            module_path = test_file_path[:-3].replace('/', '.').replace('\\', '.')
            if module_path.startswith('.'):
                module_path = module_path[1:]
            
            # Execute the test file
            import subprocess
            result = subprocess.run([
                './sim_app/MpSimulator-x86_64.AppImage', 
                test_file_path
            ], capture_output=True, text=True, cwd='/home/dsl400/work/teo/rpmsim')
            
            if result.returncode == 0:
                print(f"✅ {test_name} PASSED")
                return True, result.stdout
            else:
                print(f"❌ {test_name} FAILED")
                print(f"Error: {result.stderr}")
                return False, result.stderr
                
    except Exception as e:
        print(f"❌ {test_name} CRASHED: {e}")
        return False, str(e)

def run_all_tests():
    """Run all tests in organized categories"""
    print("🧪 ECU DIAGNOSTIC TOOL - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Test categories and their files
    test_categories = {
        "Unit Tests": [
            ("test/unit/test_main_screen_simple.py", "Main Screen Unit Test"),
            ("test/unit/test_system_selection_simple.py", "System Selection Unit Test"),
            ("test/unit/test_navigation_simple.py", "Navigation Unit Test"),
        ],
        "UI Tests": [
            ("test/ui/test_main_screen.py", "Main Screen UI Test"),
            ("test/ui/test_system_selection_screen.py", "System Selection UI Test"),
            ("test/ui/test_rpm_simulator_screen.py", "RPM Simulator UI Test"),
            ("test/ui/test_wifi_setup_screen.py", "WiFi Setup UI Test"),
            ("test/ui/test_new_system_selection.py", "New System Selection UI Test"),
            ("test/ui/test_new_system_selection_screen.py", "New System Selection Screen Test"),
        ],
        "Integration Tests": [
            ("test/integration/test_ui_working.py", "Comprehensive UI Integration Test"),
            ("test/integration/test_full_workflow.py", "Full Workflow Integration Test"),
            ("test/integration/test_final_system_selection.py", "Final System Selection Test"),
        ]
    }
    
    # Results tracking
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    # Run tests by category
    for category, tests in test_categories.items():
        print(f"\n🔍 {category.upper()}")
        print("-" * 60)
        
        category_passed = 0
        category_total = 0
        
        for test_file, test_name in tests:
            # Check if test file exists
            if os.path.exists(test_file):
                total_tests += 1
                category_total += 1
                
                success, output = run_test_file(test_file, test_name)
                if success:
                    passed_tests += 1
                    category_passed += 1
                else:
                    failed_tests.append((test_name, output))
            else:
                print(f"⚠️  {test_name} - File not found: {test_file}")
        
        print(f"\n{category} Results: {category_passed}/{category_total} passed")
    
    # Final results
    print("\n" + "=" * 80)
    print("📊 FINAL TEST RESULTS")
    print("=" * 80)
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests Run: {total_tests}")
    print(f"Tests Passed: {passed_tests}")
    print(f"Tests Failed: {len(failed_tests)}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}")
            print(f"    Error: {error[:100]}...")
    
    if success_rate >= 90:
        print(f"\n🎉 EXCELLENT! Test suite is in great shape!")
    elif success_rate >= 75:
        print(f"\n✅ GOOD! Most tests are passing.")
    elif success_rate >= 50:
        print(f"\n⚠️  NEEDS ATTENTION! Several tests are failing.")
    else:
        print(f"\n🚨 CRITICAL! Many tests are failing - immediate attention required.")
    
    return success_rate >= 75

def check_for_duplicates():
    """Check for duplicate test files"""
    print("\n🔍 CHECKING FOR DUPLICATE TESTS")
    print("-" * 60)
    
    test_files = []
    
    # Collect all test files
    for root, dirs, files in os.walk('test'):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(os.path.join(root, file))
    
    # Check for similar names
    duplicates_found = False
    checked = set()
    
    for i, file1 in enumerate(test_files):
        base1 = os.path.basename(file1)
        if base1 in checked:
            continue
            
        similar = [file1]
        for j, file2 in enumerate(test_files):
            if i != j:
                base2 = os.path.basename(file2)
                # Check for similar names (same base name in different directories)
                if base1 == base2:
                    similar.append(file2)
        
        if len(similar) > 1:
            print(f"⚠️  Potential duplicates found:")
            for sim_file in similar:
                print(f"   - {sim_file}")
            duplicates_found = True
        
        checked.add(base1)
    
    if not duplicates_found:
        print("✅ No duplicate test files found")
    
    return not duplicates_found

if __name__ == "__main__":
    print("Starting comprehensive test suite...")
    
    # Check for duplicates first
    no_duplicates = check_for_duplicates()
    
    # Run all tests
    success = run_all_tests()
    
    if success and no_duplicates:
        print("\n🎯 ALL SYSTEMS GO! Test suite is healthy.")
        sys.exit(0)
    else:
        print("\n🔧 MAINTENANCE REQUIRED! Please address failing tests.")
        sys.exit(1)
