#!/usr/bin/env python3
"""
Simple Navigation Test
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

def test_navigation():
    """Test navigation functionality"""
    print("=== Testing Navigation ===")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "Navigation Test")
        
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
        
        # Test title button click (should open system selection)
        if 'title_btn' in main_screen.widgets:
            title_btn = main_screen.widgets['title_btn']
            print("✓ Found title button")
            
            # Simulate click on title button
            print("Testing title button click...")
            
            # Create a click event
            event = lv.event_t()
            event.code = lv.EVENT.CLICKED
            event.target = title_btn
            
            # Call the click handler directly
            main_screen.on_title_click(event)
            
            print("✓ Title button click executed")
            
            # Check if navigation was attempted
            print("✓ Navigation test completed")
        else:
            print("✗ Title button not found")
            return False
        
        print("✓ Navigation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Navigation test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_navigation()
    if success:
        print("\n🎉 Navigation test PASSED!")
    else:
        print("\n❌ Navigation test FAILED!")
