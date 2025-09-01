


import lvgl as lv

class SystemSelectionScreen:
    def __init__(self, scr):
        self.scr = scr
        self.create_ui()

    def create_ui(self):
        # Create title label
        title_label = lv.label(self.scr)
        title_label.set_text("Select ECU System")
        title_label.align(lv.ALIGN.TOP_MID, 0, 10)

        # Create step labels
        self.step_labels = []
        steps = ["Brand", "System", "System Name", "Tool"]
        y_pos = 50

        for i, step in enumerate(steps):
            label = lv.label(self.scr)
            label.set_text(f"{i+1}. {step}:")
            label.align(lv.ALIGN.TOP_LEFT, 20, y_pos + (i*40))
            self.step_labels.append(label)

        # Create dropdowns for each selection step
        self.brand_dropdown = lv.dropdown(self.scr)
        self.brand_dropdown.set_options("\n".join(["Toyota", "Honda", "Ford", "BMW"]))
        self.brand_dropdown.align_to(self.step_labels[0], lv.ALIGN.RIGHT_MID, 20, 0)

        self.system_dropdown = lv.dropdown(self.scr)
        self.system_dropdown.set_options("\n".join(["Engine", "Transmission", "ABS", "Airbag"]))
        self.system_dropdown.align_to(self.step_labels[1], lv.ALIGN.RIGHT_MID, 20, 0)

        self.system_name_dropdown = lv.dropdown(self.scr)
        self.system_name_dropdown.set_options("\n".join(["Bosch ME7.9.7", "EDC17", "TCM123", "Airbag456"]))
        self.system_name_dropdown.align_to(self.step_labels[2], lv.ALIGN.RIGHT_MID, 20, 0)

        self.tool_dropdown = lv.dropdown(self.scr)
        self.tool_dropdown.set_options("\n".join(["RPM Simulator", "Clear DTC", "Read Live Data"]))
        self.tool_dropdown.align_to(self.step_labels[3], lv.ALIGN.RIGHT_MID, 20, 0)

        # Create select button
        self.select_btn = lv.btn(self.scr)
        self.select_btn.set_size(150, 50)
        self.select_btn.center()
        self.select_btn.label = lv.label(self.select_btn)
        self.select_btn.label.set_text("Select")

        # Add event handler for select button click
        self.select_btn.add_event_cb(self.on_select_click, lv.EVENT.CLICKED, None)

    def on_select_click(self, btn):
        # Get selected values from dropdowns
        brand = self.brand_dropdown.get_selected_str()
        system = self.system_dropdown.get_selected_str()
        system_name = self.system_name_dropdown.get_selected_str()
        tool = self.tool_dropdown.get_selected_str()

        # Display confirmation message with selection
        msg = lv.alert(self.scr)
        msg.set_text(f"Selected: {brand} - {system} - {system_name} - {tool}")

def create_system_selection_screen():
    """Create the system selection screen"""
    scr = lv.screen()
    SystemSelectionScreen(scr)
    return scr

