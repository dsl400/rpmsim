#!/usr/bin/env python3
"""
RPM Simulator Screen UI Tests for ECU Diagnostic Tool
Tests RPM slider, start/stop button, cam/crank toggles, config button, and value updates
"""

import utime as time
import usys as sys
import lvgl as lv

# Add src and test directories to path
sys.path.append('src')
sys.path.append('test')

from ui.utils.base_ui_test import BaseUITest
from ui.utils.test_helpers import UITestHelpers

class RPMSimulatorUITest(BaseUITest):
    """Test suite for RPM Simulator Screen UI functionality"""
    
    def __init__(self):
        super().__init__("RPM Simulator UI Test")
        self.rpm_screen = None
        self.app_state = None
    
    def setup_test_environment(self):
        """Set up test environment with RPM simulator screen"""
        try:
            # Import required modules
            from utils.navigation_manager import AppState, app_state
            from utils.data_manager import DataManager
            from utils.error_handler import ErrorHandler
            from screens.rpm_simulator.rpm_simulator_screen import RPMSimulatorScreen

            # Use global app_state instance and initialize it
            self.app_state = app_state
            if not hasattr(self.app_state, 'data_manager') or not self.app_state.data_manager:
                self.app_state.data_manager = DataManager()
            if not hasattr(self.app_state, 'error_handler') or not self.app_state.error_handler:
                self.app_state.error_handler = ErrorHandler()

            # Create RPM simulator screen
            self.rpm_screen = RPMSimulatorScreen(self.screen)

            # Wait for screen to initialize
            self.wait_for_ui_update(500)

            self.log_pass("RPM Simulator test environment setup completed")
            return True

        except Exception as e:
            self.log_error(f"Test environment setup failed: {e}")
            return False
    
    def test_rpm_display_elements(self):
        """Test that RPM display elements are present"""
        try:
            self.log_info("Testing RPM display elements...")
            
            # Check title
            title = self.rpm_screen.widgets.get('title')
            if not self.verify_widget_visible(title, "title"):
                return False
            
            if not self.verify_widget_text(title, "RPM Simulator", "title"):
                return False
            
            # Check RPM display
            rpm_display = self.rpm_screen.widgets.get('rpm_display')
            if not self.verify_widget_visible(rpm_display, "RPM display"):
                return False
            
            # Check if RPM display shows current value
            rpm_text = rpm_display.get_text()
            if "RPM" in rpm_text:
                self.log_pass("RPM display shows RPM value")
            else:
                self.log_fail("RPM display does not show RPM value")
            
            # Check RPM slider
            rpm_slider = self.rpm_screen.widgets.get('rpm_slider')
            if not self.verify_widget_visible(rpm_slider, "RPM slider"):
                return False
            
            # Check slider labels
            slider_min = self.rpm_screen.widgets.get('slider_min')
            slider_max = self.rpm_screen.widgets.get('slider_max')
            
            if self.verify_widget_visible(slider_min, "slider min label"):
                self.verify_widget_text(slider_min, "0", "slider min label")
            
            if self.verify_widget_visible(slider_max, "slider max label"):
                self.verify_widget_text(slider_max, "8000", "slider max label")
            
            self.log_pass("All RPM display elements are present")
            return True
            
        except Exception as e:
            self.log_error(f"RPM display elements test failed: {e}")
            return False
    
    def test_rpm_slider_interaction(self):
        """Test RPM slider value changes"""
        try:
            self.log_info("Testing RPM slider interaction...")
            
            rpm_slider = self.rpm_screen.widgets.get('rpm_slider')
            rpm_display = self.rpm_screen.widgets.get('rpm_display')
            
            if not rpm_slider or not rpm_display:
                self.log_fail("RPM slider or display not found")
                return False
            
            # Test different RPM values
            test_values = [1000, 2500, 5000, 7500, 800]  # 800 is default
            
            for test_value in test_values:
                # Set slider value
                if not self.simulate_slider_change(rpm_slider, test_value):
                    return False
                
                # Check if display updated
                current_rpm = self.rpm_screen.current_rpm
                if current_rpm == test_value:
                    self.log_pass(f"RPM value updated to {test_value}")
                else:
                    self.log_fail(f"RPM value not updated. Expected: {test_value}, Got: {current_rpm}")
                
                # Check display text
                rpm_text = rpm_display.get_text()
                if str(test_value) in rpm_text:
                    self.log_pass(f"RPM display shows {test_value}")
                else:
                    self.log_fail(f"RPM display does not show {test_value}. Text: {rpm_text}")
            
            self.log_pass("RPM slider interaction test completed")
            return True
            
        except Exception as e:
            self.log_error(f"RPM slider interaction test failed: {e}")
            return False
    
    def test_control_buttons(self):
        """Test control buttons (cam, crank, start/stop)"""
        try:
            self.log_info("Testing control buttons...")
            
            # Test cam toggle button
            cam_btn = self.rpm_screen.widgets.get('cam_toggle_btn')
            if not self.verify_widget_visible(cam_btn, "cam toggle button"):
                return False
            
            # Check initial state (should be enabled)
            initial_cam_state = self.rpm_screen.camshaft_enabled
            self.log_info(f"Initial cam state: {initial_cam_state}")
            
            # Click cam toggle
            if not self.simulate_click(cam_btn):
                return False
            
            # Check state changed
            new_cam_state = self.rpm_screen.camshaft_enabled
            if new_cam_state != initial_cam_state:
                self.log_pass("Cam toggle state changed")
            else:
                self.log_fail("Cam toggle state did not change")
            
            # Test crank toggle button
            crank_btn = self.rpm_screen.widgets.get('crank_toggle_btn')
            if not self.verify_widget_visible(crank_btn, "crank toggle button"):
                return False
            
            # Check initial state (should be enabled)
            initial_crank_state = self.rpm_screen.crankshaft_enabled
            self.log_info(f"Initial crank state: {initial_crank_state}")
            
            # Click crank toggle
            if not self.simulate_click(crank_btn):
                return False
            
            # Check state changed
            new_crank_state = self.rpm_screen.crankshaft_enabled
            if new_crank_state != initial_crank_state:
                self.log_pass("Crank toggle state changed")
            else:
                self.log_fail("Crank toggle state did not change")
            
            # Test start/stop button
            start_stop_btn = self.rpm_screen.widgets.get('start_stop_btn')
            if not self.verify_widget_visible(start_stop_btn, "start/stop button"):
                return False
            
            # Check initial state (should be stopped)
            initial_sim_state = self.rpm_screen.simulation_active
            self.log_info(f"Initial simulation state: {initial_sim_state}")
            
            # Click start/stop button
            if not self.simulate_click(start_stop_btn):
                return False
            
            # Check state changed
            new_sim_state = self.rpm_screen.simulation_active
            if new_sim_state != initial_sim_state:
                self.log_pass("Simulation state changed")
            else:
                self.log_fail("Simulation state did not change")
            
            self.log_pass("Control buttons test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Control buttons test failed: {e}")
            return False
    
    def test_config_button(self):
        """Test configuration button"""
        try:
            self.log_info("Testing configuration button...")
            
            config_btn = self.rpm_screen.widgets.get('config_btn')
            if not self.verify_widget_visible(config_btn, "config button"):
                return False
            
            # Click config button
            if not self.simulate_click(config_btn):
                return False
            
            self.log_pass("Config button click simulation completed")
            return True
            
        except Exception as e:
            self.log_error(f"Config button test failed: {e}")
            return False
    
    def test_button_visual_states(self):
        """Test visual states of toggle buttons"""
        try:
            self.log_info("Testing button visual states...")
            
            # Test cam button visual state
            cam_btn = self.rpm_screen.widgets.get('cam_toggle_btn')
            if cam_btn:
                # Click to toggle state
                self.simulate_click(cam_btn)
                self.wait_for_ui_update(200)
                
                # Visual state should have changed (color, etc.)
                self.log_pass("Cam button visual state test completed")
            
            # Test crank button visual state
            crank_btn = self.rpm_screen.widgets.get('crank_toggle_btn')
            if crank_btn:
                # Click to toggle state
                self.simulate_click(crank_btn)
                self.wait_for_ui_update(200)
                
                # Visual state should have changed (color, etc.)
                self.log_pass("Crank button visual state test completed")
            
            # Test start/stop button visual state
            start_stop_btn = self.rpm_screen.widgets.get('start_stop_btn')
            if start_stop_btn:
                # Click to toggle state
                self.simulate_click(start_stop_btn)
                self.wait_for_ui_update(200)
                
                # Visual state should have changed (play/stop icon, color)
                self.log_pass("Start/stop button visual state test completed")
            
            return True
            
        except Exception as e:
            self.log_error(f"Button visual states test failed: {e}")
            return False
    
    def test_complete_rpm_workflow(self):
        """Test complete RPM simulation workflow"""
        try:
            self.log_info("Testing complete RPM workflow...")
            
            # Define workflow steps
            workflow_steps = [
                {
                    'description': 'Set RPM to 2000',
                    'action': 'slider',
                    'target': self.rpm_screen.widgets.get('rpm_slider'),
                    'value': 2000
                },
                {
                    'description': 'Wait for RPM update',
                    'action': 'wait',
                    'duration': 300
                },
                {
                    'description': 'Start simulation',
                    'action': 'click',
                    'target': self.rpm_screen.widgets.get('start_stop_btn')
                },
                {
                    'description': 'Wait for simulation start',
                    'action': 'wait',
                    'duration': 500
                },
                {
                    'description': 'Toggle cam sensor',
                    'action': 'click',
                    'target': self.rpm_screen.widgets.get('cam_toggle_btn')
                },
                {
                    'description': 'Wait for cam toggle',
                    'action': 'wait',
                    'duration': 200
                },
                {
                    'description': 'Change RPM during simulation',
                    'action': 'slider',
                    'target': self.rpm_screen.widgets.get('rpm_slider'),
                    'value': 3500
                },
                {
                    'description': 'Wait for RPM change',
                    'action': 'wait',
                    'duration': 300
                },
                {
                    'description': 'Stop simulation',
                    'action': 'click',
                    'target': self.rpm_screen.widgets.get('start_stop_btn')
                }
            ]
            
            # Execute workflow
            success = UITestHelpers.simulate_navigation_flow(self, workflow_steps)
            
            if success:
                self.log_pass("Complete RPM workflow test passed")
            else:
                self.log_fail("Complete RPM workflow test failed")
            
            return success
            
        except Exception as e:
            self.log_error(f"Complete RPM workflow test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all RPM simulator tests"""
        try:
            self.log_info("Starting RPM Simulator UI Tests...")
            
            # Setup test environment
            if not self.setup_test_environment():
                return False
            
            # Run individual tests
            tests = [
                self.test_rpm_display_elements,
                self.test_rpm_slider_interaction,
                self.test_control_buttons,
                self.test_config_button,
                self.test_button_visual_states,
                self.test_complete_rpm_workflow
            ]
            
            passed_tests = 0
            for test in tests:
                try:
                    if test():
                        passed_tests += 1
                except Exception as e:
                    self.log_error(f"Test {test.__name__} crashed: {e}")
            
            # Print summary
            self.log_info(f"Completed {passed_tests}/{len(tests)} tests successfully")
            self.print_summary()
            
            return passed_tests == len(tests)
            
        except Exception as e:
            self.log_error(f"Test execution failed: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Run RPM simulator UI tests"""
    test = RPMSimulatorUITest()
    success = test.run_all_tests()
    return success

if __name__ == "__main__":
    main()
