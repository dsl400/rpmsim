# Product Requirements Document (PRD)
## ECU Diagnostic Tool

### 1. Product Overview

**Product Name:** ECU Diagnostic Tool  
**Version:** 1.0  
**Document Version:** 1.0  
**Date:** [Current Date]  

**Product Description:**  
A portable diagnostic device for automotive ECU (Electronic Control Unit) systems, featuring WiFi connectivity, touchscreen interface, and comprehensive diagnostic capabilities including RPM simulation, DTC management, and live data monitoring.

### 2. Business Objectives

- Provide automotive technicians with a portable, user-friendly ECU diagnostic solution
- Support multiple vehicle manufacturers and ECU systems
- Enable real-time diagnostic capabilities with wireless connectivity
- Offer configurable sensor simulation for testing purposes

### 3. Target Users

**Primary Users:**
- Automotive technicians
- ECU repair specialists
- Vehicle diagnostic professionals

**Secondary Users:**
- Automotive students
- Independent mechanics
- Fleet maintenance teams

### 4. Core Features & Requirements

#### 4.1 Boot Process & Initial Setup
- **REQ-001:** Device shall enter WiFi setup mode if not previously configured
- **REQ-002:** Device shall display last selected system tool upon startup
- **REQ-003:** Boot process shall be managed by `boot.py` (non-modifiable)

#### 4.2 ECU Diagnostic Tools

##### 4.2.1 RPM Simulator
- **REQ-004:** Display current RPM value with real-time updates
- **REQ-005:** Provide increment/decrement buttons for RPM adjustment
- **REQ-006:** Include RPM slider for quick value selection
- **REQ-007:** Toggle button to enable/disable sensor output for cam and crank
- **REQ-008:** Access button to RPM Sensor Configuration Editor

##### 4.2.2 Diagnostic Trouble Codes (DTC)
- **REQ-009:** Clear DTC functionality (Future Release)
- **REQ-010:** Read DTC functionality (Future Release)

##### 4.2.3 Live Data Monitoring
- **REQ-011:** Read Live Data functionality (Future Release)

#### 4.3 User Interface Requirements

##### 4.3.1 WiFi Setup Mode
- **REQ-012:** Display available WiFi networks for selection
- **REQ-013:** Show connection progress with spinner during WiFi connection
- **REQ-014:** Check for firmware updates after successful WiFi connection
- **REQ-015:** Prompt user for firmware update if available
- **REQ-016:** Navigate to Firmware Update Screen upon user confirmation

##### 4.3.2 Main Screen
- **REQ-017:** Top toolbar with three sections:
  - Left: Menu button with dropdown options
  - Center: Currently selected system + tool name
  - Right: WiFi status icon
- **REQ-018:** Menu options shall include:
  - Select ECU → System Selection Screen
  - Check for Updates → Firmware Update Screen
  - System Info → System Information Screen
- **REQ-019:** Main area displays currently selected ECU tool interface

##### 4.3.3 System Selection Screen
- **REQ-020:** Four-step selection process:
  1. Brand (Manufacturer)
  2. System (ABS, Engine, Transmission, etc.)
  3. System name (Bosch ME7.9.7, EDC17, etc.)
  4. Tool (RPM Simulator, Clear DTC, etc.)
- **REQ-021:** Auto-select tool if system has only one available tool
- **REQ-022:** Display tool list if system has multiple tools
- **REQ-023:** Update Main Screen upon system/tool selection

##### 4.3.4 RPM Sensor Configuration Editor
- **REQ-024:** Crankshaft sensor configuration:
  - Degrees per tooth setting
  - Individual tooth on/off sliders
- **REQ-025:** Camshaft sensor configuration:
  - Degrees per tooth setting
  - Individual tooth on/off sliders
- **REQ-026:** Save button to persist configuration
- **REQ-027:** System location selector with Brand/System/System Name hierarchy

#### 4.4 Data Management

##### 4.4.1 System Database
- **REQ-028:** Use JSON format for system and tool information storage
- **REQ-029:** Maintain separate JSON file for user settings and configurations
- **REQ-030:** Store user-modified systems in user settings file
- **REQ-031:** Preserve user settings during firmware updates

##### 4.4.2 User Settings
- **REQ-032:** Store last selected system and tool
- **REQ-033:** Store WiFi configuration
- **REQ-034:** Store user preferences and custom configurations

### 5. Technical Requirements

#### 5.1 Platform & Architecture
- **REQ-035:** Python-based application following PEP 8 standards
- **REQ-036:** Modular architecture with screen-based modules
- **REQ-037:** Each screen in separate module within `screens/` folder
- **REQ-038:** Hardware abstraction layer in `hardware/` directory

#### 5.2 File Structure
- **REQ-039:** Core files (non-modifiable):
  - `boot.py`: Boot process management
  - `main.py`: Application entry point
  - `display.py`: Hardware display configuration
- **REQ-040:** Application files:
  - `main_screen.py`: Main screen and navigation
  - `hardware/io.py`: Hardware I/O abstraction
  - `hardware/can.py`: CAN bus communication

#### 5.3 Data Schema
- **REQ-041:** Systems database structure:
```json
{
  "Brand": "VW",
  "Type": "Engine", 
  "System Name": "Bosch ME7.9.7",
  "Tools": [
    [
      "Rpm",
      {
        "crank": [6, 2],
        "cam": [12, 1,1,1,1,1,1,0,1,1,1,1,1]
      }
    ]
  ]
}
```

### 6. Non-Functional Requirements

#### 6.1 Performance
- **REQ-042:** Boot time shall not exceed 10 seconds
- **REQ-043:** Screen transitions shall complete within 2 seconds
- **REQ-044:** RPM updates shall refresh at minimum 10Hz

#### 6.2 Usability
- **REQ-045:** Touchscreen interface optimized for automotive environment
- **REQ-046:** Clear visual feedback for all user interactions
- **REQ-047:** Intuitive navigation with minimal training required

#### 6.3 Reliability
- **REQ-048:** System shall recover gracefully from WiFi disconnections
- **REQ-049:** User data shall be preserved during unexpected shutdowns
- **REQ-050:** Firmware updates shall not corrupt user settings

### 7. Future Enhancements

#### 7.1 Phase 2 Features
- Complete DTC management (Clear/Read functionality)
- Live data monitoring and logging
- Advanced sensor simulation capabilities
- Multi-language support

#### 7.2 Phase 3 Features
- Cloud-based system database updates
- Remote diagnostic capabilities
- Advanced reporting and analytics
- Integration with workshop management systems

### 8. Success Metrics

- **User Adoption:** 90% of target users successfully complete initial setup
- **Task Completion:** 95% success rate for common diagnostic tasks
- **Performance:** Sub-2 second response time for all UI interactions
- **Reliability:** 99.5% uptime during normal operation

### 9. Dependencies & Constraints

#### 9.1 Technical Dependencies
- MicroPython runtime environment
- WiFi hardware module
- Touchscreen display hardware
- CAN bus interface hardware

#### 9.2 Constraints
- Limited processing power of embedded hardware
- Memory constraints for data storage
- Battery life considerations for portable operation
- Automotive environment durability requirements

### 10. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | | | |
| Engineering Lead | | | |
| UX Designer | | | |
| QA Lead | | | |

---
**Document Control:**
- Created: [Date]
- Last Modified: [Date]
- Next Review: [Date + 3 months]