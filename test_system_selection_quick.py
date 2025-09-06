"""
Quick test for system selection screen navigation
"""

import lvgl as lv
import utime as time
import sys

# Add src to path for imports
sys.path.insert(0, 'src')

def test_system_selection_navigation():
    """Test navigation to system selection screen"""
    print("=== Testing System Selection Navigation ===")
    
    try:
        # Initialize LVGL
        lv.init()
        
        # Import required modules
        from utils.navigation_manager import nav_manager, app_state
        from utils.data_manager import DataManager
        from utils.error_handler import ErrorHandler
        from screens.main_screen import MainScreen
        from screens.system_selection import SystemSelectionScreen
        
        # Initialize app state
        if not hasattr(app_state, 'data_manager') or not app_state.data_manager:
            app_state.data_manager = DataManager()
        if not hasattr(app_state, 'error_handler') or not app_state.error_handler:
            app_state.error_handler = ErrorHandler()
        
        # Register system selection screen
        nav_manager.register_screen("system_selection", SystemSelectionScreen)
        
        print("✓ App state and navigation manager initialized")
        
        # Create main screen
        main_scr = lv.obj()
        main_screen = MainScreen(main_scr)
        print("✓ Main screen created")
        
        # Try to navigate to system selection
        nav_manager.navigate_to("system_selection")
        print("✓ Navigation to system selection successful")
        
        # Check if system selection screen was created
        if nav_manager.current_screen:
            print("✓ System selection screen is active")
            
            # Check if brands are loaded
            current_screen_obj = nav_manager.current_screen
            if hasattr(current_screen_obj, 'brands') and current_screen_obj.brands:
                print(f"✓ Brands loaded: {current_screen_obj.brands}")
            else:
                print("✗ No brands loaded")
                
            return True
        else:
            print("✗ No current screen active")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    return test_system_selection_navigation()

if __name__ == "__main__":
    main()
