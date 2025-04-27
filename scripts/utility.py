# Script: `.\scripts\utility.py`

# Imports
import time
from datetime import datetime, timedelta

# Functions
def validate_config(config):
    """Validate event structure and datetime values"""
    valid_events = []
    for event in config:
        try:
            if not event.get("title", "").strip():
                continue

            start = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M")
            end = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M")
            
            if start >= end:
                continue

            valid_events.append(event)
        except (KeyError, ValueError):
            continue
    return valid_events  # Fixed syntax error

def generate_recurrences(event, window_start, window_end):
    """Complete recurrence logic"""
    recurrences = []
    current = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M")
    duration = end_time - current
    
    window_start_dt = datetime.strptime(window_start, "%Y-%m-%d")
    window_end_dt = datetime.strptime(window_end, "%Y-%m-%d")

    while current <= window_end_dt:
        if current >= window_start_dt:
            recurrences.append({
                "title": event["title"],
                "start_time": current.strftime("%Y-%m-%d %H:%M"),
                "end_time": (current + duration).strftime("%Y-%m-%d %H:%M"),
                "notes": event["notes"],
                "recurrence_rule": event["recurrence_rule"],
                "is_recurring": event["is_recurring"]
            })
        
        if event["recurrence_rule"] == "daily":
            current += timedelta(days=1)
        elif event["recurrence_rule"] == "weekly":
            current += timedelta(weeks=1)
        elif event["recurrence_rule"] == "monthly":
            try:
                if current.month == 12:
                    current = current.replace(year=current.year+1, month=1)
                else:
                    current = current.replace(month=current.month+1)
            except ValueError:
                current = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        else:
            break
    
    return recurrences

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

def get_61_day_window():
    from scripts.temporary import CONFIG_PATH
    import json
    
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        days = config.get("default_view_days", 30)
    except (FileNotFoundError, json.JSONDecodeError):
        days = 30
    
    today = datetime.now().replace(hour=0, minute=0, second=0)
    start = today - timedelta(days=days)
    end = today + timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

