# WorkflowScheduler

### Description
WorkflowScheduler is a cross-platform Python application designed to help users efficiently organize their time and activities. With a user-friendly Gradio interface, it enables you to manage a rolling 61-day schedule—covering 30 days past, the current day, and 30 days future—to optimally track progress and automatically schedule repeating tasks (daily, weekly, or monthly). Whether planning a day to tidy the house or balancing work and breaks, the application supports dynamic adjustments to fit your needs. Its core focus is simplicity, effective features, and clear visualization of time, processes, and tasks.

### Features
- Intuitive Gradio Interface: Configure and manage your schedule effortlessly through a simple GUI.
- Rolling 61-Day Schedule: View and manage events from 30 days in the past to 30 days in the future, with automatic updates.
- Recurring Events: Schedule tasks that repeat daily, weekly, or monthly, with automatic rescheduling.
- Event Notes: Attach readable notes to each event for additional context or reminders.
- Real-Time Progress Updates: Monitor active events with a progress bar and remaining time display.
- Cross-Platform Compatibility: Works seamlessly on Windows 10+ and Ubuntu 20.04+.
- Interrupt and Adjust Functionality: Stop, return to configuration, or exit the application at any time.

## Requirements
- Python - 3.7 or newer, Launcher can install requirements.
- Operating System - Compatible with Windows 10+ and Ubuntu 20.04+

## Development
Next Stages...
- Implement the Gradio interface for event management, integrate event logic with the SQLite database, and test the application across platforms.
- testing and, complete/fix/improve.

### Structure
```
WorkflowScheduler/
├── launcher.py
├── Windows.bat
├── Ubuntu.sh
├── data/
│   └── persistence.json
│   └── requirements.txt
├── scripts/
    ├── gradio_interface.py
    └── utility_misc.py
```
