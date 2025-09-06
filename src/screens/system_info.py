

"""
System Information Screen for ECU Diagnostic Tool
Displays device information, firmware version, and system status
"""

import lvgl as lv
import sys
import gc
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class SystemInfoScreen(BaseScreen):
    """System information screen displaying device and firmware details"""

    def __init__(self, scr):
        super().__init__(scr)

    def create_ui(self):
        """Create the system information UI elements"""
        # Create title label
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("System Information")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)

        # Create scrollable container for info
        self.widgets['info_container'] = lv.obj(self.scr)
        self.widgets['info_container'].set_size(700, 350)
        self.widgets['info_container'].align_to(self.widgets['title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 20)
        self.widgets['info_container'].set_style_pad_all(20, 0)
        self.widgets['info_container'].set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)

        # Create info sections
        self.create_firmware_info()
        self.create_hardware_info()
        self.create_memory_info()
        self.create_network_info()

        # Create back button
        self.widgets['back_btn'] = lv.button(self.scr)
        self.widgets['back_btn'].set_size(100, 40)
        back_label = lv.label(self.widgets['back_btn'])
        back_label.set_text("Back")
        back_label.center()
        self.widgets['back_btn'].align(lv.ALIGN.BOTTOM_LEFT, 20, -20)
        self.widgets['back_btn'].add_event_cb(self.on_back_click, lv.EVENT.CLICKED, None)

        # Create refresh button
        self.widgets['refresh_btn'] = lv.button(self.scr)
        self.widgets['refresh_btn'].set_size(100, 40)
        refresh_label = lv.label(self.widgets['refresh_btn'])
        refresh_label.set_text("Refresh")
        refresh_label.center()
        self.widgets['refresh_btn'].align(lv.ALIGN.BOTTOM_RIGHT, -20, -20)
        self.widgets['refresh_btn'].add_event_cb(self.on_refresh_click, lv.EVENT.CLICKED, None)

    def create_firmware_info(self):
        """Create firmware information section"""
        # Firmware section title
        fw_title = lv.label(self.widgets['info_container'])
        fw_title.set_text("Firmware Information")
        fw_title.align(lv.ALIGN.TOP_LEFT, 0, 0)
        fw_title.set_style_text_font(lv.font_default(), 0)

        # Firmware details
        fw_info = lv.label(self.widgets['info_container'])
        fw_text = (
            "Version: v1.0.0\n"
            "Build Date: 2024-01-15\n"
            "Build Type: Simulation\n"
            "Git Commit: abc123def\n"
        )
        fw_info.set_text(fw_text)
        fw_info.align_to(fw_title, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

    def create_hardware_info(self):
        """Create hardware information section"""
        # Hardware section title
        hw_title = lv.label(self.widgets['info_container'])
        hw_title.set_text("Hardware Information")
        hw_title.align(lv.ALIGN.TOP_LEFT, 0, 120)

        # Hardware details
        hw_info = lv.label(self.widgets['info_container'])
        try:
            platform = sys.platform if hasattr(sys, 'platform') else 'Unknown'
            implementation = sys.implementation.name if hasattr(sys, 'implementation') else 'Unknown'
            hw_text = (
                f"Platform: {platform}\n"
                f"Implementation: {implementation}\n"
                "Device: ESP32-S3 (Simulated)\n"
                "Display: 800x480 TFT\n"
                "Storage: 16MB Flash\n"
            )
        except Exception:
            hw_text = "Hardware information unavailable"

        hw_info.set_text(hw_text)
        hw_info.align_to(hw_title, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

    def create_memory_info(self):
        """Create memory information section"""
        # Memory section title
        mem_title = lv.label(self.widgets['info_container'])
        mem_title.set_text("Memory Information")
        mem_title.align(lv.ALIGN.TOP_LEFT, 0, 240)

        # Memory details
        self.widgets['mem_info'] = lv.label(self.widgets['info_container'])
        self.update_memory_info()
        self.widgets['mem_info'].align_to(mem_title, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

    def create_network_info(self):
        """Create network information section"""
        # Network section title
        net_title = lv.label(self.widgets['info_container'])
        net_title.set_text("Network Information")
        net_title.align(lv.ALIGN.TOP_LEFT, 350, 0)

        # Network details
        self.widgets['net_info'] = lv.label(self.widgets['info_container'])
        self.update_network_info()
        self.widgets['net_info'].align_to(net_title, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)

    def update_memory_info(self):
        """Update memory information"""
        try:
            # Force garbage collection to get accurate memory info
            gc.collect()

            # Get memory info (this may not work in all environments)
            try:
                mem_info = lv.mem_monitor()
                mem_text = (
                    f"Total RAM: {mem_info.total_size} bytes\n"
                    f"Used RAM: {mem_info.used_size} bytes\n"
                    f"Free RAM: {mem_info.free_size} bytes\n"
                    f"Fragmentation: {mem_info.frag_pct}%\n"
                )
            except:
                mem_text = "Memory info unavailable\n(Simulation mode)\n"

            self.widgets['mem_info'].set_text(mem_text)
        except Exception as e:
            self.widgets['mem_info'].set_text("Memory info error")

    def update_network_info(self):
        """Update network information"""
        try:
            if app_state.wifi_manager:
                wifi_info = app_state.wifi_manager.get_connection_info()
                if wifi_info.get('connected', False):
                    net_text = (
                        f"Status: Connected\n"
                        f"SSID: {wifi_info.get('ssid', 'Unknown')}\n"
                        f"IP: {wifi_info.get('ip', 'Unknown')}\n"
                        f"Signal: {wifi_info.get('signal_strength', 0)}%\n"
                    )
                else:
                    net_text = "Status: Disconnected\n"
            else:
                net_text = "WiFi Manager: Not available\n"

            self.widgets['net_info'].set_text(net_text)
        except Exception as e:
            self.widgets['net_info'].set_text("Network info error")

    def on_refresh_click(self, e):
        """Handle refresh button click"""
        try:
            self.update_memory_info()
            self.update_network_info()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to refresh system info")

    def on_back_click(self, e):
        """Handle back button click"""
        try:
            nav_manager.go_back()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to navigate back")



