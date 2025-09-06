#!/usr/bin/env python3
"""
System Selection Debug Test
Diagnoses specific issues with system selection functionality
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

def test_system_selection_debug():
    """Debug system selection issues"""
    print("==================================================")
    print("SYSTEM SELECTION DEBUG TEST")
    print("==================================================")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "System Selection Debug")
        
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
        from screens.main_screen import MainScreen
        
        print("✓ All modules imported successfully")
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        print("✓ App state initialized")
        
        # Register screens
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        nav_manager.register_screen("main", MainScreen)
        
        print("✓ Screens registered")
        
        # Test 1: Create System Selection Screen
        print("\n1. Testing System Selection Screen Creation...")
        try:
            selection_screen = SystemSelectionScreen(screen)
            print("✓ System selection screen created successfully")
        except Exception as e:
            print(f"✗ Failed to create system selection screen: {e}")
            return False
        
        # Test 2: Check Required Widgets
        print("\n2. Testing Required Widgets...")
        required_widgets = ['left_container', 'right_container', 'system_list', 
                          'search_display', 'keyboard', 'close_btn', 'clear_btn', 'list_title']
        
        missing_widgets = []
        for widget in required_widgets:
            if widget in selection_screen.widgets:
                print(f"✓ Found {widget}")
            else:
                print(f"✗ Missing {widget}")
                missing_widgets.append(widget)
        
        if missing_widgets:
            print(f"✗ Missing widgets: {missing_widgets}")
            return False
        
        # Test 3: Check Event Handlers
        print("\n3. Testing Event Handlers...")
        
        # Check if methods exist
        required_methods = ['on_brand_select', 'on_system_select', 'on_close_click', 
                          'on_clear_search', 'on_search_text_change', 'navigate_to_main']
        
        missing_methods = []
        for method in required_methods:
            if hasattr(selection_screen, method):
                print(f"✓ Found method {method}")
            else:
                print(f"✗ Missing method {method}")
                missing_methods.append(method)
        
        if missing_methods:
            print(f"✗ Missing methods: {missing_methods}")
            return False
        
        # Test 4: Test Close Button Functionality
        print("\n4. Testing Close Button Functionality...")
        try:
            # Simulate close button click
            close_btn = selection_screen.widgets['close_btn']
            print(f"✓ Close button exists: {close_btn}")
            
            # Test navigate_to_main method
            selection_screen.navigate_to_main()
            print("✓ Navigate to main method executed successfully")
            
        except Exception as e:
            print(f"✗ Close button functionality failed: {e}")
            return False
        
        # Test 5: Test Brand Selection
        print("\n5. Testing Brand Selection...")
        try:
            brands = app_state.data_manager.get_brands()
            if brands:
                test_brand = brands[0]
                print(f"✓ Testing with brand: {test_brand}")
                
                # Test brand selection method
                selection_screen.on_brand_select(None, test_brand)
                print(f"✓ Brand selection method executed: {selection_screen.selected_brand}")
                
            else:
                print("✗ No brands available for testing")
                return False
                
        except Exception as e:
            print(f"✗ Brand selection failed: {e}")
            return False
        
        # Test 6: Test Search Functionality
        print("\n6. Testing Search Functionality...")
        try:
            # Test search text change
            selection_screen.search_text = "test"
            selection_screen.on_search_text_change(None)
            print(f"✓ Search text change: {selection_screen.search_text}")
            
            # Test clear search
            selection_screen.on_clear_search(None)
            print(f"✓ Clear search: {selection_screen.search_text}")
            
        except Exception as e:
            print(f"✗ Search functionality failed: {e}")
            return False
        
        # Test 7: Test System Data
        print("\n7. Testing System Data...")
        try:
            systems = app_state.data_manager.get_systems_for_brand(brands[0])
            if systems:
                print(f"✓ Found {len(systems)} systems for {brands[0]}")
                
                # Test system selection
                test_system = systems[0]
                system_data = {
                    'brand': brands[0],
                    'system': test_system['system'],
                    'system_name': test_system['system_name']
                }
                
                selection_screen.on_system_select(None, system_data)
                print("✓ System selection method executed")
                
            else:
                print(f"✗ No systems found for {brands[0]}")
                
        except Exception as e:
            print(f"✗ System data test failed: {e}")
            return False
        
        print("\n✓ System Selection debug test completed!")
        return True
        
    except Exception as e:
        print(f"✗ System Selection debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_selection_debug()
    if success:
        print("\n🎉 SYSTEM SELECTION DEBUG TEST PASSED!")
        print("✅ All components working correctly")
    else:
        print("\n❌ SYSTEM SELECTION DEBUG TEST FAILED!")
        print("🔧 Issues found that need fixing")
