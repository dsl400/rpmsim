## boot process

- After power on, 
  - it the device has not been configured yet, it should enter wifi setup mode
  - the device should display the last selected system tool


## Ecu Tools
- Rpm Simulator
  - Currently selected RPM value
  - RPM increment/decrement buttons
  - RPM slider
  - Toggle button to disable/enable sensor output for cam and crank
  - Button that opens the RPM Sensor configuration editor
- Clear DTC <!-- TODO -->
- Read DTC <!-- TODO -->
- Read Live Data <!-- TODO -->

## Graphical User Interface (GUI)

### Wifi Setup Mode
- Select wifi network
- After connection to wifi,(display spinner) check for firmware updates
- If update is available prompt if the user wants to update
  - If yes, display Firmware Update Screen

### Main Screen
- Top Toolbar
  - Let Side
    - Menu Button
      - Menu Options
        - Select ECU > Display System Selection Screen
      - Check for Updates > Display Firmware Update Screen
      - System Info > Display System Information Screen
  - Center
    - Currently selected sitem + tool name
  - Right Side
    - Wifi Status Icon
- Main Area
  - Currently selected ECU tool


### System Selection Screen
- 4 steps to select an ECU
  - Brand (Manufacturer)
  - System (ABS, Engine, Transmission, etc.)
  - System name (Bosch ME7.9.7, EDC17, etc.)
  - Tool (Rpm Simulator, Clear DTC, etc.)
- Selecting a system updates the Main Screen to show the selected system tool
  - If the selected system has multiple tools, a list of tools is displayed for selection
  - If the selected system has only one tool, it is selected automatically


## RPM Sensor Configuration Editor
- Crankshaft Sensor Configuration
  - Number of degrees per tooth
  - Teeth configuration
    - A slider to set teeth on or off for every section
- Canshaft Sensor Configuration
  - Number of degrees per tooth
  - Teeth configuration
    - A slider to set teeth on or off for every section
- Save button to save the configuration
  - System Location Selector
    - Brand (Manufacturer)
    - System (ABS, Engine, Transmission, etc.)
    - System name (Bosch ME7.9.7, EDC17, etc )

## Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Write modular and reusable code
- Comment code where necessary to explain complex logic
- Every screen sould be in its own module inside a folder named `screens`
  - Each screen module should contain submodules for different components of the screen
- Respect existing file structure and naming conventions

## Database
- Use JSON files to store system and tool information
- Use a separate JSON file to store user settings and configurations
- User modified or added systems should be stored in the user settings file
- User setting should not be overwritten during firmware updates
- User settings should include:
  - Last selected system and tool
  - Wifi configuration
  - Any other user preferences

### Database schema
- systems.json
```json
  {
    [
      "Brand": "VW",
      "Type": "Engine",
      "System Name": "Bosch ME7.9.7",
      "Tools": [
        [
          "Rpm",
          {
            "crank": [6, 2],
	          "cam":   [12, 1,1,1,1,1,1,0,1,1,1,1,1]
          }
        ]
      ]
    ]
  }

```

### Code Structure
- boot.py: Manages the boot process and initial (should not be modified)
- main.py: Entry point of the application (should not be modified)
  - display.py: Handles hardware configuration for display and touchscreen (should not be modified)
  - main_screen.py: Manages the main screen and navigation 
- hardware/
  - io.py: provides abstraction for hardware input/output operations
  - can.py: handles CAN bus communication (if applicable)