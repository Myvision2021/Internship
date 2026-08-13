@echo off
echo Starting Ikon Internship Website Server...

:: Start the Python server in a separate hidden window/background process
start /B python server.py

:: Wait for 2 seconds to ensure the server is fully running
timeout /t 2 /nobreak > NUL

:: Open the website in the default web browser
start http://localhost:3000

echo Server is running in the background. 
echo You can safely close this command window.
exit
