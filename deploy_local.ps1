Write-Host "========================================" -ForegroundColor Cyan
Write-Host " [CI] Running Automated Test Suite...  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Execute tests
python -m pytest -v

# Obtain the results 
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[CI FAILED] Tests did not pass. Deployment aborted!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " [CI PASSED] Starting CD Pipeline...    " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 2. Stop previous instances from uvicorn if they are running
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. Desplegar: Iniciar FastAPI localmente
# 3. Deploy: Start FastAPI locally 
Write-Host "[CD] Deploying FastAPI local service..." -ForegroundColor Green
python -m uvicorn main:app --reload --port 8000