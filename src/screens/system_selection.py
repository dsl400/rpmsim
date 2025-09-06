"""
System Selection Screen for ECU Diagnostic Tool
Implements full-screen system selection with search functionality
"""

import lvgl as lv
from utils.navigation_manager import BaseScreen, nav_manager, app_state
from utils.error_handler import error_handler

class SystemSelectionScreen(BaseScreen):
    """Full-screen system selection screen with search functionality"""

    def __init__(self, scr):
        self.search_text = ""
        self.is_searching = False
        self.current_view = "brands"  # "brands" or "systems"
        self.selected_brand = None
        self.all_systems = []  # Cache of all systems for search
        super().__init__(scr)

    def create_ui(self):
        """Create the full-screen system selection UI elements"""
        # Make screen full size and remove padding
        self.scr.set_style_pad_all(0, 0)
        self.scr.set_style_border_width(0, 0)

        # Create left side container for list
        self.widgets['left_container'] = lv.obj(self.scr)
        self.widgets['left_container'].set_size(400, lv.pct(100))
        self.widgets['left_container'].align(lv.ALIGN.LEFT_MID, 0, 0)
        self.widgets['left_container'].set_style_pad_all(10, 0)

        # Create title for left side
        self.widgets['list_title'] = lv.label(self.widgets['left_container'])
        self.widgets['list_title'].set_text("Select Brand")
        self.widgets['list_title'].align(lv.ALIGN.TOP_MID, 0, 10)

        # Create scrollable list
        self.widgets['system_list'] = lv.list(self.widgets['left_container'])
        self.widgets['system_list'].set_size(380, 400)
        self.widgets['system_list'].align_to(self.widgets['list_title'], lv.ALIGN.OUT_BOTTOM_MID, 0, 10)

        # Create right side container for keyboard
        self.widgets['right_container'] = lv.obj(self.scr)
        self.widgets['right_container'].set_size(400, lv.pct(100))
        self.widgets['right_container'].align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.widgets['right_container'].set_style_pad_all(10, 0)

        # Create search input area
        self.create_search_area()

        # Create virtual keyboard
        self.create_keyboard()

        # Create close button
        self.widgets['close_btn'] = lv.button(self.widgets['right_container'])
        self.widgets['close_btn'].set_size(150, 50)
        close_label = lv.label(self.widgets['close_btn'])
        close_label.set_text("Close")
        close_label.center()
        self.widgets['close_btn'].align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.widgets['close_btn'].add_event_cb(self.on_close_click, lv.EVENT.CLICKED, None)

        # Load initial data
        self.load_all_systems()
        self.update_list_display()

    def create_search_area(self):
        """Create search input area with text display and clear button"""
        # Search text display
        self.widgets['search_display'] = lv.textarea(self.widgets['right_container'])
        self.widgets['search_display'].set_size(300, 40)
        self.widgets['search_display'].align(lv.ALIGN.TOP_MID, -25, 20)
        self.widgets['search_display'].set_placeholder_text("Search systems...")
        self.widgets['search_display'].add_event_cb(self.on_search_text_change, lv.EVENT.VALUE_CHANGED, None)

        # Clear button
        self.widgets['clear_btn'] = lv.button(self.widgets['right_container'])
        self.widgets['clear_btn'].set_size(50, 40)
        self.widgets['clear_btn'].align_to(self.widgets['search_display'], lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        clear_label = lv.label(self.widgets['clear_btn'])
        clear_label.set_text("X")
        clear_label.center()
        self.widgets['clear_btn'].add_event_cb(self.on_clear_search, lv.EVENT.CLICKED, None)

    def create_keyboard(self):
        """Create virtual keyboard"""
        self.widgets['keyboard'] = lv.keyboard(self.widgets['right_container'])
        self.widgets['keyboard'].set_size(380, 200)
        self.widgets['keyboard'].align_to(self.widgets['search_display'], lv.ALIGN.OUT_BOTTOM_MID, 0, 20)
        self.widgets['keyboard'].set_textarea(self.widgets['search_display'])

    def load_all_systems(self):
        """Load all systems from data manager for search functionality"""
        try:
            self.all_systems = []
            brands = app_state.data_manager.get_brands()

            for brand in brands:
                system_types = app_state.data_manager.get_system_types(brand)
                for system_type in system_types:
                    system_names = app_state.data_manager.get_system_names(brand, system_type)
                    for system_name in system_names:
                        self.all_systems.append({
                            'brand': brand,
                            'system_type': system_type,
                            'system_name': system_name
                        })
        except Exception as e:
            error_handler.handle_error(e, "Failed to load systems", "ERROR")

    def update_list_display(self):
        """Update the list display based on search state"""
        try:
            # Clear current list
            self.widgets['system_list'].clean()

            if self.is_searching and self.search_text:
                # Show filtered systems
                self.widgets['list_title'].set_text(f"Search: '{self.search_text}'")
                self.display_filtered_systems()
            elif self.current_view == "brands":
                # Show brands
                self.widgets['list_title'].set_text("Select Brand")
                self.display_brands()
            elif self.current_view == "systems" and self.selected_brand:
                # Show systems for selected brand
                self.widgets['list_title'].set_text(f"Systems - {self.selected_brand}")
                self.display_brand_systems()

        except Exception as e:
            error_handler.handle_error(e, "Failed to update list display")

    def display_brands(self):
        """Display list of brands sorted alphabetically"""
        try:
            brands = app_state.data_manager.get_brands()
            brands.sort()  # Sort alphabetically

            for brand in brands:
                # Create button for each brand
                btn = lv.button(self.widgets['system_list'])
                btn.set_size(360, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(brand)
                btn_label.center()
                btn.add_event_cb(lambda e, b=brand: self.on_brand_select(e, b), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to display brands")

    def display_brand_systems(self):
        """Display systems for selected brand sorted by type and name"""
        try:
            systems = []
            system_types = app_state.data_manager.get_system_types(self.selected_brand)

            for system_type in system_types:
                system_names = app_state.data_manager.get_system_names(self.selected_brand, system_type)
                for system_name in system_names:
                    systems.append({
                        'type': system_type,
                        'name': system_name
                    })

            # Sort by system type, then by system name
            systems.sort(key=lambda x: (x['type'], x['name']))

            for system in systems:
                # Format: [System Type] System Name
                text = f"[{system['type']}] {system['name']}"
                btn = lv.button(self.widgets['system_list'])
                btn.set_size(360, 50)
                btn_label = lv.label(btn)
                btn_label.set_text(text)
                btn_label.center()
                btn.add_event_cb(lambda e, s=system: self.on_system_select(e, s), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to display brand systems")

    def display_filtered_systems(self):
        """Display systems matching search filter"""
        try:
            filtered_systems = []
            search_lower = self.search_text.lower()

            for system in self.all_systems:
                # Search in brand, system type, and system name
                if (search_lower in system['brand'].lower() or
                    search_lower in system['system_type'].lower() or
                    search_lower in system['system_name'].lower()):
                    filtered_systems.append(system)

            # Sort by brand, system type, then system name
            filtered_systems.sort(key=lambda x: (x['brand'], x['system_type'], x['system_name']))

            for system in filtered_systems:
                # Format: [System Type] Brand Name
                #         System Name
                text = f"[{system['system_type']}] {system['brand']}\n{system['system_name']}"
                btn = lv.button(self.widgets['system_list'])
                btn.set_size(360, 70)  # Taller for two lines
                btn_label = lv.label(btn)
                btn_label.set_text(text)
                btn_label.center()
                btn.add_event_cb(lambda e, s=system: self.on_filtered_system_select(e, s), lv.EVENT.CLICKED, None)

        except Exception as e:
            error_handler.handle_error(e, "Failed to display filtered systems")

    # Event Handlers
    def on_search_text_change(self, e):
        """Handle search text changes"""
        try:
            self.search_text = self.widgets['search_display'].get_text()
            self.is_searching = len(self.search_text) > 0
            self.update_list_display()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to handle search text change")

    def on_clear_search(self, e):
        """Clear search text and return to brand view"""
        try:
            self.widgets['search_display'].set_text("")
            self.search_text = ""
            self.is_searching = False
            self.current_view = "brands"
            self.selected_brand = None
            self.update_list_display()
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to clear search")

    def on_brand_select(self, e, brand):
        """Handle brand selection"""
        try:
            self.selected_brand = brand
            self.current_view = "systems"
            self.update_list_display()
        except Exception as ex:
            error_handler.handle_error(ex, "Brand selection failed")

    def on_system_select(self, e, system):
        """Handle system selection from brand view"""
        try:
            # Set the selected system in app state
            app_state.current_system = {
                'brand': self.selected_brand,
                'system': system['type'],
                'system_name': system['name']
            }

            # Check for available tools and navigate
            self.check_tools_and_navigate()
        except Exception as ex:
            error_handler.handle_error(ex, f"Failed to select system: {system}")

    def on_filtered_system_select(self, e, system):
        """Handle system selection from search results"""
        try:
            # Set the selected system in app state
            app_state.current_system = {
                'brand': system['brand'],
                'system': system['system_type'],
                'system_name': system['system_name']
            }

            # Check for available tools and navigate
            self.check_tools_and_navigate()
        except Exception as ex:
            error_handler.handle_error(ex, f"Failed to select filtered system: {system}")

    def check_tools_and_navigate(self):
        """Check available tools and navigate appropriately"""
        try:
            tools = app_state.data_manager.get_system_tools(
                app_state.current_system['brand'],
                app_state.current_system['system'],
                app_state.current_system['system_name']
            )

            if tools and len(tools) > 0:
                # Set first tool as default
                app_state.current_tool = tools[0]
                # Navigate back to main screen
                nav_manager.navigate_to("main")
            else:
                error_handler.show_error_dialog("No tools available for selected system")
        except Exception as e:
            error_handler.handle_error(e, "Failed to check tools")

    def on_close_click(self, e):
        """Handle close button click - exit without selection"""
        try:
            nav_manager.navigate_to("main")
        except Exception as ex:
            error_handler.handle_error(ex, "Failed to close system selection")

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