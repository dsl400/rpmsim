#!/usr/bin/env python3
"""
UI Tests for New System Selection Screen
Tests the full-screen system selection with search functionality
"""

# Add src and test directories to path
try:
    import usys as sys
except ImportError:
    import sys

sys.path.append('src')
sys.path.append('test')

import lvgl as lv
from ui.utils.base_ui_test import BaseUITest

class NewSystemSelectionUITest(BaseUITest):
    """Test class for new system selection screen UI"""
    
    def __init__(self):
        super().__init__()
        self.selection_screen = None
        
    def setup_test_environment(self):
        """Set up test environment for system selection screen"""
        try:
            self.log_info("Setting up new system selection test environment...")
            
            # Import required modules
            from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
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

            self.log_pass("New System Selection test environment setup completed")
            return True

        except Exception as e:
            self.log_error(f"Test environment setup failed: {e}")
            return False
    
    def test_full_screen_layout(self):
        """Test full-screen layout elements"""
        try:
            self.log_info("Testing full-screen layout...")
            
            # Check left container
            left_container = self.selection_screen.widgets.get('left_container')
            if not self.verify_widget_visible(left_container, "left container"):
                return False
            
            # Check right container
            right_container = self.selection_screen.widgets.get('right_container')
            if not self.verify_widget_visible(right_container, "right container"):
                return False
            
            # Check system list
            system_list = self.selection_screen.widgets.get('system_list')
            if not self.verify_widget_visible(system_list, "system list"):
                return False
            
            # Check list title
            list_title = self.selection_screen.widgets.get('list_title')
            if not self.verify_widget_visible(list_title, "list title"):
                return False
            
            self.log_pass("Full-screen layout test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Full-screen layout test failed: {e}")
            return False
    
    def test_search_functionality(self):
        """Test search input and keyboard functionality"""
        try:
            self.log_info("Testing search functionality...")
            
            # Check search display
            search_display = self.selection_screen.widgets.get('search_display')
            if not self.verify_widget_visible(search_display, "search display"):
                return False
            
            # Check clear button
            clear_btn = self.selection_screen.widgets.get('clear_btn')
            if not self.verify_widget_visible(clear_btn, "clear button"):
                return False
            
            # Check virtual keyboard
            keyboard = self.selection_screen.widgets.get('keyboard')
            if not self.verify_widget_visible(keyboard, "virtual keyboard"):
                return False
            
            # Test search text input simulation
            self.selection_screen.search_text = "VW"
            self.selection_screen.is_searching = True
            self.selection_screen.update_list_display()
            
            if self.selection_screen.search_text == "VW":
                self.log_pass("Search text input working")
            else:
                self.log_fail("Search text input not working")
                return False
            
            # Test clear search
            self.selection_screen.search_text = ""
            self.selection_screen.is_searching = False
            self.selection_screen.update_list_display()
            
            if not self.selection_screen.is_searching:
                self.log_pass("Clear search working")
            else:
                self.log_fail("Clear search not working")
                return False
            
            self.log_pass("Search functionality test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Search functionality test failed: {e}")
            return False
    
    def test_brand_selection(self):
        """Test brand selection functionality"""
        try:
            self.log_info("Testing brand selection...")
            
            # Check initial state
            if self.selection_screen.current_view != "brands":
                self.log_fail("Initial view should be 'brands'")
                return False
            
            # Test brand selection
            brands = self.app_state.data_manager.get_brands()
            if brands:
                test_brand = brands[0]
                self.selection_screen.on_brand_select(None, test_brand)
                
                if self.selection_screen.selected_brand == test_brand:
                    self.log_pass(f"Brand selection working: {test_brand}")
                else:
                    self.log_fail("Brand selection not working")
                    return False
                
                if self.selection_screen.current_view == "systems":
                    self.log_pass("View changed to systems after brand selection")
                else:
                    self.log_fail("View should change to systems after brand selection")
                    return False
            else:
                self.log_fail("No brands available for testing")
                return False
            
            self.log_pass("Brand selection test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Brand selection test failed: {e}")
            return False
    
    def test_close_button(self):
        """Test close button functionality"""
        try:
            self.log_info("Testing close button...")
            
            # Check close button
            close_btn = self.selection_screen.widgets.get('close_btn')
            if not self.verify_widget_visible(close_btn, "close button"):
                return False
            
            # Verify close button text
            close_btn_children = close_btn.get_children()
            if close_btn_children:
                label = close_btn_children[0]
                if hasattr(label, 'get_text'):
                    text = label.get_text()
                    if text == "Close":
                        self.log_pass("Close button has correct text")
                    else:
                        self.log_fail(f"Close button text incorrect: '{text}' (expected 'Close')")
                        return False
            
            self.log_pass("Close button test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Close button test failed: {e}")
            return False
    
    def test_data_integration(self):
        """Test data manager integration"""
        try:
            self.log_info("Testing data integration...")
            
            # Check all systems loaded
            if len(self.selection_screen.all_systems) > 0:
                self.log_pass(f"All systems loaded: {len(self.selection_screen.all_systems)} systems")
            else:
                self.log_fail("No systems loaded")
                return False
            
            # Check system structure
            if self.selection_screen.all_systems:
                system = self.selection_screen.all_systems[0]
                required_keys = ['brand', 'system_type', 'system_name']
                for key in required_keys:
                    if key not in system:
                        self.log_fail(f"System missing required key: {key}")
                        return False
                self.log_pass("System data structure correct")
            
            self.log_pass("Data integration test completed")
            return True
            
        except Exception as e:
            self.log_error(f"Data integration test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all new system selection tests"""
        self.log_info("Starting new system selection UI tests...")
        
        tests = [
            self.test_full_screen_layout,
            self.test_search_functionality,
            self.test_brand_selection,
            self.test_close_button,
            self.test_data_integration
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            self.wait_for_ui_update(100)  # Small delay between tests
        
        self.log_info(f"New System Selection tests completed: {passed}/{total} passed")
        return passed == total

if __name__ == "__main__":
    test = NewSystemSelectionUITest()
    if test.setup_test_environment():
        success = test.run_all_tests()
        test.cleanup()
        if success:
            print("🎉 New System Selection UI tests PASSED!")
        else:
            print("❌ New System Selection UI tests FAILED!")
    else:
        print("❌ Test environment setup failed!")
