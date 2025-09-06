#!/usr/bin/env python3
"""
Debug import issues
"""

import sys
print("Initial sys.path:", sys.path)

# Add src directory to path
sys.path.append('src')
print("After adding src:", sys.path)

try:
    import utils.navigation_manager
    print("✓ Successfully imported utils.navigation_manager")
except ImportError as e:
    print("✗ Failed to import utils.navigation_manager:", e)

try:
    from utils.navigation_manager import NavigationManager
    print("✓ Successfully imported NavigationManager")
except ImportError as e:
    print("✗ Failed to import NavigationManager:", e)

# Check if src directory exists
import os
if os.path.exists('src'):
    print("✓ src directory exists")
    if os.path.exists('src/utils'):
        print("✓ src/utils directory exists")
        if os.path.exists('src/utils/navigation_manager.py'):
            print("✓ src/utils/navigation_manager.py exists")
        else:
            print("✗ src/utils/navigation_manager.py does not exist")
    else:
        print("✗ src/utils directory does not exist")
else:
    print("✗ src directory does not exist")
