

import random
import time

def clear_dtc():
    """Clear Diagnostic Trouble Codes"""
    # Simulate clearing DTCs with a delay
    time.sleep(1)

    # Randomly determine if the operation was successful
    return random.choice([True, False])

def read_dtc():
    """Read Diagnostic Trouble Codes from the system"""
    # Simulate reading DTCs with a delay
    time.sleep(1)

    # Return a list of mock DTCs
    dtcs = [
        {
            "code": "P0300",
            "description": "Random/Multiple Cylinder Misfire Detected",
            "status": "Current"
        },
        {
            "code": "P0420",
            "description": "Catalyst System Efficiency Below Threshold",
            "status": "Pending"
        }
    ]

    # Randomly determine if we find any DTCs
    if random.choice([True, False]):
        return dtcs
    else:
        return []

