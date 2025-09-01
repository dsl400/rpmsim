



import lvgl as lv
import sys

def create_system_info_screen():
    """Create the system information screen"""
    scr = lv.screen()
    title_label = lv.label(scr)
    title_label.set_text("System Information")
    title_label.center()

    # Display basic system info
    info_label = lv.label(scr)
    info_label.set_text(f"Firmware Version: 1.0.0\nDevice ID: {sys.implementation._machine}\nMemory: {lv.mem_monitor()}")
    info_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 20)

    return scr



