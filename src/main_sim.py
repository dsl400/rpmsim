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

    # Import and display main screen
    from screens.main_screen import MainScreen

    # Create main screen
    main_scr = lv.obj()
    main_screen = MainScreen(main_scr)
    lv.screen_load(main_scr)

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
