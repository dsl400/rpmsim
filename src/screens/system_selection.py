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

        # Create header with back button (no title)
        self.widgets['header_container'] = lv.obj(self.scr)
        self.widgets['header_container'].set_size(420, 50)  # Fixed width for left side
        self.widgets['header_container'].align(lv.ALIGN.TOP_LEFT, 15, 15)
        self.widgets['header_container'].set_style_pad_all(0, 0)
        self.widgets['header_container'].set_style_border_width(0, 0)
        self.widgets['header_container'].set_style_bg_opa(0, 0)

        # Back button will be created in the right container later

        # Create scrollable list container (expanded to fill left side)
        self.widgets['list_container'] = lv.obj(self.scr)
        self.widgets['list_container'].set_size(420, 415)  # Expanded height
        self.widgets['list_container'].align_to(self.widgets['header_container'], lv.ALIGN.OUT_BOTTOM_LEFT, 0, 10)
        self.widgets['list_container'].set_style_pad_all(5, 0)
        self.widgets['list_container'].set_style_border_width(1, 0)
        self.widgets['list_container'].set_style_border_color(lv.color_hex(0xDDDDDD), 0)
        self.widgets['list_container'].set_style_radius(5, 0)
        self.widgets['list_container'].set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
        self.widgets['list_container'].set_style_bg_color(lv.color_hex(0xF5F5F5), 0)

        # Create right side container for keyboard (40% width)
        self.widgets['right_container'] = lv.obj(self.scr)
        self.widgets['right_container'].set_size(380, lv.pct(100))  # Fixed width
        self.widgets['right_container'].align(lv.ALIGN.RIGHT_MID, 0, 0)
        self.widgets['right_container'].set_style_pad_all(15, 0)
        self.widgets['right_container'].set_style_border_width(0, 0)
        self.widgets['right_container'].set_style_bg_color(lv.color_hex(0xFAFAFA), 0)
        self.widgets['right_container'].set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.widgets['right_container'].set_scroll_dir(lv.DIR.NONE)

        # Create search input area
        self.create_search_area()

        # Create virtual keyboard
        self.create_keyboard()

        # Create back button in right container (visible when in systems view, close when in brands view)
        self.widgets['back_btn'] = lv.button(self.widgets['right_container'])
        self.widgets['back_btn'].set_size(120, 40)
        back_label = lv.label(self.widgets['back_btn'])
        back_label.set_text("Back")
        back_label.center()
        self.widgets['back_btn'].align(lv.ALIGN.BOTTOM_MID, 0, -10)
        self.widgets['back_btn'].add_event_cb(self.on_back_click, lv.EVENT.CLICKED, None)

        self.widgets['keyboard'].align_to(self.widgets['back_btn'], lv.ALIGN.OUT_TOP_MID, 0, -40)

        # Load initial data
        self.load_all_systems()
        self.update_list_display()

    def create_search_area(self):
        """Create search input area with text display and clear button"""
        # Search label
        search_label = lv.label(self.widgets['right_container'])
        search_label.set_text("Search Systems:")
        search_label.align(lv.ALIGN.TOP_LEFT, 0, 10)

        # Search text display
        self.widgets['search_display'] = lv.textarea(self.widgets['right_container'])
        self.widgets['search_display'].set_size(300, 40)
        self.widgets['search_display'].align_to(search_label, lv.ALIGN.OUT_BOTTOM_LEFT, 0, 5)
        self.widgets['search_display'].set_placeholder_text("Type to search...")
        self.widgets['search_display'].add_event_cb(self.on_search_text_change, lv.EVENT.VALUE_CHANGED, None)

        # Clear button
        self.widgets['clear_btn'] = lv.button(self.widgets['right_container'])
        self.widgets['clear_btn'].set_size(50, 40)
        self.widgets['clear_btn'].align_to(self.widgets['search_display'], lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        clear_label = lv.label(self.widgets['clear_btn'])
        clear_label.set_text("✕")
        clear_label.center()
        self.widgets['clear_btn'].add_event_cb(self.on_clear_search, lv.EVENT.CLICKED, None)

    
    def create_keyboard(self):
        """Keyboard centered between search and Close via flex spacers"""
        self.widgets['keyboard'] = lv.keyboard(self.widgets['right_container'])
        self.widgets['keyboard'].set_width(lv.pct(100))
        self.widgets['keyboard'].set_height(200)
        self.widgets['keyboard'].set_textarea(self.widgets['search_display'])
        self.widgets['keyboard'].set_style_pad_all(4, 0)
        self.widgets['keyboard'].set_style_border_width(0, 0)


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
            app_state.error_handler.handle_error(e, "Failed to load systems")

    def update_list_display(self):
        """Update the list display based on search state"""
        try:
            # Clear current list by cleaning all children
            list_container = self.widgets['list_container']
            list_container.clean()

            if self.is_searching and self.search_text:
                # Show filtered systems
                # Back button acts as close when searching
                self.display_filtered_systems()
            elif self.current_view == "brands":
                # Show brands - back button acts as close
                self.display_brands()
            elif self.current_view == "systems" and self.selected_brand:
                # Show systems for selected brand - back button goes back to brands
                self.display_brand_systems()

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to update list display")

    def display_brands(self):
        """Display list of brands sorted alphabetically"""
        try:
            brands = app_state.data_manager.get_brands()
            brands.sort()  # Sort alphabetically

            y_pos = 5
            for i, brand in enumerate(brands):
                # Create button for each brand
                btn = lv.button(self.widgets['list_container'])
                btn.set_size(420, 45)
                btn.align(lv.ALIGN.TOP_MID, 0, y_pos)
                btn.set_style_margin_bottom(5, 0)
                btn.set_style_radius(5, 0)

                btn_label = lv.label(btn)
                btn_label.set_text(brand)
                btn_label.center()
                btn.add_event_cb(lambda e, b=brand: self.on_brand_select(e, b), lv.EVENT.CLICKED, None)

                y_pos += 50  # 45px button + 5px margin

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to display brands")

    def display_brand_systems(self):
        """Display systems for selected brand sorted by type and name"""
        try:
            systems = []
            system_types = app_state.data_manager.get_system_types(self.selected_brand)

            for system_type in system_types:
                system_names = app_state.data_manager.get_system_names(self.selected_brand, system_type)
                for system_name in system_names:
                    systems.append({
                        'brand': self.selected_brand,
                        'system': system_type,
                        'system_name': system_name
                    })

            # Sort by system type, then by system name
            systems.sort(key=lambda x: (x['system'], x['system_name']))

            y_pos = 5
            for system in systems:
                # Format: [System Type] System Name
                text = f"[{system['system']}] {system['system_name']}"
                btn = lv.button(self.widgets['list_container'])
                btn.set_size(420, 45)
                btn.align(lv.ALIGN.TOP_MID, 0, y_pos)
                btn.set_style_margin_bottom(5, 0)
                btn.set_style_radius(5, 0)

                btn_label = lv.label(btn)
                btn_label.set_text(text)
                btn_label.center()
                btn.add_event_cb(lambda e, s=system: self.on_system_select(e, s), lv.EVENT.CLICKED, None)

                y_pos += 50  # 45px button + 5px margin

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to display brand systems")

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

            y_pos = 5
            for system in filtered_systems:
                # Format: [System Type] Brand Name - System Name
                text = f"[{system['system_type']}] {system['brand']} - {system['system_name']}"
                btn = lv.button(self.widgets['list_container'])
                btn.set_size(420, 45)
                btn.align(lv.ALIGN.TOP_MID, 0, y_pos)
                btn.set_style_margin_bottom(5, 0)
                btn.set_style_radius(5, 0)

                btn_label = lv.label(btn)
                btn_label.set_text(text)
                btn_label.center()
                btn.add_event_cb(lambda e, s=system: self.on_filtered_system_select(e, s), lv.EVENT.CLICKED, None)

                y_pos += 50  # 45px button + 5px margin

        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to display filtered systems")

    # Event Handlers
    def on_back_click(self, e):
        """Handle back button click - back to brands if brand selected, close if no brand selected"""
        try:
            if self.current_view == "systems" and self.selected_brand:
                # Go back to brand selection
                self.current_view = "brands"
                self.selected_brand = None
                self.update_list_display()
            else:
                # Close the system selector (go back to main screen)
                nav_manager.go_back()
        except Exception as ex:
            app_state.error_handler.handle_error(ex, "Failed to handle back button")

    def on_search_text_change(self, e):
        """Handle search text changes"""
        try:
            self.search_text = self.widgets['search_display'].get_text()
            self.is_searching = len(self.search_text) > 0
            self.update_list_display()
        except Exception as ex:
            app_state.error_handler.handle_error(ex, "Failed to handle search text change")

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
            app_state.error_handler.handle_error(ex, "Failed to clear search")

    def on_brand_select(self, e, brand):
        """Handle brand selection"""
        try:
            self.selected_brand = brand
            self.current_view = "systems"
            self.update_list_display()
        except Exception as ex:
            app_state.error_handler.handle_error(ex, "Brand selection failed")

    def on_system_select(self, e, system):
        """Handle system selection from brand view"""
        try:
            # Set the selected system in app state
            app_state.current_system = {
                'brand': system['brand'],
                'system': system['system'],
                'system_name': system['system_name']
            }

            # Check for available tools and navigate
            self.check_tools_and_navigate()
        except Exception as ex:
            app_state.error_handler.handle_error(ex, f"Failed to select system: {system}")

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
            app_state.error_handler.handle_error(ex, f"Failed to select filtered system: {system}")

    def check_tools_and_navigate(self):
        """Check available tools and navigate appropriately"""
        try:
            tools = app_state.data_manager.get_system_tools(
                app_state.current_system['brand'],
                app_state.current_system['system'],
                app_state.current_system['system_name']
            )

            if tools and len(tools) > 0:
                # Set first tool as default (use tool name, not entire object)
                app_state.current_tool = tools[0]['name']
                # Navigate back to main screen
                self.navigate_to_main()
            else:
                app_state.error_handler.show_error_dialog("No tools available for selected system")
        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to check tools")

    def navigate_to_main(self):
        """Navigate to main screen with proper error handling"""
        try:
            # Check if main screen is registered
            if "main" in nav_manager.screens:
                nav_manager.navigate_to("main")
            else:
                # Register main screen if not already registered
                from screens.main_screen import MainScreen
                nav_manager.register_screen("main", MainScreen)
                nav_manager.navigate_to("main")
        except Exception as e:
            app_state.error_handler.handle_error(e, "Failed to navigate to main screen")



