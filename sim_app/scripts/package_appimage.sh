#!/bin/bash
set -e

# AppImage Packaging Script
# Creates the final AppImage from the prepared AppDir

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
APPDIR="$PROJECT_DIR/AppDir"

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

check_appdir() {
    log_info "Checking AppDir structure..."

    if [ ! -d "$APPDIR" ]; then
        log_error "AppDir not found: $APPDIR"
        exit 1
    fi

    if [ ! -f "$APPDIR/usr/bin/micropython-lvgl" ]; then
        log_error "MicroPython executable not found in AppDir"
        exit 1
    fi

    log_success "AppDir structure is valid"
}

copy_libraries() {
    log_info "Copying required libraries..."
    
    local executable="$APPDIR/usr/bin/micropython-lvgl"
    local lib_dir="$APPDIR/usr/lib"
    
    mkdir -p "$lib_dir"
    
    # Get list of required shared libraries
    local libs=$(ldd "$executable" 2>/dev/null | grep "=> /" | awk '{print $3}' | sort | uniq)
    
    # Copy libraries that are not part of the base system
    for lib in $libs; do
        local lib_name=$(basename "$lib")
        
        # Skip system libraries that should be available on all systems
        if [[ "$lib" == /lib64/* ]] || [[ "$lib" == /usr/lib64/* ]] || \
           [[ "$lib" == /lib/x86_64-linux-gnu/* ]] || [[ "$lib" == /usr/lib/x86_64-linux-gnu/* ]]; then
            continue
        fi
        
        # Copy specific libraries we need
        if [[ "$lib_name" == libSDL2* ]] || \
           [[ "$lib_name" == libGL* ]] || \
           [[ "$lib_name" == libX11* ]] || \
           [[ "$lib_name" == libXext* ]] || \
           [[ "$lib_name" == libXrandr* ]] || \
           [[ "$lib_name" == libXinerama* ]] || \
           [[ "$lib_name" == libXcursor* ]] || \
           [[ "$lib_name" == libXi* ]]; then
            
            if [ ! -f "$lib_dir/$lib_name" ]; then
                cp "$lib" "$lib_dir/"
                log_info "Copied library: $lib_name"
            fi
        fi
    done
    
    log_success "Libraries copied"
}

create_apprun() {
    log_info "Creating AppRun script..."
    
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash

# AppRun script for RPM Simulator
# Sets up environment and runs MicroPython with LVGL

APPDIR="$(dirname "$(readlink -f "$0")")"

# Set library path
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$LD_LIBRARY_PATH"

# Set Python path for MicroPython modules
export MICROPYPATH="$APPDIR/usr/share:$MICROPYPATH"

# Set SDL video driver (prefer X11)
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"

# Disable SDL audio if not needed (reduces dependencies)
export SDL_AUDIODRIVER=dummy

# Set OpenGL vendor library for better compatibility
export __GLX_VENDOR_LIBRARY_NAME=mesa

# Run MicroPython with LVGL
if [ $# -eq 0 ]; then
    # No arguments - check for default script
    if [ -f "$APPDIR/usr/share/main.py" ]; then
        exec "$APPDIR/usr/bin/micropython-lvgl" "$APPDIR/usr/share/main.py"
    else
        # Run interactive mode
        echo "RPM Simulator - MicroPython with LVGL"
        echo "Usage: $0 [script.py]"
        echo "Starting interactive mode..."
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
Categories=Development;Engineering;Electronics;
Terminal=false
StartupNotify=true
MimeType=text/x-python;
Keywords=RPM;Simulator;ESP32;MicroPython;LVGL;Automotive;
EOF

    log_success "Desktop file created"
}

create_icon() {
    log_info "Creating application icon..."
    
    # Create SVG icon
    cat > "$APPDIR/rpmsim.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="128" height="128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <!-- Background circle -->
  <circle cx="64" cy="64" r="60" fill="#2196F3" stroke="#1976D2" stroke-width="4"/>
  
  <!-- RPM text -->
  <text x="64" y="45" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="16" font-weight="bold">RPM</text>
  
  <!-- Gauge -->
  <circle cx="64" cy="64" r="35" fill="none" stroke="white" stroke-width="3"/>
  
  <!-- Gauge marks -->
  <line x1="64" y1="29" x2="64" y2="35" stroke="white" stroke-width="2"/>
  <line x1="99" y1="64" x2="93" y2="64" stroke="white" stroke-width="2"/>
  <line x1="64" y1="99" x2="64" y2="93" stroke="white" stroke-width="2"/>
  <line x1="29" y1="64" x2="35" y2="64" stroke="white" stroke-width="2"/>
  
  <!-- Needle -->
  <line x1="64" y1="64" x2="85" y2="50" stroke="#FF5722" stroke-width="3" stroke-linecap="round"/>
  <circle cx="64" cy="64" r="4" fill="#FF5722"/>
  
  <!-- ESP32 text -->
  <text x="64" y="85" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="10">ESP32S3</text>
</svg>
EOF

    # Convert to PNG if ImageMagick is available
    if command -v convert &> /dev/null; then
        convert "$APPDIR/rpmsim.svg" -resize 128x128 "$APPDIR/rpmsim.png"
        log_info "Icon converted to PNG"
    else
        log_warning "ImageMagick not found, using SVG icon only"
    fi
    
    log_success "Application icon created"
}

download_appimagetool() {
    log_info "Downloading AppImageTool..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -f "appimagetool-x86_64.AppImage" ]; then
        wget -q --show-progress https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
        chmod +x appimagetool-x86_64.AppImage
        log_success "AppImageTool downloaded"
    else
        log_info "AppImageTool already present"
    fi
}

create_appimage() {
    log_info "Creating AppImage..."
    
    cd "$PROJECT_DIR"
    
    # Remove old AppImage if it exists
    rm -f "RPMSimulator-x86_64.AppImage"
    
    # Create the AppImage
    ARCH=x86_64 ./appimagetool-x86_64.AppImage "$APPDIR" "RPMSimulator-x86_64.AppImage"
    
    if [ -f "RPMSimulator-x86_64.AppImage" ]; then
        chmod +x "RPMSimulator-x86_64.AppImage"
        log_success "AppImage created successfully: RPMSimulator-x86_64.AppImage"
        
        # Show file size
        local size=$(du -h "RPMSimulator-x86_64.AppImage" | cut -f1)
        log_info "AppImage size: $size"
    else
        log_error "Failed to create AppImage"
        exit 1
    fi
}

test_appimage() {
    log_info "Testing AppImage..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -f "RPMSimulator-x86_64.AppImage" ]; then
        log_error "AppImage not found for testing"
        exit 1
    fi
    
    # Test basic execution
    timeout 10s ./RPMSimulator-x86_64.AppImage -c "print('AppImage test successful')" || {
        log_warning "AppImage test timed out or failed (this might be expected without display)"
    }
    
    log_success "AppImage testing completed"
}

main() {
    log_info "Packaging RPM Simulator AppImage..."

    check_appdir
    create_apprun
    create_desktop_file
    create_icon
    copy_libraries
    download_appimagetool
    create_appimage
    test_appimage

    log_success "AppImage packaging completed!"
    log_info "Final AppImage: $PROJECT_DIR/RPMSimulator-x86_64.AppImage"
    log_info ""
    log_info "To run the simulator:"
    log_info "  ./RPMSimulator-x86_64.AppImage [script.py]"
    log_info ""
    log_info "To make it executable from anywhere:"
    log_info "  sudo cp RPMSimulator-x86_64.AppImage /usr/local/bin/rpmsim"
}

# Run main function
main "$@"
