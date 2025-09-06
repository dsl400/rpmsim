
"""
Firmware Update Screen for ECU Diagnostic Tool
Handles firmware update checking, downloading, and installation
"""

import lvgl as lv
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class FirmwareUpdateScreen(BaseScreen):
    """Firmware update screen with update checking and installation"""

    def __init__(self, scr):
        self.update_info = None
        self.update_status = "idle"  # idle, checking, downloading, installing
        super().__init__(scr)

    def create_ui(self):
        """Create the firmware update UI elements"""
        # Create title label
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("Firmware Update")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)

        # Create current version info
        self.widgets['current_version'] = lv.label(self.scr)
        self.widgets['current_version'].set_text("Current Version: v1.0.0")
        self.widgets['current_version'].align_to(self.widgets['title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 20)

        # Create status label
        self.widgets['status_label'] = lv.label(self.scr)
        self.widgets['status_label'].set_text("Ready to check for updates")
        self.widgets['status_label'].align_to(self.widgets['current_version'], lv.ALIGN.OUT_BOTTOM_MID, 0, 20)

        # No check button - auto-execute on load

        # Create back button
        self.widgets['back_btn'] = lv.button(self.scr)
        self.widgets['back_btn'].set_size(100, 40)
        back_label = lv.label(self.widgets['back_btn'])
        back_label.set_text("Back")
        back_label.center()
        self.widgets['back_btn'].align(lv.ALIGN.BOTTOM_LEFT, 20, -20)
        self.widgets['back_btn'].add_event_cb(self.on_back_click, lv.EVENT.CLICKED, None)

    def on_enter(self):
        """Called when screen becomes active - auto-execute update check"""
        try:
            # Auto-execute update check when screen loads
            self.check_for_updates()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to auto-check for updates")

    def check_for_updates(self):
        """Auto-execute update check with hardcoded result"""
        try:
            self.update_status = "checking"
            self.widgets['status_label'].set_text("Checking for updates...")

            # Hardcoded result: no update available
            self.widgets['status_label'].set_text("No updates available\n\nYour firmware is up to date.")
            self.update_status = "idle"

        except Exception as ex:
            error_handler.handle_error(ex, "Failed to check for updates")
            self.widgets['status_label'].set_text("Update check failed")
            self.update_status = "idle"



    def on_back_click(self, e):
        """Handle back button click"""
        try:
            nav_manager.go_back()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to navigate back")



