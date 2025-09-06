#!/usr/bin/env python3
"""
Comprehensive UI Test Runner for ECU Diagnostic Tool
Executes all UI tests, provides coverage reporting, and validates user interaction flows
"""

import utime as time
import usys as sys
import lvgl as lv
import ujson as json

# Add src and test directories to path
sys.path.append('src')
sys.path.append('test')

from ui.utils.base_ui_test import BaseUITest

class UITestRunner:
    """Comprehensive UI test runner with coverage reporting"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self):
        """Run all UI tests and generate comprehensive report"""
        try:
            self.start_time = time.time()
            print("=" * 60)
            print("ECU DIAGNOSTIC TOOL - COMPREHENSIVE UI TEST SUITE")
            print("=" * 60)
            print(f"Started at: {time.localtime()}")
            print()
            
            # Define all test modules
            test_modules = [
                {
                    'name': 'Main Screen UI Tests',
                    'module': 'ui.test_main_screen',
                    'class': 'MainScreenUITest',
                    'description': 'Tests toolbar, menu, navigation, and tool loading'
                },
                {
                    'name': 'RPM Simulator UI Tests',
                    'module': 'ui.test_rpm_simulator_screen',
                    'class': 'RPMSimulatorUITest',
                    'description': 'Tests RPM slider, buttons, toggles, and simulation'
                },
                {
                    'name': 'System Selection UI Tests',
                    'module': 'ui.test_system_selection_screen',
                    'class': 'SystemSelectionUITest',
                    'description': 'Tests 4-step selection process and navigation'
                },
                {
                    'name': 'WiFi Setup UI Tests',
                    'module': 'ui.test_wifi_setup_screen',
                    'class': 'WiFiSetupUITest',
                    'description': 'Tests network scanning, selection, and connection'
                },
                {
                    'name': 'Additional Screens UI Tests',
                    'module': 'ui.test_additional_screens',
                    'class': 'AdditionalScreensUITest',
                    'description': 'Tests firmware update, system info, DTC, and config screens'
                }
            ]
            
            # Run each test module
            for test_info in test_modules:
                self.run_test_module(test_info)
            
            # Generate final report
            self.generate_final_report()
            
            return self.failed_tests == 0 and self.error_tests == 0
            
        except Exception as e:
            print(f"Test runner failed: {e}")
            return False
    
    def run_test_module(self, test_info):
        """Run a single test module"""
        try:
            print(f"\n{'='*50}")
            print(f"RUNNING: {test_info['name']}")
            print(f"{'='*50}")
            print(f"Description: {test_info['description']}")
            print()
            
            # Import test module dynamically
            module = __import__(test_info['module'], fromlist=[test_info['class']])
            test_class = getattr(module, test_info['class'])
            
            # Create and run test instance
            test_instance = test_class()
            success = test_instance.run_all_tests()
            
            # Collect results
            summary = test_instance.get_test_summary()
            self.test_results.append({
                'module': test_info['name'],
                'success': success,
                'summary': summary
            })
            
            # Update counters
            self.total_tests += summary['total']
            self.passed_tests += summary['passed']
            self.failed_tests += summary['failed']
            self.error_tests += summary['errors']
            
            # Print module summary
            status = "PASSED" if success else "FAILED"
            print(f"\n{test_info['name']}: {status}")
            print(f"  Tests: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}, Errors: {summary['errors']}")
            print(f"  Success Rate: {summary['success_rate']:.1f}%")
            
        except ImportError as e:
            print(f"Failed to import {test_info['module']}: {e}")
            self.error_tests += 1
        except Exception as e:
            print(f"Test module {test_info['name']} crashed: {e}")
            self.error_tests += 1
    
    def generate_final_report(self):
        """Generate comprehensive final test report"""
        try:
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            
            print(f"\n{'='*60}")
            print("COMPREHENSIVE UI TEST REPORT")
            print(f"{'='*60}")
            
            # Overall statistics
            print(f"Total Test Duration: {duration:.2f} seconds")
            print(f"Total Tests Executed: {self.total_tests}")
            print(f"Tests Passed: {self.passed_tests}")
            print(f"Tests Failed: {self.failed_tests}")
            print(f"Tests with Errors: {self.error_tests}")
            
            overall_success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
            print(f"Overall Success Rate: {overall_success_rate:.1f}%")
            
            # Module breakdown
            print(f"\n{'='*40}")
            print("MODULE BREAKDOWN")
            print(f"{'='*40}")
            
            for result in self.test_results:
                status = "✓ PASS" if result['success'] else "✗ FAIL"
                summary = result['summary']
                print(f"{status} {result['module']}")
                print(f"    Tests: {summary['total']}, Success Rate: {summary['success_rate']:.1f}%")
            
            # Coverage analysis
            self.generate_coverage_report()
            
            # Recommendations
            self.generate_recommendations()
            
            # Save detailed report
            self.save_detailed_report()
            
        except Exception as e:
            print(f"Report generation failed: {e}")
    
    def generate_coverage_report(self):
        """Generate UI coverage analysis"""
        try:
            print(f"\n{'='*40}")
            print("UI COVERAGE ANALYSIS")
            print(f"{'='*40}")
            
            # Define UI features that should be tested
            ui_features = {
                'Main Screen': [
                    'Toolbar display',
                    'Menu button interaction',
                    'Title button click',
                    'WiFi status display',
                    'Tool loading',
                    'Navigation flow'
                ],
                'RPM Simulator': [
                    'RPM display',
                    'Slider interaction',
                    'Start/stop button',
                    'Cam/crank toggles',
                    'Config button',
                    'Visual state updates'
                ],
                'System Selection': [
                    'Brand selection',
                    'System type selection',
                    'System name selection',
                    'Tool selection',
                    'Back navigation',
                    'Breadcrumb updates'
                ],
                'WiFi Setup': [
                    'Network scanning',
                    'Network selection',
                    'Password entry',
                    'Connection process',
                    'Error handling'
                ],
                'Additional Screens': [
                    'Firmware update',
                    'System info',
                    'DTC screens',
                    'Live data',
                    'Sensor configuration'
                ]
            }
            
            # Calculate coverage based on test results
            total_features = sum(len(features) for features in ui_features.values())
            covered_features = 0
            
            for result in self.test_results:
                module_name = result['module'].replace(' UI Tests', '')
                if module_name in ui_features:
                    # Estimate coverage based on success rate
                    module_features = len(ui_features[module_name])
                    success_rate = result['summary']['success_rate'] / 100
                    covered_features += module_features * success_rate
            
            coverage_percentage = (covered_features / total_features * 100) if total_features > 0 else 0
            
            print(f"Estimated UI Feature Coverage: {coverage_percentage:.1f}%")
            print(f"Total UI Features: {total_features}")
            print(f"Covered Features: {covered_features:.1f}")
            
            # Feature breakdown
            for screen, features in ui_features.items():
                print(f"\n{screen}:")
                for feature in features:
                    print(f"  • {feature}")
            
        except Exception as e:
            print(f"Coverage analysis failed: {e}")
    
    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        try:
            print(f"\n{'='*40}")
            print("RECOMMENDATIONS")
            print(f"{'='*40}")
            
            recommendations = []
            
            # Analyze results and generate recommendations
            if self.failed_tests > 0:
                recommendations.append(f"• Fix {self.failed_tests} failing test(s) to improve reliability")
            
            if self.error_tests > 0:
                recommendations.append(f"• Resolve {self.error_tests} test error(s) - may indicate missing implementations")
            
            overall_success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
            if overall_success_rate < 90:
                recommendations.append("• Improve test success rate to at least 90% for production readiness")
            
            # Module-specific recommendations
            for result in self.test_results:
                if not result['success']:
                    recommendations.append(f"• Review and fix issues in {result['module']}")
                
                if result['summary']['success_rate'] < 80:
                    recommendations.append(f"• {result['module']} needs significant improvement (< 80% success rate)")
            
            # General recommendations
            recommendations.extend([
                "• Add performance benchmarks for UI responsiveness",
                "• Implement automated regression testing",
                "• Add accessibility testing for better usability",
                "• Consider adding stress testing for memory usage",
                "• Implement continuous integration for UI tests"
            ])
            
            for rec in recommendations:
                print(rec)
            
        except Exception as e:
            print(f"Recommendations generation failed: {e}")
    
    def save_detailed_report(self):
        """Save detailed test report to file"""
        try:
            report_data = {
                'timestamp': time.time(),
                'duration': self.end_time - self.start_time if self.end_time and self.start_time else 0,
                'summary': {
                    'total_tests': self.total_tests,
                    'passed_tests': self.passed_tests,
                    'failed_tests': self.failed_tests,
                    'error_tests': self.error_tests,
                    'success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
                },
                'module_results': self.test_results
            }
            
            # Save to JSON file
            with open('./test/ui/test_report.json', 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"\nDetailed report saved to: ./test/ui/test_report.json")
            
        except Exception as e:
            print(f"Failed to save detailed report: {e}")

def main():
    """Run comprehensive UI test suite"""
    print("Initializing LVGL for UI testing...")
    
    # Initialize LVGL
    lv.init()
    
    # Create display driver for testing
    disp_drv = lv.sdl_window_create(800, 480)
    lv.sdl_window_set_resizeable(disp_drv, False)
    lv.sdl_window_set_title(disp_drv, "ECU Tool - UI Test Suite")
    
    # Create input driver
    mouse = lv.sdl_mouse_create()
    
    # Run all tests
    runner = UITestRunner()
    success = runner.run_all_tests()
    
    # Final status
    print(f"\n{'='*60}")
    if success:
        print("🎉 ALL UI TESTS COMPLETED SUCCESSFULLY!")
    else:
        print("❌ SOME UI TESTS FAILED - REVIEW RESULTS ABOVE")
    print(f"{'='*60}")
    
    return success

if __name__ == "__main__":
    main()
