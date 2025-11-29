@echo off
cd /d "C:\pesoscan"
call .venv\Scripts\Activate.bat
cd backend
python stable_server.py
pause