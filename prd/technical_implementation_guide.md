# Technical Implementation Guide
## ECU Diagnostic Tool

### Document Information
**Product Name:** ECU Diagnostic Tool  
**Version:** 1.0  
**Document Version:** 1.0  
**Date:** 2025-09-06  
**Document Type:** Technical Implementation Guide  

---

## 1. Development Environment Setup

### 1.1 Required Tools and Dependencies
```bash
# Core Dependencies
- MicroPython 1.20+
- LVGL 9.2.1
- ESP32S3 SDK
- Python 3.8+ (for development tools)

# Development Tools
- ESP-IDF framework
- MicroPython cross-compiler
- LVGL GUI Guider (optional)
- Git version control
```

### 1.2 Project Structure
```
rpmsim/
├── src/                    # Main application source
│   ├── boot.py            # Boot process (immutable)
│   ├── main.py            # Hardware mode entry point
│   ├── main_sim.py        # Simulation mode entry point
│   ├── display.py         # Hardware display config (immutable)
│   ├── fs_driver.py       # File system driver
│   ├── screens/           # UI screen modules
│   │   ├── main_screen.py
│   │   ├── wifi_setup.py
│   │   ├── system_selection.py
│   │   ├── rpm_simulator/
│   │   ├── dtc/
│   │   └── live_data/
│   ├── hardware/          # Hardware abstraction layer
│   │   ├── wifi_manager.py
│   │   ├── ecu_manager.py
│   │   ├── dtc_manager.py
│   │   ├── io.py
│   │   ├── can.py
│   │   └── sim/           # Hardware simulation modules
│   │       ├── __init__.py
│   │       ├── hardware_sim.py
│   │       ├── wifi_sim.py
│   │       └── ecu_sim.py
│   ├── db/               # Database and configuration
│   │   ├── systems.json
│   │   └── user_settings.json
│   └── utils/            # Utility modules
├── sim/                  # Simulation environment
│   ├── main_sim.py
│   └── hardware/
├── sim_app/             # AppImage build system
├── prd/                 # Product requirements and design docs
└── tests/               # Test suites
```

## 2. Core Implementation Patterns

### 2.1 Screen Implementation Pattern
```python
# Base screen class pattern
import lvgl as lv

class BaseScreen:
    def __init__(self, scr):
        self.scr = scr
        self.widgets = {}
        self.create_ui()
    
    def create_ui(self):
        """Override in subclasses to create UI elements"""
        raise NotImplementedError
    
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
                widget.delete()

# Example implementation
class RPMSimulatorScreen(BaseScreen):
    def __init__(self, scr):
        self.current_rpm = 0
        super().__init__(scr)
    
    def create_ui(self):
        # Title
        self.widgets['title'] = lv.label(self.scr)
        self.widgets['title'].set_text("RPM Simulator")
        self.widgets['title'].align(lv.ALIGN.TOP_MID, 0, 10)
        
        # RPM display
        self.widgets['rpm_display'] = lv.label(self.scr)
        self.update_rpm_display()
        
        # Controls
        self.create_controls()
    
    def create_controls(self):
        # Increment/Decrement buttons
        self.widgets['inc_btn'] = lv.btn(self.scr)
        self.widgets['inc_btn'].set_size(100, 50)
        self.widgets['inc_btn'].add_event_cb(
            self.on_increment, lv.EVENT.CLICKED, None
        )
        
        # RPM slider
        self.widgets['rpm_slider'] = lv.slider(self.scr)
        self.widgets['rpm_slider'].set_range(0, 10000)
        self.widgets['rpm_slider'].add_event_cb(
            self.on_slider_change, lv.EVENT.VALUE_CHANGED, None
        )
    
    def on_increment(self, event):
        self.current_rpm = min(10000, self.current_rpm + 100)
        self.update_rpm_display()
    
    def on_slider_change(self, event):
        self.current_rpm = event.target.get_value()
        self.update_rpm_display()
    
    def update_rpm_display(self):
        self.widgets['rpm_display'].set_text(f"RPM: {self.current_rpm}")
        self.widgets['rpm_slider'].set_value(self.current_rpm)
```

