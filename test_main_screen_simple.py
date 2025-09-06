#!/usr/bin/env python3
"""
Simple Main Screen Test
"""

try:
    import usys as sys
    import utime as time
except ImportError:
    import sys
    import time

# Add paths
sys.path.append('src')
sys.path.append('test')

import lvgl as lv

def test_main_screen():
    """Test main screen functionality"""
    print("=== Testing Main Screen ===")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "Main Screen Test")
        
        # Create mouse
        mouse = lv.sdl_mouse_create()
        
        # Get screen
        screen = lv.screen_active()
        
        print("✓ LVGL setup completed")
        
        # Import modules
        from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        
        print("✓ All modules imported successfully")
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Set test data
        app_state.current_system = {
            'brand': 'VW',
            'system': 'Engine', 
            'system_name': 'Bosch ME7.9.7'
        }
        app_state.current_tool = 'RPM Simulator'
        
        print("✓ App state initialized")
        
        # Register system selection screen
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        
        # Create main screen
        main_screen = MainScreen(screen)
        
        print("✓ Main screen created successfully")
        
        # Test basic functionality
        if hasattr(main_screen, 'widgets'):
            print(f"✓ Main screen has {len(main_screen.widgets)} widgets")
            
            # Check for key widgets
            key_widgets = ['toolbar', 'menu_btn', 'title_btn', 'wifi_icon']
            for widget_name in key_widgets:
                if widget_name in main_screen.widgets:
                    print(f"✓ Found {widget_name}")
                else:
                    print(f"✗ Missing {widget_name}")
        
        print("✓ Main screen test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Main screen test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_main_screen()
    if success:
        print("\n🎉 Main screen test PASSED!")
    else:
        print("\n❌ Main screen test FAILED!")
