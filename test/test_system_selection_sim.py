"""
Test system selection in MicroPython simulator
"""

import lvgl as lv
import utime as time
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def test_data_manager():
    """Test data manager functionality in simulator"""
    print("=== Testing Data Manager in Simulator ===")
    
    try:
        from utils.data_manager import DataManager
        
        # Create data manager instance
        dm = DataManager()
        print("✓ Data manager created")
        
        # Test loading systems
        systems = dm.get_systems()
        print(f"✓ Loaded {len(systems)} systems")
        
        # Test getting brands
        brands = dm.get_brands()
        print(f"✓ Found brands: {brands}")
        
        if not brands:
            print("✗ ERROR: No brands found!")
            return False
            
        # Test getting system types for first brand
        if brands:
            first_brand = brands[0]
            system_types = dm.get_system_types(first_brand)
            print(f"✓ System types for {first_brand}: {system_types}")
            
            if system_types:
                first_type = system_types[0]
                system_names = dm.get_system_names(first_brand, first_type)
                print(f"✓ System names for {first_brand}/{first_type}: {system_names}")
                
                if system_names:
                    first_name = system_names[0]
                    tools = dm.get_system_tools(first_brand, first_type, first_name)
                    print(f"✓ Tools for {first_brand}/{first_type}/{first_name}: {[t.get('name') for t in tools]}")
        
        return True
        
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def test_app_state():
    """Test app state initialization"""
    print("\n=== Testing App State ===")
    
    try:
        from utils.navigation_manager import app_state
        
        # Initialize app state if needed
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            from utils.data_manager import DataManager
            app_state.data_manager = DataManager()
            print("✓ Initialized app state data manager")
        
        # Check if data manager is initialized
        if hasattr(app_state, 'data_manager') and app_state.data_manager:
            print("✓ App state has data manager")
            
            # Test data manager through app state
            brands = app_state.data_manager.get_brands()
            print(f"✓ Brands via app state: {brands}")
            
            return len(brands) > 0
        else:
            print("✗ ERROR: App state missing data manager")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def test_system_selection_screen():
    """Test system selection screen creation"""
    print("\n=== Testing System Selection Screen ===")
    
    try:
        from screens.system_selection import SystemSelectionScreen
        from utils.navigation_manager import app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Create a test screen
        scr = lv.obj()
        system_screen = SystemSelectionScreen(scr)
        print("✓ System selection screen created")
        
        # Test if brands are loaded
        brands = app_state.data_manager.get_brands()
        print(f"✓ Brands available: {brands}")
        
        return len(brands) > 0
        
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("Starting system selection test in simulator...\n")
    
    # Initialize LVGL (minimal setup)
    lv.init()
    
    # Test 1: Data manager directly
    dm_ok = test_data_manager()
    
    # Test 2: App state
    app_state_ok = test_app_state()
    
    # Test 3: System selection screen
    screen_ok = test_system_selection_screen()
    
    print(f"\n=== Results ===")
    print(f"Data Manager: {'✓ PASS' if dm_ok else '✗ FAIL'}")
    print(f"App State: {'✓ PASS' if app_state_ok else '✗ FAIL'}")
    print(f"System Selection Screen: {'✓ PASS' if screen_ok else '✗ FAIL'}")
    
    if dm_ok and app_state_ok and screen_ok:
        print("\n✓ All tests passed - system selection should work")
    else:
        print("\n✗ Some tests failed - system selection may have issues")

if __name__ == "__main__":
    main()
