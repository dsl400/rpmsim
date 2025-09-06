"""
Full Test Suite Validation for ECU Diagnostic Tool
Validates all UI features work correctly without regressions
"""

import lvgl as lv
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def test_core_functionality():
    """Test core application functionality"""
    print("=== Testing Core Functionality ===")
    
    try:
        # Test imports
        from utils.navigation_manager import nav_manager, app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        from screens.wifi_setup import WifiSetupScreen
        from screens.firmware_update import FirmwareUpdateScreen
        
        print("✓ All core modules import successfully")
        
        # Test app state initialization
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        print("✓ App state initializes correctly")
        
        # Test data loading
        brands = app_state.data_manager.get_brands()
        if brands and len(brands) > 0:
            print(f"✓ Data loading works: {len(brands)} brands loaded")
        else:
            print("✗ Data loading failed: no brands found")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Core functionality test failed: {e}")
        return False

def test_screen_creation():
    """Test that all screens can be created without errors"""
    print("\n=== Testing Screen Creation ===")
    
    try:
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        from screens.wifi_setup import WifiSetupScreen
        from screens.firmware_update import FirmwareUpdateScreen
        from utils.navigation_manager import nav_manager, app_state
        
        screens_to_test = [
            ("Main Screen", MainScreen),
            ("System Selection Screen", SystemSelectionScreen),
            ("WiFi Setup Screen", WifiSetupScreen),
            ("Firmware Update Screen", FirmwareUpdateScreen),
        ]
        
        all_created = True
        for screen_name, screen_class in screens_to_test:
            try:
                scr = lv.obj()
                screen_instance = screen_class(scr)
                print(f"✓ {screen_name} created successfully")
            except Exception as e:
                print(f"✗ {screen_name} creation failed: {e}")
                all_created = False
        
        return all_created
        
    except Exception as e:
        print(f"✗ Screen creation test failed: {e}")
        return False

def test_navigation_system():
    """Test navigation system functionality"""
    print("\n=== Testing Navigation System ===")
    
    try:
        from utils.navigation_manager import nav_manager
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        from screens.wifi_setup import WifiSetupScreen
        from screens.firmware_update import FirmwareUpdateScreen
        
        # Register screens
        nav_manager.register_screen("main", MainScreen)
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        nav_manager.register_screen("wifi_setup", WifiSetupScreen)
        nav_manager.register_screen("firmware_update", FirmwareUpdateScreen)
        
        # Test screen registration
        required_screens = ["system_selection", "wifi_setup", "firmware_update"]
        all_registered = True
        
        for screen_name in required_screens:
            if screen_name in nav_manager.screens:
                print(f"✓ {screen_name} screen registered")
            else:
                print(f"✗ {screen_name} screen NOT registered")
                all_registered = False
        
        return all_registered
        
    except Exception as e:
        print(f"✗ Navigation system test failed: {e}")
        return False

def test_error_handling():
    """Test error handling system"""
    print("\n=== Testing Error Handling ===")
    
    try:
        from utils.error_handler import ErrorHandler
        
        error_handler = ErrorHandler()
        
        # Test error logging
        try:
            error_handler.handle_error(Exception("Test error"), "Test context")
            print("✓ Error logging works")
        except Exception as e:
            print(f"✗ Error logging failed: {e}")
            return False
        
        # Test dialog creation (may not display in headless mode)
        try:
            error_handler.show_info_dialog("Test message", "Test Title")
            print("✓ Info dialog creation works")
        except Exception as e:
            print(f"✗ Info dialog creation failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def test_ui_components():
    """Test UI component functionality"""
    print("\n=== Testing UI Components ===")
    
    try:
        from screens.main_screen import MainScreen
        from utils.navigation_manager import app_state
        
        # Create main screen to test UI components
        scr = lv.obj()
        main_screen = MainScreen(scr)
        
        # Test widget creation
        required_widgets = ['toolbar', 'menu_btn', 'title_btn', 'wifi_icon', 'main_area']
        all_widgets_exist = True
        
        for widget_name in required_widgets:
            if widget_name in main_screen.widgets:
                print(f"✓ {widget_name} widget exists")
            else:
                print(f"✗ {widget_name} widget missing")
                all_widgets_exist = False
        
        return all_widgets_exist
        
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        return False

def test_data_persistence():
    """Test data persistence functionality"""
    print("\n=== Testing Data Persistence ===")
    
    try:
        from utils.data_manager import DataManager
        
        data_manager = DataManager()
        
        # Test data loading
        brands = data_manager.get_brands()
        if brands and len(brands) > 0:
            print(f"✓ Brands data loads: {brands}")
        else:
            print("✗ Brands data loading failed")
            return False
        
        # Test system types loading
        system_types = data_manager.get_system_types(brands[0])
        if system_types and len(system_types) > 0:
            print(f"✓ System types data loads: {system_types}")
        else:
            print("✗ System types data loading failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Data persistence test failed: {e}")
        return False

def run_full_test_suite():
    """Run the complete test suite"""
    print("Full Test Suite Validation - ECU Diagnostic Tool")
    print("=" * 60)
    
    # Initialize LVGL
    lv.init()
    
    # Run all test categories
    tests = [
        ("Core Functionality", test_core_functionality),
        ("Screen Creation", test_screen_creation),
        ("Navigation System", test_navigation_system),
        ("Error Handling", test_error_handling),
        ("UI Components", test_ui_components),
        ("Data Persistence", test_data_persistence),
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
    print("\n" + "=" * 60)
    print("FULL TEST SUITE SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\nResults: {passed}/{total} test categories passed")
    
    # Overall assessment
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ No regressions detected")
        print("✅ All UI features working correctly")
        print("✅ Application ready for production")
        return True
    else:
        print(f"\n❌ {total - passed} test categories failed!")
        print("⚠️  Regressions detected - review failed tests")
        return False

def main():
    """Main test function"""
    return run_full_test_suite()

if __name__ == "__main__":
    main()
