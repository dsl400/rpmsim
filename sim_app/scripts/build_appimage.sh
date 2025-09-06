#!/bin/bash
set -e

# RPM Simulator AppImage Build Script
# Builds a portable AppImage containing MicroPython with LVGL 9.2.1 and SDL support

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build"
APPDIR="$PROJECT_DIR/AppDir"

# Version configuration
MICROPYTHON_VERSION="v1.25.0"
LVGL_VERSION="9.2.1"
SDL_VERSION="2.30.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking build dependencies..."
    
    local missing_deps=()
    
    # Check for required tools
    for tool in gcc make cmake git python3 pkg-config; do
        if ! command -v "$tool" &> /dev/null; then
            missing_deps+=("$tool")
        fi
    done
    
    # Check for SDL2 development libraries
    if ! pkg-config --exists sdl2; then
        missing_deps+=("libsdl2-dev")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Install them with:"
        log_info "  Ubuntu/Debian: sudo apt-get install build-essential cmake git python3 libsdl2-dev pkg-config"
        log_info "  Fedora: sudo dnf install gcc make cmake git python3 SDL2-devel pkgconfig"
        log_info "  Arch: sudo pacman -S base-devel cmake git python3 sdl2 pkg-config"
        exit 1
    fi
    
    log_success "All dependencies found"
}

