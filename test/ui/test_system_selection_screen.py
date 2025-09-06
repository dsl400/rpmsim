#!/usr/bin/env python3
"""
System Selection Screen UI Tests for ECU Diagnostic Tool
Tests 4-step selection process: Brand → System → System Name → Tool
"""

import utime as time
import usys as sys
import lvgl as lv

# Add src and test directories to path
sys.path.append('src')
sys.path.append('test')

from ui.utils.base_ui_test import BaseUITest
from ui.utils.test_helpers import UITestHelpers

class SystemSelectionUITest(BaseUITest):
    """Test suite for System Selection Screen UI functionality"""
    
    def __init__(self):
        super().__init__("System Selection UI Test")
        self.selection_screen = None
        self.app_state = None
    
    def setup_test_environment(self):
        """Set up test environment with system selection screen"""
        try:
            # Import required modules
            from utils.navigation_manager import AppState, app_state
            from utils.data_manager import DataManager
            from utils.error_handler import ErrorHandler
            from screens.system_selection import SystemSelectionScreen

            # Use global app_state instance and initialize it
            self.app_state = app_state
            if not hasattr(self.app_state, 'data_manager') or not self.app_state.data_manager:
                self.app_state.data_manager = DataManager()
            if not hasattr(self.app_state, 'error_handler') or not self.app_state.error_handler:
                self.app_state.error_handler = ErrorHandler()

            # Create system selection screen
            self.selection_screen = SystemSelectionScreen(self.screen)

            # Wait for screen to initialize
            self.wait_for_ui_update(500)

            self.log_pass("System Selection test environment setup completed")
            return True

        except Exception as e:
            self.log_error(f"Test environment setup failed: {e}")
            return False
    
    def test_initial_screen_elements(self):
        """Test initial screen elements (step 1 - brand selection)"""
        try:
            self.log_info("Testing initial screen elements...")
            
            # Check title
            title = self.selection_screen.widgets.get('title')
            if not self.verify_widget_visible(title, "title"):
                return False
            
            if not self.verify_widget_text(title, "Select Vehicle Brand", "title"):
                return False
            
            # Check breadcrumb
            breadcrumb = self.selection_screen.widgets.get('breadcrumb')
            if not self.verify_widget_visible(breadcrumb, "breadcrumb"):
                return False
            
            if not self.verify_widget_text(breadcrumb, "Step 1 of 4: Brand", "breadcrumb"):
                return False
            
            # Check selection container
            selection_container = self.selection_screen.widgets.get('selection_container')
            if not self.verify_widget_visible(selection_container, "selection container"):
                return False
            
            # Check navigation buttons
            back_btn = self.selection_screen.widgets.get('back_btn')
            cancel_btn = self.selection_screen.widgets.get('cancel_btn')
            
            if not self.verify_widget_visible(cancel_btn, "cancel button"):
                return False
            
            # Back button should be hidden on first step
            if back_btn and back_btn.has_flag(lv.obj.FLAG.HIDDEN):
                self.log_pass("Back button is hidden on first step")
            else:
                self.log_fail("Back button should be hidden on first step")
            
            self.log_pass("Initial screen elements test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Initial screen elements test failed: {e}")
            return False
    
    def test_brand_selection_step(self):
        """Test brand selection (step 1)"""
        try:
            self.log_info("Testing brand selection step...")
            
            # Should be on step 0 (brand selection)
            if self.selection_screen.selection_step != 0:
                self.log_fail(f"Expected step 0, got step {self.selection_screen.selection_step}")
                return False
            
            # Look for brand buttons in selection container
            selection_container = self.selection_screen.widgets.get('selection_container')
            brand_buttons = UITestHelpers.get_all_buttons(selection_container)
            
            if len(brand_buttons) > 0:
                self.log_pass(f"Found {len(brand_buttons)} brand selection buttons")
                
                # Click first brand button
                first_brand_btn = brand_buttons[0]
                if not self.simulate_click(first_brand_btn):
                    return False
                
                # Wait for step transition
                self.wait_for_ui_update(500)
                
                # Should now be on step 1 (system selection)
                if self.selection_screen.selection_step == 1:
                    self.log_pass("Advanced to step 1 after brand selection")
                else:
                    self.log_fail(f"Expected step 1, got step {self.selection_screen.selection_step}")
                
                # Check if selected brand is stored
                if self.selection_screen.selected_brand:
                    self.log_pass(f"Brand selected: {self.selection_screen.selected_brand}")
                else:
                    self.log_fail("No brand was selected")
                
                return True
            else:
                self.log_fail("No brand selection buttons found")
                return False
                
        except Exception as e:
            self.log_error(f"Brand selection test failed: {e}")
            return False
    
    def test_system_type_selection_step(self):
        """Test system type selection (step 2)"""
        try:
            self.log_info("Testing system type selection step...")
            
            # Should be on step 1 (system type selection)
            if self.selection_screen.selection_step != 1:
                self.log_fail(f"Expected step 1, got step {self.selection_screen.selection_step}")
                return False
            
            # Check title updated
            title = self.selection_screen.widgets.get('title')
            if not self.verify_widget_text(title, "Select System Type", "title"):
                return False
            
            # Check breadcrumb updated
            breadcrumb = self.selection_screen.widgets.get('breadcrumb')
            breadcrumb_text = breadcrumb.get_text()
            if "Step 2 of 4" in breadcrumb_text:
                self.log_pass("Breadcrumb shows step 2")
            else:
                self.log_fail("Breadcrumb does not show step 2")
            
            # Back button should now be visible
            back_btn = self.selection_screen.widgets.get('back_btn')
            if back_btn and not back_btn.has_flag(lv.obj.FLAG.HIDDEN):
                self.log_pass("Back button is visible on step 2")
            else:
                self.log_fail("Back button should be visible on step 2")
            
            # Look for system type buttons
            selection_container = self.selection_screen.widgets.get('selection_container')
            system_buttons = UITestHelpers.get_all_buttons(selection_container)
            
            if len(system_buttons) > 0:
                self.log_pass(f"Found {len(system_buttons)} system type buttons")
                
                # Click first system type button
                first_system_btn = system_buttons[0]
                if not self.simulate_click(first_system_btn):
                    return False
                
                # Wait for step transition
                self.wait_for_ui_update(500)
                
                # Should now be on step 2 (system name selection)
                if self.selection_screen.selection_step == 2:
                    self.log_pass("Advanced to step 2 after system type selection")
                else:
                    self.log_fail(f"Expected step 2, got step {self.selection_screen.selection_step}")
                
                return True
            else:
                self.log_fail("No system type buttons found")
                return False
                
        except Exception as e:
            self.log_error(f"System type selection test failed: {e}")
            return False
    
    def test_back_navigation(self):
        """Test back button navigation"""
        try:
            self.log_info("Testing back navigation...")
            
            current_step = self.selection_screen.selection_step
            if current_step <= 0:
                self.log_info("Cannot test back navigation from step 0")
                return True
            
            # Click back button
            back_btn = self.selection_screen.widgets.get('back_btn')
            if not back_btn:
                self.log_fail("Back button not found")
                return False
            
            if not self.simulate_click(back_btn):
                return False
            
            # Wait for navigation
            self.wait_for_ui_update(300)
            
            # Should be on previous step
            new_step = self.selection_screen.selection_step
            if new_step == current_step - 1:
                self.log_pass(f"Successfully navigated back from step {current_step} to step {new_step}")
                return True
            else:
                self.log_fail(f"Back navigation failed. Expected step {current_step - 1}, got step {new_step}")
                return False
                
        except Exception as e:
            self.log_error(f"Back navigation test failed: {e}")
            return False
    
    def test_cancel_navigation(self):
        """Test cancel button navigation"""
        try:
            self.log_info("Testing cancel navigation...")
            
            cancel_btn = self.selection_screen.widgets.get('cancel_btn')
            if not cancel_btn:
                self.log_fail("Cancel button not found")
                return False
            
            if not self.simulate_click(cancel_btn):
                return False
            
            self.log_pass("Cancel button click simulation completed")
            return True
            
        except Exception as e:
            self.log_error(f"Cancel navigation test failed: {e}")
            return False
    
    def test_complete_selection_flow(self):
        """Test complete selection flow from brand to tool"""
        try:
            self.log_info("Testing complete selection flow...")
            
            # Reset to beginning
            self.selection_screen.selection_step = 0
            self.selection_screen.selected_brand = None
            self.selection_screen.selected_system = None
            self.selection_screen.selected_system_name = None
            self.selection_screen.selected_tool = None
            self.selection_screen.update_selection_step()
            
            self.wait_for_ui_update(300)
            
            # Step 1: Select brand
            selection_container = self.selection_screen.widgets.get('selection_container')
            brand_buttons = UITestHelpers.get_all_buttons(selection_container)
            
            if len(brand_buttons) > 0:
                self.simulate_click(brand_buttons[0])
                self.wait_for_ui_update(500)
                
                if self.selection_screen.selection_step == 1:
                    self.log_pass("Step 1 completed: Brand selected")
                else:
                    self.log_fail("Step 1 failed: Brand not selected")
                    return False
            else:
                self.log_fail("No brand buttons found for complete flow test")
                return False
            
            # Step 2: Select system type
            system_buttons = UITestHelpers.get_all_buttons(selection_container)
            if len(system_buttons) > 0:
                self.simulate_click(system_buttons[0])
                self.wait_for_ui_update(500)
                
                if self.selection_screen.selection_step == 2:
                    self.log_pass("Step 2 completed: System type selected")
                else:
                    self.log_fail("Step 2 failed: System type not selected")
                    return False
            else:
                self.log_fail("No system type buttons found")
                return False
            
            # Note: Steps 3 and 4 would require actual data from database
            # For now, we test the navigation structure
            
            self.log_pass("Complete selection flow test completed (partial)")
            return True
            
        except Exception as e:
            self.log_error(f"Complete selection flow test failed: {e}")
            return False
    
    def test_breadcrumb_updates(self):
        """Test breadcrumb navigation updates"""
        try:
            self.log_info("Testing breadcrumb updates...")
            
            breadcrumb = self.selection_screen.widgets.get('breadcrumb')
            if not breadcrumb:
                self.log_fail("Breadcrumb not found")
                return False
            
            # Test breadcrumb for different steps
            test_steps = [
                (0, "Step 1 of 4: Brand"),
                (1, "Step 2 of 4"),
                (2, "Step 3 of 4"),
                (3, "Step 4 of 4")
            ]
            
            for step, expected_text in test_steps:
                self.selection_screen.selection_step = step
                self.selection_screen.update_selection_step()
                self.wait_for_ui_update(200)
                
                breadcrumb_text = breadcrumb.get_text()
                if expected_text in breadcrumb_text:
                    self.log_pass(f"Breadcrumb correct for step {step}")
                else:
                    self.log_fail(f"Breadcrumb incorrect for step {step}. Expected: '{expected_text}', Got: '{breadcrumb_text}'")
            
            return True
            
        except Exception as e:
            self.log_error(f"Breadcrumb updates test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all system selection tests"""
        try:
            self.log_info("Starting System Selection UI Tests...")
            
            # Setup test environment
            if not self.setup_test_environment():
                return False
            
            # Run individual tests
            tests = [
                self.test_initial_screen_elements,
                self.test_brand_selection_step,
                self.test_system_type_selection_step,
                self.test_back_navigation,
                self.test_cancel_navigation,
                self.test_breadcrumb_updates,
                self.test_complete_selection_flow
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
    """Run system selection UI tests"""
    test = SystemSelectionUITest()
    success = test.run_all_tests()
    return success

if __name__ == "__main__":
    main()
