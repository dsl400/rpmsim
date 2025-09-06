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
        super().__init__(scr)

    def create_ui(self):
        """Create the RPM simulator UI"""
        # Title
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("RPM Simulator")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 10)
        self.widgets['title'].set_style_text_font(lv.font_default(), 0)

        # RPM Display (large)
        self.widgets['rpm_display'] = lv.label(self.scr)
        self.widgets['rpm_display'].align(lv.ALIGN.TOP_MID, 0, 50)
        self.widgets['rpm_display'].set_style_text_font(lv.font_default(), 0)
        self.update_rpm_display()

        # RPM Slider
        self.widgets['rpm_slider'] = lv.slider(self.scr)
        self.widgets['rpm_slider'].set_size(400, 20)
        self.widgets['rpm_slider'].set_range(0, 8000)
        self.widgets['rpm_slider'].set_value(self.current_rpm)
        self.widgets['rpm_slider'].align(lv.ALIGN.TOP_MID, 0, 120)
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

        # Simulation status
        self.widgets['status_label'] = lv.label(self.scr)
        self.widgets['status_label'].align(lv.ALIGN.TOP_MID, 0, 250)
        self.update_status_display()

        # Configuration button
        self.widgets['config_btn'] = lv.btn(self.scr)
        self.widgets['config_btn'].set_size(200, 40)
        config_label = lv.label(self.widgets['config_btn'])
        config_label.set_text("Sensor Configuration")
        config_label.center()
        self.widgets['config_btn'].align(lv.ALIGN.BOTTOM_MID, 0, -20)
        self.widgets['config_btn'].add_event_cb(self.on_config_click, lv.EVENT.CLICKED, None)

    def create_control_buttons(self):
        """Create RPM control buttons"""
        button_y = 180
        
        # Decrease buttons
        self.widgets['dec_100_btn'] = lv.btn(self.scr)
        self.widgets['dec_100_btn'].set_size(80, 40)
        dec_100_label = lv.label(self.widgets['dec_100_btn'])
        dec_100_label.set_text("-100")
        dec_100_label.center()
        self.widgets['dec_100_btn'].align(lv.ALIGN.TOP_LEFT, 50, button_y)
        self.widgets['dec_100_btn'].add_event_cb(lambda e: self.adjust_rpm(-100), lv.EVENT.CLICKED, None)

        self.widgets['dec_10_btn'] = lv.btn(self.scr)
        self.widgets['dec_10_btn'].set_size(80, 40)
        dec_10_label = lv.label(self.widgets['dec_10_btn'])
        dec_10_label.set_text("-10")
        dec_10_label.center()
        self.widgets['dec_10_btn'].align_to(self.widgets['dec_100_btn'], lv.ALIGN.OUT_RIGHT_MID, 10, 0)
        self.widgets['dec_10_btn'].add_event_cb(lambda e: self.adjust_rpm(-10), lv.EVENT.CLICKED, None)

        # Start/Stop button
        self.widgets['start_stop_btn'] = lv.btn(self.scr)
        self.widgets['start_stop_btn'].set_size(100, 40)
        self.widgets['start_stop_label'] = lv.label(self.widgets['start_stop_btn'])
        self.widgets['start_stop_label'].center()
        self.widgets['start_stop_btn'].align(lv.ALIGN.TOP_MID, 0, button_y)
        self.widgets['start_stop_btn'].add_event_cb(self.on_start_stop_click, lv.EVENT.CLICKED, None)
        self.update_start_stop_button()

        # Increase buttons
        self.widgets['inc_10_btn'] = lv.btn(self.scr)
        self.widgets['inc_10_btn'].set_size(80, 40)
        inc_10_label = lv.label(self.widgets['inc_10_btn'])
        inc_10_label.set_text("+10")
        inc_10_label.center()
        self.widgets['inc_10_btn'].align(lv.ALIGN.TOP_RIGHT, -140, button_y)
        self.widgets['inc_10_btn'].add_event_cb(lambda e: self.adjust_rpm(10), lv.EVENT.CLICKED, None)

        self.widgets['inc_100_btn'] = lv.btn(self.scr)
        self.widgets['inc_100_btn'].set_size(80, 40)
        inc_100_label = lv.label(self.widgets['inc_100_btn'])
        inc_100_label.set_text("+100")
        inc_100_label.center()
        self.widgets['inc_100_btn'].align_to(self.widgets['inc_10_btn'], lv.ALIGN.OUT_RIGHT_MID, 10, 0)
        self.widgets['inc_100_btn'].add_event_cb(lambda e: self.adjust_rpm(100), lv.EVENT.CLICKED, None)

    def update_rpm_display(self):
        """Update the RPM display"""
        self.widgets['rpm_display'].set_text(f"{self.current_rpm} RPM")
        self.widgets['rpm_slider'].set_value(self.current_rpm)

    def update_status_display(self):
        """Update simulation status display"""
        if self.simulation_active:
            self.widgets['status_label'].set_text("Simulation: ACTIVE")
            self.widgets['status_label'].set_style_text_color(lv.color_hex(0x4CAF50), 0)  # Green
        else:
            self.widgets['status_label'].set_text("Simulation: STOPPED")
            self.widgets['status_label'].set_style_text_color(lv.color_hex(0xF44336), 0)  # Red

    def update_start_stop_button(self):
        """Update start/stop button text"""
        if self.simulation_active:
            self.widgets['start_stop_label'].set_text("STOP")
            self.widgets['start_stop_btn'].set_style_bg_color(lv.color_hex(0xF44336), 0)  # Red
        else:
            self.widgets['start_stop_label'].set_text("START")
            self.widgets['start_stop_btn'].set_style_bg_color(lv.color_hex(0x4CAF50), 0)  # Green

    def adjust_rpm(self, delta):
        """Adjust RPM by delta amount"""
        try:
            new_rpm = max(0, min(8000, self.current_rpm + delta))
            self.current_rpm = new_rpm
            self.update_rpm_display()
            
            # Update ECU manager if simulation is active
            if self.simulation_active and app_state.ecu_manager:
                app_state.ecu_manager.simulate_rpm(self.current_rpm)
                
        except Exception as e:
            error_handler.handle_error(e, "Failed to adjust RPM")

    def on_slider_change(self, event):
        """Handle slider value change"""
        try:
            self.current_rpm = event.target.get_value()
            self.update_rpm_display()
            
            # Update ECU manager if simulation is active
            if self.simulation_active and app_state.ecu_manager:
                app_state.ecu_manager.simulate_rpm(self.current_rpm)
                
        except Exception as e:
            error_handler.handle_error(e, "Failed to update RPM from slider")

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
            self.update_status_display()
            self.update_start_stop_button()
            
        except Exception as e:
            error_handler.handle_error(e, "Failed to start simulation")

    def stop_simulation(self):
        """Stop RPM simulation"""
        try:
            if app_state.ecu_manager:
                app_state.ecu_manager.stop_simulation()
                
            self.simulation_active = False
            self.update_status_display()
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
