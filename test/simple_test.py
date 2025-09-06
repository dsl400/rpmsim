#!/usr/bin/env python3
"""
Simple test for ECU Diagnostic Tool core components
Runs in MicroPython simulator without GUI
"""

import usys as sys

# Add src directory to path
sys.path.append('/src')

def test_data_manager():
    """Test data manager functionality"""
    print("Testing Data Manager...")
    
    try:
        from utils.data_manager import DataManager
        
        # Create data manager instance
        dm = DataManager()
        
        # Test loading systems
        systems = dm.load_systems()
        print(f"✓ Loaded systems database with {len(systems.get('systems', []))} systems")
        
        # Test getting brands
        brands = dm.get_brands()
        print(f"✓ Found brands: {brands}")
        
        # Test getting system types for a brand
        if brands:
            system_types = dm.get_system_types(brands[0])
            print(f"✓ System types for {brands[0]}: {system_types}")
            
            # Test getting system names
            if system_types:
                system_names = dm.get_system_names(brands[0], system_types[0])
                print(f"✓ System names for {brands[0]} {system_types[0]}: {system_names}")
                
                # Test getting tools
                if system_names:
                    tools = dm.get_system_tools(brands[0], system_types[0], system_names[0])
                    print(f"✓ Tools for {brands[0]} {system_types[0]} {system_names[0]}: {[t['name'] for t in tools]}")
        
        # Test user settings
        settings = dm.get_user_settings()
        print(f"✓ User settings loaded: {list(settings.keys())}")
        
        print("Data Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Data Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handler():
    """Test error handler functionality"""
    print("\nTesting Error Handler...")
    
    try:
        from utils.error_handler import ErrorHandler
        
        # Create error handler instance
        eh = ErrorHandler()
        
        # Test error logging
        eh.handle_error("Test error", "Test context", "INFO")
        eh.handle_error("Test warning", "Test context", "WARNING")
        eh.handle_error("Test error", "Test context", "ERROR")
        
        # Test log retrieval
        log = eh.get_error_log()
        print(f"✓ Error log contains {len(log)} entries")
        
        # Test log summary
        summary = eh.get_log_summary()
        print(f"✓ Log summary: {summary}")
        
        print("Error Handler tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error Handler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hardware_managers():
    """Test hardware manager functionality"""
    print("\nTesting Hardware Managers...")
    
    try:
        # Test WiFi Manager
        from hardware.wifi_manager import WiFiManager
        wm = WiFiManager()
        success = wm.initialize()
        networks = wm.scan_networks()
        print(f"✓ WiFi Manager: Init={success}, Networks={len(networks)}")
        
        # Test ECU Manager
        from hardware.ecu_manager import ECUManager
        em = ECUManager()
        success = em.initialize()
        live_data = em.get_live_data()
        print(f"✓ ECU Manager: Init={success}, Data points={len(live_data)}")
        
        # Test RPM simulation
        em.simulate_rpm(2000)
        current_rpm = em.get_current_rpm()
        print(f"✓ RPM Simulation: Set to {current_rpm} RPM")
        
        print("Hardware Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Hardware Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ECU Diagnostic Tool - Simple Test Suite")
    print("=" * 60)
    
    tests = [
        test_data_manager,
        test_error_handler,
        test_hardware_managers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Implementation is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
