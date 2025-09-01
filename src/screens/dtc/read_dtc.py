


import lvgl as lv
from hardware import dtc_manager

class ReadDTCScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("Read Diagnostic Trouble Codes")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Add description text
        desc_label = lv.label(self.scr)
        desc_label.set_text("This will read all DTCs from the selected system.")
        desc_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 10)

        # Create Read DTC button
        self.read_btn = lv.btn(self.scr)
        self.read_btn.set_size(200, 50)
        self.read_btn.center()
        self.read_btn.label = lv.label(self.read_btn)
        self.read_btn.label.set_text("Read DTCs")

        # Add event handler for button
        self.read_btn.add_event_cb(self.on_read_click, lv.EVENT.CLICKED, None)

        # Create area to display DTCs
        self.dtc_list = lv.list(self.scr)
        self.dtc_list.set_size(400, 300)
        self.dtc_list.align(lv.ALIGN.BOTTOM_MID, 0, -10)

    def on_read_click(self, btn):
        # Read DTCs from the system
        dtcs = dtc_manager.read_dtc()

        # Clear any existing DTCs in the list
        self.dtc_list.clear()

        if dtcs:
            for dtc in dtcs:
                # Add each DTC to the list with details
                btn = self.dtc_list.add_btn(f"{dtc['code']}: {dtc['description']}", lv.SYMBOL.WARNING)
                btn.set_user_data(dtc)

                # Show detailed information when a DTC is clicked
                def on_dtc_click(event):
                    dtc_details = event.target.get_user_data()
                    details_screen = lv.screen()
                    title = lv.label(details_screen)
                    title.set_text(f"DTC Details: {dtc_details['code']}")
                    title.align(lv.ALIGN.TOP_MID, 0, 10)

                    # Display detailed information
                    info_label = lv.label(details_screen)
                    info_label.set_text(f"Description: {dtc_details['description']}\nStatus: {dtc_details['status']}")
                    info_label.align_to(title, lv.ALIGN.BOTTOM_MID, 0, 10)

                btn.add_event_cb(on_dtc_click, lv.EVENT.CLICKED, None)
        else:
            # Show message if no DTCs found
            msg = lv.alert(self.scr)
            msg.set_text("No DTCs found")

def create_read_dtc_screen():
    scr = lv.screen()
    ReadDTCScreen(scr)
    return scr


