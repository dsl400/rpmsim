


import lvgl as lv

class RPMSimulatorScreen:
    def __init__(self, scr):
        self.scr = scr
        self.current_rpm = 0
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("RPM Simulator")
        title_label.align(lv.ALIGN_TOP_MID, 0, 10)

        # Display current RPM value
        self.rpm_value_label = lv.label(self.scr)
        self.rpm_value_label.set_text(f"Current RPM: {self.current_rpm}")
        self.rpm_value_label.align(lv.ALIGN_TOP_MID, 0, 40)

        # Create increment and decrement buttons
        btn_size = (120, 50)

        self.decrement_btn = lv.btn(self.scr)
        self.decrement_btn.set_size(btn_size[0], btn_size[1])
        self.decrement_btn.label = lv.label(self.decrement_btn)
        self.decrement_btn.label.set_text("-")
        self.decrement_btn.align(lv.ALIGN_CENTER, -80, 120)

        self.increment_btn = lv.btn(self.scr)
        self.increment_btn.set_size(btn_size[0], btn_size[1])
        self.increment_btn.label = lv.label(self.increment_btn)
        self.increment_btn.label.set_text("+")
        self.increment_btn.align(lv.ALIGN_CENTER, 80, 120)

        # Add event handlers for buttons
        self.decrement_btn.add_event_cb(self.on_decrement_click, lv.EVENT.CLICKED, None)
        self.increment_btn.add_event_cb(self.on_increment_click, lv.EVENT.CLICKED, None)

        # Create RPM slider
        self.rpm_slider = lv.slider(self.scr)
        self.rpm_slider.set_range(0, 10000)  # Set range from 0 to 10000 RPM
        self.rpm_slider.set_value(self.current_rpm)
        self.rpm_slider.align(lv.ALIGN_CENTER, 0, 200)

        # Add event handler for slider
        self.rpm_slider.add_event_cb(self.on_slider_change, lv.EVENT.VALUE_CHANGED, None)

        # Create toggle button for sensor output
        self.sensor_toggle = lv.switch(self.scr)
        self.sensor_toggle.align(lv.ALIGN_CENTER, 0, 280)
        self.sensor_toggle.label = lv.label(self.scr)
        self.sensor_toggle.label.set_text("Disable Sensor Output")
        self.sensor_toggle.label.align_to(self.sensor_toggle, lv.ALIGN.LEFT_MID, -10, 0)

        # Create configuration editor button
        self.config_btn = lv.btn(self.scr)
        self.config_btn.set_size(200, 50)
        self.config_btn.center()
        self.config_btn.label = lv.label(self.config_btn)
        self.config_btn.label.set_text("Configure Sensor")
        self.config_btn.align(lv.ALIGN.BOTTOM_MID, 0, -10)

    def on_decrement_click(self, btn):
        if self.current_rpm > 0:
            self.current_rpm -= 100
            self.update_rpm_display()

    def on_increment_click(self, btn):
        if self.current_rpm < 10000:
            self.current_rpm += 100
            self.update_rpm_display()

    def on_slider_change(self, slider):
        self.current_rpm = slider.get_value()
        self.update_rpm_display()

    def update_rpm_display(self):
        self.rpm_value_label.set_text(f"Current RPM: {self.current_rpm}")
        self.rpm_slider.set_value(self.current_rpm)

def create_rpm_simulator_screen():
    scr = lv.screen()
    RPMSimulatorScreen(scr)
    return scr