### 2.2 Hardware Abstraction Pattern
```python
# Hardware manager base class
class HardwareManager:
    def __init__(self):
        self.initialized = False
        self.error_state = None
    
    def initialize(self):
        """Initialize hardware component"""
        try:
            self._hw_init()
            self.initialized = True
            return True
        except Exception as e:
            self.error_state = str(e)
            return False
    
    def _hw_init(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def is_available(self):
        return self.initialized and self.error_state is None

# WiFi Manager implementation
class WiFiManager(HardwareManager):
    def __init__(self):
        super().__init__()
        self.networks = []
        self.connected_ssid = None
    
    def _hw_init(self):
        # Initialize WiFi hardware
        import network
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
    
    def scan_networks(self):
        if not self.is_available():
            return []
        
        try:
            scan_results = self.wlan.scan()
            self.networks = [
                {
                    'ssid': result[0].decode('utf-8'),
                    'signal': result[3],
                    'security': result[4]
                }
                for result in scan_results
            ]
            return self.networks
        except Exception as e:
            self.error_state = f"Scan failed: {e}"
            return []
    
    def connect(self, ssid, password):
        if not self.is_available():
            return False
        
        try:
            self.wlan.connect(ssid, password)
            # Wait for connection with timeout
            timeout = 30
            while timeout > 0 and not self.wlan.isconnected():
                time.sleep(1)
                timeout -= 1
            
            if self.wlan.isconnected():
                self.connected_ssid = ssid
                return True
            return False
        except Exception as e:
            self.error_state = f"Connection failed: {e}"
            return False
```

### 2.3 Data Management Pattern
```python
import ujson
import os

class DataManager:
    def __init__(self, base_path="/db"):
        self.base_path = base_path
        self.systems_file = f"{base_path}/systems.json"
        self.user_settings_file = f"{base_path}/user_settings.json"
        self._cache = {}
    
    def load_systems(self):
        """Load systems database with caching"""
        if 'systems' not in self._cache:
            try:
                with open(self.systems_file, 'r') as f:
                    self._cache['systems'] = ujson.load(f)
            except (OSError, ValueError):
                self._cache['systems'] = {"systems": []}
        return self._cache['systems']
    
    def save_user_settings(self, settings):
        """Save user settings with atomic write"""
        temp_file = f"{self.user_settings_file}.tmp"
        try:
            with open(temp_file, 'w') as f:
                ujson.dump(settings, f)
            
            # Atomic rename
            os.rename(temp_file, self.user_settings_file)
            self._cache['user_settings'] = settings
            return True
        except Exception as e:
            # Clean up temp file
            try:
                os.remove(temp_file)
            except:
                pass
            return False
    
    def get_user_settings(self):
        """Load user settings with defaults"""
        if 'user_settings' not in self._cache:
            try:
                with open(self.user_settings_file, 'r') as f:
                    self._cache['user_settings'] = ujson.load(f)
            except (OSError, ValueError):
                self._cache['user_settings'] = self._default_settings()
        return self._cache['user_settings']
    
    def _default_settings(self):
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
                "language": "en"
            }
        }
    
    def update_last_selected(self, brand, system, system_name, tool):
        """Update last selected system and tool"""
        settings = self.get_user_settings()
        settings["last_selected"] = {
            "brand": brand,
            "system": system,
            "system_name": system_name,
            "tool": tool
        }
        return self.save_user_settings(settings)
```

## 3. Navigation and State Management

### 3.1 Screen Navigation System
```python
class NavigationManager:
    def __init__(self):
        self.screen_stack = []
        self.current_screen = None
        self.screens = {}
    
    def register_screen(self, name, screen_class):
        """Register a screen class"""
        self.screens[name] = screen_class
    
    def navigate_to(self, screen_name, **kwargs):
        """Navigate to a screen"""
        if screen_name not in self.screens:
            raise ValueError(f"Screen {screen_name} not registered")
        
        # Clean up current screen
        if self.current_screen:
            self.current_screen.on_exit()
            self.screen_stack.append(self.current_screen)
        
        # Create and show new screen
        scr = lv.screen()
        screen_instance = self.screens[screen_name](scr, **kwargs)
        screen_instance.on_enter()
        
        lv.screen_load(scr)
        self.current_screen = screen_instance
    
    def go_back(self):
        """Navigate back to previous screen"""
        if not self.screen_stack:
            return False
        
        # Clean up current screen
        if self.current_screen:
            self.current_screen.cleanup()
        
        # Restore previous screen
        previous_screen = self.screen_stack.pop()
        previous_screen.on_enter()
        lv.screen_load(previous_screen.scr)
        self.current_screen = previous_screen
        return True

# Global navigation instance
nav_manager = NavigationManager()
```

