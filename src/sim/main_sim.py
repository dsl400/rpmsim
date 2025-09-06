import lvgl as lv
from hardware.hardware import WifiMock, FileSystemMock

def setup_simulation():
    """Set up the simulation environment with display and hardware mocks."""
    print("Setting up simulation...")

    # Create SDL window for display simulation
    disp_drv = lv.sdl_window_create(480, 272)
    lv.sdl_window_set_resizeable(disp_drv, False)
    lv.sdl_window_set_title(disp_drv, "Simulator (MicroPython)")

    # Create mouse driver for interaction
    mouse = lv.sdl_mouse_create()

    print("Display simulation initialized")

    # Initialize hardware mocks
    wifi = WifiMock()
    file_system = FileSystemMock()

    print("Hardware mocks initialized")
    return disp_drv, mouse, wifi, file_system

if __name__ == "__main__":
    setup_simulation()
