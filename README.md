# WorkflowScheduler

### Description
WorkflowScheduler is a cross-platform Python application that helps users organize their time and activities efficiently. The user can organize their time upon activities, while also factoring in time for breaks, and it uses a gradio interface, users can configure, 30 days past, 30 days future, the current day, thats 61 days rolling, to optimally, track progress, and automatically schedule repeating, daily, weekly, monthly, tasks and times, and dynamically adjust their schedule to fit their needs. The idea is people have plan for day, like tidy whole house, they can now schedule work and breaks, and complete task effectively in day; main thing, simplicity and effective features and visualization of time processes and tasks.

### Features
- Intuitive Gradio Interface: User-friendly GUI to configure and manage schedules effortlessly.
- Dynamic Event Tracking: Allows up to 10 events, each with customizable labels and durations.
- Real-Time Progress Updates: Displays active events, a progress bar, and remaining time for each activity.
- Cross-Platform Compatibility: Fully compatible with both Windows and Linux environments.
- Interrupt and Adjust Functionality: Includes options to stop, return to configuration, or exit anytime.

## Requirements
- Python - 3.7 or newer, Launcher can install requirements.
- Operating System - Compatible with Windows 10+ and Ubuntu 20.04+

## Development
- Next stage: testing and, complete/fix/improve.

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
