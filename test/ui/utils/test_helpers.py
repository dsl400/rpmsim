#!/usr/bin/env python3
"""
Test Helper Functions for UI Testing
Common utilities and helper functions for UI tests
"""

import utime as time
import usys as sys
import lvgl as lv

# Add src directory to path for imports
sys.path.append('src')

class UITestHelpers:
    """Collection of helper functions for UI testing"""
    
    @staticmethod
    def find_widget_by_text(parent, text, widget_type=None):
        """Find widget by text content"""
        try:
            def search_children(obj):
                # Check current object
                if hasattr(obj, 'get_text'):
                    try:
                        if obj.get_text() == text:
                            if widget_type is None or isinstance(obj, widget_type):
                                return obj
                    except:
                        pass
                
                # Search children
                child_count = obj.get_child_cnt()
                for i in range(child_count):
                    child = obj.get_child(i)
                    result = search_children(child)
                    if result:
                        return result
                return None
            
            return search_children(parent)
            
        except Exception as e:
            print(f"Widget search failed: {e}")
            return None
    
    @staticmethod
    def find_button_by_text(parent, text):
        """Find button widget by text"""
        return UITestHelpers.find_widget_by_text(parent, text, lv.button)
    
    @staticmethod
    def find_label_by_text(parent, text):
        """Find label widget by text"""
        return UITestHelpers.find_widget_by_text(parent, text, lv.label)
    
    @staticmethod
    def get_all_buttons(parent):
        """Get all button widgets in parent"""
        buttons = []
        try:
            def search_buttons(obj):
                if isinstance(obj, lv.button):
                    buttons.append(obj)

                child_count = obj.get_child_cnt()
                for i in range(child_count):
                    child = obj.get_child(i)
                    search_buttons(child)

            search_buttons(parent)
            return buttons

        except Exception as e:
            print(f"Button search failed: {e}")
            return []
    
    @staticmethod
    def get_all_sliders(parent):
        """Get all slider widgets in parent"""
        sliders = []
        try:
            def search_sliders(obj):
                if isinstance(obj, lv.slider):
                    sliders.append(obj)
                
                child_count = obj.get_child_cnt()
                for i in range(child_count):
                    child = obj.get_child(i)
                    search_sliders(child)
            
            search_sliders(parent)
            return sliders
            
        except Exception as e:
            print(f"Slider search failed: {e}")
            return []
    
    @staticmethod
    def wait_for_screen_load(screen, timeout_ms=5000):
        """Wait for screen to fully load"""
        try:
            start_time = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
                lv.task_handler()
                time.sleep_ms(50)
                
                # Check if screen has content
                if screen.get_child_cnt() > 0:
                    return True
            
            return False
            
        except Exception as e:
            print(f"Screen load wait failed: {e}")
            return False
    
    @staticmethod
    def simulate_navigation_flow(test_instance, steps):
        """
        Simulate a complete navigation flow
        steps: list of dicts with 'action', 'target', 'verify' keys
        """
        try:
            for i, step in enumerate(steps):
                test_instance.log_info(f"Step {i+1}: {step.get('description', 'Navigation step')}")
                
                action = step.get('action')
                target = step.get('target')
                verify = step.get('verify')
                
                if action == 'click':
                    if not test_instance.simulate_click(target):
                        test_instance.log_fail(f"Step {i+1}: Click failed")
                        return False
                
                elif action == 'slider':
                    value = step.get('value', 0)
                    if not test_instance.simulate_slider_change(target, value):
                        test_instance.log_fail(f"Step {i+1}: Slider change failed")
                        return False
                
                elif action == 'wait':
                    duration = step.get('duration', 1000)
                    test_instance.wait_for_ui_update(duration)
                
                # Verify step if specified
                if verify:
                    verify_type = verify.get('type')
                    verify_target = verify.get('target')
                    
                    if verify_type == 'visible':
                        if not test_instance.verify_widget_visible(verify_target, verify.get('name', 'widget')):
                            test_instance.log_fail(f"Step {i+1}: Visibility verification failed")
                            return False
                    
                    elif verify_type == 'text':
                        expected_text = verify.get('text')
                        if not test_instance.verify_widget_text(verify_target, expected_text, verify.get('name', 'widget')):
                            test_instance.log_fail(f"Step {i+1}: Text verification failed")
                            return False
                    
                    elif verify_type == 'state':
                        expected_state = verify.get('state')
                        if not test_instance.verify_widget_state(verify_target, expected_state, verify.get('name', 'widget')):
                            test_instance.log_fail(f"Step {i+1}: State verification failed")
                            return False
            
            test_instance.log_pass("Navigation flow completed successfully")
            return True
            
        except Exception as e:
            test_instance.log_error(f"Navigation flow failed: {e}")
            return False
    
    @staticmethod
    def create_mock_app_state():
        """Create mock app state for testing"""
        try:
            from utils.navigation_manager import AppState
            from utils.data_manager import DataManager
            from utils.error_handler import ErrorHandler
            
            # Create mock instances
            app_state = AppState()
            app_state.data_manager = DataManager()
            app_state.error_handler = ErrorHandler()
            
            # Set default test data
            app_state.current_system = {
                'brand': 'VW',
                'system': 'Engine',
                'system_name': 'Bosch ME7.9.7'
            }
            app_state.current_tool = 'RPM Simulator'
            
            return app_state
            
        except Exception as e:
            print(f"Mock app state creation failed: {e}")
            return None
    
    @staticmethod
    def verify_screen_elements(test_instance, screen, expected_elements):
        """
        Verify that expected UI elements exist on screen
        expected_elements: list of dicts with 'type', 'text', 'name' keys
        """
        try:
            all_found = True
            
            for element in expected_elements:
                element_type = element.get('type')
                element_text = element.get('text')
                element_name = element.get('name', f"{element_type} with text '{element_text}'")
                
                if element_type == 'button':
                    widget = UITestHelpers.find_button_by_text(screen, element_text)
                elif element_type == 'label':
                    widget = UITestHelpers.find_label_by_text(screen, element_text)
                else:
                    widget = UITestHelpers.find_widget_by_text(screen, element_text)
                
                if widget:
                    test_instance.log_pass(f"Found {element_name}")
                else:
                    test_instance.log_fail(f"Missing {element_name}")
                    all_found = False
            
            return all_found
            
        except Exception as e:
            test_instance.log_error(f"Screen element verification failed: {e}")
            return False
    
    @staticmethod
    def measure_performance(test_instance, operation_name, operation_func):
        """Measure performance of an operation"""
        try:
            start_time = time.ticks_ms()
            result = operation_func()
            end_time = time.ticks_ms()
            
            duration = time.ticks_diff(end_time, start_time)
            test_instance.log_info(f"{operation_name} took {duration}ms")
            
            return result, duration
            
        except Exception as e:
            test_instance.log_error(f"Performance measurement failed for {operation_name}: {e}")
            return None, -1