setup_build_environment() {
    log_info "Setting up build environment..."
    
    # Create build directories
    mkdir -p "$BUILD_DIR"
    mkdir -p "$APPDIR/usr/bin"
    mkdir -p "$APPDIR/usr/lib"
    mkdir -p "$APPDIR/usr/share"
    
    # Clean previous builds
    rm -rf "$BUILD_DIR"/*
    
    log_success "Build environment ready"
}

download_sources() {
    log_info "Downloading source code..."
    
    cd "$BUILD_DIR"
    
    # Download MicroPython
    if [ ! -d "micropython" ]; then
        log_info "Downloading MicroPython $MICROPYTHON_VERSION..."
        git clone --depth 1 --branch "$MICROPYTHON_VERSION" https://github.com/micropython/micropython.git
    fi
    
    # Download LVGL MicroPython bindings
    if [ ! -d "lv_micropython" ]; then
        log_info "Downloading LVGL MicroPython bindings..."
        git clone --recursive https://github.com/lvgl/lv_micropython.git
        cd lv_micropython
        # Checkout specific LVGL version
        cd lib/lvgl
        git checkout "v$LVGL_VERSION"
        cd ../..
    fi
    
    log_success "Source code downloaded"
}

build_micropython_with_lvgl() {
    log_info "Building MicroPython with LVGL bindings..."

    cd "$BUILD_DIR/lv_micropython"

    # Initialize submodules
    git submodule update --init --recursive

    # Build the unix port with SDL
    cd ports/unix

    # Configure build with SDL support
    export SDL_CFLAGS="$(pkg-config --cflags sdl2)"
    export SDL_LDFLAGS="$(pkg-config --libs sdl2)"
    export CFLAGS_EXTRA="-DLV_CONF_INCLUDE_SIMPLE=1 -I../../lib/lvgl $SDL_CFLAGS"
    export LDFLAGS_EXTRA="$SDL_LDFLAGS"

    # Build MicroPython
    make clean
    make -j$(nproc) \
        USER_C_MODULES=../../lib/lvgl/bindings/micropython/micropython.cmake \
        CFLAGS_EXTRA="$CFLAGS_EXTRA" \
        LDFLAGS_EXTRA="$LDFLAGS_EXTRA"

    # Copy the executable to AppDir
    cp micropython "$APPDIR/usr/bin/micropython-lvgl"

    log_success "MicroPython with LVGL built successfully"
}

copy_libraries() {
    log_info "Copying required libraries..."
    
    # Get list of required shared libraries
    local libs=$(ldd "$APPDIR/usr/bin/micropython-lvgl" | grep "=> /" | awk '{print $3}' | grep -v "^/lib64\|^/usr/lib64\|^/lib/x86_64\|^/usr/lib/x86_64")
    
    # Copy SDL2 and other required libraries
    for lib in $libs; do
        if [[ "$lib" == *"libSDL2"* ]] || [[ "$lib" == *"libGL"* ]] || [[ "$lib" == *"libX11"* ]]; then
            cp "$lib" "$APPDIR/usr/lib/"
            log_info "Copied library: $(basename "$lib")"
        fi
    done
    
    log_success "Libraries copied"
}

create_apprun_script() {
    log_info "Creating AppRun script..."
    
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash

# AppRun script for RPM Simulator
# This script sets up the environment and runs MicroPython with LVGL

APPDIR="$(dirname "$(readlink -f "$0")")"

# Set library path
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

# Set Python path for MicroPython modules
export MICROPYPATH="$APPDIR/usr/share:$MICROPYPATH"

# Run MicroPython with LVGL
if [ $# -eq 0 ]; then
    # No arguments - run interactive mode or default script
    if [ -f "$APPDIR/usr/share/main.py" ]; then
        exec "$APPDIR/usr/bin/micropython-lvgl" "$APPDIR/usr/share/main.py"
    else
        exec "$APPDIR/usr/bin/micropython-lvgl"
    fi
else
    # Run with provided arguments
    exec "$APPDIR/usr/bin/micropython-lvgl" "$@"
fi
EOF

    chmod +x "$APPDIR/AppRun"
    
    log_success "AppRun script created"
}

create_desktop_file() {
    log_info "Creating desktop file..."
    
    cat > "$APPDIR/rpmsim.desktop" << EOF
[Desktop Entry]
Type=Application
Name=RPM Simulator
Comment=ESP32S3 RPM Signal Generator Simulator
Exec=AppRun
Icon=rpmsim
Categories=Development;Engineering;
Terminal=false
StartupNotify=true
EOF

    log_success "Desktop file created"
}

create_icon() {
    log_info "Creating application icon..."
    
    # Create a simple SVG icon
    cat > "$APPDIR/rpmsim.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="30" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="32" y="38" text-anchor="middle" fill="white" font-family="Arial" font-size="12" font-weight="bold">RPM</text>
  <circle cx="32" cy="20" r="3" fill="white"/>
  <line x1="32" y1="20" x2="32" y2="32" stroke="white" stroke-width="2"/>
  <line x1="32" y1="32" x2="42" y2="32" stroke="white" stroke-width="2"/>
</svg>
EOF

    # Convert to PNG if possible
    if command -v convert &> /dev/null; then
        convert "$APPDIR/rpmsim.svg" "$APPDIR/rpmsim.png"
    fi
    
    log_success "Application icon created"
}

package_appimage() {
    log_info "Packaging AppImage..."
    
    cd "$PROJECT_DIR"
    
    # Download appimagetool if not present
    if [ ! -f "appimagetool-x86_64.AppImage" ]; then
        log_info "Downloading appimagetool..."
        wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
        chmod +x appimagetool-x86_64.AppImage
    fi
    
    # Create the AppImage
    ./appimagetool-x86_64.AppImage "$APPDIR" "RPMSimulator-x86_64.AppImage"
    
    log_success "AppImage created: RPMSimulator-x86_64.AppImage"
}

main() {
    log_info "Starting RPM Simulator AppImage build..."
    log_info "Target versions: MicroPython $MICROPYTHON_VERSION, LVGL $LVGL_VERSION"
    
    check_dependencies
    setup_build_environment
    download_sources
    build_micropython_with_lvgl
    copy_libraries
    create_apprun_script
    create_desktop_file
    create_icon
    package_appimage
    
    log_success "Build completed successfully!"
    log_info "AppImage location: $PROJECT_DIR/RPMSimulator-x86_64.AppImage"
    log_info "To run: ./RPMSimulator-x86_64.AppImage [script.py]"
}

# Run main function
main "$@"
