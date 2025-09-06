# ECU Diagnostic Tool - UI Testing Framework

This directory contains comprehensive UI tests for the ECU Diagnostic Tool, focusing on user interaction testing with LVGL simulation.

## Overview

The UI testing framework provides automated testing for all user interface components and interactions, ensuring:
- **100% UI Feature Coverage**: Every button, slider, input field, and interactive element
- **User Interaction Testing**: Click events, slider movements, toggle states, form inputs
- **Navigation Flow Testing**: Screen transitions and menu interactions
- **Error Scenario Testing**: Invalid inputs, network failures, system errors
- **Performance Testing**: Screen load times and responsiveness

## Test Structure

```
./test/ui/
├── utils/
│   ├── base_ui_test.py      # Base testing framework
│   ├── test_helpers.py      # Helper functions and utilities
│   └── __init__.py
├── test_main_screen.py      # Main screen UI tests
├── test_rpm_simulator_screen.py  # RPM simulator tests
├── test_system_selection_screen.py  # System selection tests
├── test_wifi_setup_screen.py      # WiFi setup tests
├── test_additional_screens.py     # Other screens tests
├── run_all_ui_tests.py      # Comprehensive test runner
└── README.md               # This file
```

## Running Tests

### Run All Tests
```bash
cd /path/to/rpmsim
python3 test/ui/run_all_ui_tests.py
```

### Run Individual Test Suites
```bash
# Main screen tests
python3 test/ui/test_main_screen.py

# RPM simulator tests
python3 test/ui/test_rpm_simulator_screen.py

# System selection tests
python3 test/ui/test_system_selection_screen.py

# WiFi setup tests
python3 test/ui/test_wifi_setup_screen.py

# Additional screens tests
python3 test/ui/test_additional_screens.py
```

## Test Categories

### 1. Main Screen Tests (`test_main_screen.py`)
- **Toolbar Elements**: Menu button, title button, WiFi icon visibility
- **Menu Interaction**: Menu opening/closing, menu item clicks
- **Title Button**: System selection navigation
- **WiFi Status**: Status display and interaction
- **Tool Loading**: Current tool display in main area
- **Navigation Flow**: Complete menu → action → back workflows

### 2. RPM Simulator Tests (`test_rpm_simulator_screen.py`)
- **RPM Display**: Value display and updates
- **Slider Interaction**: RPM value changes via slider
- **Control Buttons**: Start/stop, cam/crank toggles
- **Config Button**: Sensor configuration access
- **Visual States**: Button color/icon changes
- **Complete Workflow**: Full RPM simulation process

### 3. System Selection Tests (`test_system_selection_screen.py`)
- **4-Step Process**: Brand → System → System Name → Tool
- **Navigation**: Back/cancel button functionality
- **Breadcrumb**: Step indicator updates
- **Selection Flow**: Complete selection process
- **Error Handling**: Invalid selections

### 4. WiFi Setup Tests (`test_wifi_setup_screen.py`)
- **Network Scanning**: Scan button and network discovery
- **Network Selection**: Network list interaction
- **Password Entry**: Input field testing
- **Connection Process**: Connection workflow
- **Error Scenarios**: Connection failures, timeouts

### 5. Additional Screens Tests (`test_additional_screens.py`)
- **Firmware Update**: Update checking and installation
- **System Info**: Information display
- **DTC Screens**: Clear/Read DTC functionality
- **Live Data**: Real-time data monitoring
- **Sensor Config**: RPM sensor configuration

## Test Framework Features

### Base UI Test Class (`base_ui_test.py`)
- **LVGL Simulation**: Automated display and input setup
- **Widget Interaction**: Click, slider, text input simulation
- **Verification Methods**: Visibility, text, state checking
- **Result Logging**: Comprehensive test result tracking
- **Error Handling**: Graceful failure management

### Test Helpers (`test_helpers.py`)
- **Widget Finding**: Search by text, type, properties
- **Navigation Flows**: Multi-step interaction simulation
- **Performance Measurement**: Timing and responsiveness
- **Mock Data**: Test environment setup
- **Screen Verification**: Element existence checking

## Test Execution Flow

1. **Setup**: Initialize LVGL display and input simulation
2. **Environment**: Create mock app state and data managers
3. **Screen Creation**: Instantiate screen under test
4. **Interaction Testing**: Simulate user interactions
5. **Verification**: Check expected outcomes
6. **Cleanup**: Release resources and reset state

## Example Test Pattern

```python
def test_button_interaction(self):
    """Test button click functionality"""
    try:
        # Find button
        button = self.screen_instance.widgets.get('test_button')
        if not self.verify_widget_visible(button, "test button"):
            return False
        
        # Simulate click
        if not self.simulate_click(button):
            return False
        
        # Verify result
        if self.verify_expected_outcome():
            self.log_pass("Button interaction successful")
            return True
        else:
            self.log_fail("Button interaction failed")
            return False
            
    except Exception as e:
        self.log_error(f"Button test failed: {e}")
        return False
```

## Coverage Reporting

The test runner provides comprehensive coverage analysis:
- **Feature Coverage**: Percentage of UI features tested
- **Success Rates**: Per-module and overall success metrics
- **Performance Metrics**: Test execution times
- **Recommendations**: Improvement suggestions
- **Detailed Reports**: JSON output for CI/CD integration

## Integration with CI/CD

Tests can be integrated into continuous integration:
```bash
# In CI pipeline
python3 test/ui/run_all_ui_tests.py
if [ $? -eq 0 ]; then
    echo "UI tests passed"
else
    echo "UI tests failed"
    exit 1
fi
```

## Requirements

- **Python 3.x** with MicroPython compatibility
- **LVGL** with SDL simulation support
- **SDL2** development libraries
- **Source code** in `./src/` directory

## Best Practices

1. **Test Independence**: Each test should be self-contained
2. **Cleanup**: Always clean up resources after tests
3. **Error Handling**: Graceful failure with informative messages
4. **Performance**: Keep tests fast and efficient
5. **Maintainability**: Clear test names and documentation
6. **Coverage**: Aim for 100% UI feature coverage

## Troubleshooting

### Common Issues

1. **Display Initialization Failed**
   - Ensure SDL2 libraries are installed
   - Check LVGL configuration

2. **Import Errors**
   - Verify `src/` directory is in Python path
   - Check module dependencies

3. **Widget Not Found**
   - Verify screen initialization completed
   - Check widget naming consistency

4. **Test Timeouts**
   - Increase wait times for slow operations
   - Check for infinite loops in UI code

### Debug Mode

Enable verbose logging by setting debug flags in test files:
```python
# In test file
self.debug_mode = True  # Enable detailed logging
```

## Contributing

When adding new UI features:
1. Create corresponding test file
2. Follow existing test patterns
3. Update this README
4. Ensure 100% test coverage for new features
5. Run full test suite before committing

## Future Enhancements

- **Visual Regression Testing**: Screenshot comparison
- **Accessibility Testing**: Screen reader compatibility
- **Performance Benchmarking**: Response time metrics
- **Stress Testing**: Memory usage under load
- **Cross-Platform Testing**: Different display sizes
