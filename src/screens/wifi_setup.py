

"""
WiFi Setup Screen for ECU Diagnostic Tool
Handles network scanning, selection, and connection
"""

import lvgl as lv
import time
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class WifiSetupScreen(BaseScreen):
    """WiFi setup and configuration screen"""

    def __init__(self, scr):
        self.selected_network = None
        self.networks = []
        super().__init__(scr)

    def create_ui(self):
        """Create the WiFi setup UI elements"""
        # Create title label
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("WiFi Setup")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)
        self.widgets['title'].set_style_text_font(lv.font_default(), 0)

        # Add description text
        self.widgets['description'] = lv.label(self.scr)
        self.widgets['description'].set_text("Please select a WiFi network and enter the password.")
        self.widgets['description'].align_to(self.widgets['title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        self.widgets['description'].set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

        # Create list to display available networks
        self.widgets['network_list'] = lv.list(self.scr)
        self.widgets['network_list'].set_size(500, 200)
        self.widgets['network_list'].align(lv.ALIGN.TOP_MID, 0, 80)

        # Add button to scan for networks
        self.widgets['scan_btn'] = lv.btn(self.scr)
        self.widgets['scan_btn'].set_size(150, 40)
        scan_label = lv.label(self.widgets['scan_btn'])
        scan_label.set_text("Scan Networks")
        scan_label.center()
        self.widgets['scan_btn'].align_to(self.widgets['network_list'], lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

        # Add event handler for scan button
        self.widgets['scan_btn'].add_event_cb(self.on_scan_click, lv.EVENT.CLICKED, None)

        # Password input label
        self.widgets['password_label'] = lv.label(self.scr)
        self.widgets['password_label'].set_text("Password:")
        self.widgets['password_label'].align_to(self.widgets['scan_btn'], lv.ALIGN.OUT_BOTTOM_LEFT, 0, 20)

        # Create input field for password entry
        self.widgets['password_input'] = lv.textarea(self.scr)
        self.widgets['password_input'].set_size(400, 50)
        self.widgets['password_input'].align_to(self.widgets['password_label'], lv.ALIGN.OUT_BOTTOM_LEFT, 0, 5)
        self.widgets['password_input'].set_placeholder_text("Enter WiFi password")

        # Create connect button
        self.widgets['connect_btn'] = lv.btn(self.scr)
        self.widgets['connect_btn'].set_size(150, 50)
        connect_label = lv.label(self.widgets['connect_btn'])
        connect_label.set_text("Connect")
        connect_label.center()
        self.widgets['connect_btn'].align_to(self.widgets['password_input'], lv.ALIGN.OUT_RIGHT_MID, 10, 0)

        # Add event handler for connect button
        self.widgets['connect_btn'].add_event_cb(self.on_connect_click, lv.EVENT.CLICKED, None)

        # Skip button for testing
        self.widgets['skip_btn'] = lv.btn(self.scr)
        self.widgets['skip_btn'].set_size(100, 40)
        skip_label = lv.label(self.widgets['skip_btn'])
        skip_label.set_text("Skip")
        skip_label.center()
        self.widgets['skip_btn'].align(lv.ALIGN.BOTTOM_RIGHT, -20, -20)
        self.widgets['skip_btn'].add_event_cb(self.on_skip_click, lv.EVENT.CLICKED, None)

        # Auto-scan on startup
        self.auto_scan_networks()

    def auto_scan_networks(self):
        """Automatically scan for networks on screen load"""
        try:
            self.scan_networks()
        except Exception as e:
            error_handler.handle_error(e, "Auto-scan failed")

    def scan_networks(self):
        """Scan for available WiFi networks"""
        try:
            # Show scanning indicator
            self.show_scanning_indicator()

            # Get WiFi manager from app state
            wifi_mgr = app_state.wifi_manager
            if not wifi_mgr:
                error_handler.show_error_dialog("WiFi manager not available")
                return

            # Scan for networks
            self.networks = wifi_mgr.scan_networks()

            # Hide scanning indicator
            self.hide_scanning_indicator()

            # Update network list
            self.update_network_list()

        except Exception as e:
            self.hide_scanning_indicator()
            error_handler.handle_error(e, "Network scan failed")

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
        self.widgets['network_list'].clear()

        if not self.networks:
            # Show message if no networks found
            error_handler.show_info_dialog("No WiFi networks found")
            return

        # Add networks to list
        for network in self.networks:
            # Create network button with signal strength indicator
            signal_icon = self.get_signal_icon(network.get('signal', -100))
            btn_text = f"{network['ssid']} {signal_icon}"

            btn = self.widgets['network_list'].add_button(btn_text)
            btn.set_user_data(network)
            btn.add_event_cb(self.on_network_select, lv.EVENT.CLICKED, None)

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
        """Handle network selection"""
        try:
            self.selected_network = event.target.get_user_data()

            # Update UI to show selected network
            if self.selected_network:
                # Clear password field for new selection
                self.widgets['password_input'].set_text("")

                # Update password field placeholder
                if self.selected_network.get('security', 0) == 0:
                    self.widgets['password_input'].set_placeholder_text("Open network - no password needed")
                else:
                    self.widgets['password_input'].set_placeholder_text(f"Password for {self.selected_network['ssid']}")

        except Exception as e:
            error_handler.handle_error(e, "Network selection failed")

    def on_connect_click(self, event):
        """Handle connect button click"""
        try:
            # Validate selection
            if not self.selected_network:
                error_handler.show_warning_dialog("Please select a network first")
                return

            password = self.widgets['password_input'].get_text()

            # Check if password is needed
            if self.selected_network.get('security', 0) > 0 and not password:
                error_handler.show_warning_dialog("Please enter the WiFi password")
                return

            # Show connection progress
            self.show_connection_progress()

            # Attempt connection
            wifi_mgr = app_state.wifi_manager
            success = wifi_mgr.connect(self.selected_network['ssid'], password)

            # Hide progress indicator
            self.hide_connection_progress()

            if success:
                # Save WiFi configuration
                app_state.data_manager.update_wifi_config(
                    self.selected_network['ssid'],
                    password
                )

                # Update app state
                app_state.is_configured = True
                app_state.wifi_connected = True

                # Check for firmware updates
                self.check_for_updates()

            else:
                error_handler.show_error_dialog("Failed to connect. Please check your password and try again.")

        except Exception as e:
            self.hide_connection_progress()
            error_handler.handle_error(e, "Connection attempt failed")

    def show_connection_progress(self):
        """Show connection progress indicator"""
        if 'connect_spinner' not in self.widgets:
            self.widgets['connect_spinner'] = lv.spinner(self.scr)
            self.widgets['connect_spinner'].set_size(50, 50)
            self.widgets['connect_spinner'].align(lv.ALIGN.CENTER, 0, 0)

    def hide_connection_progress(self):
        """Hide connection progress indicator"""
        if 'connect_spinner' in self.widgets:
            self.widgets['connect_spinner'].delete()
            del self.widgets['connect_spinner']

    def check_for_updates(self):
        """Check for firmware updates after successful connection"""
        try:
            wifi_mgr = app_state.wifi_manager
            update_info = wifi_mgr.check_for_updates()

            if update_info.get('available', False):
                # Show update available dialog
                error_handler.show_info_dialog(
                    f"Firmware update available: {update_info.get('version', 'Unknown')}\n"
                    "You can update later from the main menu."
                )

            # Navigate to main screen
            nav_manager.navigate_to("main")

        except Exception as e:
            error_handler.handle_error(e, "Update check failed")
            # Still navigate to main screen
            nav_manager.navigate_to("main")

    def on_skip_click(self, event):
        """Handle skip button click (for testing)"""
        try:
            # Mark as configured with dummy data for testing
            app_state.data_manager.update_wifi_config("TestNetwork", "test123")
            app_state.is_configured = True

            # Navigate to main screen
            nav_manager.navigate_to("main")

        except Exception as e:
            error_handler.handle_error(e, "Skip failed")


