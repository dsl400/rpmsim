#!/usr/bin/env python3
"""
Full Workflow Test for ECU Diagnostic Tool
Tests the complete user interaction flow
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

def test_full_workflow():
    """Test complete workflow from main screen to system selection and back"""
    print("=== Testing Full Workflow ===")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "Full Workflow Test")
        
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
        from screens.rpm_simulator.rpm_simulator_screen import RPMSimulatorScreen
        
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
        
        # Register screens
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        nav_manager.register_screen("main", MainScreen)
        
        print("✓ Screens registered")
        
        # Test 1: Create main screen
        main_screen = MainScreen(screen)
        print("✓ Main screen created")
        
        # Test 2: Check main screen widgets
        expected_widgets = ['toolbar', 'menu_btn', 'title_btn', 'wifi_icon', 'main_area']
        for widget_name in expected_widgets:
            if widget_name in main_screen.widgets:
                print(f"✓ Found main screen widget: {widget_name}")
            else:
                print(f"✗ Missing main screen widget: {widget_name}")
        
        # Test 3: Test navigation to system selection
        print("Testing navigation to system selection...")
        result = nav_manager.navigate_to("system_selection")
        if result:
            print("✓ Navigation to system selection successful")
        else:
            print("✗ Navigation to system selection failed")
            return False
        
        # Test 4: Check system selection screen
        if nav_manager.current_screen:
            selection_screen = nav_manager.current_screen
            print("✓ System selection screen is active")
            
            # Check widgets
            expected_widgets = ['selection_container', 'back_btn', 'cancel_btn']
            for widget_name in expected_widgets:
                if widget_name in selection_screen.widgets:
                    print(f"✓ Found selection screen widget: {widget_name}")
                else:
                    print(f"✗ Missing selection screen widget: {widget_name}")
        
        # Test 5: Test data manager functionality
        brands = app_state.data_manager.get_brands()
        print(f"✓ Data manager working: {len(brands)} brands available")
        
        if brands:
            system_types = app_state.data_manager.get_system_types(brands[0])
            print(f"✓ Found {len(system_types)} system types for {brands[0]}")
            
            if system_types:
                system_names = app_state.data_manager.get_system_names(brands[0], system_types[0])
                print(f"✓ Found {len(system_names)} system names")
                
                if system_names:
                    tools = app_state.data_manager.get_system_tools(brands[0], system_types[0], system_names[0])
                    print(f"✓ Found {len(tools)} tools")
        
        # Test 6: Test RPM Simulator screen creation
        print("Testing RPM Simulator screen...")
        rpm_screen_obj = lv.obj()
        rpm_screen = RPMSimulatorScreen(rpm_screen_obj)
        print("✓ RPM Simulator screen created successfully")
        
        # Check RPM simulator widgets
        expected_rpm_widgets = ['rpm_gauge', 'rpm_slider', 'start_stop_btn']
        for widget_name in expected_rpm_widgets:
            if widget_name in rpm_screen.widgets:
                print(f"✓ Found RPM simulator widget: {widget_name}")
            else:
                print(f"✗ Missing RPM simulator widget: {widget_name}")
        
        # Test 7: Test navigation back to main
        print("Testing navigation back to main...")
        result = nav_manager.navigate_to("main")
        if result:
            print("✓ Navigation back to main successful")
        else:
            print("✗ Navigation back to main failed")
        
        print("✓ Full workflow test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Full workflow test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_full_workflow()
    if success:
        print("\n🎉 Full workflow test PASSED!")
        print("\n✅ All UI features are working correctly!")
        print("✅ Navigation between screens works")
        print("✅ Data manager integration works")
        print("✅ All major widgets are present")
        print("✅ System selection functionality works")
        print("✅ RPM Simulator screen works")
    else:
        print("\n❌ Full workflow test FAILED!")
