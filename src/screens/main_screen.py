



import lvgl as lv
from hardware import wifi_manager
from screens.system_selection import create_system_selection_screen
from screens.firmware_update import create_firmware_update_screen
from screens.system_info import create_system_info_screen

class MainScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create top toolbar container
        self.toolbar = lv.obj(self.scr)
        self.toolbar.set_size(lv.pct(100), 50)  # Full width, 50px height
        self.toolbar.align(lv.ALIGN.TOP_MID, 0, 0)

        # Create left side menu button
        self.menu_btn = lv.btn(self.toolbar)
        self.menu_btn.set_size(50, 50)  # 50x50px
        self.menu_btn.align(lv.ALIGN.LEFT_MID, 10, 0)
        self.menu_btn.label = lv.label(self.menu_btn)
        self.menu_btn.label.set_text("≡")  # Menu icon

        # Add event handler for menu button click
        self.menu_btn.add_event_cb(self.on_menu_click, lv.EVENT.CLICKED, None)

        # Create center area for selected system and tool name
        self.title_label = lv.label(self.toolbar)
        self.title_label.align(lv.ALIGN.CENTER, 0, 0)
        self.title_label.set_text("Main Screen")

        # Create right side wifi status icon
        self.wifi_icon = lv.imgbtn(self.toolbar)
        self.wifi_icon.set_size(32, 32)  # 32x32px
        self.wifi_icon.align(lv.ALIGN.RIGHT_MID, -10, 0)

        # Load wifi status icon based on connection status
        if wifi_manager.is_connected():
            self.wifi_icon.set_src(lv.SYMBOL.WIFI)
        else:
            self.wifi_icon.set_src(lv.SYMBOL.CLOSE)

        # Create main area for displaying selected ECU tool
        self.main_area = lv.obj(self.scr)
        self.main_area.set_size(lv.pct(100), lv.pct(100) - 50)  # Full width, remaining height after toolbar
        self.main_area.align_to(self.toolbar, lv.ALIGN.BOTTOM_MID, 0, 0)

    def on_menu_click(self, btn):
        # Create a dropdown menu with options
        menu = lv.dropdown(self.scr)
        menu.set_options("\n".join([
            "Select ECU",
            "Check for Updates",
            "System Info"
        ]))
        menu.align(lv.ALIGN.TOP_LEFT, 10, 50)

        # Add event handler for menu selection
        def on_menu_select(event):
            selected = event.target.get_selected_str()

            if selected == "Select ECU":
                # Display system selection screen
                create_system_selection_screen()
            elif selected == "Check for Updates":
                # Display firmware update screen
                create_firmware_update_screen()
            elif selected == "System Info":
                # Display system information screen
                create_system_info_screen()

        menu.add_event_cb(on_menu_select, lv.EVENT.VALUE_CHANGED, None)

def create_main_screen():
    scr = lv.screen()
    MainScreen(scr)
    return scr



