import time

def validate_config(config):
    """Ensure all events have valid labels and durations."""
    return [item for item in config if item["event"].strip() and item["duration"] > 0]

def countdown_timer(duration, update_callback, interrupt_event=None):
    """
    Run a countdown timer with progress updates and optional interrupt.
    :param duration: Total time in seconds.
    :param update_callback: Function to update the UI with remaining time and total duration.
    :param interrupt_event: Optional threading event to stop the timer.
    """
    for elapsed in range(duration):
        if interrupt_event and interrupt_event.is_set():
            break  # Interrupt if event is set
        remaining = duration - elapsed
        update_callback(remaining, duration)
        time.sleep(1)  # Simulate real-time countdown

