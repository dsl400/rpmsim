
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
        # Remove all padding from the main screen
        self.scr.set_style_pad_all(0, 0)
        self.scr.set_style_border_width(0, 0)

        # Create top toolbar container
        self.widgets['toolbar'] = lv.obj(self.scr)
        self.widgets['toolbar'].set_size(lv.pct(100), 60)  # Full width, 60px height
        self.widgets['toolbar'].align(lv.ALIGN.TOP_MID, 0, 0)
        self.widgets['toolbar'].set_style_bg_color(lv.color_hex(0x2196F3), 0)  # Blue background
        self.widgets['toolbar'].set_style_radius(0, 0)
        self.widgets['toolbar'].set_style_pad_all(0, 0)  # Remove toolbar padding
        self.widgets['toolbar'].set_style_border_width(0, 0)  # Remove toolbar border

        # Create left side menu button
        self.widgets['menu_btn'] = lv.button(self.widgets['toolbar'])
        self.widgets['menu_btn'].set_size(50, 50)
        self.widgets['menu_btn'].align(lv.ALIGN.LEFT_MID, 5, 0)
        self.widgets['menu_btn'].set_style_bg_color(lv.color_hex(0x1976D2), 0)

        menu_label = lv.label(self.widgets['menu_btn'])
        menu_label.set_text(lv.SYMBOL.LIST)
        menu_label.center()

        # Add event handler for menu button click
        self.widgets['menu_btn'].add_event_cb(self.on_menu_click, lv.EVENT.CLICKED, None)

        # Track menu state
        self.menu_modal = None

        # Create center area for selected system and tool name (clickable button)
        self.widgets['title_btn'] = lv.button(self.widgets['toolbar'])
        self.widgets['title_btn'].set_size(300, 50)  # Adjust size as needed
        self.widgets['title_btn'].align(lv.ALIGN.CENTER, 0, 0)
        self.widgets['title_btn'].set_style_bg_color(lv.color_hex(0x1976D2), 0)  # Same as toolbar
        self.widgets['title_btn'].set_style_border_width(0, 0)  # No border
        self.widgets['title_btn'].set_style_shadow_width(0, 0)  # No shadow
        self.widgets['title_btn'].add_event_cb(self.on_title_click, lv.EVENT.CLICKED, None)

        self.widgets['title_label'] = lv.label(self.widgets['title_btn'])
        self.widgets['title_label'].center()
        self.widgets['title_label'].set_style_text_color(lv.color_hex(0xFFFFFF), 0)  # White text
        self.update_title()

        # Create right side wifi status icon
        self.widgets['wifi_icon'] = lv.button(self.widgets['toolbar'])
        self.widgets['wifi_icon'].set_size(50, 50)
        self.widgets['wifi_icon'].align(lv.ALIGN.RIGHT_MID, -5, 0)
        self.widgets['wifi_icon'].set_style_bg_color(lv.color_hex(0x1976D2), 0)
        self.widgets['wifi_icon'].add_event_cb(self.on_wifi_click, lv.EVENT.CLICKED, None)

        self.widgets['wifi_label'] = lv.label(self.widgets['wifi_icon'])
        self.widgets['wifi_label'].center()
        self.update_wifi_status()

        # Create main area for displaying selected ECU tool
        self.widgets['main_area'] = lv.obj(self.scr)
        self.widgets['main_area'].set_size(lv.pct(100), 420)  # 480 - 60 = 420 pixels height
        self.widgets['main_area'].align_to(self.widgets['toolbar'], lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
        self.widgets['main_area'].set_style_pad_all(0, 0)  # Remove padding
        self.widgets['main_area'].set_style_bg_opa(0, 0)  # Make background transparent
        self.widgets['main_area'].set_style_border_width(0, 0)  # Remove border
        self.widgets['main_area'].set_style_margin_all(0, 0)  # Remove margins

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
            self.widgets['wifi_label'].set_text(lv.SYMBOL.WIFI)  # WiFi icon for disconnected
            self.widgets['wifi_label'].set_style_text_color(lv.color_hex(0xF44336), 0)  # Red

    def load_current_tool(self):
        """Load the currently selected tool interface"""
        # Set default system if none selected
        if not app_state.current_system or not app_state.current_tool:
            self.set_default_system()

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

    def set_default_system(self):
        """Set a default system selection"""
        try:
            # Get first available system from database
            systems = app_state.data_manager.get_systems()
            if systems:
                first_system = systems[0]
                app_state.set_current_system(
                    first_system.get('brand', 'VW'),
                    first_system.get('system', 'Engine'),
                    first_system.get('system_name', 'Bosch ME7.9.7'),
                    'RPM Simulator'
                )
                self.update_title()
        except Exception as e:
            print(f"Failed to set default system: {e}")



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

    def on_title_click(self, event):
        """Handle title button click to open system selection"""
        try:
            # Navigate to system selection screen
            nav_manager.navigate_to("system_selection")
        except Exception as e:
            error_handler.handle_error(e, "Failed to open system selection")

    def on_wifi_click(self, event):
        """Handle WiFi button click"""
        try:
            # Show WiFi status or open WiFi settings
            if app_state.wifi_manager and app_state.wifi_manager.is_connected():
                error_handler.show_info_dialog("WiFi Connected", "Currently connected to WiFi network")
            else:
                error_handler.show_info_dialog("WiFi Disconnected", "WiFi is not connected")
        except Exception as e:
            error_handler.handle_error(e, "Failed to show WiFi status")

    def on_menu_click(self, event):
        """Handle menu button click"""
        try:
            # If menu is already open, close it
            if self.menu_modal:
                self.menu_modal.delete()
                self.menu_modal = None
                return

            # Create modal menu with semi-transparent overlay
            self.menu_modal = lv.obj(self.scr)
            self.menu_modal.set_size(lv.pct(100), lv.pct(100))
            self.menu_modal.align(lv.ALIGN.CENTER, 0, 0)
            self.menu_modal.set_style_bg_color(lv.color_hex(0x000000), 0)
            self.menu_modal.set_style_bg_opa(100, 0)  # Semi-transparent overlay
            self.menu_modal.set_style_pad_all(0, 0)  # Remove padding
            self.menu_modal.set_style_border_width(0, 0)  # Remove border

            # Add click handler to close menu when clicking outside
            self.menu_modal.add_event_cb(self.on_menu_background_click, lv.EVENT.CLICKED, None)

            # Create menu container positioned under menu button (extends to bottom)
            menu_container = lv.obj(self.menu_modal)
            menu_container.set_size(200, 420)  # Full height from toolbar to bottom (480 - 60 = 420)
            menu_container.set_style_pad_all(10, 0)  # Add padding inside menu
            menu_container.set_style_border_width(1, 0)
            menu_container.set_style_border_color(lv.color_hex(0xCCCCCC), 0)
            # Remove scrollbars from menu container
            menu_container.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
            menu_container.set_scroll_dir(lv.DIR.NONE)  # Disable scrolling

            # Position menu under the menu button
            menu_container.align_to(self.widgets['menu_btn'], lv.ALIGN.OUT_BOTTOM_LEFT, 0, 5)
            menu_container.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)
            menu_container.set_style_radius(8, 0)

            # Menu buttons (no title, more compact)
            btn_y = 10

            # Check for Updates button (removed Select ECU System)
            update_btn = lv.button(menu_container)
            update_btn.set_size(180, 35)
            update_btn.align(lv.ALIGN.TOP_MID, 0, btn_y)
            update_btn.set_style_bg_color(lv.color_hex(0x2196F3), 0)
            update_label = lv.label(update_btn)
            update_label.set_text("Check for Updates")
            update_label.center()
            update_btn.add_event_cb(lambda e: self.on_menu_select("updates"), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to show menu")

    def on_menu_background_click(self, event):
        """Handle click outside menu to close it"""
        try:
            if self.menu_modal:
                self.menu_modal.delete()
                self.menu_modal = None
        except Exception as e:
            pass  # Ignore errors when closing menu

    def on_menu_select(self, action):
        """Handle menu selection"""
        try:
            # Close menu
            if self.menu_modal:
                self.menu_modal.delete()
                self.menu_modal = None

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

    def on_exit(self):
        """Called when screen becomes inactive"""
        # Close menu if open
        if self.menu_modal:
            self.menu_modal.delete()
            self.menu_modal = None

    def cleanup(self):
        """Clean up resources"""
        if self.current_tool_screen:
            self.current_tool_screen.cleanup()
        super().cleanup()



