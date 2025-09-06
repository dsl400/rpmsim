"""
Main entry point for ECU Diagnostic Tool (Simulation Mode)
Initializes the simulation environment, hardware simulation, and displays the main screen
"""

import lvgl as lv
import utime as time

def initialize_simulation_environment():
    """Initialize the simulation environment"""
    # Initialize LVGL
    lv.init()

    # Create SDL window for display simulation
    disp_drv = lv.sdl_window_create(800, 480)
    lv.sdl_window_set_resizeable(disp_drv, False)
    lv.sdl_window_set_title(disp_drv, "ECU Diagnostic Tool - Simulator")

    # Create mouse driver for interaction
    mouse = lv.sdl_mouse_create()

    print("Simulation environment initialized")
    return disp_drv, mouse

def initialize_hardware_simulation():
    """Initialize hardware simulation modules"""
    from hardware.sim.hardware_sim import initialize_hardware_simulation

    # Initialize hardware simulation
    success = initialize_hardware_simulation()
    if not success:
        raise RuntimeError("Hardware simulation initialization failed")

    print("Hardware simulation initialized")
    return success

def main():
    """Main application entry point for simulation"""
    print("Starting ECU Diagnostic Tool (Simulation Mode)...")

    # Initialize simulation environment
    disp_drv, mouse = initialize_simulation_environment()

    # Initialize hardware simulation
    initialize_hardware_simulation()

    # Import and register screens
    from screens.main_screen import MainScreen
    from screens.system_selection import SystemSelectionScreen
    from utils.navigation_manager import nav_manager

    # Register screens with navigation manager
    nav_manager.register_screen("system_selection", SystemSelectionScreen)

    # Get the active screen and use it directly
    main_scr = lv.screen_active()
    # Remove all padding and borders from the root screen
    main_scr.set_style_pad_all(0, 0)
    main_scr.set_style_border_width(0, 0)
    main_scr.set_style_radius(0, 0)
    main_scr.set_style_margin_all(0, 0)  # Remove margins
    # Set background to match the toolbar color to eliminate white borders
    main_scr.set_style_bg_color(lv.color_hex(0x2196F3), 0)
    main_screen = MainScreen(main_scr)

    print("Main screen loaded - ECU Diagnostic Tool Simulator ready")
    print("Use mouse to interact with the interface")

    # Main simulation loop
    try:
        while True:
            lv.task_handler()
            time.sleep_ms(5)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except Exception as e:
        print(f"Simulation error: {e}")

if __name__ == "__main__":
    main()
