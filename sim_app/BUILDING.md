# Building the RPM Simulator AppImage

This document provides detailed instructions for building the RPM Simulator AppImage.

## Overview

The AppImage contains:
- **MicroPython v1.23.0** - Latest stable version with ESP32 support
- **LVGL 9.2.1** - Exact version matching the real ESP32S3 device
- **SDL2** - For graphics and input simulation
- **All dependencies** - Bundled for portability

## Prerequisites

### System Requirements
- Linux x86_64 system
- At least 2GB free disk space
- Internet connection for downloading sources

### Build Dependencies
The build system will automatically detect your Linux distribution and install the required packages.

#### Ubuntu/Debian
```bash
sudo apt-get install build-essential cmake git python3 libsdl2-dev pkg-config
```

#### Fedora/RHEL
```bash
sudo dnf install gcc gcc-c++ make cmake git python3 SDL2-devel pkgconfig
```

#### Arch Linux
```bash
sudo pacman -S base-devel cmake git python3 sdl2 pkg-config
```

## Quick Start

1. **Setup dependencies** (requires sudo):
   ```bash
   cd sim_app
   make setup
   ```

2. **Build the AppImage**:
   ```bash
   make all
   ```

3. **Test the result**:
   ```bash
   make test
   ```

The final AppImage will be created as `RPMSimulator-x86_64.AppImage`.

## Manual Build Process

If you prefer to run the build steps manually:

### 1. Install Dependencies
```bash
./scripts/setup_dependencies.sh
```

### 2. Build MicroPython with LVGL
```bash
./scripts/build_micropython.sh
```

### 3. Package the AppImage
```bash
./scripts/package_appimage.sh
```

## Build Scripts

### `setup_dependencies.sh`
- Detects your Linux distribution
- Installs all required build dependencies
- Verifies the installation

### `build_micropython.sh`
- Downloads MicroPython v1.23.0 source
- Downloads LVGL MicroPython bindings
- Configures LVGL for SDL simulation
- Builds MicroPython with LVGL support
- Tests the build

### `package_appimage.sh`
- Copies required libraries
- Creates AppRun script
- Creates desktop integration files
- Downloads AppImageTool
- Packages the final AppImage

### `build_appimage.sh`
- Main build script that runs all steps
- Comprehensive logging and error handling
- Automatic cleanup and verification

## Configuration

### LVGL Configuration
The build uses a custom LVGL configuration optimized for simulation:
- 16-bit color depth (RGB565)
- SDL driver enabled
- 64KB memory allocation
- Optimized for desktop performance

### MicroPython Configuration
- Unix port with SDL support
- LVGL module enabled
- ESP32-compatible modules included
- Task handler support

## Troubleshooting

### Common Issues

1. **Missing SDL2 development libraries**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libsdl2-dev
   
   # Fedora
   sudo dnf install SDL2-devel
   ```

2. **Build fails with "No module named 'lvgl'"**
   - This is expected during build
   - The module is built as part of the process

3. **AppImage doesn't run**
   - Check if you have X11 or Wayland display
   - Try: `SDL_VIDEODRIVER=x11 ./RPMSimulator-x86_64.AppImage`

4. **Permission denied**
   - Make sure the AppImage is executable: `chmod +x RPMSimulator-x86_64.AppImage`

### Build Logs
All build scripts provide detailed logging with color-coded output:
- 🔵 **INFO**: General information
- 🟢 **SUCCESS**: Successful operations
- 🟡 **WARNING**: Non-critical issues
- 🔴 **ERROR**: Critical failures

### Clean Build
To start fresh:
```bash
make clean
make all
```

## Testing

### Basic Test
```bash
./RPMSimulator-x86_64.AppImage -c "import lvgl as lv; print('LVGL version:', lv.version_info())"
```

### Interactive Mode
```bash
./RPMSimulator-x86_64.AppImage
```

### Run Your Code
```bash
./RPMSimulator-x86_64.AppImage /path/to/your/main.py
```

## Distribution

The resulting AppImage is completely portable and can be:
- Copied to any Linux x86_64 system
- Run without installation
- Distributed as a single file
- Integrated with desktop environments

## Version Information

- **MicroPython**: v1.23.0
- **LVGL**: 9.2.1 (matches ESP32S3 device)
- **SDL**: 2.30.0+
- **Target**: Linux x86_64

## Support

For build issues:
1. Check the build logs for specific error messages
2. Verify all dependencies are installed
3. Try a clean build
4. Check the troubleshooting section above