### 3.2 Application State Management
```python
class AppState:
    def __init__(self):
        self.data_manager = DataManager()
        self.wifi_manager = WiFiManager()
        self.ecu_manager = ECUManager()
        self.current_system = None
        self.current_tool = None
        self.is_configured = False
    
    def initialize(self):
        """Initialize application state"""
        # Initialize hardware managers
        self.wifi_manager.initialize()
        self.ecu_manager.initialize()
        
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
    
    def set_current_system(self, brand, system, system_name, tool):
        """Set current system and tool"""
        self.current_system = {
            "brand": brand,
            "system": system,
            "system_name": system_name
        }
        self.current_tool = tool
        
        # Save to user settings
        self.data_manager.update_last_selected(
            brand, system, system_name, tool
        )
    
    def get_system_tools(self, brand, system, system_name):
        """Get available tools for a system"""
        systems_db = self.data_manager.load_systems()
        for system_entry in systems_db.get("systems", []):
            if (system_entry["brand"] == brand and 
                system_entry["type"] == system and
                system_entry["system_name"] == system_name):
                return system_entry.get("tools", [])
        return []

# Global application state
app_state = AppState()
```

## 4. Error Handling and Logging

### 4.1 Error Handling Framework
```python
class ErrorHandler:
    def __init__(self):
        self.error_log = []
        self.max_log_size = 100
    
    def handle_error(self, error, context="", severity="ERROR"):
        """Handle and log errors"""
        error_entry = {
            "timestamp": time.time(),
            "error": str(error),
            "context": context,
            "severity": severity
        }
        
        self.error_log.append(error_entry)
        if len(self.error_log) > self.max_log_size:
            self.error_log.pop(0)
        
        # Show user notification for critical errors
        if severity == "CRITICAL":
            self.show_error_dialog(error, context)
    
    def show_error_dialog(self, error, context):
        """Show error dialog to user"""
        # Create modal dialog
        dialog = lv.msgbox(lv.screen_active())
        dialog.set_title("Error")
        dialog.set_text(f"An error occurred: {error}")
        dialog.add_button("OK")

# Global error handler
error_handler = ErrorHandler()

# Decorator for error handling
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(e, f"Function: {func.__name__}")
            return None
    return wrapper
```

## 5. Performance Optimization

### 5.1 Memory Management
```python
import gc

class MemoryManager:
    def __init__(self):
        self.gc_threshold = 1000  # bytes
    
    def check_memory(self):
        """Check available memory and trigger GC if needed"""
        free_mem = gc.mem_free()
        if free_mem < self.gc_threshold:
            gc.collect()
            return gc.mem_free()
        return free_mem
    
    def optimize_screen_transition(self):
        """Optimize memory during screen transitions"""
        gc.collect()
        # Force cleanup of LVGL objects
        lv.refr_now(None)

# Global memory manager
memory_manager = MemoryManager()
```

### 5.2 Performance Monitoring
```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, operation):
        """Start timing an operation"""
        self.metrics[operation] = time.ticks_ms()
    
    def end_timer(self, operation):
        """End timing and return duration"""
        if operation in self.metrics:
            duration = time.ticks_diff(time.ticks_ms(), self.metrics[operation])
            del self.metrics[operation]
            return duration
        return 0
    
    def measure_performance(self, func):
        """Decorator to measure function performance"""
        def wrapper(*args, **kwargs):
            start = time.ticks_ms()
            result = func(*args, **kwargs)
            duration = time.ticks_diff(time.ticks_ms(), start)
            print(f"{func.__name__} took {duration}ms")
            return result
        return wrapper

# Global performance monitor
perf_monitor = PerformanceMonitor()
```

## 6. Testing Framework

### 6.1 Unit Testing Setup
```python
# Simple unit testing framework for MicroPython
class TestCase:
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def assertEqual(self, a, b, msg=""):
        if a != b:
            raise AssertionError(f"Expected {a} == {b}. {msg}")
    
    def assertTrue(self, condition, msg=""):
        if not condition:
            raise AssertionError(f"Expected True. {msg}")
    
    def assertFalse(self, condition, msg=""):
        if condition:
            raise AssertionError(f"Expected False. {msg}")

class TestRunner:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_test(self, test_class):
        """Run all test methods in a test class"""
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_')]
        
        for method_name in test_methods:
            self.tests_run += 1
            try:
                test_instance.setUp()
                getattr(test_instance, method_name)()
                test_instance.tearDown()
                self.tests_passed += 1
                print(f"✓ {method_name}")
            except Exception as e:
                self.tests_failed += 1
                print(f"✗ {method_name}: {e}")
    
    def print_summary(self):
        print(f"\nTests run: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
```

