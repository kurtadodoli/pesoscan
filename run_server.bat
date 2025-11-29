@echo off
echo Starting PesoScan API Server...
cd /d "C:\pesoscan"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting server on port 8001...
python backend\main.py

pause