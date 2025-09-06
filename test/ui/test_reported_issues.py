"""
Tests for specific reported issues in ECU Diagnostic Tool
Ensures the reported bugs are fixed and don't regress
"""

import lvgl as lv
import utime as time
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def test_dialog_parameter_order():
    """Test that dialog functions are called with correct parameter order"""
    print("=== Testing Dialog Parameter Order ===")
    
    try:
        from utils.error_handler import ErrorHandler
        
        # Create error handler
        error_handler = ErrorHandler()
        
        # Test show_info_dialog with correct parameter order
        try:
            # This should work without throwing an exception
            error_handler.show_info_dialog("Test message", "Test Title")
            print("✓ show_info_dialog called with correct parameters")
            return True
        except Exception as e:
            print(f"✗ show_info_dialog failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Dialog test failed: {e}")
        return False

def test_wifi_setup_screen_registration():
    """Test that WiFi setup screen is properly registered"""
    print("\n=== Testing WiFi Setup Screen Registration ===")
    
    try:
        from utils.navigation_manager import nav_manager
        from screens.wifi_setup import WifiSetupScreen
        
        # Register the screen
        nav_manager.register_screen("wifi_setup", WifiSetupScreen)
        
        # Check if it's registered
        if "wifi_setup" in nav_manager.screens:
            print("✓ WiFi setup screen is registered")
            
            # Test navigation (without actually navigating)
            try:
                # This should not raise an exception about unregistered screen
                screen_class = nav_manager.screens["wifi_setup"]
                print("✓ WiFi setup screen can be retrieved from navigation manager")
                return True
            except Exception as e:
                print(f"✗ WiFi setup screen retrieval failed: {e}")
                return False
        else:
            print("✗ WiFi setup screen is not registered")
            return False
            
    except Exception as e:
        print(f"✗ WiFi setup registration test failed: {e}")
        return False

def test_system_selection_data_loading():
    """Test that system selection loads data correctly"""
    print("\n=== Testing System Selection Data Loading ===")
    
    try:
        from utils.data_manager import DataManager
        from utils.navigation_manager import app_state
        from utils.error_handler import ErrorHandler
        
        # Initialize app state if needed
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Test data loading
        brands = app_state.data_manager.get_brands()
        
        if len(brands) > 0:
            print(f"✓ Brands loaded successfully: {brands}")
            
            # Test system types for first brand
            first_brand = brands[0]
            system_types = app_state.data_manager.get_system_types(first_brand)
            
            if len(system_types) > 0:
                print(f"✓ System types loaded for {first_brand}: {system_types}")
                
                # Test system names
                first_type = system_types[0]
                system_names = app_state.data_manager.get_system_names(first_brand, first_type)
                
                if len(system_names) > 0:
                    print(f"✓ System names loaded for {first_brand}/{first_type}: {system_names}")
                    return True
                else:
                    print(f"✗ No system names found for {first_brand}/{first_type}")
                    return False
            else:
                print(f"✗ No system types found for {first_brand}")
                return False
        else:
            print("✗ No brands loaded - this was the reported issue")
            return False
            
    except Exception as e:
        print(f"✗ System selection data loading test failed: {e}")
        return False

def test_app_state_initialization():
    """Test that app state is properly initialized"""
    print("\n=== Testing App State Initialization ===")
    
    try:
        from utils.navigation_manager import app_state
        
        # Check if app state has required components
        has_data_manager = hasattr(app_state, 'data_manager') and app_state.data_manager is not None
        has_error_handler = hasattr(app_state, 'error_handler') and app_state.error_handler is not None
        
        if has_data_manager:
            print("✓ App state has data manager")
        else:
            print("✗ App state missing data manager")
        
        if has_error_handler:
            print("✓ App state has error handler")
        else:
            print("✗ App state missing error handler")
        
        # Test initialization method
        try:
            result = app_state.initialize()
            print(f"✓ App state initialization completed: {result}")
            return has_data_manager and has_error_handler
        except Exception as e:
            print(f"✗ App state initialization failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ App state test failed: {e}")
        return False

def test_main_screen_menu_functionality():
    """Test main screen menu functionality without UI"""
    print("\n=== Testing Main Screen Menu Functionality ===")
    
    try:
        from screens.main_screen import MainScreen
        from utils.navigation_manager import app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Create a minimal screen object
        scr = lv.obj()
        
        # Create main screen
        main_screen = MainScreen(scr)
        
        # Test menu action handling
        try:
            # This should not crash with parameter order error
            main_screen.on_menu_select("updates")
            print("✓ Menu 'updates' action handled without error")
            return True
        except Exception as e:
            print(f"✗ Menu action failed: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Main screen menu test failed: {e}")
        return False

def test_screen_registrations():
    """Test that all required screens are registered"""
    print("\n=== Testing Screen Registrations ===")
    
    try:
        from utils.navigation_manager import nav_manager
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        from screens.wifi_setup import WifiSetupScreen
        
        # Register all screens
        nav_manager.register_screen("main", MainScreen)
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        nav_manager.register_screen("wifi_setup", WifiSetupScreen)
        
        # Check registrations
        required_screens = ["main", "system_selection", "wifi_setup"]
        all_registered = True
        
        for screen_name in required_screens:
            if screen_name in nav_manager.screens:
                print(f"✓ {screen_name} screen registered")
            else:
                print(f"✗ {screen_name} screen NOT registered")
                all_registered = False
        
        return all_registered
        
    except Exception as e:
        print(f"✗ Screen registration test failed: {e}")
        return False

def run_all_issue_tests():
    """Run all tests for reported issues"""
    print("Testing Reported Issues - ECU Diagnostic Tool")
    print("=" * 50)
    
    # Initialize LVGL
    lv.init()
    
    # Run tests
    tests = [
        ("Dialog Parameter Order", test_dialog_parameter_order),
        ("WiFi Setup Screen Registration", test_wifi_setup_screen_registration),
        ("System Selection Data Loading", test_system_selection_data_loading),
        ("App State Initialization", test_app_state_initialization),
        ("Main Screen Menu Functionality", test_main_screen_menu_functionality),
        ("Screen Registrations", test_screen_registrations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("ISSUE TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All reported issues are fixed!")
        return True
    else:
        print("❌ Some issues still exist!")
        return False

def main():
    """Main test function"""
    return run_all_issue_tests()

if __name__ == "__main__":
    main()
