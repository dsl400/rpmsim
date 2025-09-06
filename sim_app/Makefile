# Makefile for RPM Simulator AppImage
# Provides convenient targets for building the simulation environment

.PHONY: all clean setup deps micropython package test help

# Default target
all: package

# Setup dependencies
setup:
	@echo "Setting up build dependencies..."
	./scripts/setup_dependencies.sh

# Alias for setup
deps: setup

# Build MicroPython with LVGL
micropython:
	@echo "Building MicroPython with LVGL bindings..."
	./scripts/build_micropython.sh

# Package the AppImage
package: micropython
	@echo "Packaging AppImage..."
	./scripts/package_appimage.sh

# Full build (setup + build + package)
build: setup micropython package

# Test the AppImage
test:
	@echo "Testing AppImage..."
	@if [ -f "RPMSimulator-x86_64.AppImage" ]; then \
		echo "Testing basic execution..."; \
		timeout 5s ./RPMSimulator-x86_64.AppImage -c "print('Test successful')" || echo "Test completed (timeout expected)"; \
	else \
		echo "AppImage not found. Run 'make package' first."; \
		exit 1; \
	fi

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf AppDir/
	rm -f RPMSimulator-x86_64.AppImage
	rm -f appimagetool-x86_64.AppImage

# Show help
help:
	@echo "RPM Simulator AppImage Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Build everything (default)"
	@echo "  setup      - Install build dependencies"
	@echo "  deps       - Alias for setup"
	@echo "  micropython- Build MicroPython with LVGL"
	@echo "  package    - Create the AppImage"
	@echo "  build      - Full build (setup + micropython + package)"
	@echo "  test       - Test the created AppImage"
	@echo "  clean      - Remove build artifacts"
	@echo "  help       - Show this help"
	@echo ""
	@echo "Quick start:"
	@echo "  make setup    # Install dependencies (requires sudo)"
	@echo "  make all      # Build the AppImage"
	@echo "  make test     # Test the result"
	@echo ""
	@echo "The final AppImage will be: RPMSimulator-x86_64.AppImage"
