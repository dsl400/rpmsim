



import lvgl as lv
from hardware import dtc_manager

class ClearDTCScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("Clear Diagnostic Trouble Codes")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Add description text
        desc_label = lv.label(self.scr)
        desc_label.set_text("This will clear all DTCs from the selected system.")
        desc_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 10)

        # Create Clear DTC button
        self.clear_btn = lv.btn(self.scr)
        self.clear_btn.set_size(200, 50)
        self.clear_btn.center()
        self.clear_btn.label = lv.label(self.clear_btn)
        self.clear_btn.label.set_text("Clear DTCs")

        # Add event handler for button
        self.clear_btn.add_event_cb(self.on_clear_click, lv.EVENT.CLICKED, None)

    def on_clear_click(self, btn):
        # Show confirmation dialog before clearing
        confirm = lv.confirm(self.scr)
        confirm.set_text("Are you sure you want to clear all DTCs?")
        confirm.align(lv.ALIGN.CENTER, 0, 0)

        # Add event handler for confirmation response
        def on_confirm_response(event):
            if event.code == lv.EVENT.VALUE_CHANGED:
                if event.value:
                    # User confirmed, proceed with clearing DTCs
                    success = dtc_manager.clear_dtc()
                    if success:
                        # Show success message
                        msg = lv.alert(self.scr)
                        msg.set_text("DTCs cleared successfully!")
                    else:
                        # Show error message
                        msg = lv.alert(self.scr)
                        msg.set_text("Failed to clear DTCs")

        confirm.add_event_cb(on_confirm_response, lv.EVENT.VALUE_CHANGED, None)

def create_clear_dtc_screen():
    scr = lv.screen()
    ClearDTCScreen(scr)
    return scr



