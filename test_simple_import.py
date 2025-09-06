#!/usr/bin/env python3
"""
Simple import test
"""

try:
    import usys as sys
except ImportError:
    import sys

# Add src directory to path FIRST
sys.path.append('src')

print("Testing imports...")

try:
    from utils.navigation_manager import NavigationManager, AppState, nav_manager, app_state
    print("✓ Successfully imported navigation_manager")
except ImportError as e:
    print("✗ Failed to import navigation_manager:", e)

try:
    from utils.data_manager import DataManager
    print("✓ Successfully imported data_manager")
except ImportError as e:
    print("✗ Failed to import data_manager:", e)

try:
    from utils.error_handler import ErrorHandler
    print("✓ Successfully imported error_handler")
except ImportError as e:
    print("✗ Failed to import error_handler:", e)

try:
    from screens.main_screen import MainScreen
    print("✓ Successfully imported main_screen")
except ImportError as e:
    print("✗ Failed to import main_screen:", e)

print("All imports completed!")
