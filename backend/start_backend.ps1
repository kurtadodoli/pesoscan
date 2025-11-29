# PesoScan Backend Server Startup Script
Write-Host "🚀 Starting PesoScan Backend Server..." -ForegroundColor Cyan
Write-Host "📍 Location: C:\pesoscan\backend" -ForegroundColor Yellow
Write-Host "🌐 Server will run on: http://localhost:8000" -ForegroundColor Green
Write-Host ""

Set-Location C:\pesoscan\backend

# Check if virtual environment exists
if (Test-Path "C:\pesoscan\.venv\Scripts\Activate.ps1") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & C:\pesoscan\.venv\Scripts\Activate.ps1
}

Write-Host "🔥 Starting server... (Press Ctrl+C to stop)" -ForegroundColor Yellow
Write-Host ""

# Start the server
python start_server.py
