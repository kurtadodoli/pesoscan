# Start the PesoScan API server
Write-Host "Starting PesoScan API server..." -ForegroundColor Green

# Navigate to the project directory
Set-Location "C:\pesoscan"

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Start the server in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\pesoscan; .\venv\Scripts\python.exe backend\simple_server.py"

# Wait for server to start
Start-Sleep -Seconds 3

# Test the API
Write-Host "Testing API connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/api/health" -UseBasicParsing
    Write-Host "✅ API is working! Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ API test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Frontend should now be able to connect to the API!" -ForegroundColor Green
Write-Host "Server running at: http://localhost:8001" -ForegroundColor Cyan