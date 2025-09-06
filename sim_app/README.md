# RPM Simulator - AppImage Build Environment

This directory contains the build system for creating an AppImage of the RPM Simulator.

## Overview

The AppImage provides a portable simulation environment that wraps MicroPython compiled with LVGL 9.2.1 bindings and SDL support. This allows running the same code as the real ESP32S3 device in a desktop simulation environment.

## Directory Structure

```
sim_app/
├── README.md                 # This file
├── AppDir/                   # AppImage directory structure
│   ├── usr/                  # Application files
│   │   ├── bin/              # MicroPython executable with LVGL+SDL
│   │   ├── lib/              # Required libraries (SDL2, etc.)
│   │   └── share/            # Shared resources and assets
│   ├── AppRun                # AppImage entry point script
│   └── rpmsim.desktop        # Desktop file for integration
├── build/                    # Build artifacts and temporary files
├── scripts/                  # Build scripts
│   ├── build_appimage.sh     # Main AppImage build script
│   ├── build_micropython.sh  # MicroPython compilation with LVGL
│   ├── setup_dependencies.sh # System dependencies setup
│   └── package_appimage.sh   # Final AppImage packaging
└── requirements.txt          # Build dependencies
```

## Features

- **MicroPython Runtime**: Custom MicroPython build with LVGL 9.2.1 bindings
- **SDL Graphics**: Hardware-accelerated graphics via SDL2
- **Exact Compatibility**: Same LVGL version (9.2.1) as the real ESP32S3 device
- **Portable**: Single AppImage file that runs on any Linux system
- **No Dependencies**: All required libraries bundled in the AppImage

## Building

Run the build script to create the AppImage:

```bash
./scripts/build_appimage.sh
```

This will:
1. Download and compile MicroPython with LVGL bindings
2. Build SDL2 support for graphics
3. Package everything into a portable AppImage

## Running

After building, run the simulator:

```bash
./RPMSimulator-x86_64.AppImage /path/to/your/micropython/code.py
```

Or simply double-click the AppImage file in your file manager.

## Build Requirements

- Linux x86_64 system
- Build tools: gcc, make, cmake, git
- SDL2 development libraries
- Python 3.8+ (for build scripts only)

## Runtime Components

- **MicroPython**: Custom build with ESP32 modules
- **LVGL**: 9.2.1 with SDL driver
- **SDL2**: Graphics and input handling
- **Bundled Libraries**: All dependencies included
