@echo off
cd /d "%~dp0"

echo =====================================
echo Flask Equipment Timeline
echo =====================================
echo.

"..\.venv\Scripts\python.exe" app.py

echo.
echo =====================================
echo Flask has stopped.
echo =====================================
pause