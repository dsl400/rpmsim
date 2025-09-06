# System Architecture and Technical Design Document
## ECU Diagnostic Tool

### Document Information
**Product Name:** ECU Diagnostic Tool  
**Version:** 1.0  
**Document Version:** 1.0  
**Date:** 2025-09-06  
**Document Type:** System Architecture and Technical Design  

---

## 1. Executive Summary

This document defines the system architecture and technical design for the ECU Diagnostic Tool, a portable automotive diagnostic device built on ESP32S3 hardware with MicroPython runtime. The system provides comprehensive ECU diagnostic capabilities including RPM simulation, DTC management, and live data monitoring through a touchscreen interface with WiFi connectivity.

## 2. System Overview

### 2.1 High-Level Architecture

The ECU Diagnostic Tool follows a layered architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ WiFi Setup  │ │ Main Screen │ │   System Selection      │ │
│  │   Screen    │ │             │ │       Screen            │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ RPM Sim     │ │ DTC Manager │ │   Live Data Monitor     │ │
│  │   Screen    │ │   Screen    │ │       Screen            │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Application Logic Layer                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ Navigation  │ │ State Mgmt  │ │   Configuration Mgmt    │ │
│  │  Manager    │ │             │ │                         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                Hardware Abstraction Layer                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ WiFi Mgr    │ │ ECU Manager │ │     DTC Manager         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ I/O Manager │ │ CAN Manager │ │   File System Mgr       │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Hardware Layer                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ ESP32S3 MCU │ │ 5" LCD      │ │    Touch Controller     │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ WiFi Module │ │ CAN Bus     │ │    Signal Generators    │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

#### 2.2.1 Boot System
- **boot.py**: Immutable boot process manager
- **main.py**: Application entry point with LVGL initialization
- **display.py**: Hardware display and touchscreen configuration

#### 2.2.2 User Interface Layer
- **Screen Modules**: Modular screen implementations in `screens/` directory
- **Navigation System**: Centralized screen management and transitions
- **LVGL Integration**: Hardware-accelerated GUI framework

#### 2.2.3 Hardware Abstraction Layer
- **WiFi Manager**: Network connectivity and firmware updates
- **ECU Manager**: Live data acquisition and sensor simulation
- **DTC Manager**: Diagnostic trouble code operations
- **I/O Manager**: Hardware input/output abstraction
- **CAN Manager**: CAN bus communication interface

#### 2.2.4 Data Management Layer
- **JSON Database**: System and tool configuration storage
- **User Settings**: Persistent user preferences and state
- **Configuration Manager**: Runtime configuration management

## 3. Detailed Component Design

### 3.1 Boot Process Architecture

```python
# Boot Sequence Flow
boot.py → main.py → display.py → main_screen.py
    ↓         ↓         ↓            ↓
Hardware   LVGL     Display      Navigation
 Init      Init     Config       Decision
```

**Boot Process Requirements:**
- REQ-001: WiFi setup mode if unconfigured
- REQ-002: Display last selected system tool
- REQ-003: Non-modifiable boot.py management
- REQ-042: Boot time ≤ 10 seconds

### 3.1.1 Boot Failure Recovery System

**Boot Loop Detection:**
```python
class BootRecovery:
    def __init__(self):
        self.max_boot_attempts = 3
        self.boot_counter_file = "/boot_counter.txt"
        self.safe_mode_flag = "/safe_mode.flag"
    
    def check_boot_health(self):
        """Check for boot loops and initiate recovery if needed"""
        boot_count = self.get_boot_counter()
        
        if boot_count >= self.max_boot_attempts:
            self.enter_safe_mode()
            return False
        
        self.increment_boot_counter()
        return True
    
    def enter_safe_mode(self):
        """Enter safe mode with minimal functionality"""
        self.create_safe_mode_flag()
        self.load_minimal_ui()
        self.enable_recovery_options()
```

**Recovery Requirements:**
- **REQ-051:** System shall detect boot loops after 3 consecutive failed boots
- **REQ-052:** Safe mode shall provide firmware rollback option
- **REQ-053:** Safe mode shall maintain WiFi connectivity for recovery
- **REQ-054:** Boot counter shall reset after successful 5-minute operation
- **REQ-055:** Recovery mode shall display clear error messages and options

### 3.2 Screen Management System

