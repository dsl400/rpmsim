"""
Main entry point for ECU Diagnostic Tool (Hardware Mode)
Initializes the environment, hardware, and displays the main screen
"""

import lvgl as lv
import task_handler
import fs_driver
import display

def initialize_environment():
    """Initialize the basic environment"""
    # Initialize LVGL
    lv.init()

    # Initialize file system driver
    fs_drv = lv.fs_drv_t()
    fs_driver.fs_register(fs_drv, 'Z')

    # Initialize display hardware
    display.init()

    print("Environment initialized for hardware mode")

def initialize_hardware():
    """Initialize real hardware modules"""
    from hardware.wifi_manager import WiFiManager
    from hardware.ecu_manager import ECUManager

    # Initialize hardware managers
    wifi_manager = WiFiManager()
    ecu_manager = ECUManager()

    # Initialize hardware
    wifi_manager.initialize()
    ecu_manager.initialize()

    print("Hardware modules initialized")
    return wifi_manager, ecu_manager

def main():
    """Main application entry point"""
    print("Starting ECU Diagnostic Tool (Hardware Mode)...")

    # Initialize environment
    initialize_environment()

    # Initialize hardware
    wifi_manager, ecu_manager = initialize_hardware()

    # Initialize task handler
    task_handler.TaskHandler()

    # Import and display main screen
    from screens.main_screen import MainScreen

    # Create main screen
    main_scr = lv.obj()
    main_screen = MainScreen(main_scr)
    lv.screen_load(main_scr)

    print("Main screen loaded - ECU Diagnostic Tool ready")

if __name__ == "__main__":
    main()

