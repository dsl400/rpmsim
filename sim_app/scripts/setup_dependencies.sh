#!/bin/bash
set -e

# Setup Dependencies Script
# Installs all required dependencies for building the RPM Simulator AppImage

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

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    else
        echo "unknown"
    fi
}

install_ubuntu_debian() {
    log_info "Installing dependencies for Ubuntu/Debian..."
    
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        cmake \
        git \
        python3 \
        python3-pip \
        pkg-config \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libgl1-mesa-dev \
        libglu1-mesa-dev \
        libx11-dev \
        libxext-dev \
        libxrandr-dev \
        libxinerama-dev \
        libxcursor-dev \
        libxi-dev \
        wget \
        file \
        desktop-file-utils
    
    # Install ImageMagick for icon conversion (optional)
    sudo apt-get install -y imagemagick || log_warning "ImageMagick not installed (optional)"
    
    log_success "Ubuntu/Debian dependencies installed"
}

install_fedora_rhel() {
    log_info "Installing dependencies for Fedora/RHEL..."
    
    sudo dnf install -y \
        gcc \
        gcc-c++ \
        make \
        cmake \
        git \
        python3 \
        python3-pip \
        pkgconfig \
        SDL2-devel \
        SDL2_image-devel \
        SDL2_mixer-devel \
        SDL2_ttf-devel \
        mesa-libGL-devel \
        mesa-libGLU-devel \
        libX11-devel \
        libXext-devel \
        libXrandr-devel \
        libXinerama-devel \
        libXcursor-devel \
        libXi-devel \
        wget \
        file \
        desktop-file-utils
    
    # Install ImageMagick for icon conversion (optional)
    sudo dnf install -y ImageMagick || log_warning "ImageMagick not installed (optional)"
    
    log_success "Fedora/RHEL dependencies installed"
}

install_arch() {
    log_info "Installing dependencies for Arch Linux..."
    
    sudo pacman -S --needed \
        base-devel \
        cmake \
        git \
        python3 \
        python-pip \
        pkgconfig \
        sdl2 \
        sdl2_image \
        sdl2_mixer \
        sdl2_ttf \
        mesa \
        libx11 \
        libxext \
        libxrandr \
        libxinerama \
        libxcursor \
        libxi \
        wget \
        file \
        desktop-file-utils
    
    # Install ImageMagick for icon conversion (optional)
    sudo pacman -S --needed imagemagick || log_warning "ImageMagick not installed (optional)"
    
    log_success "Arch Linux dependencies installed"
}

install_opensuse() {
    log_info "Installing dependencies for openSUSE..."
    
    sudo zypper install -y \
        gcc \
        gcc-c++ \
        make \
        cmake \
        git \
        python3 \
        python3-pip \
        pkg-config \
        libSDL2-devel \
        libSDL2_image-devel \
        libSDL2_mixer-devel \
        libSDL2_ttf-devel \
        Mesa-libGL-devel \
        Mesa-libGLU-devel \
        libX11-devel \
        libXext-devel \
        libXrandr-devel \
        libXinerama-devel \
        libXcursor-devel \
        libXi-devel \
        wget \
        file \
        desktop-file-utils
    
    # Install ImageMagick for icon conversion (optional)
    sudo zypper install -y ImageMagick || log_warning "ImageMagick not installed (optional)"
    
    log_success "openSUSE dependencies installed"
}

verify_installation() {
    log_info "Verifying installation..."
    
    local missing_tools=()
    
    # Check for required tools
    for tool in gcc make cmake git python3 pkg-config; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    # Check for SDL2
    if ! pkg-config --exists sdl2; then
        missing_tools+=("SDL2 development libraries")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Some tools are still missing: ${missing_tools[*]}"
        return 1
    fi
    
    log_success "All required tools are available"
    
    # Show versions
    log_info "Tool versions:"
    echo "  GCC: $(gcc --version | head -n1)"
    echo "  Make: $(make --version | head -n1)"
    echo "  CMake: $(cmake --version | head -n1)"
    echo "  Git: $(git --version)"
    echo "  Python: $(python3 --version)"
    echo "  SDL2: $(pkg-config --modversion sdl2)"
}

main() {
    log_info "Setting up build dependencies for RPM Simulator AppImage..."
    
    local distro=$(detect_distro)
    log_info "Detected distribution: $distro"
    
    case "$distro" in
        ubuntu|debian|linuxmint|pop)
            install_ubuntu_debian
            ;;
        fedora|rhel|centos|rocky|almalinux)
            install_fedora_rhel
            ;;
        arch|manjaro|endeavouros)
            install_arch
            ;;
        opensuse*|sles)
            install_opensuse
            ;;
        *)
            log_error "Unsupported distribution: $distro"
            log_info "Please install the following packages manually:"
            log_info "  - Build tools: gcc, make, cmake, git"
            log_info "  - Python 3 and pip"
            log_info "  - SDL2 development libraries"
            log_info "  - OpenGL development libraries"
            log_info "  - X11 development libraries"
            exit 1
            ;;
    esac
    
    verify_installation
    
    log_success "Dependencies setup completed!"
    log_info "You can now run: ./scripts/build_appimage.sh"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    log_error "Do not run this script as root!"
    log_info "The script will use sudo when needed."
    exit 1
fi

# Run main function
main "$@"
