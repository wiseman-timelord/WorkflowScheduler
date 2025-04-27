# Script: `.\scripts\database.py`

# Imports
import sqlite3
import os
from scripts.temporary import BASE_DIR

# Globals
DB_PATH = os.path.join(BASE_DIR, "data", "events.db")

# Functions
def connect_db():
    return sqlite3.connect(DB_PATH)

def add_event(title, start_time, end_time, recurrence_rule, notes, is_recurring):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (title, start_time, end_time, recurrence_rule, notes, is_recurring) VALUES (?, ?, ?, ?, ?, ?)",
        (title, start_time, end_time, recurrence_rule, notes, int(is_recurring))
    )
    conn.commit()
    conn.close()

def get_events_in_window(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM events 
        WHERE 
            (is_recurring = 0 AND 
                (start_time BETWEEN ? AND ? OR  -- Starts in window
                end_time BETWEEN ? AND ? OR    -- Ends in window
                (start_time <= ? AND end_time >= ?))) OR  -- Spans window
            (is_recurring = 1 AND start_time <= ?)  -- Recurring events
    ''', (start_date, end_date, start_date, end_date, 
          start_date, end_date, end_date))
    events = cursor.fetchall()
    conn.close()
    return [{
        "id": e[0],
        "title": e[3],
        "start_time": e[1],
        "end_time": e[2],
        "recurrence_rule": e[5],
        "notes": e[4],
        "is_recurring": e[6]
    } for e in events]

def update_event(event_id, title, start_time, end_time, recurrence_rule, notes, is_recurring):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE events SET title=?, start_time=?, end_time=?, recurrence_rule=?, notes=?, is_recurring=? WHERE id=?",
        (title, start_time, end_time, recurrence_rule, notes, int(is_recurring), event_id)
    )
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    
def delete_all_events():
    """Clear all events from the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events")
    conn.commit()
    conn.close()