# PesoScan Complete Application Startup Script
# This script starts both the backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🚀 PesoScan Application Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend Server in new window
Write-Host "1️⃣  Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\pesoscan\backend; Write-Host '🔧 BACKEND SERVER' -ForegroundColor Green; python start_server.py"

# Wait for backend to initialize
Write-Host "⏳ Waiting for backend to initialize (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if backend is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend server is running!" -ForegroundColor Green
    Write-Host "   📍 API URL: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "   📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Backend server might still be starting..." -ForegroundColor Yellow
}

Write-Host ""

# Start Frontend Server in new window
Write-Host "2️⃣  Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\pesoscan\frontend; Write-Host '🎨 FRONTEND SERVER' -ForegroundColor Green; npm start"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ Application Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Two PowerShell windows have opened:" -ForegroundColor Yellow
Write-Host "   - Backend Server (port 8000)" -ForegroundColor White
Write-Host "   - Frontend Server (port 3000)" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Keep both windows open while using the application" -ForegroundColor Yellow
Write-Host "🛑 Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
