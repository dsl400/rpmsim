


import lvgl as lv
from hardware import wifi_manager

class WifiSetupScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("WiFi Setup")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Add description text
        desc_label = lv.label(self.scr)
        desc_label.set_text("Please select a WiFi network and enter the password.")
        desc_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 10)

        # Create list to display available networks
        self.network_list = lv.list(self.scr)
        self.network_list.set_size(400, 200)
        self.network_list.align(lv.ALIGN.TOP_MID, 0, 60)

        # Add button to scan for networks
        self.scan_btn = lv.btn(self.scr)
        self.scan_btn.set_size(150, 40)
        self.scan_btn.label = lv.label(self.scan_btn)
        self.scan_btn.label.set_text("Scan Networks")
        self.scan_btn.align_to(self.network_list, lv.ALIGN.BOTTOM_MID, 0, 10)

        # Add event handler for scan button
        self.scan_btn.add_event_cb(self.on_scan_click, lv.EVENT.CLICKED, None)

        # Create input field for password entry
        self.password_input = lv.textarea(self.scr)
        self.password_input.set_size(400, 50)
        self.password_input.align_to(self.network_list, lv.ALIGN.BOTTOM_MID, 0, 80)
        self.password_input.label = lv.label(self.scr)
        self.password_input.label.set_text("Password:")
        self.password_input.label.align_to(self.password_input, lv.ALIGN.LEFT_MID, -150, 0)

        # Create connect button
        self.connect_btn = lv.btn(self.scr)
        self.connect_btn.set_size(200, 50)
        self.connect_btn.center()
        self.connect_btn.label = lv.label(self.connect_btn)
        self.connect_btn.label.set_text("Connect")

        # Add event handler for connect button
        self.connect_btn.add_event_cb(self.on_connect_click, lv.EVENT.CLICKED, None)

    def on_scan_click(self, btn):
        # Scan for available networks and display them in the list
        networks = wifi_manager.scan_networks()

        # Clear any existing networks in the list
        self.network_list.clear()

        if networks:
            for network in networks:
                # Add each network to the list with an event handler
                btn = self.network_list.add_btn(network['ssid'], lv.SYMBOL.WIFI)
                btn.set_user_data(network)

                def on_network_select(event):
                    selected_network = event.target.get_user_data()
                    # Set this as the selected network for connection
                    self.selected_network = selected_network

                btn.add_event_cb(on_network_select, lv.EVENT.CLICKED, None)
        else:
            # Show message if no networks found
            msg = lv.alert(self.scr)
            msg.set_text("No WiFi networks found")

    def on_connect_click(self, btn):
        # Check if a network has been selected and password entered
        if not hasattr(self, 'selected_network') or not self.selected_network:
            msg = lv.alert(self.scr)
            msg.set_text("Please select a network first")
            return

        password = self.password_input.get_text()

        if not password:
            msg = lv.alert(self.scr)
            msg.set_text("Please enter the WiFi password")
            return

        # Show spinner while connecting
        spinner = lv.spinner(self.scr)
        spinner.align(lv.ALIGN.CENTER, 0, 0)

        # Connect to the selected network in a separate thread
        success = wifi_manager.connect_to_network(self.selected_network['ssid'], password)

        # Remove spinner and show connection result
        spinner.delete()

        if success:
            msg = lv.alert(self.scr)
            msg.set_text("Connected successfully!")
        else:
            msg = lv.alert(self.scr)
            msg.set_text("Failed to connect. Please try again.")

def create_wifi_setup_screen():
    scr = lv.screen()
    WifiSetupScreen(scr)
    return scr


