

import lvgl as lv
import ujson
from screens.wifi.wifi import create_wifi_setup_screen

def show_main_screen():
    """Show the main screen of the application"""
    scr = lv.screen()
    # Create a simple label for now
    label = lv.label(scr)
    label.set_text("Main Screen")
    label.center()

def is_device_configured():
    """Check if the device has been configured with WiFi settings"""
    try:
        with open('/workspace/rpmsim/src/db/user_settings.json', 'r') as f:
            settings = ujson.loads(f.read())
            return 'wifi' in settings and settings['wifi']['ssid'] is not None
    except:
        return False

def display_initial_screen():
    """Display the appropriate initial screen based on device configuration"""
    if not is_device_configured():
        # Show WiFi setup screen if device is not configured
        wifi_screen = create_wifi_setup_screen()
    else:
        # Otherwise, show the main screen
        show_main_screen()

