"""
Data Management System for ECU Diagnostic Tool
Handles JSON-based storage, user settings, and system configurations
"""

import ujson
import os
from utils.error_handler import ErrorHandler

class DataManager:
    """Centralized data management for the ECU Diagnostic Tool"""
    
    def __init__(self, base_path="src/db"):
        self.base_path = base_path
        self.systems_file = f"{base_path}/db.json"
        self.user_settings_file = f"{base_path}/user_settings.json"
        self._cache = {}
        self.error_handler = ErrorHandler()

        # Ensure database directory exists (skip in simulation if permission issues)
        try:
            self._ensure_db_directory()
        except Exception as e:
            print(f"Warning: Could not ensure db directory: {e}")
            # Continue anyway - files might already exist
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists"""
        try:
            # MicroPython compatible directory creation
            try:
                os.stat(self.base_path)
            except OSError:
                # Directory doesn't exist, create it
                os.mkdir(self.base_path)
        except OSError as e:
            self.error_handler.handle_error(e, "Failed to create database directory", "CRITICAL")
    
    def load_systems(self):
        """
        Load systems database with caching
        
        Returns:
            dict: Systems database with 'systems' key containing list of system definitions
        """
        if 'systems' not in self._cache:
            try:
                with open(self.systems_file, 'r') as f:
                    self._cache['systems'] = ujson.load(f)
            except (OSError, ValueError) as e:
                self.error_handler.handle_error(e, f"Failed to load systems from {self.systems_file}")
                self._cache['systems'] = {"systems": []}
        return self._cache['systems']

    def get_systems(self):
        """
        Get list of all systems

        Returns:
            list: List of system definitions
        """
        systems_data = self.load_systems()
        return systems_data.get('systems', [])

    def save_user_settings(self, settings):
        """
        Save user settings with atomic write operation
        
        Args:
            settings (dict): User settings dictionary
            
        Returns:
            bool: True if save successful, False otherwise
        """
        temp_file = f"{self.user_settings_file}.tmp"
        try:
            # Write to temporary file first
            with open(temp_file, 'w') as f:
                ujson.dump(settings, f)
            
            # Atomic rename operation
            os.rename(temp_file, self.user_settings_file)
            self._cache['user_settings'] = settings
            return True
            
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to save user settings")
            # Clean up temporary file
            try:
                os.remove(temp_file)
            except:
                pass
            return False
    
    def get_user_settings(self):
        """
        Load user settings with defaults
        
        Returns:
            dict: User settings with default values if file doesn't exist
        """
        if 'user_settings' not in self._cache:
            try:
                with open(self.user_settings_file, 'r') as f:
                    self._cache['user_settings'] = ujson.load(f)
            except (OSError, ValueError) as e:
                self.error_handler.handle_error(e, f"Failed to load user settings, using defaults")
                self._cache['user_settings'] = self._default_settings()
        return self._cache['user_settings']
    
    def _default_settings(self):
        """
        Get default user settings
        
        Returns:
            dict: Default settings structure
        """
        return {
            "last_selected": {
                "brand": None,
                "system": None,
                "system_name": None,
                "tool": None
            },
            "wifi": {
                "ssid": None,
                "password": None,
                "auto_connect": True
            },
            "preferences": {
                "theme": "light",
                "language": "en",
                "auto_update": True
            },
            "custom_systems": []
        }
    
    def update_last_selected(self, brand, system, system_name, tool):
        """
        Update last selected system and tool
        
        Args:
            brand (str): Vehicle brand
            system (str): System type (Engine, ABS, etc.)
            system_name (str): Specific system name
            tool (str): Selected tool name
            
        Returns:
            bool: True if update successful
        """
        settings = self.get_user_settings()
        settings["last_selected"] = {
            "brand": brand,
            "system": system,
            "system_name": system_name,
            "tool": tool
        }
        return self.save_user_settings(settings)
    
    def update_wifi_config(self, ssid, password, auto_connect=True):
        """
        Update WiFi configuration
        
        Args:
            ssid (str): Network SSID
            password (str): Network password
            auto_connect (bool): Auto-connect on startup
            
        Returns:
            bool: True if update successful
        """
        settings = self.get_user_settings()
        settings["wifi"] = {
            "ssid": ssid,
            "password": password,
            "auto_connect": auto_connect
        }
        return self.save_user_settings(settings)
    
    def get_brands(self):
        """
        Get list of available vehicle brands
        
        Returns:
            list: Sorted list of unique brands
        """
        systems_db = self.load_systems()
        brands = set()
        for system in systems_db.get("systems", []):
            brands.add(system.get("brand"))
        return sorted(list(brands))
    
    def get_system_types(self, brand):
        """
        Get system types for a specific brand
        
        Args:
            brand (str): Vehicle brand
            
        Returns:
            list: Sorted list of system types for the brand
        """
        systems_db = self.load_systems()
        types = set()
        for system in systems_db.get("systems", []):
            if system.get("brand") == brand:
                types.add(system.get("type"))
        return sorted(list(types))
    
    def get_system_names(self, brand, system_type):
        """
        Get system names for a specific brand and type
        
        Args:
            brand (str): Vehicle brand
            system_type (str): System type
            
        Returns:
            list: Sorted list of system names
        """
        systems_db = self.load_systems()
        names = set()
        for system in systems_db.get("systems", []):
            if (system.get("brand") == brand and 
                system.get("type") == system_type):
                names.add(system.get("system_name"))
        return sorted(list(names))
    
    def get_system_tools(self, brand, system_type, system_name):
        """
        Get available tools for a specific system
        
        Args:
            brand (str): Vehicle brand
            system_type (str): System type
            system_name (str): System name
            
        Returns:
            list: List of tool dictionaries
        """
        systems_db = self.load_systems()
        for system in systems_db.get("systems", []):
            if (system.get("brand") == brand and 
                system.get("type") == system_type and
                system.get("system_name") == system_name):
                return system.get("tools", [])
        return []
    
    def get_tool_config(self, brand, system_type, system_name, tool_name):
        """
        Get configuration for a specific tool
        
        Args:
            brand (str): Vehicle brand
            system_type (str): System type
            system_name (str): System name
            tool_name (str): Tool name
            
        Returns:
            dict: Tool configuration or None if not found
        """
        tools = self.get_system_tools(brand, system_type, system_name)
        for tool in tools:
            if tool.get("name") == tool_name:
                return tool.get("config", {})
        return None
    
    def is_configured(self):
        """
        Check if device is configured (has WiFi settings)
        
        Returns:
            bool: True if device is configured
        """
        settings = self.get_user_settings()
        wifi_config = settings.get("wifi", {})
        return wifi_config.get("ssid") is not None
    
    def backup_user_data(self, backup_path="/backup"):
        """
        Create backup of user data
        
        Args:
            backup_path (str): Backup directory path
            
        Returns:
            bool: True if backup successful
        """
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Copy user settings
            import shutil
            shutil.copy2(self.user_settings_file, f"{backup_path}/user_settings.json")
            
            return True
        except Exception as e:
            self.error_handler.handle_error(e, "Failed to backup user data")
            return False
    
    def clear_cache(self):
        """Clear internal cache to force reload from disk"""
        self._cache.clear()

# Global data manager instance
data_manager = DataManager()
