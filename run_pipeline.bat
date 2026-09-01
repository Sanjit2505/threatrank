@echo off
title Cyber Threat Priority Engine launcher
echo ========================================================
echo   STARTING LIVE CYBERSECURITY THREAT PIPELINE & AI DEMO
echo ========================================================
echo.

set PROJECT_DIR=%~dp0

echo [1/3] Launching FastAPI Backend Server & AI Predictor...
start "Backend Server (FastAPI + AI Model)" cmd /k "cd /d "%PROJECT_DIR%backend" && python -m uvicorn server:app --reload"

echo [2/3] Launching React Dashboard Frontend...
start "React Dashboard (Vite)" cmd /k "cd /d "%PROJECT_DIR%frontend" && npm run dev"

echo.
echo Waiting 5 seconds for services to initialize...
timeout /t 5 /nobreak >nul

echo [3/3] Launching Live Threat Generator...
start "Live Threat Generator" cmd /k "cd /d "%PROJECT_DIR%" && python threat_generator.py"

echo.
echo Opening Dashboard in browser...
start http://localhost:5173

echo ========================================================
echo   ALL SERVICES STARTED! 
echo   Check the opened Command Prompt windows to see live logs.
echo ========================================================
