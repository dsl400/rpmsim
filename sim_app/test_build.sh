#!/bin/bash
set -e

# Test Build System
# Validates the build system without actually building everything

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

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

test_directory_structure() {
    log_info "Testing directory structure..."
    
    local required_dirs=(
        "scripts"
        "AppDir"
        "build"
    )
    
    local required_files=(
        "README.md"
        "BUILDING.md"
        "Makefile"
        "requirements.txt"
        "scripts/build_appimage.sh"
        "scripts/setup_dependencies.sh"
        "scripts/build_micropython.sh"
        "scripts/package_appimage.sh"
    )
    
    # Check directories
    for dir in "${required_dirs[@]}"; do
        if [ -d "$PROJECT_DIR/$dir" ]; then
            log_success "Directory exists: $dir"
        else
            log_error "Missing directory: $dir"
            return 1
        fi
    done
    
    # Check files
    for file in "${required_files[@]}"; do
        if [ -f "$PROJECT_DIR/$file" ]; then
            log_success "File exists: $file"
        else
            log_error "Missing file: $file"
            return 1
        fi
    done
    
    log_success "Directory structure is valid"
}

test_script_permissions() {
    log_info "Testing script permissions..."
    
    local scripts=(
        "scripts/build_appimage.sh"
        "scripts/setup_dependencies.sh"
        "scripts/build_micropython.sh"
        "scripts/package_appimage.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [ -x "$PROJECT_DIR/$script" ]; then
            log_success "Script is executable: $script"
        else
            log_error "Script is not executable: $script"
            return 1
        fi
    done
    
    log_success "All scripts have correct permissions"
}

test_makefile() {
    log_info "Testing Makefile..."
    
    cd "$PROJECT_DIR"
    
    # Test make help
    if make help > /dev/null 2>&1; then
        log_success "Makefile help target works"
    else
        log_error "Makefile help target failed"
        return 1
    fi
    
    # Check if required targets exist
    local targets=$(make -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$)/ {split($1,A,/ /);for(i in A)print A[i]}' | sort -u)
    
    local required_targets=(
        "all"
        "setup"
        "micropython"
        "package"
        "clean"
        "help"
    )
    
    for target in "${required_targets[@]}"; do
        if echo "$targets" | grep -q "^$target$"; then
            log_success "Makefile target exists: $target"
        else
            log_error "Missing Makefile target: $target"
            return 1
        fi
    done
    
    log_success "Makefile is valid"
}

test_dependency_detection() {
    log_info "Testing dependency detection..."
    
    # Test the setup script's dependency detection
    cd "$PROJECT_DIR"
    
    # Run setup script in dry-run mode (just check dependencies)
    if ./scripts/setup_dependencies.sh --help > /dev/null 2>&1; then
        log_info "Setup script can be executed"
    else
        log_warning "Setup script help not available (this is expected)"
    fi
    
    # Check if we can detect the distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        log_success "Detected distribution: $ID"
    else
        log_warning "Cannot detect distribution"
    fi
    
    # Check for basic build tools
    local tools=(
        "gcc"
        "make"
        "cmake"
        "git"
        "python3"
        "pkg-config"
    )
    
    local missing_tools=()
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            log_success "Tool available: $tool"
        else
            missing_tools+=("$tool")
            log_warning "Tool missing: $tool"
        fi
    done
    
    if [ ${#missing_tools[@]} -eq 0 ]; then
        log_success "All basic build tools are available"
    else
        log_warning "Missing tools: ${missing_tools[*]}"
        log_info "Run './scripts/setup_dependencies.sh' to install them"
    fi
}

test_build_configuration() {
    log_info "Testing build configuration..."
    
    # Check version configuration in build scripts
    local micropython_version=$(grep "MICROPYTHON_VERSION=" "$PROJECT_DIR/scripts/build_appimage.sh" | cut -d'"' -f2)
    local lvgl_version=$(grep "LVGL_VERSION=" "$PROJECT_DIR/scripts/build_appimage.sh" | cut -d'"' -f2)
    
    if [ "$micropython_version" = "v1.23.0" ]; then
        log_success "MicroPython version configured: $micropython_version"
    else
        log_error "Unexpected MicroPython version: $micropython_version"
        return 1
    fi
    
    if [ "$lvgl_version" = "9.2.1" ]; then
        log_success "LVGL version configured: $lvgl_version"
    else
        log_error "Unexpected LVGL version: $lvgl_version"
        return 1
    fi
    
    log_success "Build configuration is correct"
}

test_documentation() {
    log_info "Testing documentation..."
    
    local docs=(
        "README.md"
        "BUILDING.md"
    )
    
    for doc in "${docs[@]}"; do
        if [ -s "$PROJECT_DIR/$doc" ]; then
            local lines=$(wc -l < "$PROJECT_DIR/$doc")
            log_success "Documentation exists: $doc ($lines lines)"
        else
            log_error "Documentation missing or empty: $doc"
            return 1
        fi
    done
    
    log_success "Documentation is complete"
}

run_quick_build_test() {
    log_info "Running quick build test (dependency check only)..."
    
    cd "$PROJECT_DIR"
    
    # Test if we can at least start the build process
    if timeout 30s ./scripts/build_appimage.sh --help > /dev/null 2>&1; then
        log_info "Build script can be executed"
    else
        log_warning "Build script help not available (this is expected)"
    fi
    
    # Check if we have SDL2 development libraries
    if pkg-config --exists sdl2; then
        local sdl_version=$(pkg-config --modversion sdl2)
        log_success "SDL2 development libraries available: $sdl_version"
    else
        log_warning "SDL2 development libraries not found"
        log_info "Install with: sudo apt-get install libsdl2-dev (Ubuntu/Debian)"
    fi
    
    log_success "Quick build test completed"
}

main() {
    log_info "Testing RPM Simulator AppImage build system..."
    log_info "This test validates the build system without actually building."
    echo ""
    
    test_directory_structure
    echo ""
    
    test_script_permissions
    echo ""
    
    test_makefile
    echo ""
    
    test_dependency_detection
    echo ""
    
    test_build_configuration
    echo ""
    
    test_documentation
    echo ""
    
    run_quick_build_test
    echo ""
    
    log_success "Build system test completed successfully!"
    echo ""
    log_info "Next steps:"
    log_info "1. Install dependencies: make setup"
    log_info "2. Build the AppImage: make all"
    log_info "3. Test the result: make test"
    echo ""
    log_info "For detailed instructions, see: BUILDING.md"
}

# Run main function
main "$@"
