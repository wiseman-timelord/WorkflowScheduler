#!/bin/bash

while true; do
    clear
    echo "================================================================================"
    echo "                           WorkflowScheduler Launcher                           "
    echo "================================================================================"
    echo ""
    echo "     1. Run Workflow Scheduler"
    echo "     2. Install Requirements"
    echo ""
    echo "--------------------------------------------------------------------------------"
    read -p "Selection; Menu Options = 1-2, Exit Launcher = X: " choice

    case $choice in
        1)
            python3 main_script.py
            ;;
        2)
            pip install -r data/requirements.txt
            ;;
        [Xx])
            echo "Exiting Launcher..."
            exit 0
            ;;
        *)
            echo "Invalid selection. Please choose a valid option (1-2) or press X to exit."
            sleep 2
            ;;
    esac
done

