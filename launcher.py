# Script: `.\launcher.py`

# Imports
import os
import json
from scripts.utility import validate_config, countdown_timer
from scripts.temporary import CONFIG_PATH
from scripts.interface import launch_interface

# Functions
def load_config():
    """Load events from the database."""
    from scripts.database import get_events_in_window
    from scripts.utility import get_61_day_window
    start, end = get_61_day_window()
    return get_events_in_window(start, end)

def save_config(config):
    """Save events to the database (redundant; remove this function)."""
    pass  # Events are saved directly via database in the interface.

def main():
    launch_interface(load_config(), save_config)  # No longer uses JSON

if __name__ == "__main__":
    main()