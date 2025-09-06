"""
System Selection Screen for ECU Diagnostic Tool
Implements four-step selection process: Brand → System → System Name → Tool
"""

import lvgl as lv
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class SystemSelectionScreen(BaseScreen):
    """Four-step system selection screen"""

    def __init__(self, scr):
        self.selection_step = 0  # 0=Brand, 1=System, 2=System Name, 3=Tool
        self.selected_brand = None
        self.selected_system = None
        self.selected_system_name = None
        self.selected_tool = None
        super().__init__(scr)

    def create_ui(self):
        """Create the system selection UI"""
        # Create title label
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 20)

        # Create breadcrumb navigation
        self.widgets['breadcrumb'] = lv.label(self.scr)
        self.widgets['breadcrumb'].align_to(self.widgets['title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 10)
        self.widgets['breadcrumb'].set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

        # Create main selection container
        self.widgets['selection_container'] = lv.obj(self.scr)
        self.widgets['selection_container'].set_size(600, 300)
        self.widgets['selection_container'].align(lv.ALIGN.CENTER, 0, 0)
        self.widgets['selection_container'].set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.widgets['selection_container'].set_flex_align(lv.FLEX_ALIGN.START, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)

        # Create navigation buttons
        self.widgets['back_btn'] = lv.button(self.scr)
        self.widgets['back_btn'].set_size(100, 40)
        back_label = lv.label(self.widgets['back_btn'])
        back_label.set_text("Back")
        back_label.center()
        self.widgets['back_btn'].align(lv.ALIGN.BOTTOM_LEFT, 20, -20)
        self.widgets['back_btn'].add_event_cb(self.on_back_click, lv.EVENT.CLICKED, None)

        self.widgets['cancel_btn'] = lv.button(self.scr)
        self.widgets['cancel_btn'].set_size(100, 40)
        cancel_label = lv.label(self.widgets['cancel_btn'])
        cancel_label.set_text("Cancel")
        cancel_label.center()
        self.widgets['cancel_btn'].align(lv.ALIGN.BOTTOM_RIGHT, -20, -20)
        self.widgets['cancel_btn'].add_event_cb(self.on_cancel_click, lv.EVENT.CLICKED, None)

        # Start with brand selection
        self.update_selection_step()

    def update_selection_step(self):
        """Update UI based on current selection step"""
        try:
            # Clear previous buttons
            self.widgets['selection_container'].clean()

            # Update title and breadcrumb
            if self.selection_step == 0:
                self.widgets['title'].set_text("Select Vehicle Brand")
                self.widgets['breadcrumb'].set_text("Step 1 of 4: Brand")
                self.load_brands()
            elif self.selection_step == 1:
                self.widgets['title'].set_text("Select System Type")
                self.widgets['breadcrumb'].set_text(f"Step 2 of 4: {self.selected_brand} → System")
                self.load_system_types()
            elif self.selection_step == 2:
                self.widgets['title'].set_text("Select System Name")
                self.widgets['breadcrumb'].set_text(f"Step 3 of 4: {self.selected_brand} → {self.selected_system} → System Name")
                self.load_system_names()
            elif self.selection_step == 3:
                self.widgets['title'].set_text("Select Tool")
                self.widgets['breadcrumb'].set_text(f"Step 4 of 4: {self.selected_brand} → {self.selected_system} → {self.selected_system_name} → Tool")
                self.load_tools()

            # Update back button visibility
            self.widgets['back_btn'].set_hidden(self.selection_step == 0)

        except Exception as e:
            error_handler.handle_error(e, "Failed to update selection step")

    def load_brands(self):
        """Load available vehicle brands"""
        try:
            brands = app_state.data_manager.get_brands()

            if not brands:
                error_handler.show_error_dialog("No vehicle brands found in database")
                return

            for brand in brands:
                btn = lv.button(self.widgets['selection_container'])
                btn.set_size(550, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(brand)
                btn_label.center()
                btn.add_event_cb(lambda evt, b=brand: self.on_brand_select(evt, b), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to load brands")

    def load_system_types(self):
        """Load system types for selected brand"""
        try:
            system_types = app_state.data_manager.get_system_types(self.selected_brand)

            if not system_types:
                error_handler.show_error_dialog(f"No systems found for {self.selected_brand}")
                return

            for system_type in system_types:
                btn = lv.button(self.widgets['selection_container'])
                btn.set_size(550, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(system_type)
                btn_label.center()
                btn.add_event_cb(lambda evt, s=system_type: self.on_system_select(evt, s), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to load system types")

    def load_system_names(self):
        """Load system names for selected brand and type"""
        try:
            system_names = app_state.data_manager.get_system_names(self.selected_brand, self.selected_system)

            if not system_names:
                error_handler.show_error_dialog(f"No system names found for {self.selected_brand} {self.selected_system}")
                return

            for system_name in system_names:
                btn = lv.button(self.widgets['selection_container'])
                btn.set_size(550, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(system_name)
                btn_label.center()
                btn.add_event_cb(lambda evt, n=system_name: self.on_system_name_select(evt, n), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to load system names")

    def load_tools(self):
        """Load tools for selected system"""
        try:
            tools = app_state.data_manager.get_system_tools(
                self.selected_brand,
                self.selected_system,
                self.selected_system_name
            )

            if not tools:
                error_handler.show_error_dialog("No tools found for selected system")
                return

            # If only one tool, auto-select it
            if len(tools) == 1:
                self.selected_tool = tools[0]['name']
                self.complete_selection()
                return

            # Show multiple tools
            for tool in tools:
                btn = lv.button(self.widgets['selection_container'])
                btn.set_size(550, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(tool['name'])
                btn_label.center()
                btn.add_event_cb(lambda evt, t=tool['name']: self.on_tool_select(evt, t), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to load tools")

    def on_brand_select(self, event, brand):
        """Handle brand selection"""
        try:
            self.selected_brand = brand
            self.selection_step = 1
            self.update_selection_step()
        except Exception as e:
            error_handler.handle_error(e, "Brand selection failed")

    def on_system_select(self, event, system_type):
        """Handle system type selection"""
        try:
            self.selected_system = system_type
            self.selection_step = 2
            self.update_selection_step()
        except Exception as e:
            error_handler.handle_error(e, "System selection failed")

    def on_system_name_select(self, event, system_name):
        """Handle system name selection"""
        try:
            self.selected_system_name = system_name
            self.selection_step = 3
            self.update_selection_step()
        except Exception as e:
            error_handler.handle_error(e, "System name selection failed")

    def on_tool_select(self, event, tool_name):
        """Handle tool selection"""
        try:
            self.selected_tool = tool_name
            self.complete_selection()
        except Exception as e:
            error_handler.handle_error(e, "Tool selection failed")

    def complete_selection(self):
        """Complete the selection process"""
        try:
            # Update app state with selection
            app_state.set_current_system(
                self.selected_brand,
                self.selected_system,
                self.selected_system_name,
                self.selected_tool
            )

            # Show confirmation
            error_handler.show_info_dialog(
                f"Selected: {self.selected_brand} {self.selected_system_name} - {self.selected_tool}"
            )

            # Navigate back to main screen
            nav_manager.navigate_to("main")

        except Exception as e:
            error_handler.handle_error(e, "Failed to complete selection")

    def on_back_click(self, event):
        """Handle back button click"""
        try:
            if self.selection_step > 0:
                self.selection_step -= 1
                self.update_selection_step()
        except Exception as e:
            error_handler.handle_error(e, "Back navigation failed")

    def on_cancel_click(self, event):
        """Handle cancel button click"""
        try:
            nav_manager.go_back()
        except Exception as e:
            error_handler.handle_error(e, "Cancel failed")