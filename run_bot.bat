@echo off
setlocal
cd /d "%~dp0"

set "PORT=8001"
set "NGROK_EXE=%LOCALAPPDATA%\ngrok\ngrok.exe"
set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"

if not exist "%NGROK_EXE%" (
    where ngrok >nul 2>nul
    if errorlevel 1 (
        echo ERROR: ngrok.exe not found.
        echo Expected: %LOCALAPPDATA%\ngrok\ngrok.exe
        echo Install ngrok or add it to PATH.
        echo.
        pause
        exit /b 1
    )
    set "NGROK_EXE=ngrok"
)

if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

timeout /t 1 /nobreak >nul

echo Starting ngrok...
start "ngrok Tunnel" cmd /k ""%NGROK_EXE%" http %PORT%"

timeout /t 3 /nobreak >nul

echo Starting FastAPI...
start "FastAPI Server" cmd /k ""%PYTHON_EXE%" app.py"

echo.
echo Done.
echo Webhook path: /webhook/zalo
echo Copy HTTPS link from the ngrok window and update WEBHOOK_URL in .env if it changed.
echo.

pause
