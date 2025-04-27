# Script: `.\installer.py` (a standalone installer script, that should not reference other scripts unless it is checking/creating them)

# Imports
import os
import sys
import subprocess
import json
import sqlite3
import time

# Globals
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "venv")

# Database
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT,
    end_time TEXT,
    title TEXT,
    notes TEXT,
    recurrence_rule TEXT,
    is_recurring INTEGER
);

# Functions
def clean_previous_installation():
    for directory in ["data", "venv"]:
        path = os.path.join(BASE_DIR, directory)
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)
    print("Cleaned previous installation artifacts.")

def ensure_directories():
    for directory in ["data", "scripts"]:
        path = os.path.join(BASE_DIR, directory)
        os.makedirs(path, exist_ok=True)
    with open(os.path.join(BASE_DIR, "scripts", "__init__.py"), "w") as f:
        f.write("")
    print("Created required directories and files.")

def create_requirements_file():
    requirements = ["gradio", "python-dateutil"]
    with open(os.path.join(BASE_DIR, "data", "requirements.txt"), "w") as f:
        f.write("\n".join(requirements))
    print("Created requirements.txt.")

def create_persistent_json():
    persistent_file = os.path.join(BASE_DIR, "data", "persistence.json")
    default_settings = {
        "version": "1.0",
        "default_view_days": 30
    }
    with open(persistent_file, "w") as f:
        json.dump(default_settings, f, indent=4)
    print("Created persistence.json with default configuration.")

def create_database():
    db_path = os.path.join(BASE_DIR, "data", "events.db")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                end_time TEXT,
                title TEXT,
                notes TEXT,
                recurrence_rule TEXT,
                is_recurring INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print("Created events.db with initial schema.")
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

def verify_installation():
    required = [
        os.path.join(BASE_DIR, "data", "requirements.txt"),
        os.path.join(BASE_DIR, "data", "events.db"),
        os.path.join(VENV_DIR, "pyvenv.cfg")
    ]
    missing = [path for path in required if not os.path.exists(path)]
    
    # Verify database schema
    try:
        conn = sqlite3.connect(os.path.join(BASE_DIR, "data", "events.db"))
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(events)")
        columns = [col[1] for col in cursor.fetchall()]
        if "recurrence_rule" not in columns:
            missing.append("Database schema")
    except Exception as e:
        missing.append(f"Database connection: {str(e)}")
    
    if missing:
        print(f"Installation incomplete. Missing: {', '.join(missing)}")
        return False
    print("Installation verified successfully.")
    return True

def main():
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        clean_previous_installation()
        ensure_directories()
        create_requirements_file()
        if not os.path.exists(VENV_DIR):
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        pip_executable = os.path.join(VENV_DIR, "bin" if os.name != "nt" else "Scripts", "pip")
        subprocess.check_call([pip_executable, "install", "-r", os.path.join(BASE_DIR, "data", "requirements.txt")])
        python_executable = os.path.join(VENV_DIR, "bin" if os.name != "nt" else "Scripts", "python")
        subprocess.run([python_executable, __file__])
    else:
        ensure_directories()
        create_persistent_json()
        create_database()
        if not verify_installation():
            print("Setup failed.")
            time.sleep(5)
            sys.exit(1)
        print("Setup completed successfully.")
        time.sleep(2)

if __name__ == "__main__":
    main()