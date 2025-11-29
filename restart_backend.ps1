# PesoScan Backend Restart Script
Write-Host "Restarting PesoScan Backend Server..." -ForegroundColor Yellow
Write-Host ""

# Find and kill existing Python processes for PesoScan
Write-Host "Step 1: Stopping existing backend servers..." -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# Start the backend server in a new window
Write-Host ""
Write-Host "Step 2: Starting new backend server..." -ForegroundColor Cyan
$command = "cd C:\pesoscan\backend; python start_server.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $command

Write-Host ""
Write-Host "Backend server restarted!" -ForegroundColor Green
Write-Host "Wait 10 seconds for models to load..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "The server is starting in a new window - check that window for status" -ForegroundColor White
Write-Host ""
