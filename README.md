# ECU Diagnostic Tool

A comprehensive automotive diagnostic device built on ESP32S3 hardware with MicroPython runtime. This tool provides ECU diagnostic capabilities including RPM simulation, DTC management, and live data monitoring through a touchscreen interface with WiFi connectivity.

## Features

### Core Functionality
- **RPM Signal Generation**: Configurable crankshaft and camshaft sensor simulation
- **ECU Database**: Comprehensive database of vehicle systems from major manufacturers
- **Live Data Monitoring**: Real-time ECU parameter display and logging
- **DTC Management**: Diagnostic Trouble Code reading, clearing, and analysis
- **WiFi Connectivity**: Network configuration and firmware updates
- **Touchscreen Interface**: Intuitive LVGL-based user interface

### Development Features
- **Simulation Mode**: Complete hardware simulation for development without physical device
- **Testing Framework**: Comprehensive test suite with automated validation
- **Modular Architecture**: Clean separation between UI, logic, and hardware layers
- **Error Handling**: Robust error management with user notifications

## Hardware Specifications
- **Microcontroller**: ESP32S3 with SPIRAM
- **Display**: 5-inch LCD touchscreen (800x480)
- **Connectivity**: WiFi 802.11 b/g/n
- **Storage**: Flash memory for firmware and user data
- **I/O**: GPIO pins for sensor signal generation

## Software Specifications
- **Runtime**: MicroPython 1.20+
- **GUI Framework**: LVGL 9.2.1
- **Architecture**: Layered design (UI/Logic/Hardware)
- **Database**: JSON-based system configuration storage
- **Testing**: Integrated simulation and testing environment

## Quick Start

### Simulation Mode (Development)
```bash
# Clone the repository
git clone <repository-url>
cd rpmsim

# Start simulation mode
./sim_app/MpSimulator-x86_64.AppImage src/main_sim.py
```

### Hardware Mode (Production)
```bash
# Flash firmware to ESP32S3
cd firmware/
./flash.sh

# Device automatically boots to src/main.py
```

## Project Structure
```
rpmsim/
├── src/                    # Main application source
│   ├── main.py            # Hardware mode entry point
│   ├── main_sim.py        # Simulation mode entry point
│   ├── screens/           # UI screen modules
│   ├── hardware/          # Hardware abstraction layer
│   │   └── sim/           # Hardware simulation modules
│   ├── utils/             # Utility modules
│   └── db/                # Database and configuration
├── test/                  # Test suite
├── prd/                   # Product documentation
├── firmware/              # ESP32S3 firmware
└── sim_app/               # Simulation environment
```

## Development Workflow

### 1. Simulation Development
```bash
# Start interactive simulation
./sim_app/MpSimulator-x86_64.AppImage src/main_sim.py

# Run comprehensive tests
./sim_app/MpSimulator-x86_64.AppImage test/comprehensive_test.py

# Run visual UI tests
./sim_app/MpSimulator-x86_64.AppImage test/visual_test.py
```

### 2. Hardware Testing
```bash
# Flash to ESP32S3
cd firmware/
./flash.sh

# Monitor serial output
screen /dev/ttyUSB0 115200
```

### 3. Testing
```bash
# Run all tests in simulation
./sim_app/MpSimulator-x86_64.AppImage test/integrated_test.py

# Test specific functionality
./sim_app/MpSimulator-x86_64.AppImage test/simple_test.py
```

## Key Components

### Hardware Abstraction
- **WiFiManager**: Network scanning, connection, and management
- **ECUManager**: ECU communication and data simulation
- **Hardware Simulation**: Complete mock hardware for development

### User Interface
- **MainScreen**: Primary interface with toolbar and navigation
- **SystemSelection**: Four-step vehicle system selection process
- **WiFiSetup**: Network configuration and connection
- **RPMSimulator**: Real-time RPM signal generation and control

### Data Management
- **DataManager**: JSON-based configuration and system database
- **NavigationManager**: Screen transitions and application state
- **ErrorHandler**: Centralized error logging and user notifications

## Documentation

Comprehensive documentation is available in the `prd/` directory:
- **Product Requirements**: Complete feature specifications
- **System Architecture**: Technical design and component structure
- **Implementation Guide**: Development procedures and best practices
- **API Specification**: Interface definitions and protocols

## Testing

The project includes extensive testing capabilities:
- **Unit Tests**: Individual component validation
- **Integration Tests**: End-to-end workflow testing
- **Visual Tests**: Interactive UI demonstration
- **Hardware Simulation**: Complete development environment without physical hardware

## Contributing

1. Use simulation mode for development and testing
2. Follow the modular architecture patterns
3. Add tests for new functionality
4. Update documentation for significant changes
5. Test in both simulation and hardware modes before deployment

## License

[License information to be added]






