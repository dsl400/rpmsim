#!/usr/bin/env python3
"""
Main Screen UI Tests for ECU Diagnostic Tool
Tests toolbar functionality, menu interactions, navigation, and tool loading
"""

try:
    import usys as sys
except ImportError:
    import sys

# Add src and test directories to path FIRST
sys.path.append('src')
sys.path.append('test')

try:
    import utime as time
except ImportError:
    import time
import lvgl as lv

from ui.utils.base_ui_test import BaseUITest
from ui.utils.test_helpers import UITestHelpers

# Import required modules for testing
from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
from utils.data_manager import DataManager
from utils.error_handler import ErrorHandler
from screens.main_screen import MainScreen
from screens.system_selection import SystemSelectionScreen

class MainScreenUITest(BaseUITest):
    """Test suite for Main Screen UI functionality"""
    
    def __init__(self):
        super().__init__("Main Screen UI Test")
        self.main_screen = None
        self.app_state = None
        self.nav_manager = None
    
    def setup_test_environment(self):
        """Set up test environment with mock data"""
        try:
            # Use global app_state instance and initialize it
            self.app_state = app_state
            if not hasattr(self.app_state, 'data_manager') or not self.app_state.data_manager:
                self.app_state.data_manager = DataManager()
            if not hasattr(self.app_state, 'error_handler') or not self.app_state.error_handler:
                self.app_state.error_handler = ErrorHandler()

            # Set default system for testing
            self.app_state.current_system = {
                'brand': 'VW',
                'system': 'Engine',
                'system_name': 'Bosch ME7.9.7'
            }
            self.app_state.current_tool = 'RPM Simulator'

            # Use global navigation manager
            self.nav_manager = nav_manager

            # Register system selection screen for navigation testing
            self.nav_manager.register_screen("system_selection", SystemSelectionScreen)

            # Create main screen
            self.main_screen = MainScreen(self.screen)

            self.log_pass("Test environment setup completed")
            return True

        except Exception as e:
            self.log_error(f"Test environment setup failed: {e}")
            return False
    
    def test_toolbar_elements(self):
        """Test that all toolbar elements are present and visible"""
        try:
            self.log_info("Testing toolbar elements...")
            
            # Check if toolbar exists
            toolbar = self.main_screen.widgets.get('toolbar')
            if not self.verify_widget_visible(toolbar, "toolbar"):
                return False
            
            # Check menu button
            menu_btn = self.main_screen.widgets.get('menu_btn')
            if not self.verify_widget_visible(menu_btn, "menu button"):
                return False
            
            # Check title button
            title_btn = self.main_screen.widgets.get('title_btn')
            if not self.verify_widget_visible(title_btn, "title button"):
                return False
            
            # Check WiFi icon
            wifi_icon = self.main_screen.widgets.get('wifi_icon')
            if not self.verify_widget_visible(wifi_icon, "WiFi icon"):
                return False
            
            # Check main area
            main_area = self.main_screen.widgets.get('main_area')
            if not self.verify_widget_visible(main_area, "main area"):
                return False
            
            self.log_pass("All toolbar elements are present and visible")
            return True
            
        except Exception as e:
            self.log_error(f"Toolbar elements test failed: {e}")
            return False
    
    def test_menu_button_interaction(self):
        """Test menu button click and menu display"""
        try:
            self.log_info("Testing menu button interaction...")
            
            menu_btn = self.main_screen.widgets.get('menu_btn')
            if not menu_btn:
                self.log_fail("Menu button not found")
                return False
            
            # Click menu button
            if not self.simulate_click(menu_btn):
                return False
            
            # Wait for menu to appear
            self.wait_for_ui_update(500)
            
            # Check if menu modal appeared
            if self.main_screen.menu_modal:
                self.log_pass("Menu modal appeared after click")
                
                # Look for menu items
                update_btn = UITestHelpers.find_button_by_text(self.main_screen.menu_modal, "Check for Updates")
                if update_btn:
                    self.log_pass("Found 'Check for Updates' menu item")
                else:
                    self.log_fail("'Check for Updates' menu item not found")
                
                # Click outside to close menu
                if not self.simulate_click(self.main_screen.menu_modal):
                    return False
                
                self.wait_for_ui_update(300)
                
                # Verify menu closed
                if not self.main_screen.menu_modal:
                    self.log_pass("Menu closed after clicking outside")
                else:
                    self.log_fail("Menu did not close after clicking outside")
                
                return True
            else:
                self.log_fail("Menu modal did not appear")
                return False
                
        except Exception as e:
            self.log_error(f"Menu button interaction test failed: {e}")
            return False
    
    def test_title_button_interaction(self):
        """Test title button click for system selection"""
        try:
            self.log_info("Testing title button interaction...")
            
            title_btn = self.main_screen.widgets.get('title_btn')
            if not title_btn:
                self.log_fail("Title button not found")
                return False
            
            # Verify title text shows current system
            title_label = self.main_screen.widgets.get('title_label')
            if title_label:
                title_text = title_label.get_text()
                self.log_info(f"Title text: {title_text}")
                
                # Should contain system information
                if "VW" in title_text or "Bosch" in title_text or "RPM" in title_text:
                    self.log_pass("Title displays system information")
                else:
                    self.log_fail("Title does not display expected system information")
            
            # Click title button (would normally navigate to system selection)
            if not self.simulate_click(title_btn):
                return False
            
            self.log_pass("Title button click simulation completed")
            return True
            
        except Exception as e:
            self.log_error(f"Title button interaction test failed: {e}")
            return False
    
    def test_wifi_status_display(self):
        """Test WiFi status icon and interaction"""
        try:
            self.log_info("Testing WiFi status display...")
            
            wifi_icon = self.main_screen.widgets.get('wifi_icon')
            if not wifi_icon:
                self.log_fail("WiFi icon not found")
                return False
            
            wifi_label = self.main_screen.widgets.get('wifi_label')
            if not wifi_label:
                self.log_fail("WiFi label not found")
                return False
            
            # Check WiFi icon text (should be WiFi symbol)
            wifi_text = wifi_label.get_text()
            if lv.SYMBOL.WIFI in wifi_text:
                self.log_pass("WiFi icon displays WiFi symbol")
            else:
                self.log_fail("WiFi icon does not display WiFi symbol")
            
            # Click WiFi icon
            if not self.simulate_click(wifi_icon):
                return False
            
            self.log_pass("WiFi icon click simulation completed")
            return True
            
        except Exception as e:
            self.log_error(f"WiFi status display test failed: {e}")
            return False
    
    def test_tool_loading(self):
        """Test that the current tool loads in main area"""
        try:
            self.log_info("Testing tool loading...")
            
            main_area = self.main_screen.widgets.get('main_area')
            if not main_area:
                self.log_fail("Main area not found")
                return False
            
            # Wait for tool to load
            self.wait_for_ui_update(1000)
            
            # Check if main area has content (tool loaded)
            if main_area.get_child_cnt() > 0:
                self.log_pass("Tool content loaded in main area")
                
                # If RPM simulator is loaded, check for its elements
                if self.main_screen.current_tool_screen:
                    self.log_pass("Current tool screen instance created")
                    
                    # Look for RPM simulator elements
                    rpm_display = UITestHelpers.find_label_by_text(main_area, "RPM")
                    if rpm_display:
                        self.log_pass("Found RPM display element")
                    
                    sliders = UITestHelpers.get_all_sliders(main_area)
                    if sliders:
                        self.log_pass(f"Found {len(sliders)} slider(s) in tool area")
                    
                    buttons = UITestHelpers.get_all_buttons(main_area)
                    if buttons:
                        self.log_pass(f"Found {len(buttons)} button(s) in tool area")
                
                return True
            else:
                self.log_fail("No tool content loaded in main area")
                return False
                
        except Exception as e:
            self.log_error(f"Tool loading test failed: {e}")
            return False
    
    def test_complete_navigation_flow(self):
        """Test complete navigation flow: menu -> menu item -> back"""
        try:
            self.log_info("Testing complete navigation flow...")
            
            # Define navigation steps
            navigation_steps = [
                {
                    'description': 'Click menu button',
                    'action': 'click',
                    'target': self.main_screen.widgets.get('menu_btn'),
                    'verify': {
                        'type': 'visible',
                        'target': self.main_screen.menu_modal,
                        'name': 'menu modal'
                    }
                },
                {
                    'description': 'Wait for menu to stabilize',
                    'action': 'wait',
                    'duration': 300
                },
                {
                    'description': 'Click outside menu to close',
                    'action': 'click',
                    'target': self.main_screen.menu_modal
                },
                {
                    'description': 'Wait for menu to close',
                    'action': 'wait',
                    'duration': 300
                }
            ]
            
            # Execute navigation flow
            success = UITestHelpers.simulate_navigation_flow(self, navigation_steps)
            
            if success:
                self.log_pass("Complete navigation flow test passed")
            else:
                self.log_fail("Complete navigation flow test failed")
            
            return success
            
        except Exception as e:
            self.log_error(f"Complete navigation flow test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all main screen tests"""
        try:
            self.log_info("Starting Main Screen UI Tests...")
            
            # Setup test environment
            if not self.setup_test_environment():
                return False
            
            # Run individual tests
            tests = [
                self.test_toolbar_elements,
                self.test_menu_button_interaction,
                self.test_title_button_interaction,
                self.test_wifi_status_display,
                self.test_tool_loading,
                self.test_complete_navigation_flow
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
    """Run main screen UI tests"""
    test = MainScreenUITest()
    success = test.run_all_tests()
    return success

if __name__ == "__main__":
    main()
