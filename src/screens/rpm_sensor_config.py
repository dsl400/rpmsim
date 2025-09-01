



import lvgl as lv

class RPMSensorConfigScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("RPM Sensor Configuration")
        title_label.align(lv.ALIGN.TOP_MID, 0, 10)

        # Add description text
        desc_label = lv.label(self.scr)
        desc_label.set_text("Configure crankshaft and camshaft sensors below:")
        desc_label.align_to(title_label, lv.ALIGN.BOTTOM_MID, 0, 20)

        # Create container for crankshaft sensor configuration
        self.crank_container = lv.obj(self.scr)
        self.crank_container.set_size(460, 150)
        self.crank_container.align(lv.ALIGN.TOP_LEFT, 20, 80)
        self.crank_container.label = lv.label(self.crank_container)
        self.crank_container.label.set_text("Crankshaft Sensor")
        self.crank_container.label.align(lv.ALIGN.TOP_LEFT, 10, 5)

        # Add degrees per tooth input
        self.degrees_input = lv.textarea(self.crank_container)
        self.degrees_input.set_size(200, 40)
        self.degrees_input.align_to(self.crank_container.label, lv.ALIGN.BOTTOM_LEFT, 10, 10)
        self.degrees_input.label = lv.label(self.crank_container)
        self.degrees_input.label.set_text("Degrees per tooth:")
        self.degrees_input.label.align_to(self.degrees_input, lv.ALIGN.LEFT_MID, -220, 0)

        # Add teeth configuration slider
        self.teeth_slider = lv.slider(self.crank_container)
        self.teeth_slider.set_size(420, 30)
        self.teeth_slider.align_to(self.degrees_input, lv.ALIGN.BOTTOM_LEFT, 0, 10)

        # Create container for camshaft sensor configuration
        self.cam_container = lv.obj(self.scr)
        self.cam_container.set_size(460, 150)
        self.cam_container.align_to(self.crank_container, lv.ALIGN.BOTTOM_LEFT, 0, 20)
        self.cam_container.label = lv.label(self.cam_container)
        self.cam_container.label.set_text("Camshaft Sensor")
        self.cam_container.label.align(lv.ALIGN.TOP_LEFT, 10, 5)

        # Add degrees per tooth input
        self.degrees_input2 = lv.textarea(self.cam_container)
        self.degrees_input2.set_size(200, 40)
        self.degrees_input2.align_to(self.cam_container.label, lv.ALIGN.BOTTOM_LEFT, 10, 10)
        self.degrees_input2.label = lv.label(self.cam_container)
        self.degrees_input2.label.set_text("Degrees per tooth:")
        self.degrees_input2.label.align_to(self.degrees_input2, lv.ALIGN.LEFT_MID, -220, 0)

        # Add teeth configuration slider
        self.teeth_slider2 = lv.slider(self.cam_container)
        self.teeth_slider2.set_size(420, 30)
        self.teeth_slider2.align_to(self.degrees_input2, lv.ALIGN.BOTTOM_LEFT, 0, 10)

        # Create save button
        self.save_btn = lv.btn(self.scr)
        self.save_btn.set_size(150, 50)
        self.save_btn.center()
        self.save_btn.label = lv.label(self.save_btn)
        self.save_btn.label.set_text("Save")

        # Add event handler for save button click
        self.save_btn.add_event_cb(self.on_save_click, lv.EVENT.CLICKED, None)

    def on_save_click(self, btn):
        # Get configuration values from inputs and sliders
        crank_degrees = self.degrees_input.get_text()
        cam_degrees = self.degrees_input2.get_text()

        # For simplicity, just show a confirmation message with the saved values
        msg = lv.alert(self.scr)
        msg.set_text(f"Configuration saved:\nCrankshaft: {crank_degrees} degrees\nCamshaft: {cam_degrees} degrees")

def create_rpm_sensor_config_screen():
    """Create the RPM sensor configuration screen"""
    scr = lv.screen()
    RPMSensorConfigScreen(scr)
    return scr



