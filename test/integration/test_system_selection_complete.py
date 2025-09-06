#!/usr/bin/env python3
"""
Complete System Selection Test
Tests all system selection functionality including navigation and interaction
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

def test_system_selection_complete():
    """Complete test of system selection functionality"""
    print("==================================================")
    print("COMPLETE SYSTEM SELECTION TEST")
    print("==================================================")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Create display
        display = lv.sdl_window_create(800, 480)
        lv.sdl_window_set_title(display, "Complete System Selection Test")
        
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
        
        # Test 1: Navigation to System Selection
        print("\n1. Testing Navigation to System Selection...")
        try:
            result = nav_manager.navigate_to("system_selection")
            if result:
                print("✓ Navigation to system selection successful")
            else:
                print("✗ Navigation to system selection failed")
                return False
        except Exception as e:
            print(f"✗ Navigation failed: {e}")
            return False
        
        # Test 2: System Selection Screen Functionality
        print("\n2. Testing System Selection Screen Functionality...")
        try:
            current_screen = nav_manager.current_screen
            if current_screen and hasattr(current_screen, 'widgets'):
                print("✓ System selection screen loaded")
                
                # Test widget existence
                required_widgets = ['left_container', 'right_container', 'system_list', 
                                  'search_display', 'keyboard', 'close_btn']
                
                for widget in required_widgets:
                    if widget in current_screen.widgets:
                        print(f"✓ Widget {widget} exists")
                    else:
                        print(f"✗ Widget {widget} missing")
                        return False
                        
            else:
                print("✗ System selection screen not properly loaded")
                return False
        except Exception as e:
            print(f"✗ Screen functionality test failed: {e}")
            return False
        
        # Test 3: Brand Display
        print("\n3. Testing Brand Display...")
        try:
            brands = app_state.data_manager.get_brands()
            if brands and len(brands) > 0:
                print(f"✓ Found {len(brands)} brands: {brands}")
                
                # Test brand selection
                test_brand = brands[0]
                current_screen.on_brand_select(None, test_brand)
                
                if current_screen.selected_brand == test_brand:
                    print(f"✓ Brand selection working: {test_brand}")
                else:
                    print("✗ Brand selection not working")
                    return False
                    
            else:
                print("✗ No brands found")
                return False
        except Exception as e:
            print(f"✗ Brand display test failed: {e}")
            return False
        
        # Test 4: System Data for Brand
        print("\n4. Testing System Data for Brand...")
        try:
            systems = app_state.data_manager.get_systems_for_brand(test_brand)
            if systems and len(systems) > 0:
                print(f"✓ Found {len(systems)} systems for {test_brand}")
                
                # Test system selection
                test_system = systems[0]
                current_screen.on_system_select(None, test_system)
                
                if hasattr(app_state, 'current_system') and app_state.current_system:
                    print(f"✓ System selection working: {app_state.current_system}")
                else:
                    print("✗ System selection not working")
                    return False
                    
            else:
                print(f"✗ No systems found for {test_brand}")
                return False
        except Exception as e:
            print(f"✗ System data test failed: {e}")
            return False
        
        # Test 5: Search Functionality
        print("\n5. Testing Search Functionality...")
        try:
            # Test search text change
            current_screen.search_text = "engine"
            current_screen.is_searching = True
            current_screen.update_list_display()
            
            print(f"✓ Search text set: '{current_screen.search_text}'")
            print(f"✓ Search mode: {current_screen.is_searching}")
            
            # Test clear search
            current_screen.on_clear_search(None)
            
            if current_screen.search_text == "" and not current_screen.is_searching:
                print("✓ Clear search working")
            else:
                print("✗ Clear search not working")
                return False
                
        except Exception as e:
            print(f"✗ Search functionality test failed: {e}")
            return False
        
        # Test 6: Close Button Functionality
        print("\n6. Testing Close Button Functionality...")
        try:
            # Test close button click
            current_screen.on_close_click(None)
            
            # Check if we navigated back to main
            current_screen_name = nav_manager.get_current_screen_name()
            if current_screen_name == "MainScreen":
                print("✓ Close button navigation working")
            else:
                print(f"✗ Close button navigation failed - current screen: {current_screen_name}")
                return False
                
        except Exception as e:
            print(f"✗ Close button test failed: {e}")
            return False
        
        # Test 7: Full Workflow Test
        print("\n7. Testing Full Workflow...")
        try:
            # Navigate back to system selection
            nav_manager.navigate_to("system_selection")
            current_screen = nav_manager.current_screen
            
            # Select a brand
            brands = app_state.data_manager.get_brands()
            test_brand = brands[0]
            current_screen.on_brand_select(None, test_brand)
            
            # Get systems for the brand
            systems = app_state.data_manager.get_systems_for_brand(test_brand)
            if systems:
                test_system = systems[0]
                
                # Select a system
                current_screen.on_system_select(None, test_system)
                
                # Check if app state was updated
                if (hasattr(app_state, 'current_system') and 
                    app_state.current_system and
                    app_state.current_system['brand'] == test_system['brand']):
                    print("✓ Full workflow working")
                else:
                    print("✗ Full workflow failed - app state not updated")
                    return False
            else:
                print("✗ No systems available for workflow test")
                return False
                
        except Exception as e:
            print(f"✗ Full workflow test failed: {e}")
            return False
        
        print("\n✓ Complete System Selection test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Complete System Selection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_system_selection_complete()
    if success:
        print("\n🎉 COMPLETE SYSTEM SELECTION TEST PASSED!")
        print("\n✅ All functionality working:")
        print("   ✅ Navigation to/from system selection")
        print("   ✅ Screen layout and widgets")
        print("   ✅ Brand display and selection")
        print("   ✅ System data and selection")
        print("   ✅ Search functionality")
        print("   ✅ Close button navigation")
        print("   ✅ Full workflow integration")
        print("\n🚀 System selection is fully functional!")
    else:
        print("\n❌ COMPLETE SYSTEM SELECTION TEST FAILED!")
        print("🔧 System selection needs additional fixes")
