@echo off
:: =====================================================
::  Ikon Server - Auto Start on Windows Login
::  This script registers a Windows Scheduled Task
::  that starts server.py every time you log in.
:: =====================================================

set TASK_NAME=IkonInternshipServer
set SERVER_DIR=D:\Internshipsite
set PYTHON_EXE=python

:: Remove old task if exists (ignore errors)
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: Create a new task that runs at user logon
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "cmd /c cd /d %SERVER_DIR% && %PYTHON_EXE% server.py" ^
  /sc ONLOGON ^
  /rl HIGHEST ^
  /f

if %errorlevel%==0 (
    echo.
    echo ============================================
    echo   SUCCESS! Server will auto-start on login.
    echo   Task Name: %TASK_NAME%
    echo ============================================
    echo.
    echo   The Python server will now start automatically
    echo   every time you log into Windows.
    echo.
    echo   Just open http://localhost:3000 in your browser
    echo   and the site will be ready!
    echo.
    echo   To remove this, run:
    echo     schtasks /delete /tn "%TASK_NAME%" /f
    echo ============================================
) else (
    echo.
    echo ERROR: Could not create scheduled task.
    echo Please try running this script as Administrator.
    echo Right-click the file and select "Run as administrator"
)

pause
