

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

def get_last_selected_system_and_tool():
    """Get the last selected system and tool from user settings"""
    try:
        with open('/workspace/rpmsim/src/db/user_settings.json', 'r') as f:
            settings = ujson.loads(f.read())
            if 'last_selected_system' in settings and settings['last_selected_system']:
                return settings['last_selected_system'], settings.get('last_selected_tool', None)
    except:
        pass
    return None, None

def display_last_selected_screen():
    """Display the last selected system screen"""
    system_name, tool_name = get_last_selected_system_and_tool()
    if system_name:
        scr = lv.screen()
        title_label = lv.label(scr)
        text = f"Last Selected: {system_name}"
        if tool_name:
            text += f" - Tool: {tool_name}"
        title_label.set_text(text)
        title_label.center()

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
        # Display last selected system screen
        display_last_selected_screen()

