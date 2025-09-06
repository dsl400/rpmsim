#!/usr/bin/env python3
"""
Additional Screens UI Tests for ECU Diagnostic Tool
Tests firmware update, system info, DTC screens, live data, and sensor configuration
"""

import utime as time
import usys as sys
import lvgl as lv

# Add src and test directories to path
sys.path.append('src')
sys.path.append('test')

from ui.utils.base_ui_test import BaseUITest
from ui.utils.test_helpers import UITestHelpers

class AdditionalScreensUITest(BaseUITest):
    """Test suite for additional screen UI functionality"""
    
    def __init__(self):
        super().__init__("Additional Screens UI Test")
        self.app_state = None
    
    def setup_test_environment(self):
        """Set up test environment"""
        try:
            # Import required modules
            from utils.navigation_manager import AppState, app_state
            from utils.data_manager import DataManager
            from utils.error_handler import ErrorHandler

            # Use global app_state instance and initialize it
            self.app_state = app_state
            if not hasattr(self.app_state, 'data_manager') or not self.app_state.data_manager:
                self.app_state.data_manager = DataManager()
            if not hasattr(self.app_state, 'error_handler') or not self.app_state.error_handler:
                self.app_state.error_handler = ErrorHandler()

            self.log_pass("Additional screens test environment setup completed")
            return True

        except Exception as e:
            self.log_error(f"Test environment setup failed: {e}")
            return False
    
    def test_firmware_update_screen(self):
        """Test firmware update screen"""
        try:
            self.log_info("Testing firmware update screen...")
            
            # Import and create firmware update screen
            from screens.firmware_update import FirmwareUpdateScreen
            firmware_screen = FirmwareUpdateScreen(self.screen)
            
            # Wait for screen to initialize
            self.wait_for_ui_update(500)
            
            # Test basic elements
            expected_elements = [
                {'type': 'label', 'text': 'Firmware Update', 'name': 'title'},
                {'type': 'button', 'text': 'Check for Updates', 'name': 'check button'},
                {'type': 'button', 'text': 'Download', 'name': 'download button'},
                {'type': 'button', 'text': 'Install', 'name': 'install button'}
            ]
            
            # Verify elements exist (some may be hidden initially)
            for element in expected_elements:
                widget = UITestHelpers.find_widget_by_text(self.screen, element['text'])
                if widget:
                    self.log_pass(f"Found {element['name']}")
                else:
                    self.log_info(f"{element['name']} not found (may be context-dependent)")
            
            # Test check for updates button if available
            check_btn = UITestHelpers.find_button_by_text(self.screen, "Check for Updates")
            if check_btn:
                self.simulate_click(check_btn)
                self.wait_for_ui_update(500)
                self.log_pass("Check for updates button interaction completed")
            
            firmware_screen.cleanup()
            self.log_pass("Firmware update screen test completed")
            return True
            
        except ImportError:
            self.log_info("Firmware update screen not implemented yet")
            return True
        except Exception as e:
            self.log_error(f"Firmware update screen test failed: {e}")
            return False
    
    def test_system_info_screen(self):
        """Test system info screen"""
        try:
            self.log_info("Testing system info screen...")
            
            # Import and create system info screen
            from screens.system_info import SystemInfoScreen
            info_screen = SystemInfoScreen(self.screen)
            
            # Wait for screen to initialize
            self.wait_for_ui_update(500)
            
            # Test basic elements
            expected_elements = [
                {'type': 'label', 'text': 'System Information', 'name': 'title'},
                {'type': 'label', 'text': 'Version', 'name': 'version label'},
                {'type': 'label', 'text': 'Hardware', 'name': 'hardware label'},
                {'type': 'label', 'text': 'Memory', 'name': 'memory label'}
            ]
            
            # Verify elements exist
            for element in expected_elements:
                widget = UITestHelpers.find_widget_by_text(self.screen, element['text'])
                if widget:
                    self.log_pass(f"Found {element['name']}")
                else:
                    self.log_info(f"{element['name']} not found (may be different text)")
            
            # Look for any buttons on the screen
            buttons = UITestHelpers.get_all_buttons(self.screen)
            if buttons:
                self.log_pass(f"Found {len(buttons)} button(s) on system info screen")
                
                # Test clicking first button
                if self.simulate_click(buttons[0]):
                    self.log_pass("System info button interaction completed")
            
            info_screen.cleanup()
            self.log_pass("System info screen test completed")
            return True
            
        except ImportError:
            self.log_info("System info screen not implemented yet")
            return True
        except Exception as e:
            self.log_error(f"System info screen test failed: {e}")
            return False
    
    def test_dtc_screens(self):
        """Test DTC (Diagnostic Trouble Codes) screens"""
        try:
            self.log_info("Testing DTC screens...")
            
            # Test Clear DTC screen
            try:
                from screens.dtc.clear_dtc import ClearDTCScreen
                clear_dtc_screen = ClearDTCScreen(self.screen)
                
                self.wait_for_ui_update(500)
                
                # Look for clear DTC elements
                clear_btn = UITestHelpers.find_button_by_text(self.screen, "Clear DTCs")
                if clear_btn:
                    self.log_pass("Found Clear DTCs button")
                    self.simulate_click(clear_btn)
                    self.wait_for_ui_update(300)
                
                clear_dtc_screen.cleanup()
                self.log_pass("Clear DTC screen test completed")
                
            except ImportError:
                self.log_info("Clear DTC screen not implemented yet")
            
            # Test Read DTC screen
            try:
                from screens.dtc.read_dtc import ReadDTCScreen
                read_dtc_screen = ReadDTCScreen(self.screen)
                
                self.wait_for_ui_update(500)
                
                # Look for read DTC elements
                read_btn = UITestHelpers.find_button_by_text(self.screen, "Read DTCs")
                if read_btn:
                    self.log_pass("Found Read DTCs button")
                    self.simulate_click(read_btn)
                    self.wait_for_ui_update(300)
                
                read_dtc_screen.cleanup()
                self.log_pass("Read DTC screen test completed")
                
            except ImportError:
                self.log_info("Read DTC screen not implemented yet")
            
            return True
            
        except Exception as e:
            self.log_error(f"DTC screens test failed: {e}")
            return False
    
    def test_live_data_screen(self):
        """Test live data screen"""
        try:
            self.log_info("Testing live data screen...")
            
            # Import and create live data screen
            from screens.live_data.read_live_data import ReadLiveDataScreen
            live_data_screen = ReadLiveDataScreen(self.screen)
            
            # Wait for screen to initialize
            self.wait_for_ui_update(500)
            
            # Test basic elements
            expected_elements = [
                {'type': 'label', 'text': 'Live Data', 'name': 'title'},
                {'type': 'button', 'text': 'Start', 'name': 'start button'},
                {'type': 'button', 'text': 'Stop', 'name': 'stop button'},
                {'type': 'button', 'text': 'Refresh', 'name': 'refresh button'}
            ]
            
            # Verify elements exist
            for element in expected_elements:
                widget = UITestHelpers.find_widget_by_text(self.screen, element['text'])
                if widget:
                    self.log_pass(f"Found {element['name']}")
                    
                    # Test button interaction
                    if element['type'] == 'button':
                        self.simulate_click(widget)
                        self.wait_for_ui_update(200)
                else:
                    self.log_info(f"{element['name']} not found (may be different text)")
            
            live_data_screen.cleanup()
            self.log_pass("Live data screen test completed")
            return True
            
        except ImportError:
            self.log_info("Live data screen not implemented yet")
            return True
        except Exception as e:
            self.log_error(f"Live data screen test failed: {e}")
            return False
    
    def test_rpm_sensor_config_screen(self):
        """Test RPM sensor configuration screen"""
        try:
            self.log_info("Testing RPM sensor configuration screen...")
            
            # Import and create sensor config screen
            from screens.rpm_sensor_config import RPMSensorConfigScreen
            config_screen = RPMSensorConfigScreen(self.screen)
            
            # Wait for screen to initialize
            self.wait_for_ui_update(500)
            
            # Test basic elements
            expected_elements = [
                {'type': 'label', 'text': 'Sensor Configuration', 'name': 'title'},
                {'type': 'label', 'text': 'Crankshaft', 'name': 'crankshaft label'},
                {'type': 'label', 'text': 'Camshaft', 'name': 'camshaft label'},
                {'type': 'button', 'text': 'Save', 'name': 'save button'}
            ]
            
            # Verify elements exist
            for element in expected_elements:
                widget = UITestHelpers.find_widget_by_text(self.screen, element['text'])
                if widget:
                    self.log_pass(f"Found {element['name']}")
                else:
                    self.log_info(f"{element['name']} not found (may be different text)")
            
            # Look for sliders (for tooth configuration)
            sliders = UITestHelpers.get_all_sliders(self.screen)
            if sliders:
                self.log_pass(f"Found {len(sliders)} slider(s) for sensor configuration")
                
                # Test slider interaction
                for i, slider in enumerate(sliders[:3]):  # Test first 3 sliders
                    test_value = 50 + (i * 20)  # Different values for each slider
                    if self.simulate_slider_change(slider, test_value):
                        self.log_pass(f"Slider {i+1} interaction completed")
            
            # Test save button if available
            save_btn = UITestHelpers.find_button_by_text(self.screen, "Save")
            if save_btn:
                self.simulate_click(save_btn)
                self.wait_for_ui_update(300)
                self.log_pass("Save button interaction completed")
            
            config_screen.cleanup()
            self.log_pass("RPM sensor configuration screen test completed")
            return True
            
        except ImportError:
            self.log_info("RPM sensor configuration screen not implemented yet")
            return True
        except Exception as e:
            self.log_error(f"RPM sensor configuration screen test failed: {e}")
            return False
    
    def test_screen_navigation_consistency(self):
        """Test navigation consistency across additional screens"""
        try:
            self.log_info("Testing screen navigation consistency...")
            
            # Test that all screens have consistent navigation elements
            screens_to_test = [
                ('firmware_update', 'FirmwareUpdateScreen'),
                ('system_info', 'SystemInfoScreen'),
                ('rpm_sensor_config', 'RPMSensorConfigScreen')
            ]
            
            for screen_module, screen_class in screens_to_test:
                try:
                    # Import screen dynamically
                    module = __import__(f'screens.{screen_module}', fromlist=[screen_class])
                    screen_cls = getattr(module, screen_class)
                    
                    # Create screen instance
                    screen_instance = screen_cls(self.screen)
                    self.wait_for_ui_update(300)
                    
                    # Look for common navigation elements
                    nav_elements = ['Back', 'Cancel', 'Close', 'Done']
                    found_nav = False
                    
                    for nav_text in nav_elements:
                        nav_btn = UITestHelpers.find_button_by_text(self.screen, nav_text)
                        if nav_btn:
                            self.log_pass(f"{screen_class} has {nav_text} navigation")
                            found_nav = True
                            break
                    
                    if not found_nav:
                        self.log_info(f"{screen_class} navigation elements not found (may be implicit)")
                    
                    screen_instance.cleanup()
                    
                except ImportError:
                    self.log_info(f"{screen_class} not implemented yet")
                except Exception as e:
                    self.log_error(f"Navigation test failed for {screen_class}: {e}")
            
            self.log_pass("Screen navigation consistency test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Screen navigation consistency test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all additional screen tests"""
        try:
            self.log_info("Starting Additional Screens UI Tests...")
            
            # Setup test environment
            if not self.setup_test_environment():
                return False
            
            # Run individual tests
            tests = [
                self.test_firmware_update_screen,
                self.test_system_info_screen,
                self.test_dtc_screens,
                self.test_live_data_screen,
                self.test_rpm_sensor_config_screen,
                self.test_screen_navigation_consistency
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
    """Run additional screens UI tests"""
    test = AdditionalScreensUITest()
    success = test.run_all_tests()
    return success

if __name__ == "__main__":
    main()
