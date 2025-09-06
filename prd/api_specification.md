# API Specification Document
## ECU Diagnostic Tool

### Document Information
**Product Name:** ECU Diagnostic Tool  
**Version:** 1.0  
**Document Version:** 1.0  
**Date:** 2025-09-06  
**Document Type:** API Specification  

---

## 1. Overview

This document defines the internal API specifications for the ECU Diagnostic Tool, including hardware abstraction layer interfaces, data management APIs, and inter-component communication protocols.

## 2. Hardware Abstraction Layer APIs

### 2.1 WiFi Manager API

#### 2.1.1 WiFiManager Class
```python
class WiFiManager:
    """WiFi connectivity management interface"""
    
    def __init__(self) -> None:
        """Initialize WiFi manager"""
        pass
    
    def scan_networks(self) -> List[Dict[str, Any]]:
        """
        Scan for available WiFi networks
        
        Returns:
            List of network dictionaries with keys:
            - ssid: str - Network name
            - signal: int - Signal strength in dBm
            - security: int - Security type (0=Open, 1=WEP, 2=WPA, 3=WPA2)
            - channel: int - WiFi channel
        
        Raises:
            WiFiError: If scan operation fails
        """
        pass
    
    def connect(self, ssid: str, password: str, timeout: int = 30) -> bool:
        """
        Connect to WiFi network
        
        Args:
            ssid: Network name
            password: Network password (empty for open networks)
            timeout: Connection timeout in seconds
        
        Returns:
            bool: True if connection successful, False otherwise
        
        Raises:
            WiFiError: If connection attempt fails
        """
        pass
    
    def disconnect(self) -> None:
        """Disconnect from current WiFi network"""
        pass
    
    def is_connected(self) -> bool:
        """
        Check if connected to WiFi
        
        Returns:
            bool: True if connected, False otherwise
        """
        pass
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get current connection information
        
        Returns:
            Dictionary with keys:
            - ssid: str - Connected network name
            - ip: str - Assigned IP address
            - signal: int - Current signal strength
            - channel: int - Current channel
        """
        pass
    
    def check_for_updates(self) -> Dict[str, Any]:
        """
        Check for firmware updates
        
        Returns:
            Dictionary with keys:
            - available: bool - Update available
            - version: str - Available version
            - size: int - Update size in bytes
            - url: str - Download URL
        """
        pass
```

### 2.2 ECU Manager API

#### 2.2.1 ECUManager Class
```python
class ECUManager:
    """ECU communication and simulation interface"""
    
    def __init__(self) -> None:
        """Initialize ECU manager"""
        pass
    
    def get_live_data(self) -> Dict[str, Any]:
        """
        Retrieve live data from ECU
        
        Returns:
            Dictionary with live data parameters:
            - rpm: int - Engine RPM
            - coolant_temp: float - Coolant temperature in Celsius
            - throttle_position: float - Throttle position percentage
            - engine_load: float - Engine load percentage
            - fuel_level: float - Fuel level percentage
            - timestamp: float - Data timestamp
        
        Raises:
            ECUError: If data retrieval fails
        """
        pass
    
    def simulate_rpm(self, rpm: int, enable_output: bool = True) -> None:
        """
        Simulate RPM signal output
        
        Args:
            rpm: Target RPM value (0-10000)
            enable_output: Enable/disable signal output
        
        Raises:
            ECUError: If simulation setup fails
            ValueError: If RPM value out of range
        """
        pass
    
    def configure_sensors(self, config: Dict[str, Any]) -> bool:
        """
        Configure sensor simulation parameters
        
        Args:
            config: Configuration dictionary with keys:
                - crank: Dict with 'degrees_per_tooth', 'missing_teeth'
                - cam: Dict with 'degrees_per_tooth', 'tooth_pattern'
        
        Returns:
            bool: True if configuration successful
        
        Raises:
            ECUError: If configuration fails
            ValueError: If configuration invalid
        """
        pass
    
    def start_simulation(self) -> None:
        """Start sensor signal simulation"""
        pass
    
    def stop_simulation(self) -> None:
        """Stop sensor signal simulation"""
        pass
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """
        Get current simulation status
        
        Returns:
            Dictionary with keys:
            - active: bool - Simulation running
            - rpm: int - Current RPM
            - crank_enabled: bool - Crank sensor enabled
            - cam_enabled: bool - Cam sensor enabled
        """
        pass
```

### 2.3 DTC Manager API

