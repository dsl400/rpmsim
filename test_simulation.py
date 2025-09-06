import subprocess
import sys
import time
import os

def test_simulation():
    """Run the simulation and check if it starts successfully."""
    print("Testing simulation environment...")

    try:
        result = subprocess.run(
            [".env/bin/python", "sim/main_sim.py"],
            capture_output=True,
            text=True,
            timeout=10
        )

        print("Simulation output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

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

def test_missing_lvgl_module():
    """Test simulation failure when lvgl module is missing."""
    print("Testing simulation with missing lvgl module...")
    # Temporarily rename lvgl if present to simulate missing module
    lvgl_path = os.path.join("sim", "lvgl.py")
    temp_path = os.path.join("sim", "lvgl_temp.py")
    renamed = False
    if os.path.exists(lvgl_path):
        os.rename(lvgl_path, temp_path)
        renamed = True

    try:
        result = subprocess.run(
            [".env/bin/python", "sim/main_sim.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert "No module named 'lvgl'" in result.stderr, "lvgl import error not detected"
        print("SUCCESS: Missing lvgl module error detected.")
    finally:
        if renamed:
            os.rename(temp_path, lvgl_path)

def test_timeout():
    """Test simulation timeout handling."""
    print("Testing simulation timeout...")
    try:
        result = subprocess.run(
            [".env/bin/python", "-c", "import time; time.sleep(15)"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("FAILURE: Timeout not triggered as expected.")
        return False
    except subprocess.TimeoutExpired:
        print("SUCCESS: Timeout triggered correctly.")
        return True

if __name__ == "__main__":
    all_passed = True
    all_passed &= test_simulation()
    try:
        test_missing_lvgl_module()
    except AssertionError as e:
        print(f"FAILURE: {e}")
        all_passed = False
    all_passed &= test_timeout()
    sys.exit(0 if all_passed else 1)
