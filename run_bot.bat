@echo off
cd /d C:\Users\Admin\Desktop\telechatbot

timeout /t 1 /nobreak >nul

echo Starting ngrok...
start "ngrok Tunnel" cmd /k "ngrok http 8001"

timeout /t 3 /nobreak >nul

echo Starting FastAPI...
start "FastAPI Server" cmd /k "python app.py"

echo.
echo Done.
echo Webhook: https://xxxxx.ngrok-free.app/webhook/zalo
echo Copy link HTTPS tu cua so ngrok roi gan vao Zalo.
echo.

pause