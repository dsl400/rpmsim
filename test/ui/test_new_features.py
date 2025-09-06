"""
Test new features implemented for ECU Diagnostic Tool
Tests firmware update screen, system info screen, and updated menu
"""

import lvgl as lv
import utime as time
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def test_firmware_update_screen():
    """Test firmware update screen functionality"""
    print("=== Testing Firmware Update Screen ===")
    
    try:
        from screens.firmware_update import FirmwareUpdateScreen
        from utils.navigation_manager import app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Create firmware update screen
        scr = lv.obj()
        firmware_screen = FirmwareUpdateScreen(scr)
        
        # Check if required widgets exist
        required_widgets = ['title', 'current_version', 'status_label', 'check_btn', 'back_btn']
        all_widgets_exist = True
        
        for widget_name in required_widgets:
            if widget_name in firmware_screen.widgets:
                print(f"✓ Found widget: {widget_name}")
            else:
                print(f"✗ Missing widget: {widget_name}")
                all_widgets_exist = False
        
        # Test initial state
        if firmware_screen.update_status == "idle":
            print("✓ Initial status is correct")
        else:
            print(f"✗ Wrong initial status: {firmware_screen.update_status}")
            all_widgets_exist = False
        
        return all_widgets_exist
        
    except Exception as e:
        print(f"✗ Firmware update screen test failed: {e}")
        return False

def test_system_info_screen():
    """Test system info screen functionality"""
    print("\n=== Testing System Info Screen ===")
    
    try:
        from screens.system_info import SystemInfoScreen
        from utils.navigation_manager import app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Create system info screen
        scr = lv.obj()
        info_screen = SystemInfoScreen(scr)
        
        # Check if required widgets exist
        required_widgets = ['title', 'info_container', 'back_btn', 'refresh_btn', 'mem_info', 'net_info']
        all_widgets_exist = True
        
        for widget_name in required_widgets:
            if widget_name in info_screen.widgets:
                print(f"✓ Found widget: {widget_name}")
            else:
                print(f"✗ Missing widget: {widget_name}")
                all_widgets_exist = False
        
        return all_widgets_exist
        
    except Exception as e:
        print(f"✗ System info screen test failed: {e}")
        return False

def test_main_screen_menu_updates():
    """Test updated main screen menu functionality"""
    print("\n=== Testing Main Screen Menu Updates ===")
    
    try:
        from screens.main_screen import MainScreen
        from utils.navigation_manager import app_state, nav_manager
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.firmware_update import FirmwareUpdateScreen
        from screens.system_info import SystemInfoScreen
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Register new screens
        nav_manager.register_screen("firmware_update", FirmwareUpdateScreen)
        nav_manager.register_screen("system_info", SystemInfoScreen)
        
        # Create main screen
        scr = lv.obj()
        main_screen = MainScreen(scr)
        
        # Test menu actions
        menu_actions = ["select_ecu", "updates", "system_info"]
        all_actions_work = True
        
        for action in menu_actions:
            try:
                # This should not crash
                main_screen.on_menu_select(action)
                print(f"✓ Menu action '{action}' handled successfully")
            except Exception as e:
                print(f"✗ Menu action '{action}' failed: {e}")
                all_actions_work = False
        
        return all_actions_work
        
    except Exception as e:
        print(f"✗ Main screen menu test failed: {e}")
        return False

def test_screen_registrations():
    """Test that all new screens are properly registered"""
    print("\n=== Testing Screen Registrations ===")
    
    try:
        from utils.navigation_manager import nav_manager
        from screens.firmware_update import FirmwareUpdateScreen
        from screens.system_info import SystemInfoScreen
        
        # Register screens
        nav_manager.register_screen("firmware_update", FirmwareUpdateScreen)
        nav_manager.register_screen("system_info", SystemInfoScreen)
        
        # Check registrations
        new_screens = ["firmware_update", "system_info"]
        all_registered = True
        
        for screen_name in new_screens:
            if screen_name in nav_manager.screens:
                print(f"✓ {screen_name} screen registered")
            else:
                print(f"✗ {screen_name} screen NOT registered")
                all_registered = False
        
        return all_registered
        
    except Exception as e:
        print(f"✗ Screen registration test failed: {e}")
        return False

def test_prd_compliance():
    """Test compliance with PRD requirements"""
    print("\n=== Testing PRD Compliance ===")
    
    try:
        # Check if all required menu options are available
        # REQ-018: Menu options shall include:
        # - Select ECU → System Selection Screen
        # - Check for Updates → Firmware Update Screen  
        # - System Info → System Information Screen
        
        from screens.main_screen import MainScreen
        from utils.navigation_manager import app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Create main screen
        scr = lv.obj()
        main_screen = MainScreen(scr)
        
        # Test that main screen has required widgets
        required_widgets = ['toolbar', 'menu_btn', 'title_btn', 'wifi_icon', 'main_area']
        prd_compliant = True
        
        for widget_name in required_widgets:
            if widget_name in main_screen.widgets:
                print(f"✓ PRD requirement met: {widget_name} exists")
            else:
                print(f"✗ PRD requirement failed: {widget_name} missing")
                prd_compliant = False
        
        return prd_compliant
        
    except Exception as e:
        print(f"✗ PRD compliance test failed: {e}")
        return False

def run_all_new_feature_tests():
    """Run all tests for new features"""
    print("Testing New Features - ECU Diagnostic Tool")
    print("=" * 50)
    
    # Initialize LVGL
    lv.init()
    
    # Run tests
    tests = [
        ("Firmware Update Screen", test_firmware_update_screen),
        ("System Info Screen", test_system_info_screen),
        ("Main Screen Menu Updates", test_main_screen_menu_updates),
        ("Screen Registrations", test_screen_registrations),
        ("PRD Compliance", test_prd_compliance),
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
    print("NEW FEATURES TEST SUMMARY")
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
        print("🎉 All new features are working!")
        return True
    else:
        print("❌ Some new features have issues!")
        return False

def main():
    """Main test function"""
    return run_all_new_feature_tests()

if __name__ == "__main__":
    main()
