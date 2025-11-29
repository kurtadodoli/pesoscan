# PesoScan Frontend Startup Script
Write-Host "🚀 Starting PesoScan Frontend..." -ForegroundColor Cyan
Write-Host "📍 Location: C:\pesoscan\frontend" -ForegroundColor Yellow
Write-Host "🌐 Frontend will run on: http://localhost:3000" -ForegroundColor Green
Write-Host ""

Set-Location C:\pesoscan\frontend

Write-Host "🔥 Starting React development server... (Press Ctrl+C to stop)" -ForegroundColor Yellow
Write-Host ""

# Start the frontend
npm start
