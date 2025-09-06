"""
RPM Simulator Screen for ECU Diagnostic Tool
Provides RPM simulation with real-time display, controls, and sensor configuration
"""

import lvgl as lv
import time
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class RPMSimulatorScreen(BaseScreen):
    """RPM simulator tool screen"""
    
    def __init__(self, scr):
        self.current_rpm = 800  # Default idle RPM
        self.simulation_active = False
        self.update_timer = None
        self.camshaft_enabled = True  # Camshaft signal enabled by default
        self.crankshaft_enabled = True  # Crankshaft signal enabled by default
        super().__init__(scr)

    def create_ui(self):
        """Create the RPM simulator UI"""
        # Title
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("RPM Simulator")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)

        # RPM Display (large)
        self.widgets['rpm_display'] = lv.label(self.scr)
        self.widgets['rpm_display'].align(lv.ALIGN.TOP_MID, 0, 60)

        self.update_rpm_display()

        # RPM Slider
        self.widgets['rpm_slider'] = lv.slider(self.scr)
        self.widgets['rpm_slider'].set_size(400, 20)
        self.widgets['rpm_slider'].set_range(0, 8000)
        self.widgets['rpm_slider'].set_value(self.current_rpm, False)
        self.widgets['rpm_slider'].align(lv.ALIGN.TOP_MID, 0, 120)
        # Enable slider event handling with improved error handling
        self.widgets['rpm_slider'].add_event_cb(self.on_slider_change, lv.EVENT.VALUE_CHANGED, None)

        # Slider labels
        self.widgets['slider_min'] = lv.label(self.scr)
        self.widgets['slider_min'].set_text("0")
        self.widgets['slider_min'].align_to(self.widgets['rpm_slider'], lv.ALIGN.OUT_LEFT_MID, -10, 0)

        self.widgets['slider_max'] = lv.label(self.scr)
        self.widgets['slider_max'].set_text("8000")
        self.widgets['slider_max'].align_to(self.widgets['rpm_slider'], lv.ALIGN.OUT_RIGHT_MID, 10, 0)

        # Control buttons row
        self.create_control_buttons()

        # Configuration button (aligned with WiFi button vertically)
        self.widgets['config_btn'] = lv.button(self.scr)
        self.widgets['config_btn'].set_size(50, 50)
        self.widgets['config_btn'].align(lv.ALIGN.TOP_RIGHT, -20, 5)  # Align with toolbar WiFi button (5px from top)
        self.widgets['config_btn'].set_style_bg_color(lv.color_hex(0xFFFFFF), 0)  # White background
        self.widgets['config_btn'].set_style_border_width(0, 0)  # No contour
        self.widgets['config_btn'].set_style_shadow_width(0, 0)  # No shadow
        config_label = lv.label(self.widgets['config_btn'])
        config_label.set_text(lv.SYMBOL.SETTINGS)  # Gear icon
        config_label.set_style_text_color(lv.color_hex(0x666666), 0)  # Gray icon
        config_label.center()
        self.widgets['config_btn'].add_event_cb(self.on_config_click, lv.EVENT.CLICKED, None)

    def create_control_buttons(self):
        """Create RPM control buttons"""
        # Bottom row controls - all on the same line
        bottom_y = -20  # Distance from bottom

        # Camshaft toggle button (bottom left)
        self.widgets['cam_toggle_btn'] = lv.button(self.scr)
        self.widgets['cam_toggle_btn'].set_size(80, 40)
        self.widgets['cam_toggle_btn'].align(lv.ALIGN.BOTTOM_LEFT, 20, bottom_y)
        self.widgets['cam_toggle_btn'].set_style_border_width(2, 0)
        self.widgets['cam_toggle_btn'].set_style_radius(5, 0)
        self.widgets['cam_toggle_label'] = lv.label(self.widgets['cam_toggle_btn'])
        self.widgets['cam_toggle_label'].set_text("CAM")
        self.widgets['cam_toggle_label'].center()
        self.widgets['cam_toggle_btn'].add_event_cb(self.on_cam_toggle, lv.EVENT.CLICKED, None)

        # Crankshaft toggle button (bottom center-left)
        self.widgets['crank_toggle_btn'] = lv.button(self.scr)
        self.widgets['crank_toggle_btn'].set_size(80, 40)
        self.widgets['crank_toggle_btn'].align(lv.ALIGN.BOTTOM_LEFT, 110, bottom_y)
        self.widgets['crank_toggle_btn'].set_style_border_width(2, 0)
        self.widgets['crank_toggle_btn'].set_style_radius(5, 0)
        self.widgets['crank_toggle_label'] = lv.label(self.widgets['crank_toggle_btn'])
        self.widgets['crank_toggle_label'].set_text("CRANK")
        self.widgets['crank_toggle_label'].center()
        self.widgets['crank_toggle_btn'].add_event_cb(self.on_crank_toggle, lv.EVENT.CLICKED, None)

        # Start/Stop button (bottom right, with play/stop icons and contour)
        self.widgets['start_stop_btn'] = lv.button(self.scr)
        self.widgets['start_stop_btn'].set_size(60, 60)
        self.widgets['start_stop_btn'].align(lv.ALIGN.BOTTOM_RIGHT, -20, bottom_y)
        self.widgets['start_stop_btn'].set_style_bg_color(lv.color_hex(0x4CAF50), 0)
        self.widgets['start_stop_btn'].set_style_border_width(2, 0)  # Add contour
        self.widgets['start_stop_btn'].set_style_border_color(lv.color_hex(0x2E7D32), 0)  # Darker green border
        self.widgets['start_stop_btn'].set_style_radius(30, 0)  # Make it circular
        self.widgets['start_stop_label'] = lv.label(self.widgets['start_stop_btn'])
        self.widgets['start_stop_label'].center()
        self.widgets['start_stop_btn'].add_event_cb(self.on_start_stop_click, lv.EVENT.CLICKED, None)

        # Update all button states
        self.update_start_stop_button()
        self.update_toggle_buttons()

    def update_rpm_display(self):
        """Update the RPM display"""
        if 'rpm_display' in self.widgets:
            self.widgets['rpm_display'].set_text(f"{self.current_rpm} RPM")
        if 'rpm_slider' in self.widgets:
            self.widgets['rpm_slider'].set_value(self.current_rpm, False)

    def update_start_stop_button(self):
        """Update start/stop button with play/stop icons"""
        if self.simulation_active:
            self.widgets['start_stop_label'].set_text(lv.SYMBOL.STOP)  # Stop icon
            self.widgets['start_stop_btn'].set_style_bg_color(lv.color_hex(0xF44336), 0)  # Red
            self.widgets['start_stop_btn'].set_style_border_color(lv.color_hex(0xC62828), 0)  # Darker red border
        else:
            self.widgets['start_stop_label'].set_text(lv.SYMBOL.PLAY)  # Play icon
            self.widgets['start_stop_btn'].set_style_bg_color(lv.color_hex(0x4CAF50), 0)  # Green
            self.widgets['start_stop_btn'].set_style_border_color(lv.color_hex(0x2E7D32), 0)  # Darker green border

    def update_toggle_buttons(self):
        """Update toggle button states"""
        # Update camshaft button
        if self.camshaft_enabled:
            self.widgets['cam_toggle_btn'].set_style_bg_color(lv.color_hex(0x4CAF50), 0)  # Green
            self.widgets['cam_toggle_btn'].set_style_border_color(lv.color_hex(0x2E7D32), 0)  # Dark green border
        else:
            self.widgets['cam_toggle_btn'].set_style_bg_color(lv.color_hex(0x9E9E9E), 0)  # Gray
            self.widgets['cam_toggle_btn'].set_style_border_color(lv.color_hex(0x616161), 0)  # Dark gray border

        # Update crankshaft button
        if self.crankshaft_enabled:
            self.widgets['crank_toggle_btn'].set_style_bg_color(lv.color_hex(0x4CAF50), 0)  # Green
            self.widgets['crank_toggle_btn'].set_style_border_color(lv.color_hex(0x2E7D32), 0)  # Dark green border
        else:
            self.widgets['crank_toggle_btn'].set_style_bg_color(lv.color_hex(0x9E9E9E), 0)  # Gray
            self.widgets['crank_toggle_btn'].set_style_border_color(lv.color_hex(0x616161), 0)  # Dark gray border

    def on_cam_toggle(self, event):
        """Handle camshaft toggle button click"""
        try:
            self.camshaft_enabled = not self.camshaft_enabled
            self.update_toggle_buttons()

            # Update ECU simulation if active
            if self.simulation_active and app_state.ecu_manager:
                app_state.ecu_manager.set_camshaft_signal(self.camshaft_enabled)

        except Exception as e:
            print(f"Camshaft toggle error: {e}")

    def on_crank_toggle(self, event):
        """Handle crankshaft toggle button click"""
        try:
            self.crankshaft_enabled = not self.crankshaft_enabled
            self.update_toggle_buttons()

            # Update ECU simulation if active
            if self.simulation_active and app_state.ecu_manager:
                app_state.ecu_manager.set_crankshaft_signal(self.crankshaft_enabled)

        except Exception as e:
            print(f"Crankshaft toggle error: {e}")



    def on_slider_change(self, event):
        """Handle slider value change"""
        try:
            # Get the slider widget directly from our widgets dict
            slider = self.widgets.get('rpm_slider')
            if slider:
                # Get the current value from the slider
                new_rpm = slider.get_value()

                # Update the current RPM and display
                self.current_rpm = new_rpm
                self.update_rpm_display()

                # Update ECU simulation if active
                if self.simulation_active and app_state.ecu_manager:
                    app_state.ecu_manager.simulate_rpm(self.current_rpm)

        except Exception as e:
            # Print error for debugging but don't show dialog
            print(f"Slider update error: {e}")

    def on_start_stop_click(self, event):
        """Handle start/stop button click"""
        try:
            if self.simulation_active:
                self.stop_simulation()
            else:
                self.start_simulation()
                
        except Exception as e:
            error_handler.handle_error(e, "Failed to toggle simulation")

    def start_simulation(self):
        """Start RPM simulation"""
        try:
            if app_state.ecu_manager:
                app_state.ecu_manager.simulate_rpm(self.current_rpm)
                app_state.ecu_manager.start_simulation()

            self.simulation_active = True
            self.update_start_stop_button()

        except Exception as e:
            error_handler.handle_error(e, "Failed to start simulation")

    def stop_simulation(self):
        """Stop RPM simulation"""
        try:
            if app_state.ecu_manager:
                app_state.ecu_manager.stop_simulation()

            self.simulation_active = False
            self.update_start_stop_button()

        except Exception as e:
            error_handler.handle_error(e, "Failed to stop simulation")

    def on_config_click(self, event):
        """Handle configuration button click"""
        try:
            # Navigate to sensor configuration screen (to be implemented)
            error_handler.show_info_dialog("Sensor configuration screen coming soon!")
            
        except Exception as e:
            error_handler.handle_error(e, "Failed to open configuration")

    def on_enter(self):
        """Called when screen becomes active"""
        # Load current tool configuration
        if app_state.current_system and app_state.current_tool:
            config = app_state.get_tool_config(
                app_state.current_system['brand'],
                app_state.current_system['system'],
                app_state.current_system['system_name'],
                app_state.current_tool
            )
            if config:
                # Apply configuration to ECU manager
                if app_state.ecu_manager:
                    app_state.ecu_manager.configure_sensors(config)

    def cleanup(self):
        """Clean up resources"""
        if self.simulation_active:
            self.stop_simulation()
        super().cleanup()
