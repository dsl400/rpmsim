"""
Navigation and State Management System for ECU Diagnostic Tool
Handles screen transitions, state persistence, and application flow
"""

import lvgl as lv
import gc
from utils.error_handler import ErrorHandler
from utils.data_manager import DataManager

class NavigationManager:
    """Centralized navigation and screen management"""
    
    def __init__(self):
        self.screen_stack = []
        self.current_screen = None
        self.screens = {}
        self.error_handler = ErrorHandler()
        
    def register_screen(self, name, screen_class):
        """
        Register a screen class for navigation
        
        Args:
            name (str): Screen identifier
            screen_class: Screen class to instantiate
        """
        self.screens[name] = screen_class
    
    def navigate_to(self, screen_name, **kwargs):
        """
        Navigate to a screen
        
        Args:
            screen_name (str): Name of screen to navigate to
            **kwargs: Additional arguments to pass to screen constructor
            
        Returns:
            bool: True if navigation successful
        """
        if screen_name not in self.screens:
            self.error_handler.handle_error(
                f"Screen '{screen_name}' not registered", 
                "Navigation error"
            )
            return False
        
        try:
            # Clean up current screen
            if self.current_screen:
                if hasattr(self.current_screen, 'on_exit'):
                    self.current_screen.on_exit()
                self.screen_stack.append(self.current_screen)
            
            # Create new screen
            scr = lv.screen()
            screen_instance = self.screens[screen_name](scr, **kwargs)
            
            # Call on_enter if available
            if hasattr(screen_instance, 'on_enter'):
                screen_instance.on_enter()
            
            # Load the screen
            lv.screen_load(scr)
            self.current_screen = screen_instance
            
            # Force garbage collection to free memory
            gc.collect()
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, f"Failed to navigate to {screen_name}")
            return False
    
    def go_back(self):
        """
        Navigate back to previous screen
        
        Returns:
            bool: True if navigation successful
        """
        if not self.screen_stack:
            return False
        
        try:
            # Clean up current screen
            if self.current_screen:
                if hasattr(self.current_screen, 'cleanup'):
                    self.current_screen.cleanup()
            
            # Restore previous screen
            previous_screen = self.screen_stack.pop()
            
            if hasattr(previous_screen, 'on_enter'):
                previous_screen.on_enter()
            
            lv.screen_load(previous_screen.scr)
            self.current_screen = previous_screen
            
            # Force garbage collection
            gc.collect()
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to navigate back")
            return False
    
    def clear_stack(self):
        """Clear the navigation stack"""
        for screen in self.screen_stack:
            if hasattr(screen, 'cleanup'):
                screen.cleanup()
        self.screen_stack.clear()
        gc.collect()
    
    def get_current_screen_name(self):
        """
        Get name of current screen
        
        Returns:
            str: Current screen name or None
        """
        if self.current_screen:
            return self.current_screen.__class__.__name__
        return None

class AppState:
    """Application state management"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.error_handler = ErrorHandler()
        self.current_system = None
        self.current_tool = None
        self.is_configured = False
        self.wifi_connected = False
        
        # Hardware managers will be initialized later
        self.wifi_manager = None
        self.ecu_manager = None
    
    def initialize(self):
        """Initialize application state"""
        try:
            # Load user settings
            settings = self.data_manager.get_user_settings()
            self.is_configured = settings["wifi"]["ssid"] is not None
            
            # Restore last selected system
            last_selected = settings["last_selected"]
            if all(last_selected.values()):
                self.current_system = {
                    "brand": last_selected["brand"],
                    "system": last_selected["system"],
                    "system_name": last_selected["system_name"]
                }
                self.current_tool = last_selected["tool"]
            
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to initialize application state")
            return False
    
    def set_current_system(self, brand, system, system_name, tool):
        """
        Set current system and tool
        
        Args:
            brand (str): Vehicle brand
            system (str): System type
            system_name (str): System name
            tool (str): Tool name
        """
        self.current_system = {
            "brand": brand,
            "system": system,
            "system_name": system_name
        }
        self.current_tool = tool
        
        # Save to user settings
        self.data_manager.update_last_selected(brand, system, system_name, tool)
    
    def get_current_system_display(self):
        """
        Get display string for current system
        
        Returns:
            str: Formatted system display string
        """
        if not self.current_system or not self.current_tool:
            return "No System Selected"
        
        return f"{self.current_system['brand']} {self.current_system['system_name']} - {self.current_tool}"
    
    def get_system_tools(self, brand, system, system_name):
        """
        Get available tools for a system
        
        Args:
            brand (str): Vehicle brand
            system (str): System type
            system_name (str): System name
            
        Returns:
            list: List of available tools
        """
        return self.data_manager.get_system_tools(brand, system, system_name)
    
    def get_tool_config(self, brand, system, system_name, tool_name):
        """
        Get configuration for a specific tool
        
        Args:
            brand (str): Vehicle brand
            system (str): System type
            system_name (str): System name
            tool_name (str): Tool name
            
        Returns:
            dict: Tool configuration
        """
        return self.data_manager.get_tool_config(brand, system, system_name, tool_name)
    
    def set_wifi_manager(self, wifi_manager):
        """Set WiFi manager instance"""
        self.wifi_manager = wifi_manager
    
    def set_ecu_manager(self, ecu_manager):
        """Set ECU manager instance"""
        self.ecu_manager = ecu_manager
    
    def update_wifi_status(self, connected):
        """Update WiFi connection status"""
        self.wifi_connected = connected

class BaseScreen:
    """Base class for all screens"""
    
    def __init__(self, scr):
        self.scr = scr
        self.widgets = {}
        self.error_handler = ErrorHandler()
        self.create_ui()
    
    def create_ui(self):
        """Override in subclasses to create UI elements"""
        raise NotImplementedError("Subclasses must implement create_ui()")
    
    def on_enter(self):
        """Called when screen becomes active"""
        pass
    
    def on_exit(self):
        """Called when leaving screen"""
        pass
    
    def cleanup(self):
        """Clean up resources"""
        for widget in self.widgets.values():
            if hasattr(widget, 'delete'):
                try:
                    widget.delete()
                except:
                    pass
        self.widgets.clear()

# Global instances
nav_manager = NavigationManager()
app_state = AppState()
