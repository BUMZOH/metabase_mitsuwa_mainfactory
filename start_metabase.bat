@echo off
setlocal

cd /d "%~dp0"

echo ======================================
echo       Copying database...
echo ======================================
echo.

set "SOURCE_DB=\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db"
set "DEST_DIR=C:\Metabase\Data"
set "DEST_DB=%DEST_DIR%\main_factory_production_data.db"

rem コピー先フォルダがなければ作成
if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

rem データベースを上書きコピー
copy /Y "%SOURCE_DB%" "%DEST_DB%"

if errorlevel 1 (
    echo.
    echo ======================================
    echo       Database copy failed.
    echo ======================================
    echo.
    echo コピー元:
    echo %SOURCE_DB%
    echo.
    pause
    exit /b 1
)

echo.
echo Database copy completed.
echo.

echo ======================================
echo         Starting Metabase...
echo ======================================
echo.

rem Metabaseの起動を待ってからChromeを開く
start "" powershell.exe -NoProfile -WindowStyle Hidden -Command ^
    "Start-Sleep -Seconds 3; Start-Process 'chrome.exe' 'http://localhost:3000'"

rem Metabase起動
java -jar metabase.jar

echo.
echo ======================================
echo      Metabase has stopped.
echo ======================================
pause

endlocal