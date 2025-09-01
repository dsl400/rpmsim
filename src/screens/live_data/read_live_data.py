

import lvgl as lv
from hardware import ecu_manager

class ReadLiveDataScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("Read Live Data")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Add description text
        desc_label = lv.label(self.scr)
        desc_label.set_text("This will read live data from the selected system.")
        desc_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 10)

        # Create Read Live Data button
        self.read_btn = lv.btn(self.scr)
        self.read_btn.set_size(200, 50)
        self.read_btn.center()
        self.read_btn.label = lv.label(self.read_btn)
        self.read_btn.label.set_text("Read Live Data")

        # Add event handler for button
        self.read_btn.add_event_cb(self.on_read_click, lv.EVENT.CLICKED, None)

        # Create area to display live data
        self.data_container = lv.obj(self.scr)
        self.data_container.set_size(400, 300)
        self.data_container.align(lv.ALIGN.BOTTOM_MID, 0, -10)

    def on_read_click(self, btn):
        # Start reading live data
        self.read_live_data()

    def read_live_data(self):
        # Read live data from the ECU at regular intervals
        while True:
            # Get live data from the ECU
            live_data = ecu_manager.get_live_data()

            # Update display with new data
            self.update_display(live_data)

            # Wait for a short period before reading again
            lv.delay(1000)  # Update every second

    def update_display(self, data):
        # Clear any existing data in the container
        self.data_container.clean()

        # Display each piece of live data
        y_pos = 0
        for key, value in data.items():
            label = lv.label(self.data_container)
            label.set_text(f"{key}: {value}")
            label.align(lv.ALIGN.TOP_LEFT, 0, y_pos)
            y_pos += 20

def create_read_live_data_screen():
    scr = lv.screen()
    ReadLiveDataScreen(scr)
    return scr

