@echo off
:menu
cls
echo ================================================================================
echo                            WorkflowScheduler Launcher                           
echo ================================================================================
echo.
echo      1. Run Workflow Scheduler
echo      2. Install Requirements
echo.
echo --------------------------------------------------------------------------------
set /p choice=Selection; Menu Options = 1-2, Exit Launcher = X: 

if "%choice%" == "1" (
    python main_script.py
    goto menu
) else if "%choice%" == "2" (
    pip install -r data/requirements.txt
    goto menu
) else if /i "%choice%" == "X" (
    echo Exiting Launcher...
    exit /b
) else (
    echo Invalid selection. Please choose a valid option (1-2) or press X to exit.
    timeout /t 2 >nul
    goto menu
)

