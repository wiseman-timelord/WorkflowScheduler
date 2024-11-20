import os
import json
from scripts.gradio_interface import launch_interface

# Global variables and initialization
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "data", "persistence.json")

def load_config():
    """Load configuration from the persistence.json file."""
    if not os.path.exists(CONFIG_PATH):
        return [{"event": "", "duration": 0} for _ in range(10)]
    try:
        with open(CONFIG_PATH, "r", newline="") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # Return default config if file is malformed or missing
        return [{"event": "", "duration": 0} for _ in range(10)]

def save_config(config):
    """Save the current configuration to the persistence.json file."""
    try:
        with open(CONFIG_PATH, "w", newline="") as file:
            json.dump(config, file, indent=4)
    except IOError as e:
        print(f"Error saving configuration: {e}")

def main():
    """Main function to load configuration and launch the Gradio interface."""
    config = load_config()
    launch_interface(config, save_config)

if __name__ == "__main__":
    main()

