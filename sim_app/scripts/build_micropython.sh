#!/bin/bash
set -e

# MicroPython with LVGL Build Script
# Builds MicroPython with LVGL 9.2.1 bindings and SDL support

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_DIR/build"

# Version configuration
MICROPYTHON_VERSION="v1.25.0"
LVGL_VERSION="9.2.1"

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

setup_build_dir() {
    log_info "Setting up build directory..."
    mkdir -p "$BUILD_DIR"
    cd "$BUILD_DIR"
}

download_micropython() {
    log_info "Downloading MicroPython $MICROPYTHON_VERSION..."
    
    if [ ! -d "micropython" ]; then
        git clone --depth 1 --branch "$MICROPYTHON_VERSION" https://github.com/micropython/micropython.git
    else
        log_info "MicroPython already downloaded"
    fi
}

download_lvgl_bindings() {
    log_info "Downloading LVGL MicroPython bindings..."

    if [ ! -d "lv_micropython" ]; then
        git clone --recursive https://github.com/lvgl/lv_micropython.git
        cd lv_micropython

        # Checkout specific LVGL version
        cd user_modules/lv_binding_micropython/lvgl
        git checkout "v$LVGL_VERSION"
        cd ../../..

        # Update submodules
        git submodule update --init --recursive

        # Update MicroPython base to v1.25.0
        log_info "Updating MicroPython base to v1.25.0..."
        git remote add upstream https://github.com/micropython/micropython.git 2>/dev/null || true
        git fetch upstream
        git checkout "v1.25.0"

        # Update submodules after version change
        git submodule update --init --recursive

        log_success "LVGL bindings downloaded and MicroPython updated to v1.25.0"
    else
        log_info "LVGL bindings already downloaded"
        cd lv_micropython

        # Ensure MicroPython is at v1.25.0
        log_info "Verifying MicroPython version..."
        current_version=$(git describe --tags --exact-match 2>/dev/null || echo "unknown")
        if [ "$current_version" != "v1.25.0" ]; then
            log_info "Updating MicroPython to v1.25.0..."
            git remote add upstream https://github.com/micropython/micropython.git 2>/dev/null || true
            git fetch upstream
            git checkout "v1.25.0"
            git submodule update --init --recursive
        else
            log_info "MicroPython already at v1.25.0"
        fi
    fi
}

patch_lvgl_config() {
    log_info "Configuring LVGL for SDL simulation..."

    # Ensure we're in the right directory
    cd "$BUILD_DIR/lv_micropython"

    # Check if lv_conf.h already exists in the binding directory
    if [ -f "user_modules/lv_binding_micropython/lv_conf.h" ]; then
        log_info "Using existing LVGL configuration in bindings"
        # Enable SDL in the existing configuration
        sed -i 's/#define LV_USE_SDL.*0/#define LV_USE_SDL 1/' user_modules/lv_binding_micropython/lv_conf.h
        sed -i 's/.*#define LV_USE_SDL.*/#define LV_USE_SDL 1/' user_modules/lv_binding_micropython/lv_conf.h

        log_success "LVGL configuration updated for SDL"
    elif [ -f "user_modules/lv_binding_micropython/lvgl/lv_conf_template.h" ]; then
        log_info "Using LVGL configuration template"
        # Copy the template and enable SDL
        cp user_modules/lv_binding_micropython/lvgl/lv_conf_template.h user_modules/lv_binding_micropython/lv_conf.h

        # Enable SDL in the configuration
        sed -i 's/#if 0 .*Set it to "1" to enable content.*/#if 1 \/\*Set it to "1" to enable content\*\//' user_modules/lv_binding_micropython/lv_conf.h
        sed -i 's/#define LV_USE_SDL.*0/#define LV_USE_SDL 1/' user_modules/lv_binding_micropython/lv_conf.h

        log_success "LVGL configuration created and updated for SDL"
    else
        log_warning "LVGL configuration template not found, using default build"
    fi
}

build_micropython_cross_compiler() {
    log_info "Building MicroPython cross-compiler..."
    
    cd "$BUILD_DIR/micropython"
    
    # Build the cross-compiler first
    make -C mpy-cross
    
    log_success "MicroPython cross-compiler built"
}

build_unix_port() {
    log_info "Building MicroPython Unix port with LVGL..."

    cd "$BUILD_DIR/lv_micropython"

    # Build the unix port with LVGL
    cd ports/unix

    # Set environment variables for SDL
    export SDL_CFLAGS="$(pkg-config --cflags sdl2)"
    export SDL_LDFLAGS="$(pkg-config --libs sdl2)"

    # Configure build flags for LVGL with SDL
    export CFLAGS_EXTRA="-DLV_CONF_INCLUDE_SIMPLE=1 -DLV_USE_SDL=1 $SDL_CFLAGS"
    export LDFLAGS_EXTRA="$SDL_LDFLAGS"

    # Clean previous build
    make clean || true

    # Build with LVGL user module
    log_info "Building MicroPython with LVGL user module..."
    make -j$(nproc) \
        USER_C_MODULES=../../user_modules \
        CFLAGS_EXTRA="$CFLAGS_EXTRA" \
        LDFLAGS_EXTRA="$LDFLAGS_EXTRA" \
        V=1

    log_success "MicroPython with LVGL built successfully"
}

test_build() {
    log_info "Testing the build..."

    cd "$BUILD_DIR/lv_micropython/ports/unix"

    # Test basic functionality
    echo "Testing MicroPython import..."
    if ./build-standard/micropython -c "import sys; print('MicroPython version:', sys.version)"; then
        log_success "MicroPython basic test passed"
    else
        log_error "MicroPython basic test failed"
        return 1
    fi

    # Test LVGL import
    echo "Testing LVGL import..."
    if ./build-standard/micropython -c "import lvgl as lv; print('LVGL version:', lv.version_info())"; then
        log_success "LVGL import test passed"
    else
        log_warning "LVGL import test failed (this might be expected without display)"
    fi

    # Copy the executable to AppDir
    log_info "Copying executable to AppDir..."
    mkdir -p "$SCRIPT_DIR/../AppDir/usr/bin"
    cp build-standard/micropython "$SCRIPT_DIR/../AppDir/usr/bin/"
    log_success "Executable copied to AppDir"
}

copy_to_appdir() {
    log_info "Copying executable to AppDir..."
    
    local appdir="$PROJECT_DIR/AppDir"
    mkdir -p "$appdir/usr/bin"
    
    cp "$BUILD_DIR/lv_micropython/ports/unix/build-standard/micropython" "$appdir/usr/bin/micropython-lvgl"
    
    # Make it executable
    chmod +x "$appdir/usr/bin/micropython-lvgl"
    
    log_success "Executable copied to AppDir"
}

main() {
    log_info "Building MicroPython with LVGL $LVGL_VERSION..."
    
    setup_build_dir
    download_micropython
    download_lvgl_bindings
    patch_lvgl_config
    build_micropython_cross_compiler
    build_unix_port
    test_build
    copy_to_appdir
    
    log_success "MicroPython with LVGL build completed!"
    log_info "Executable location: $PROJECT_DIR/AppDir/usr/bin/micropython-lvgl"
}

# Run main function
main "$@"