#### 3.2.1 Screen Hierarchy
```
Main Screen (Root)
├── WiFi Setup Screen
├── System Selection Screen
│   ├── Brand Selection
│   ├── System Type Selection  
│   ├── System Name Selection
│   └── Tool Selection
├── Diagnostic Tools
│   ├── RPM Simulator
│   │   └── RPM Sensor Config Editor
│   ├── DTC Manager
│   │   ├── Clear DTC
│   │   └── Read DTC
│   └── Live Data Monitor
├── Firmware Update Screen
└── System Information Screen
```

#### 3.2.2 Screen State Management
Each screen implements the following interface:
```python
class BaseScreen:
    def __init__(self, scr: lv.screen)
    def create_ui(self) -> None
    def on_enter(self) -> None
    def on_exit(self) -> None
    def cleanup(self) -> None
```

### 3.3 Data Architecture

#### 3.3.1 Database Schema

**Systems Database (systems.json)**
```json
{
  "systems": [
    {
      "brand": "VW",
      "type": "Engine",
      "system_name": "Bosch ME7.9.7",
      "tools": [
        {
          "name": "RPM Simulator",
          "type": "rpm",
          "config": {
            "crank": {
              "degrees_per_tooth": 6,
              "missing_teeth": 2
            },
            "cam": {
              "degrees_per_tooth": 12,
              "tooth_pattern": [1,1,1,1,1,1,0,1,1,1,1,1]
            }
          }
        }
      ]
    }
  ]
}
```

**User Settings (user_settings.json)**
```json
{
  "last_selected": {
    "brand": "VW",
    "system": "Engine",
    "system_name": "Bosch ME7.9.7",
    "tool": "RPM Simulator"
  },
  "wifi": {
    "ssid": "NetworkName",
    "password": "encrypted_password",
    "auto_connect": true
  },
  "preferences": {
    "theme": "light",
    "language": "en",
    "auto_update": true
  },
  "custom_systems": []
}
```

#### 3.3.2 Data Access Layer
```python
class DataManager:
    def load_systems(self) -> dict
    def save_user_settings(self, settings: dict) -> bool
    def get_last_selected(self) -> tuple
    def update_wifi_config(self, config: dict) -> bool
    def backup_user_data(self) -> bool
    def restore_user_data(self) -> bool
```

### 3.4 Hardware Abstraction Layer

#### 3.4.1 WiFi Management
```python
class WiFiManager:
    def scan_networks(self) -> List[dict]
    def connect(self, ssid: str, password: str) -> bool
    def disconnect(self) -> None
    def is_connected(self) -> bool
    def get_signal_strength(self) -> int
    def check_for_updates(self) -> bool
```

#### 3.4.2 ECU Communication
```python
class ECUManager:
    def get_live_data(self) -> dict
    def simulate_rpm(self, rpm: int) -> None
    def configure_sensors(self, config: dict) -> bool
    def start_simulation(self) -> None
    def stop_simulation(self) -> None
```

#### 3.4.3 DTC Management
```python
class DTCManager:
    def read_dtc(self) -> List[dict]
    def clear_dtc(self) -> bool
    def get_dtc_definitions(self) -> dict
    def format_dtc_display(self, dtcs: List[dict]) -> str
```

## 4. System Integration

### 4.1 Inter-Component Communication

#### 4.1.1 Event-Driven Architecture
- LVGL event system for UI interactions
- Observer pattern for state changes
- Message passing for hardware operations

#### 4.1.2 State Synchronization
- Centralized state management
- Atomic operations for critical data
- Rollback mechanisms for failed operations

### 4.2 Error Handling Strategy

#### 4.2.1 Error Categories
1. **Hardware Errors**: WiFi disconnection, CAN bus failure
2. **Data Errors**: Corrupted JSON, missing files
3. **User Errors**: Invalid input, unsupported operations
4. **System Errors**: Memory exhaustion, timeout conditions

#### 4.2.2 Recovery Mechanisms
- Graceful degradation for non-critical failures
- Automatic retry with exponential backoff
- User notification with recovery options
- Safe mode operation for critical failures

## 5. Performance Specifications

### 5.1 Response Time Requirements
- REQ-043: Screen transitions ≤ 2 seconds
- REQ-044: RPM updates ≥ 10Hz refresh rate
- UI interactions ≤ 100ms response time
- WiFi connection establishment ≤ 30 seconds

### 5.2 Memory Management
- Heap memory monitoring and cleanup
- Screen buffer optimization
- JSON parsing memory efficiency
- Garbage collection optimization

