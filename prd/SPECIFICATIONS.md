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
- **Full Screen Layout**:
  - **Left Side**: Scrollable list displaying brands or systems
  - **Right Side**: Virtual keyboard with search functionality
    - Search text input line at top
    - Clear filter button next to search line
    - Virtual keyboard below
    - Close button at bottom to exit without selection

- **Search Functionality**:
  - **Without Search Filter**:
    - List displays available vehicle brands sorted alphabetically
    - When a brand is clicked, all systems of that brand are displayed sorted by:
      1. System type
      2. System name
    - List items show: `[System Type] System Name`

  - **With Search Filter**:
    - List displays systems matching the filter from all brands sorted by:
      1. Brand name
      2. System type
      3. System name
    - List items show:
      - Line 1: `[System Type] Brand Name`
      - Line 2: `System Name`

- **Selection Behavior**:
  - Selecting a system updates the Main Screen to show the selected system tool
  - If the selected system has multiple tools, a list of tools is displayed for selection
  - If the selected system has only one tool, it is selected automatically
  - Cancel button preserves current selection without changes


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

## Testing Requirements

### UI Testing Standards
- All UI screens must have comprehensive test coverage
- Tests should focus on user interactions (click, slide, touch, navigation)
- Each UI component must be tested for proper functionality
- Navigation flows between screens must be validated
- Error handling and edge cases must be tested

### Test Coverage Requirements
- **100% UI Feature Coverage**: Every button, slider, input field, and interactive element must be tested
- **Navigation Testing**: All screen transitions and menu interactions must be validated
- **User Interaction Testing**: Click events, slider movements, toggle states, and form inputs
- **Error Scenario Testing**: Invalid inputs, network failures, and system errors
- **Performance Testing**: Screen load times, responsiveness, and memory usage

### Testing Methodology
- **Automated UI Tests**: Use LVGL simulation for automated testing
- **User Flow Testing**: Test complete user journeys (e.g., menu → system selection → tool usage)
- **Component Testing**: Individual UI component functionality
- **Integration Testing**: Screen-to-screen navigation and data flow
- **Regression Testing**: Ensure new changes don't break existing functionality

### Test Structure
- All UI tests located in `./test/ui/` directory
- Each screen has dedicated test file (e.g., `test_main_screen.py`)
- Common testing utilities in `./test/ui/utils/`
- Test runner for executing complete test suite
- Test reports with coverage metrics

### Test Examples
- **Menu Interaction**: Click menu → verify menu visible → click menu item → verify navigation
- **Slider Testing**: Move RPM slider → verify value updates → verify simulation responds
- **Form Testing**: Enter WiFi password → verify input accepted → test connection flow
- **Toggle Testing**: Click cam/crank toggles → verify state changes → verify visual feedback

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