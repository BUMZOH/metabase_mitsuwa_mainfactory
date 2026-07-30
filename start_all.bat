@echo off
setlocal

rem ========================================
rem Project paths
rem ========================================
set "PROJECT_DIR=%~dp0"
set "FLASK_DIR=%PROJECT_DIR%flask_display_timeline"
set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"
set "METABASE_JAR=%PROJECT_DIR%metabase.jar"

set "SOURCE_DB=\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db"

cd /d "%PROJECT_DIR%"
if errorlevel 1 goto PROJECT_DIR_FAILED


rem ========================================
rem Startup file checks
rem ========================================
echo ========================================
echo Startup file check
echo ========================================
echo.

if not exist "%PYTHON_EXE%" goto PYTHON_NOT_FOUND
if not exist "%FLASK_DIR%\app.py" goto APP_NOT_FOUND
if not exist "%METABASE_JAR%" goto METABASE_NOT_FOUND
if not exist "%SOURCE_DB%" goto DATABASE_NOT_FOUND

echo Python:
echo %PYTHON_EXE%
echo.

echo Flask:
echo %FLASK_DIR%\app.py
echo.

echo Metabase:
echo %METABASE_JAR%
echo.

echo NAS database:
echo %SOURCE_DB%
echo.
echo NAS database connection confirmed.
echo Metabase will read the NAS database directly.
echo.


rem ========================================
rem Start Flask in another window
rem ========================================
echo ========================================
echo Starting Flask...
echo ========================================
echo URL: http://127.0.0.1:5000
echo.

start "Flask Server" /D "%FLASK_DIR%" "%PYTHON_EXE%" app.py

if errorlevel 1 goto FLASK_START_FAILED

rem Flaskの起動処理を少し待つ
timeout /t 2 /nobreak > nul


rem ========================================
rem Open Metabase in Chrome
rem ========================================
start "" powershell.exe -NoProfile -WindowStyle Hidden -Command ^
    "Start-Sleep -Seconds 3; Start-Process 'chrome.exe' 'http://localhost:3000'"


rem ========================================
rem Start Metabase
rem ========================================
echo ========================================
echo Starting Metabase...
echo ========================================
echo URL: http://localhost:3000
echo.
echo Flask is running in another window.
echo.

java -jar "%METABASE_JAR%"
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo ========================================
echo Metabase has stopped.
echo Exit code: %EXIT_CODE%
echo ========================================
echo.
echo Flask may still be running in its own window.
echo Close the Flask window when it is no longer needed.
echo.
pause
exit /b %EXIT_CODE%


rem ========================================
rem Error handling
rem ========================================
:PROJECT_DIR_FAILED
echo [ERROR] Could not change to the project directory:
echo %PROJECT_DIR%
goto ERROR_EXIT

:PYTHON_NOT_FOUND
echo [ERROR] Python was not found:
echo %PYTHON_EXE%
goto ERROR_EXIT

:APP_NOT_FOUND
echo [ERROR] Flask app.py was not found:
echo %FLASK_DIR%\app.py
goto ERROR_EXIT

:METABASE_NOT_FOUND
echo [ERROR] metabase.jar was not found:
echo %METABASE_JAR%
goto ERROR_EXIT

:DATABASE_NOT_FOUND
echo [ERROR] The NAS database was not found:
echo %SOURCE_DB%
echo.
echo Check the network connection and NAS availability.
goto ERROR_EXIT

:FLASK_START_FAILED
echo [ERROR] Flask could not be started.
echo Python:
echo %PYTHON_EXE%
echo.
echo Application:
echo %FLASK_DIR%\app.py
goto ERROR_EXIT

:ERROR_EXIT
echo.
pause
exit /b 1
