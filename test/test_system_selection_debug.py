#!/usr/bin/env python3
"""
Debug test for system selection issues
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_data_manager():
    """Test data manager functionality"""
    print("=== Testing Data Manager ===")
    
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
        import traceback
        traceback.print_exc()
        return False

def test_app_state():
    """Test app state initialization"""
    print("\n=== Testing App State ===")
    
    try:
        from utils.navigation_manager import app_state
        
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
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Starting system selection debug test...\n")
    
    # Test 1: Data manager directly
    dm_ok = test_data_manager()
    
    # Test 2: App state
    app_state_ok = test_app_state()
    
    print(f"\n=== Results ===")
    print(f"Data Manager: {'✓ PASS' if dm_ok else '✗ FAIL'}")
    print(f"App State: {'✓ PASS' if app_state_ok else '✗ FAIL'}")
    
    if dm_ok and app_state_ok:
        print("\n✓ All tests passed - system selection should work")
    else:
        print("\n✗ Some tests failed - system selection may have issues")

if __name__ == "__main__":
    main()
