
import utime as time
import usys as sys
import lvgl as lv

lv.init()

# Register display driver.
disp_drv = lv.sdl_window_create(800, 480)
lv.sdl_window_set_resizeable(disp_drv, False)
lv.sdl_window_set_title(disp_drv, "Simulator (MicroPython)")

# Regsiter input driver
mouse = lv.sdl_mouse_create()

# Create a screen
scr = lv.obj()
lv.screen_load(scr)

# Create a label for counter
counter_label = lv.label(scr)
counter_label.set_text("0")
counter_label.center()

# Counter variable
counter = 0

def increment_counter(evt):
    global counter
    counter += 1
    counter_label.set_text(str(counter))

def decrement_counter(evt):
    global counter
    counter -= 1
    counter_label.set_text(str(counter))

# Create + button
plus_btn = lv.button(scr)
plus_btn.set_size(80, 50)
plus_btn.align(lv.ALIGN.CENTER, 100, 0)
plus_btn.add_event_cb(increment_counter, lv.EVENT.CLICKED, None)

plus_label = lv.label(plus_btn)
plus_label.set_text("+")
plus_label.center()

# Create - button
minus_btn = lv.button(scr)
minus_btn.set_size(80, 50)
minus_btn.align(lv.ALIGN.CENTER, -100, 0)
minus_btn.add_event_cb(decrement_counter, lv.EVENT.CLICKED, None)

minus_label = lv.label(minus_btn)
minus_label.set_text("-")
minus_label.center()

if __name__ == '__main__':
    while True:
        lv.task_handler()
        time.sleep_ms(5)