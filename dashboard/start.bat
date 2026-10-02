@echo off
rem Starts the read-only dashboard in the background (it keeps running after this window closes) and opens it.
rem If it is already running, the second copy exits and the browser just opens the running one.
cd /d "%~dp0.."
if not exist logs\dashboard mkdir logs\dashboard
set PYTHONIOENCODING=utf-8
start "" /min pythonw dashboard\server.py --teams-every 600
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8765
