
"""
Main Screen for ECU Diagnostic Tool
Displays toolbar with menu, system/tool info, and WiFi status
Shows the currently selected diagnostic tool interface
"""

import lvgl as lv
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class MainScreen(BaseScreen):
    """Main application screen with toolbar and tool display area"""

    def __init__(self, scr):
        self.current_tool_screen = None
        super().__init__(scr)

    def create_ui(self):
        """Create the main screen UI elements"""
        # Create top toolbar container
        self.widgets['toolbar'] = lv.obj(self.scr)
        self.widgets['toolbar'].set_size(lv.pct(100), 60)  # Full width, 60px height
        self.widgets['toolbar'].align(lv.ALIGN.TOP_MID, 0, 0)
        self.widgets['toolbar'].set_style_bg_color(lv.color_hex(0x2196F3), 0)  # Blue background
        self.widgets['toolbar'].set_style_radius(0, 0)

        # Create left side menu button
        self.widgets['menu_btn'] = lv.btn(self.widgets['toolbar'])
        self.widgets['menu_btn'].set_size(50, 50)
        self.widgets['menu_btn'].align(lv.ALIGN.LEFT_MID, 5, 0)
        self.widgets['menu_btn'].set_style_bg_color(lv.color_hex(0x1976D2), 0)

        menu_label = lv.label(self.widgets['menu_btn'])
        menu_label.set_text(lv.SYMBOL.LIST)
        menu_label.center()

        # Add event handler for menu button click
        self.widgets['menu_btn'].add_event_cb(self.on_menu_click, lv.EVENT.CLICKED, None)

        # Create center area for selected system and tool name
        self.widgets['title_label'] = lv.label(self.widgets['toolbar'])
        self.widgets['title_label'].align(lv.ALIGN.CENTER, 0, 0)
        self.widgets['title_label'].set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White text
        self.update_title()

        # Create right side wifi status icon
        self.widgets['wifi_icon'] = lv.btn(self.widgets['toolbar'])
        self.widgets['wifi_icon'].set_size(50, 50)
        self.widgets['wifi_icon'].align(lv.ALIGN.RIGHT_MID, -5, 0)
        self.widgets['wifi_icon'].set_style_bg_color(lv.color_hex(0x1976D2), 0)

        self.widgets['wifi_label'] = lv.label(self.widgets['wifi_icon'])
        self.widgets['wifi_label'].center()
        self.update_wifi_status()

        # Create main area for displaying selected ECU tool
        self.widgets['main_area'] = lv.obj(self.scr)
        self.widgets['main_area'].set_size(lv.pct(100), lv.pct(100) - 60)
        self.widgets['main_area'].align_to(self.widgets['toolbar'], lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        self.widgets['main_area'].set_style_pad_all(10, 0)

        # Load the current tool if available
        self.load_current_tool()

    def update_title(self):
        """Update the title label with current system information"""
        display_text = app_state.get_current_system_display()
        self.widgets['title_label'].set_text(display_text)

    def update_wifi_status(self):
        """Update WiFi status icon"""
        if app_state.wifi_manager and app_state.wifi_manager.is_connected():
            self.widgets['wifi_label'].set_text(lv.SYMBOL.WIFI)
            self.widgets['wifi_label'].set_style_text_color(lv.color_hex(0x4CAF50), 0)  # Green
        else:
            self.widgets['wifi_label'].set_text(lv.SYMBOL.CLOSE)
            self.widgets['wifi_label'].set_style_text_color(lv.color_hex(0xF44336), 0)  # Red

    def load_current_tool(self):
        """Load the currently selected tool interface"""
        if not app_state.current_system or not app_state.current_tool:
            # Show welcome message if no tool selected
            self.show_welcome_message()
            return

        # Clear existing tool screen
        if self.current_tool_screen:
            self.current_tool_screen.cleanup()
            self.current_tool_screen = None

        # Load the appropriate tool based on current selection
        tool_name = app_state.current_tool
        if tool_name == "RPM Simulator":
            self.load_rpm_simulator()
        else:
            # Show placeholder for other tools
            self.show_tool_placeholder(tool_name)

    def show_welcome_message(self):
        """Show welcome message when no system is selected"""
        welcome_label = lv.label(self.widgets['main_area'])
        welcome_label.set_text("Welcome to ECU Diagnostic Tool\n\nPlease select a system from the menu to begin.")
        welcome_label.center()
        welcome_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

    def load_rpm_simulator(self):
        """Load the RPM simulator tool"""
        try:
            # Import here to avoid circular imports
            from screens.rpm_simulator.rpm_simulator_screen import RPMSimulatorScreen

            # Create RPM simulator screen in the main area
            tool_container = lv.obj(self.widgets['main_area'])
            tool_container.set_size(lv.pct(100), lv.pct(100))
            tool_container.align(lv.ALIGN.CENTER, 0, 0)

            self.current_tool_screen = RPMSimulatorScreen(tool_container)

        except ImportError:
            self.show_tool_placeholder("RPM Simulator")

    def show_tool_placeholder(self, tool_name):
        """Show placeholder for tools not yet implemented"""
        placeholder_label = lv.label(self.widgets['main_area'])
        placeholder_label.set_text(f"{tool_name}\n\n(Coming in Phase 2)")
        placeholder_label.center()
        placeholder_label.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

    def on_menu_click(self, event):
        """Handle menu button click"""
        try:
            # Create modal menu
            menu_modal = lv.obj(self.scr)
            menu_modal.set_size(lv.pct(100), lv.pct(100))
            menu_modal.align(lv.ALIGN.CENTER, 0, 0)
            menu_modal.set_style_bg_color(lv.color_hex(0x000000), 0)
            menu_modal.set_style_bg_opa(128, 0)  # Semi-transparent background

            # Create menu container
            menu_container = lv.obj(menu_modal)
            menu_container.set_size(300, 200)
            menu_container.center()
            menu_container.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
            menu_container.set_style_radius(10, 0)

            # Menu title
            title = lv.label(menu_container)
            title.set_text("Menu")
            title.align(lv.ALIGN.TOP_MID, 0, 10)
            title.set_style_text_font(lv.font_default(), 0)

            # Menu buttons
            btn_y = 50

            # Select ECU button
            select_btn = lv.btn(menu_container)
            select_btn.set_size(250, 40)
            select_btn.align(lv.ALIGN.TOP_MID, 0, btn_y)
            select_label = lv.label(select_btn)
            select_label.set_text("Select ECU System")
            select_label.center()
            select_btn.add_event_cb(lambda e: self.on_menu_select("select_ecu", menu_modal), lv.EVENT.CLICKED, None)

            # Check for Updates button
            update_btn = lv.btn(menu_container)
            update_btn.set_size(250, 40)
            update_btn.align(lv.ALIGN.TOP_MID, 0, btn_y + 50)
            update_label = lv.label(update_btn)
            update_label.set_text("Check for Updates")
            update_label.center()
            update_btn.add_event_cb(lambda e: self.on_menu_select("updates", menu_modal), lv.EVENT.CLICKED, None)

            # Close button
            close_btn = lv.btn(menu_container)
            close_btn.set_size(100, 30)
            close_btn.align(lv.ALIGN.BOTTOM_RIGHT, -10, -10)
            close_label = lv.label(close_btn)
            close_label.set_text("Close")
            close_label.center()
            close_btn.add_event_cb(lambda e: menu_modal.delete(), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to show menu")

    def on_menu_select(self, action, menu_modal):
        """Handle menu selection"""
        try:
            # Close menu
            menu_modal.delete()

            if action == "select_ecu":
                nav_manager.navigate_to("system_selection")
            elif action == "updates":
                # Navigate to firmware update screen (to be implemented)
                error_handler.show_info_dialog("Firmware update feature coming soon!")

        except Exception as e:
            error_handler.handle_error(e, f"Failed to handle menu action: {action}")

    def on_enter(self):
        """Called when screen becomes active"""
        # Update title and WiFi status
        self.update_title()
        self.update_wifi_status()

        # Reload current tool in case system changed
        self.load_current_tool()

    def cleanup(self):
        """Clean up resources"""
        if self.current_tool_screen:
            self.current_tool_screen.cleanup()
        super().cleanup()



