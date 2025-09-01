



import lvgl as lv
from hardware import wifi_manager

def create_firmware_update_screen():
    """Create the firmware update screen"""
    scr = lv.screen()
    title_label = lv.label(scr)
    title_label.set_text("Check for Firmware Updates")
    title_label.center()

    # Check for updates and show status
    if wifi_manager.check_for_updates():
        msg_label = lv.label(scr)
        msg_label.set_text("Firmware update available!")
        msg_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 20)
    else:
        msg_label = lv.label(scr)
        msg_label.set_text("No firmware updates found.")
        msg_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 20)

    return scr



