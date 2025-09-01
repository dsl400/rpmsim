

#!/usr/bin/env python3

"""
Test script for the RPM Simulation Environment
This script runs main_sim.py and verifies that it works correctly.
"""

import subprocess
import sys
import time

def test_simulation():
    """Run the simulation and check if it starts successfully."""
    print("Testing simulation environment...")

    # Run main_sim.py using the virtual environment
    try:
        result = subprocess.run(
            ["venv/bin/python", "sim/main_sim.py"],
            capture_output=True,
            text=True,
            timeout=10  # Set a timeout of 10 seconds
        )

        print("Simulation output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        # Check for success indicators in the output
        if "Display simulation initialized" in result.stdout and \
           "Hardware mocks initialized" in result.stdout:
            print("SUCCESS: Simulation environment works correctly!")
            return True
        else:
            print("FAILURE: Simulation did not initialize properly.")
            return False

    except subprocess.TimeoutExpired:
        print("ERROR: Simulation process timed out after 10 seconds.")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_simulation()
    sys.exit(0 if success else 1)

