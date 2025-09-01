

import lvgl as lv
import ujson
from hardware import wifi_manager

class WifiSetupScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()
        self.populate_networks()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("WiFi Setup")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Create list for WiFi networks
        self.network_list = lv.list(self.scr)
        self.network_list.set_size(400, 300)
        self.network_list.center()

    def populate_networks(self):
        # Get available networks (this would be from the actual WiFi scan in a real implementation)
        networks = wifi_manager.scan_networks()

        for network in networks:
            btn = self.network_list.add_btn(network['ssid'], lv.SYMBOL_WIFI)
            btn.set_user_data(network)

    def on_network_selected(self, btn):
        # Get selected network data
        network = btn.get_user_data()

        # Show password input
        passwd = lv.textarea(self.scr)
        passwd.set_text("Password")
        passwd.align(lv.ALIGN_CENTER, 0, 50)

        # Connect button
        connect_btn = lv.btn(self.scr)
        connect_btn.set_size(150, 50)
        connect_btn.center()
        connect_btn.label = lv.label(connect_btn)
        connect_btn.label.set_text("Connect")

        def on_connect_click(event):
            password = passwd.get_text()
            # Show spinner while connecting
            spinner = lv.spinner(self.scr)
            spinner.align(lv.ALIGN_CENTER, 0, 0)

            # Connect to WiFi in the background
            wifi_manager.connect(network['ssid'], password, on_connection_complete)

        connect_btn.add_event_cb(on_connect_click, lv.EVENT.CLICKED, None)

    def on_connection_complete(self, success):
        if success:
            # Hide spinner and show update check
            lv.spinner.stop(spinner)
            lv.label.set_text("Checking for updates...")
        else:
            # Show error message
            lv.alert(self.scr, "Connection failed")

def create_wifi_setup_screen():
    scr = lv.screen()
    WifiSetupScreen(scr)
    return scr