### 5.3 Power Management
- Sleep mode during inactivity
- Display brightness auto-adjustment
- WiFi power saving modes
- Battery level monitoring

## 6. Security Architecture

### 6.1 Data Protection
- WiFi password encryption in storage
- Secure firmware update verification
- User data backup encryption
- Access control for system modifications

### 6.2 Network Security
- WPA2/WPA3 WiFi security protocols
- HTTPS for firmware updates
- Certificate validation
- Network isolation for diagnostic operations

## 7. Deployment Architecture

### 7.1 Firmware Structure
```
firmware/
├── boot.py (immutable)
├── main.py (immutable)  
├── display.py (immutable)
├── application/
│   ├── screens/
│   ├── hardware/
│   ├── utils/
│   └── db/
└── user_data/
    ├── user_settings.json
    └── custom_systems.json
```

### 7.2 Update Strategy
- Differential updates for application code
- User data preservation during updates
- Rollback capability for failed updates
- Version compatibility checking

### 7.2.1 Firmware Update Failure Recovery

**Atomic Update Process:**
```python
class SecureUpdateManager:
    def apply_update_with_recovery(self, update_data):
        """Apply update with comprehensive rollback capability"""
        try:
            # Create complete system backup
            self.create_full_backup()
            
            # Verify update integrity before application
            if not self.verify_update_integrity(update_data):
                raise UpdateError("Update integrity check failed")
            
            # Apply update atomically
            self.atomic_update_application(update_data)
            
            # Verify new firmware boots successfully
            if not self.test_boot_sequence():
                self.rollback_to_backup()
                raise UpdateError("New firmware failed boot test")
            
            # Clear boot failure counters
            self.reset_boot_counters()
            
        except Exception as e:
            self.handle_update_failure(e)
            self.enter_recovery_mode()
```

**Update Failure Requirements:**
- **REQ-056:** Failed updates shall automatically rollback within 30 seconds
- **REQ-057:** System shall maintain previous firmware version during update
- **REQ-058:** Update process shall be resumable after power failure
- **REQ-059:** Recovery mode shall allow manual firmware selection
- **REQ-060:** All update operations shall be logged for diagnostics

## 8. Testing Strategy

### 8.1 Unit Testing
- Hardware abstraction layer mocking
- Screen component isolation testing
- Data manager functionality validation
- Error condition simulation

### 8.2 Integration Testing
- End-to-end user workflow validation
- Hardware-software integration testing
- Performance benchmarking
- Stress testing under load

### 8.3 Simulation Environment
- SDL-based display simulation
- Hardware mock implementations
- Automated UI testing framework
- Continuous integration pipeline

## 9. Quality Assurance and Testing

### 9.1 Testing Strategy Overview
- **Unit Testing**: Individual component validation
- **Integration Testing**: Component interaction verification
- **System Testing**: End-to-end functionality validation
- **Performance Testing**: Response time and resource usage validation
- **Usability Testing**: User experience validation

### 9.2 Test Coverage Requirements
- Hardware abstraction layer: 90% code coverage
- Screen components: 85% code coverage
- Data management: 95% code coverage
- Critical path functions: 100% code coverage

### 9.3 Automated Testing Framework
```python
# Test automation structure
tests/
├── unit/
│   ├── test_wifi_manager.py
│   ├── test_ecu_manager.py
│   ├── test_data_manager.py
│   └── test_navigation.py
├── integration/
│   ├── test_screen_navigation.py
│   ├── test_hardware_integration.py
│   └── test_data_persistence.py
├── system/
│   ├── test_user_workflows.py
│   ├── test_error_scenarios.py
│   └── test_performance.py
└── fixtures/
    ├── mock_hardware.py
    ├── test_data.json
    └── test_configs.py
```

## 10. Deployment and Maintenance

### 10.1 Firmware Packaging
- Modular firmware structure for selective updates
- User data preservation during updates
- Rollback capability for failed updates
- Digital signature verification for security

### 10.2 Remote Management
- Over-the-air (OTA) update capability
- Remote diagnostics and logging
- Configuration management
- Performance monitoring

### 10.3 Maintenance Procedures
- Regular system health checks
- Automated backup procedures
- Performance optimization routines
- Security update protocols

---

**Document Control:**
- Created: 2025-09-06
- Last Modified: 2025-09-06
- Next Review: 2025-12-06
- Version: 1.0
