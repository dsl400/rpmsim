import sys
import os
import lvgl as lv
import task_handler

# Initialize LVGL
lv.init()

# Get the directory of this file (MicroPython doesn't have os.path)
current_dir = os.getcwd()
generated_dir = current_dir + "/generated"

# Add generated directory to sys.path
sys.path.insert(0, generated_dir)

import display

import main_screen

task_handler.TaskHandler()

# Display the appropriate initial screen based on device configuration
main_screen.display_initial_screen()






# try:
#     gui_guider.main()
# except Exception as e:
#     print("Application crashed:", e)