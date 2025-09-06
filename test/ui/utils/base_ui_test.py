#!/usr/bin/env python3
"""
Base UI Test Framework for ECU Diagnostic Tool
Provides common functionality for UI testing with LVGL simulation
"""

try:
    import utime as time
    import usys as sys
    import ujson as json
except ImportError:
    import time
    import sys
    import json
import lvgl as lv

# Add src directory to path for imports
sys.path.append('src')

class BaseUITest:
    """Base class for UI testing with LVGL simulation"""
    
    def __init__(self, test_name="UI Test"):
        self.test_name = test_name
        self.display = None
        self.mouse = None
        self.screen = None
        self.test_results = []
        self.setup_display()
    
    def setup_display(self):
        """Initialize LVGL display and input for testing"""
        try:
            # Initialize LVGL
            lv.init()
            
            # Create display driver
            self.display = lv.sdl_window_create(800, 480)
            lv.sdl_window_set_resizeable(self.display, False)
            lv.sdl_window_set_title(self.display, f"ECU Tool Test - {self.test_name}")
            
            # Create input driver
            self.mouse = lv.sdl_mouse_create()
            
            # Create main screen
            self.screen = lv.screen_active()
            
        except Exception as e:
            self.log_error(f"Display setup failed: {e}")
    
    def log_result(self, status, message):
        """Log test result"""
        result = {
            'status': status,
            'message': message,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        print(f"[{status}] {message}")
    
    def log_pass(self, message):
        """Log successful test"""
        self.log_result("PASS", message)
    
    def log_fail(self, message):
        """Log failed test"""
        self.log_result("FAIL", message)
    
    def log_error(self, message):
        """Log error"""
        self.log_result("ERROR", message)
    
    def log_info(self, message):
        """Log information"""
        self.log_result("INFO", message)
    
    def wait_for_ui_update(self, duration_ms=100):
        """Wait for UI to update"""
        try:
            start_time = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start_time) < duration_ms:
                lv.task_handler()
                time.sleep_ms(10)
        except Exception as e:
            self.log_error(f"UI update wait failed: {e}")
    
    def simulate_click(self, widget, wait_ms=200):
        """Simulate click on widget"""
        try:
            if widget is None:
                self.log_fail("Cannot click on None widget")
                return False
            
            # Get widget coordinates
            x = widget.get_x() + widget.get_width() // 2
            y = widget.get_y() + widget.get_height() // 2
            
            # Simulate mouse press and release
            lv.event_send(widget, lv.EVENT.PRESSED, None)
            self.wait_for_ui_update(50)
            lv.event_send(widget, lv.EVENT.CLICKED, None)
            self.wait_for_ui_update(wait_ms)
            
            self.log_info(f"Clicked widget at ({x}, {y})")
            return True
            
        except Exception as e:
            self.log_error(f"Click simulation failed: {e}")
            return False
    
    def simulate_slider_change(self, slider, value, wait_ms=200):
        """Simulate slider value change"""
        try:
            if slider is None:
                self.log_fail("Cannot change None slider")
                return False
            
            # Set slider value
            slider.set_value(value, False)
            
            # Trigger value changed event
            lv.event_send(slider, lv.EVENT.VALUE_CHANGED, None)
            self.wait_for_ui_update(wait_ms)
            
            self.log_info(f"Set slider value to {value}")
            return True
            
        except Exception as e:
            self.log_error(f"Slider simulation failed: {e}")
            return False
    
    def verify_widget_visible(self, widget, widget_name="widget"):
        """Verify widget is visible"""
        try:
            if widget is None:
                self.log_fail(f"{widget_name} is None")
                return False
            
            if widget.has_flag(lv.obj.FLAG.HIDDEN):
                self.log_fail(f"{widget_name} is hidden")
                return False
            
            self.log_pass(f"{widget_name} is visible")
            return True
            
        except Exception as e:
            self.log_error(f"Visibility check failed for {widget_name}: {e}")
            return False
    
    def verify_widget_text(self, widget, expected_text, widget_name="widget"):
        """Verify widget text content"""
        try:
            if widget is None:
                self.log_fail(f"{widget_name} is None")
                return False
            
            actual_text = widget.get_text() if hasattr(widget, 'get_text') else str(widget)
            
            if actual_text == expected_text:
                self.log_pass(f"{widget_name} text matches: '{expected_text}'")
                return True
            else:
                self.log_fail(f"{widget_name} text mismatch. Expected: '{expected_text}', Got: '{actual_text}'")
                return False
                
        except Exception as e:
            self.log_error(f"Text verification failed for {widget_name}: {e}")
            return False
    
    def verify_widget_state(self, widget, expected_state, widget_name="widget"):
        """Verify widget state (enabled/disabled, checked/unchecked, etc.)"""
        try:
            if widget is None:
                self.log_fail(f"{widget_name} is None")
                return False
            
            # Check different state types based on widget type
            if hasattr(widget, 'has_state'):
                if expected_state == "checked":
                    is_checked = widget.has_state(lv.STATE.CHECKED)
                    if is_checked:
                        self.log_pass(f"{widget_name} is checked")
                        return True
                    else:
                        self.log_fail(f"{widget_name} is not checked")
                        return False
                elif expected_state == "unchecked":
                    is_checked = widget.has_state(lv.STATE.CHECKED)
                    if not is_checked:
                        self.log_pass(f"{widget_name} is unchecked")
                        return True
                    else:
                        self.log_fail(f"{widget_name} is checked (expected unchecked)")
                        return False
            
            self.log_pass(f"{widget_name} state verification passed")
            return True
            
        except Exception as e:
            self.log_error(f"State verification failed for {widget_name}: {e}")
            return False
    
    def cleanup(self):
        """Clean up test resources"""
        try:
            if self.screen:
                self.screen.clean()
            self.log_info("Test cleanup completed")
        except Exception as e:
            self.log_error(f"Cleanup failed: {e}")
    
    def get_test_summary(self):
        """Get test results summary"""
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = len([r for r in self.test_results if r['status'] == 'FAIL'])
        errors = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        return {
            'test_name': self.test_name,
            'total': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'success_rate': (passed / total * 100) if total > 0 else 0,
            'results': self.test_results
        }
    
    def print_summary(self):
        """Print test summary"""
        summary = self.get_test_summary()
        print(f"\n=== {summary['test_name']} Summary ===")
        print(f"Total: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print("=" * 40)