#### 2.3.1 DTCManager Class
```python
class DTCManager:
    """Diagnostic Trouble Code management interface"""
    
    def __init__(self) -> None:
        """Initialize DTC manager"""
        pass
    
    def read_dtc(self) -> List[Dict[str, Any]]:
        """
        Read diagnostic trouble codes
        
        Returns:
            List of DTC dictionaries with keys:
            - code: str - DTC code (e.g., "P0300")
            - description: str - Human readable description
            - status: str - Status ("Current", "Pending", "Stored")
            - freeze_frame: Dict - Associated freeze frame data
            - timestamp: float - Detection timestamp
        
        Raises:
            DTCError: If read operation fails
        """
        pass
    
    def clear_dtc(self, codes: List[str] = None) -> bool:
        """
        Clear diagnostic trouble codes
        
        Args:
            codes: List of specific codes to clear (None for all)
        
        Returns:
            bool: True if clear operation successful
        
        Raises:
            DTCError: If clear operation fails
        """
        pass
    
    def get_dtc_definitions(self) -> Dict[str, str]:
        """
        Get DTC code definitions
        
        Returns:
            Dictionary mapping DTC codes to descriptions
        """
        pass
    
    def format_dtc_display(self, dtcs: List[Dict[str, Any]]) -> str:
        """
        Format DTCs for display
        
        Args:
            dtcs: List of DTC dictionaries
        
        Returns:
            str: Formatted display string
        """
        pass
```

## 3. Data Management APIs

### 3.1 Data Manager API

#### 3.1.1 DataManager Class
```python
class DataManager:
    """Data persistence and configuration management"""
    
    def __init__(self, base_path: str = "/db") -> None:
        """
        Initialize data manager
        
        Args:
            base_path: Base directory for data files
        """
        pass
    
    def load_systems(self) -> Dict[str, Any]:
        """
        Load systems database
        
        Returns:
            Dictionary containing systems configuration
        
        Raises:
            DataError: If load operation fails
        """
        pass
    
    def save_systems(self, systems: Dict[str, Any]) -> bool:
        """
        Save systems database
        
        Args:
            systems: Systems configuration dictionary
        
        Returns:
            bool: True if save successful
        
        Raises:
            DataError: If save operation fails
        """
        pass
    
    def get_user_settings(self) -> Dict[str, Any]:
        """
        Load user settings
        
        Returns:
            Dictionary containing user settings
        """
        pass
    
    def save_user_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Save user settings
        
        Args:
            settings: User settings dictionary
        
        Returns:
            bool: True if save successful
        
        Raises:
            DataError: If save operation fails
        """
        pass
    
    def update_last_selected(self, brand: str, system: str, 
                           system_name: str, tool: str) -> bool:
        """
        Update last selected system and tool
        
        Args:
            brand: Vehicle brand
            system: System type
            system_name: Specific system name
            tool: Selected tool
        
        Returns:
            bool: True if update successful
        """
        pass
    
    def get_system_config(self, brand: str, system: str, 
                         system_name: str) -> Dict[str, Any]:
        """
        Get configuration for specific system
        
        Args:
            brand: Vehicle brand
            system: System type
            system_name: Specific system name
        
        Returns:
            Dictionary containing system configuration
        
        Raises:
            DataError: If system not found
        """
        pass
    
    def backup_user_data(self, backup_path: str) -> bool:
        """
        Create backup of user data
        
        Args:
            backup_path: Backup file path
        
        Returns:
            bool: True if backup successful
        """
        pass
    
    def restore_user_data(self, backup_path: str) -> bool:
        """
        Restore user data from backup
        
        Args:
            backup_path: Backup file path
        
        Returns:
            bool: True if restore successful
        """
        pass
```

## 4. Screen Management APIs

### 4.1 Navigation Manager API

#### 4.1.1 NavigationManager Class
```python
class NavigationManager:
    """Screen navigation and state management"""
    
    def __init__(self) -> None:
        """Initialize navigation manager"""
        pass
    
    def register_screen(self, name: str, screen_class: type) -> None:
        """
        Register a screen class
        
        Args:
            name: Screen identifier
            screen_class: Screen class to register
        """
        pass
    
    def navigate_to(self, screen_name: str, **kwargs) -> None:
        """
        Navigate to specified screen
        
        Args:
            screen_name: Target screen identifier
            **kwargs: Parameters to pass to screen constructor
        
        Raises:
            NavigationError: If screen not found or navigation fails
        """
        pass
    
    def go_back(self) -> bool:
        """
        Navigate back to previous screen
        
        Returns:
            bool: True if navigation successful, False if no previous screen
        """
        pass
    
    def get_current_screen(self) -> str:
        """
        Get current screen name
        
        Returns:
            str: Current screen identifier
        """
        pass
    
    def clear_history(self) -> None:
        """Clear navigation history"""
        pass
```

### 4.2 Base Screen API

