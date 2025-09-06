

"""
WiFi Setup Screen for ECU Diagnostic Tool
Handles network scanning, selection, and connection
"""

import lvgl as lv
import time
from utils.navigation_manager import BaseScreen, nav_manager, app_state

class WifiSetupScreen(BaseScreen):
    """WiFi setup and configuration screen"""

    def __init__(self, scr):
        self.selected_network = None
        self.networks = []
        self.network_buttons = {}  # Map button objects to network data
        super().__init__(scr)

    def create_ui(self):
        """Create the WiFi setup UI elements"""
        # Create title label
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("WiFi Setup")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)
        # Use default font (remove explicit font setting)

        # Add description text
        self.widgets['description'] = lv.label(self.scr)
        self.widgets['description'].set_text("Select a WiFi network to connect.")
        self.widgets['description'].align_to(self.widgets['title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        self.widgets['description'].set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

        # Add close button in top right corner
        self.widgets['close_btn'] = lv.button(self.scr)
        self.widgets['close_btn'].set_size(40, 40)
        close_label = lv.label(self.widgets['close_btn'])
        close_label.set_text(lv.SYMBOL.CLOSE)
        close_label.center()
        self.widgets['close_btn'].align(lv.ALIGN.TOP_RIGHT, -20, 20)
        self.widgets['close_btn'].add_event_cb(self.on_close_click, lv.EVENT.CLICKED, None)

        # Create container to display available networks (adjusted size to fit scan button)
        self.widgets['network_list'] = lv.obj(self.scr)
        self.widgets['network_list'].set_size(600, 280)
        self.widgets['network_list'].align(lv.ALIGN.CENTER, 0, 10)
        self.widgets['network_list'].set_style_pad_all(10, 0)
        self.widgets['network_list'].set_style_border_width(1, 0)
        self.widgets['network_list'].set_style_border_color(lv.color_hex(0xDDDDDD), 0)
        self.widgets['network_list'].set_style_radius(5, 0)
        self.widgets['network_list'].set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

        # Add button to scan for networks
        self.widgets['scan_btn'] = lv.button(self.scr)
        self.widgets['scan_btn'].set_size(150, 40)
        scan_label = lv.label(self.widgets['scan_btn'])
        scan_label.set_text("Scan Networks")
        scan_label.center()
        self.widgets['scan_btn'].align_to(self.widgets['network_list'], lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

        # Add event handler for scan button
        self.widgets['scan_btn'].add_event_cb(self.on_scan_click, lv.EVENT.CLICKED, None)

        # Auto-scan on startup
        self.auto_scan_networks()

    def auto_scan_networks(self):
        """Automatically scan for networks on screen load"""
        try:
            self.scan_networks()
        except Exception as e:
            app_state.error_handler.handle_error(e, "Auto-scan failed")

    def scan_networks(self):
        """Scan for available WiFi networks with mocked data and 1-second delay"""
        try:
            # Show scanning indicator
            self.show_scanning_indicator()

            # Simulate 1-second delay for network scanning (reduced from 3 seconds)
            import time
            time.sleep(1)

            # Mock network list with 3 entries as specified
            self.networks = [
                {
                    'ssid': 'password_test',
                    'signal_strength': 85,
                    'security': 'WPA2',
                    'requires_password': True,
                    'test_password': 'test'  # For simulation
                },
                {
                    'ssid': 'OpenNetwork',
                    'signal_strength': 70,
                    'security': 'Open',
                    'requires_password': False
                },
                {
                    'ssid': 'unknown network',
                    'signal_strength': 60,
                    'security': 'WPA2',
                    'requires_password': True,
                    'should_reject': True  # For simulation
                }
            ]

            # Hide scanning indicator
            self.hide_scanning_indicator()

            # Update network list
            self.update_network_list()

        except Exception as e:
            self.hide_scanning_indicator()
            app_state.error_handler.handle_error(e, "Network scan failed")

    def show_scanning_indicator(self):
        """Show scanning progress indicator"""
        if 'scan_spinner' not in self.widgets:
            self.widgets['scan_spinner'] = lv.spinner(self.scr)
            self.widgets['scan_spinner'].set_size(50, 50)
            self.widgets['scan_spinner'].align(lv.ALIGN.CENTER, 0, -50)

    def hide_scanning_indicator(self):
        """Hide scanning progress indicator"""
        if 'scan_spinner' in self.widgets:
            self.widgets['scan_spinner'].delete()
            del self.widgets['scan_spinner']

    def update_network_list(self):
        """Update the network list with scan results"""
        # Clear existing networks
        self.widgets['network_list'].clean()

        if not self.networks:
            # Show message if no networks found
            error_handler.show_info_dialog("No WiFi networks found")
            return

        # Add networks to list
        y_pos = 10
        for network in self.networks:
            # Create network button with signal strength indicator
            signal_icon = self.get_signal_icon(network.get('signal_strength', -100))
            security_icon = "🔒" if network.get('requires_password', False) else "🔓"
            btn_text = f"{network['ssid']} {signal_icon} {security_icon}"

            # Create button manually
            btn = lv.button(self.widgets['network_list'])
            btn.set_size(560, 50)
            btn.align(lv.ALIGN.TOP_MID, 0, y_pos)
            btn.set_style_margin_bottom(5, 0)
            btn.set_style_radius(5, 0)

            # Add label to button
            btn_label = lv.label(btn)
            btn_label.set_text(btn_text)
            btn_label.center()

            # Store network data and add event handler
            self.network_buttons[btn] = network
            btn.add_event_cb(self.on_network_select, lv.EVENT.CLICKED, None)

            y_pos += 60

    def get_signal_icon(self, signal_strength):
        """Get signal strength icon based on dBm value"""
        if signal_strength > -50:
            return "📶"  # Excellent
        elif signal_strength > -60:
            return "📶"  # Good
        elif signal_strength > -70:
            return "📶"  # Fair
        else:
            return "📶"  # Poor

    def on_scan_click(self, event):
        """Handle scan button click"""
        self.scan_networks()

    def on_network_select(self, event):
        """Handle network selection - show password dialog if needed"""
        try:
            target_btn = event.get_target()
            self.selected_network = self.network_buttons.get(target_btn)

            if self.selected_network:
                if self.selected_network.get('requires_password', False):
                    # Show password dialog
                    self.show_password_dialog()
                else:
                    # Connect directly for open networks
                    self.connect_to_network("")

        except Exception as e:
            app_state.error_handler.handle_error(e, "Network selection failed")

    def show_password_dialog(self):
        """Show password input dialog for selected network"""
        try:
            # Create modal dialog
            dialog = lv.obj(self.scr)
            dialog.set_size(350, 200)
            dialog.center()
            dialog.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
            dialog.set_style_border_width(2, 0)
            dialog.set_style_radius(10, 0)

            # Add title
            title_label = lv.label(dialog)
            title_label.set_text(f"Connect to {self.selected_network['ssid']}")
            title_label.align(lv.ALIGN.TOP_MID, 0, 10)

            # Add instruction
            inst_label = lv.label(dialog)
            inst_label.set_text("Enter network password:")
            inst_label.align_to(title_label, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

            # Create password input
            password_input = lv.textarea(dialog)
            password_input.set_size(250, 40)
            password_input.set_placeholder_text("Password")
            password_input.set_password_mode(True)
            password_input.align_to(inst_label, lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

            # Add Connect button
            connect_btn = lv.button(dialog)
            connect_btn.set_size(80, 35)
            connect_btn.align(lv.ALIGN.BOTTOM_LEFT, 20, -15)
            connect_label = lv.label(connect_btn)
            connect_label.set_text("Connect")
            connect_label.center()

            # Add Cancel button
            cancel_btn = lv.button(dialog)
            cancel_btn.set_size(80, 35)
            cancel_btn.align(lv.ALIGN.BOTTOM_RIGHT, -20, -15)
            cancel_label = lv.label(cancel_btn)
            cancel_label.set_text("Cancel")
            cancel_label.center()

            # Store references for callback
            self.password_dialog = dialog
            self.password_input_field = password_input

            # Add event handlers
            connect_btn.add_event_cb(lambda e: self.on_password_connect(), lv.EVENT.CLICKED, None)
            cancel_btn.add_event_cb(lambda e: dialog.delete(), lv.EVENT.CLICKED, None)

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to show password dialog")

    def on_password_connect(self):
        """Handle connect button in password dialog"""
        try:
            password = self.password_input_field.get_text()
            self.connect_to_network(password)
            self.password_dialog.delete()
        except Exception as e:
            error_handler.handle_error(e, "Password connect error")



    def connect_to_network(self, password):
        """Connect to the selected network with given password"""
        try:
            if not self.selected_network:
                return

            ssid = self.selected_network['ssid']

            # Simulate connection based on network type
            if ssid == "password_test":
                if password == "test":
                    self.show_connection_result(True, "Connected successfully!")
                else:
                    self.show_connection_result(False, "Incorrect password")
            elif ssid == "OpenNetwork":
                self.show_connection_result(True, "Connected successfully!")
            elif ssid == "unknown network":
                self.show_connection_result(False, "Connection failed - network rejected")
            else:
                self.show_connection_result(False, "Unknown network")

        except Exception as e:
            error_handler.handle_error(e, "Connection failed")

    def show_connection_result(self, success, message):
        """Show connection result dialog"""
        try:
            if success:
                error_handler.show_info_dialog(message, "Connection Success")
                # Close WiFi setup screen after successful connection
                nav_manager.go_back()
            else:
                app_state.error_handler.show_error_dialog(message, "Connection Failed")

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to show connection result")

    def on_close_click(self, event):
        """Handle close button click"""
        try:
            nav_manager.go_back()
        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to close WiFi setup")




