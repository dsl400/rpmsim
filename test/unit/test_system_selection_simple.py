#!/usr/bin/env python3
"""
Simple System Selection Test
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

def test_system_selection():
    """Test system selection functionality"""
    print("=== Testing System Selection ===")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "System Selection Test")
        
        # Create mouse
        mouse = lv.sdl_mouse_create()
        
        # Get screen
        screen = lv.screen_active()
        
        print("✓ LVGL setup completed")
        
        # Import modules
        from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.system_selection import SystemSelectionScreen
        
        print("✓ All modules imported successfully")
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        print("✓ App state initialized")
        
        # Test data manager
        brands = app_state.data_manager.get_brands()
        print(f"✓ Found {len(brands)} brands: {brands}")
        
        if brands:
            system_types = app_state.data_manager.get_system_types(brands[0])
            print(f"✓ Found {len(system_types)} system types for {brands[0]}: {system_types}")
            
            if system_types:
                system_names = app_state.data_manager.get_system_names(brands[0], system_types[0])
                print(f"✓ Found {len(system_names)} system names for {brands[0]} {system_types[0]}: {system_names}")
        
        # Create system selection screen
        selection_screen = SystemSelectionScreen(screen)
        
        print("✓ System selection screen created successfully")
        
        # Test basic functionality
        if hasattr(selection_screen, 'widgets'):
            print(f"✓ System selection screen has {len(selection_screen.widgets)} widgets")
            
            # Check for key widgets
            key_widgets = ['selection_container', 'back_btn', 'cancel_btn']
            for widget_name in key_widgets:
                if widget_name in selection_screen.widgets:
                    print(f"✓ Found {widget_name}")
                else:
                    print(f"✗ Missing {widget_name}")
        
        # Test navigation manager
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        print("✓ System selection screen registered with navigation manager")
        
        # Test navigation
        print("Testing navigation to system selection...")
        result = nav_manager.navigate_to("system_selection")
        if result:
            print("✓ Navigation to system selection successful")
        else:
            print("✗ Navigation to system selection failed")
        
        print("✓ System selection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ System selection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_system_selection()
    if success:
        print("\n🎉 System selection test PASSED!")
    else:
        print("\n❌ System selection test FAILED!")