#### 4.2.1 BaseScreen Interface
```python
class BaseScreen:
    """Base interface for all screens"""
    
    def __init__(self, scr: lv.screen, **kwargs) -> None:
        """
        Initialize screen
        
        Args:
            scr: LVGL screen object
            **kwargs: Screen-specific parameters
        """
        pass
    
    def create_ui(self) -> None:
        """Create UI elements - must be implemented by subclasses"""
        raise NotImplementedError
    
    def on_enter(self) -> None:
        """Called when screen becomes active"""
        pass
    
    def on_exit(self) -> None:
        """Called when leaving screen"""
        pass
    
    def cleanup(self) -> None:
        """Clean up resources"""
        pass
    
    def handle_event(self, event_type: str, data: Any) -> None:
        """
        Handle system events
        
        Args:
            event_type: Type of event
            data: Event data
        """
        pass
```

## 5. Event System APIs

### 5.1 Event Manager API

#### 5.1.1 EventManager Class
```python
class EventManager:
    """System-wide event management"""
    
    def __init__(self) -> None:
        """Initialize event manager"""
        pass
    
    def subscribe(self, event_type: str, callback: callable) -> str:
        """
        Subscribe to event type
        
        Args:
            event_type: Type of event to subscribe to
            callback: Function to call when event occurs
        
        Returns:
            str: Subscription ID for unsubscribing
        """
        pass
    
    def unsubscribe(self, subscription_id: str) -> None:
        """
        Unsubscribe from events
        
        Args:
            subscription_id: ID returned from subscribe()
        """
        pass
    
    def emit(self, event_type: str, data: Any = None) -> None:
        """
        Emit an event
        
        Args:
            event_type: Type of event to emit
            data: Event data to pass to subscribers
        """
        pass
    
    def clear_subscribers(self, event_type: str = None) -> None:
        """
        Clear event subscribers
        
        Args:
            event_type: Specific event type to clear (None for all)
        """
        pass
```

## 6. Error Handling APIs

### 6.1 Error Classes

```python
class ECUDiagnosticError(Exception):
    """Base exception for ECU diagnostic tool"""
    pass

class WiFiError(ECUDiagnosticError):
    """WiFi operation errors"""
    pass

class ECUError(ECUDiagnosticError):
    """ECU communication errors"""
    pass

class DTCError(ECUDiagnosticError):
    """DTC operation errors"""
    pass

class DataError(ECUDiagnosticError):
    """Data management errors"""
    pass

class NavigationError(ECUDiagnosticError):
    """Navigation errors"""
    pass

class HardwareError(ECUDiagnosticError):
    """Hardware abstraction errors"""
    pass
```

### 6.2 Error Handler API

#### 6.2.1 ErrorHandler Class
```python
class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self, max_log_size: int = 100) -> None:
        """
        Initialize error handler
        
        Args:
            max_log_size: Maximum number of log entries to keep
        """
        pass
    
    def handle_error(self, error: Exception, context: str = "", 
                    severity: str = "ERROR") -> None:
        """
        Handle and log error
        
        Args:
            error: Exception that occurred
            context: Context information
            severity: Error severity ("INFO", "WARNING", "ERROR", "CRITICAL")
        """
        pass
    
    def get_error_log(self) -> List[Dict[str, Any]]:
        """
        Get error log entries
        
        Returns:
            List of error log dictionaries
        """
        pass
    
    def clear_error_log(self) -> None:
        """Clear error log"""
        pass
    
    def show_error_dialog(self, error: Exception, context: str = "") -> None:
        """
        Show error dialog to user
        
        Args:
            error: Exception to display
            context: Additional context information
        """
        pass
```

## 7. Configuration Schema

### 7.1 Systems Database Schema
```json
{
  "systems": [
    {
      "brand": "string",
      "type": "string",
      "system_name": "string",
      "tools": [
        {
          "name": "string",
          "type": "string",
          "config": {
            "crank": {
              "degrees_per_tooth": "number",
              "missing_teeth": "number"
            },
            "cam": {
              "degrees_per_tooth": "number",
              "tooth_pattern": "array of numbers"
            }
          }
        }
      ]
    }
  ]
}
```

### 7.2 User Settings Schema
```json
{
  "last_selected": {
    "brand": "string",
    "system": "string",
    "system_name": "string",
    "tool": "string"
  },
  "wifi": {
    "ssid": "string",
    "password": "string",
    "auto_connect": "boolean"
  },
  "preferences": {
    "theme": "string",
    "language": "string",
    "auto_update": "boolean"
  },
  "custom_systems": "array"
}
```

---

**Document Control:**
- Created: 2025-09-06
- Last Modified: 2025-09-06
- Next Review: 2025-12-06
- Version: 1.0
