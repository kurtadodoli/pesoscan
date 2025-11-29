# Quick Backend Status Checker
Write-Host "Checking PesoScan Backend Server..." -ForegroundColor Cyan
Write-Host ""

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing -TimeoutSec 3
    $health = $response.Content | ConvertFrom-Json
    
    Write-Host "✅ SERVER IS RUNNING!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Status: $($health.status)" -ForegroundColor White
    Write-Host "Version: $($health.version)" -ForegroundColor White
    Write-Host "YOLO Model: $($health.models_loaded.yolo)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Ready to test!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Open http://localhost:3000" -ForegroundColor White
    Write-Host "2. Upload a peso bill image" -ForegroundColor White
    Write-Host "3. Select 'Comprehensive Scan'" -ForegroundColor White  
    Write-Host "4. Click 'Scan'" -ForegroundColor White
    Write-Host "5. Look for COLORED BOUNDING BOXES on the image!" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "❌ Server is not responding yet" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "• Still loading models (can take 30-60 seconds)" -ForegroundColor White
    Write-Host "• Server failed to start (check backend window for errors)" -ForegroundColor White
    Write-Host ""
    Write-Host "What to do:" -ForegroundColor Cyan
    Write-Host "1. Look at the backend PowerShell window" -ForegroundColor White
    Write-Host "2. Look for '✅ All models loaded successfully!'" -ForegroundColor White
    Write-Host "3. Look for 'INFO: Uvicorn running on http://0.0.0.0:8000'" -ForegroundColor White
    Write-Host "4. If you see errors, run: .\restart_backend.ps1" -ForegroundColor White
    Write-Host ""
}

Write-Host "Run this script again to recheck: .\check_backend.ps1" -ForegroundColor Gray