## 8. Simulation Development

### 8.1 Simulation Environment Setup

The ECU Diagnostic Tool includes a comprehensive simulation environment for development and testing without physical hardware.

#### 8.1.1 Simulation Prerequisites
```bash
# Required for simulation
- MpSimulator-x86_64.AppImage (provided in sim_app/)
- SDL2 libraries (included in simulator)
- Linux/Windows/macOS development environment
```

#### 8.1.2 Starting Simulation Mode
```bash
# Navigate to project root
cd rpmsim/

# Start simulation mode
./sim_app/MpSimulator-x86_64.AppImage src/main_sim.py

# Run specific tests
./sim_app/MpSimulator-x86_64.AppImage test/integrated_test.py
```

### 8.2 Hardware Simulation Components

#### 8.2.1 WiFi Simulation (src/hardware/sim/wifi_sim.py)
```python
from hardware.sim.wifi_sim import WiFiSimulator

# Initialize WiFi simulation
wifi_sim = WiFiSimulator()
wifi_sim.initialize()

# Simulate network scanning
networks = wifi_sim.scan_networks()

# Simulate connection
success = wifi_sim.connect("TestNetwork", "password123")
```

#### 8.2.2 ECU Simulation (src/hardware/sim/ecu_sim.py)
```python
from hardware.sim.ecu_sim import ECUSimulator

# Initialize ECU simulation
ecu_sim = ECUSimulator()
ecu_sim.initialize()

# Start RPM simulation
ecu_sim.start_simulation()
ecu_sim.set_target_rpm(2500)

# Get live data
live_data = ecu_sim.get_live_data()
```

### 8.3 Development Workflow

#### 8.3.1 Simulation vs Hardware Mode
```python
# Entry points
main.py      # Hardware mode (ESP32S3)
main_sim.py  # Simulation mode (Development)

# Hardware abstraction
hardware/wifi_manager.py    # Real WiFi hardware
hardware/sim/wifi_sim.py    # WiFi simulation

hardware/ecu_manager.py     # Real ECU hardware
hardware/sim/ecu_sim.py     # ECU simulation
```

#### 8.3.2 Testing in Simulation
```bash
# Run comprehensive tests
./sim_app/MpSimulator-x86_64.AppImage test/comprehensive_test.py

# Run visual UI tests
./sim_app/MpSimulator-x86_64.AppImage test/visual_test.py

# Run integration tests
./sim_app/MpSimulator-x86_64.AppImage test/integrated_test.py
```

### 8.4 Simulation Features

#### 8.4.1 Realistic Hardware Behavior
- WiFi network scanning with signal strength variation
- ECU live data simulation with realistic automotive parameters
- Connection success/failure simulation based on conditions
- Hardware fault injection for error testing

#### 8.4.2 Interactive Development
- Real-time UI interaction with mouse simulation
- Live parameter adjustment during simulation
- Debug output and logging
- Performance monitoring

#### 8.4.3 Testing Capabilities
- Automated test execution in simulation environment
- UI interaction testing without physical hardware
- Error scenario simulation and recovery testing
- Performance benchmarking

### 8.5 Deployment Transition

#### 8.5.1 From Simulation to Hardware
```bash
# 1. Test in simulation
./sim_app/MpSimulator-x86_64.AppImage src/main_sim.py

# 2. Validate all functionality
./sim_app/MpSimulator-x86_64.AppImage test/comprehensive_test.py

# 3. Flash to hardware
cd firmware/
./flash.sh

# 4. Hardware automatically runs src/main.py
```

#### 8.5.2 Code Compatibility
The same application code runs in both simulation and hardware modes:
- UI screens work identically in both environments
- Hardware abstraction layer provides seamless transition
- Configuration and data management remain consistent
- Error handling and recovery work in both modes

---

**Document Control:**
- Created: 2025-09-06
- Last Modified: 2025-09-06
- Next Review: 2025-12-06
- Version: 1.0
