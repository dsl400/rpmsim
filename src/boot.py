
from machine import UART
import os
try:
    uart = UART(0, baudrate=115200, tx=44, rx=43)
    os.dupterm(uart)
except: 
    pass

# # boot.py — IRQ long-press (>3s) moves main.py->main.bad; no resets/prints

# import machine, micropython, uos

# SAFE_PIN  = 0          # BOOT button GPIO (pull-up)
# MAIN_FILE = "main.py"
# BAK_FILE  = "main.bak"
# LONG_MS   = 3000
# _SOFT_RESET_ = "_soft_reset_"  # Marker file for soft reset detection
# import time




# def _exists(p):
#     try:
#         uos.stat(p); return True
#     except OSError:
#         return False

# def copy_file(src, dst, chunk=1024):
#     try:
#         with open(src, "rb") as r, open(dst, "wb") as w:
#             while True:
#                 b = r.read(chunk)
#                 if not b:
#                     break
#                 w.write(b)
#     except Exception:
#         pass

# def _do_rename():
#     try:
#         if _exists(MAIN_FILE) and not _exists(BAK_FILE):
#             uos.rename(MAIN_FILE, BAK_FILE)
#         elif _exists(MAIN_FILE) and _exists(BAK_FILE):
#             uos.remove(MAIN_FILE)
#     except Exception:
#         pass
#     # Create a marker file to indicate soft reset
#     try:
#         with open(_SOFT_RESET_, "w") as f:
#             f.write("1")
#     except Exception:
#         pass

#     machine.reset()


# BTN_BOOT_LAST_TIME_DOWN = 0

# _btn = machine.Pin(SAFE_PIN, machine.Pin.IN, machine.Pin.PULL_UP)



# def _timer_cb(t):
#     global BTN_BOOT_LAST_TIME_DOWN, _btn
#     _btn.value(1)
#     print(_btn.value())
#     if _btn.value() == 1:
#         BTN_BOOT_LAST_TIME_DOWN = time.ticks_ms()
#     elif time.ticks_diff(time.ticks_ms(), BTN_BOOT_LAST_TIME_DOWN) > LONG_MS:
#         _do_rename()

# _tim = machine.Timer(0)
# _tim.init(period=500, mode=machine.Timer.PERIODIC, callback=_timer_cb)






# # Restore: if main.bak exists and main.py doesn't, put it back
# if not _exists(_SOFT_RESET_) and _exists(BAK_FILE) and not _exists(MAIN_FILE):
#     try:
#         copy_file(BAK_FILE, MAIN_FILE)
#     except Exception:
#         pass

# try:
#     uos.remove(_SOFT_RESET_)
# except Exception:
#     pass








# # Do not import main.py here; firmware will run it if present.
# # If long-pressed, it gets renamed before execution; otherwise normal boot proceeds.
