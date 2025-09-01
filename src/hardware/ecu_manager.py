


import random
import time

def get_live_data():
    """Get live data from the ECU"""
    # Simulate reading live data with a delay
    time.sleep(0.5)

    # Return mock live data
    return {
        "RPM": random.randint(600, 4000),
        "Coolant Temp": f"{random.randint(70, 110)}°F",
        "Throttle Position": f"{random.randint(0, 100)}%",
        "Engine Load": f"{random.randint(0, 100)}%",
        "Fuel Level": f"{random.randint(0, 100)}%"
    }


