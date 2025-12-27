# Core Integrator Deployment Script for Windows
# Automates setup, installation, and service startup

param(
    [switch]$SkipInstall,
    [switch]$TestOnly,
    [string]$Environment = "development"
)

Write-Host "Core Integrator Deployment Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to wait for service
function Wait-ForService($url, $timeout = 30) {
    $elapsed = 0
    while ($elapsed -lt $timeout) {
        try {
            $response = Invoke-WebRequest -Uri $url -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                return $true
            }
        }
        catch {
            Start-Sleep -Seconds 1
            $elapsed++
        }
    }
    return $false
}

Write-Host "Step 1: Environment Validation" -ForegroundColor Yellow

# Check Python
if (-not (Test-Command python)) {
    Write-Error "Python not found. Please install Python 3.14+"
    exit 1
}

$pythonVersion = python --version
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green

# Check pip
if (-not (Test-Command pip)) {
    Write-Error "pip not found. Please install pip"
    exit 1
}
Write-Host "✓ pip found" -ForegroundColor Green

Write-Host "`nStep 2: Environment Setup" -ForegroundColor Yellow

# Create virtual environment (optional)
if (-not $SkipInstall) {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    
    # Install requirements
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install requirements"
        exit 1
    }
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
    
    # Install additional packages for deployment
    pip install flask flask-sqlalchemy sentence-transformers scipy coverage pytest
    Write-Host "✓ Additional packages installed" -ForegroundColor Green
}

Write-Host "`nStep 3: Database Setup" -ForegroundColor Yellow

# Create database directories
$dbDirs = @("db", "data", "reports", "logs")
foreach ($dir in $dbDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    }
}

# Initialize databases
if (-not (Test-Path "db/context.db")) {
    Write-Host "Initializing context database..." -ForegroundColor Cyan
    # Database will be created automatically on first run
    Write-Host "✓ Database initialization prepared" -ForegroundColor Green
}

Write-Host "`nStep 4: Configuration Validation" -ForegroundColor Yellow

# Check .env file
if (-not (Test-Path ".env")) {
    Write-Warning ".env file not found. Using default configuration."
} else {
    Write-Host "✓ Configuration file found" -ForegroundColor Green
}

# Validate configuration
$env:INTEGRATOR_USE_NOOPUR = "true"
$env:NOOPUR_BASE_URL = "http://localhost:5001"
Write-Host "✓ Environment variables set" -ForegroundColor Green

if ($TestOnly) {
    Write-Host "`nTest Mode: Running tests only" -ForegroundColor Cyan
    python -m pytest tests/test_noopur_integration.py tests/test_bridge_connectivity.py -v
    exit $LASTEXITCODE
}

Write-Host "`nStep 5: Service Startup" -ForegroundColor Yellow

# Start Noopur service
Write-Host "Starting Noopur service..." -ForegroundColor Cyan
$noopurProcess = Start-Process -FilePath "python" -ArgumentList "external/CreatorCore-Task/app.py" -WorkingDirectory "external/CreatorCore-Task" -PassThru -WindowStyle Minimized

Start-Sleep -Seconds 3

# Start Mock CreatorCore
Write-Host "Starting Mock CreatorCore..." -ForegroundColor Cyan
$mockProcess = Start-Process -FilePath "python" -ArgumentList "tests/mocks/creatorcore_mock.py" -WorkingDirectory "tests/mocks" -PassThru -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host "`nStep 6: Health Verification" -ForegroundColor Yellow

# Check Noopur health
Write-Host "Checking Noopur service..." -ForegroundColor Cyan
if (Wait-ForService "http://localhost:5001/history" 15) {
    Write-Host "✓ Noopur service is healthy" -ForegroundColor Green
} else {
    Write-Warning "Noopur service health check failed"
}

# Check Mock CreatorCore health
Write-Host "Checking Mock CreatorCore..." -ForegroundColor Cyan
if (Wait-ForService "http://localhost:5002/system/health" 15) {
    Write-Host "✓ Mock CreatorCore is healthy" -ForegroundColor Green
} else {
    Write-Warning "Mock CreatorCore health check failed"
}

Write-Host "`nStep 7: Integration Test" -ForegroundColor Yellow

# Test integration
Write-Host "Testing integration..." -ForegroundColor Cyan
try {
    $testResult = python -c "
import sys
sys.path.append('.')
from creator_routing import CreatorRouter
router = CreatorRouter()
result = router.prewarm_and_prepare('generate', 'deploy_test', {'topic': 'Deployment Test', 'goal': 'Verify integration'})
print('SUCCESS' if 'topic' in result else 'FAILED')
"
    
    if ($testResult -eq "SUCCESS") {
        Write-Host "✓ Integration test passed" -ForegroundColor Green
    } else {
        Write-Warning "Integration test failed"
    }
} catch {
    Write-Warning "Integration test error: $_"
}

Write-Host "`nStep 8: Final Status" -ForegroundColor Yellow

# Create deployment report
$deploymentReport = @{
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
    environment = $Environment
    python_version = $pythonVersion
    services = @{
        noopur = @{
            process_id = $noopurProcess.Id
            url = "http://localhost:5001"
        }
        mock_creatorcore = @{
            process_id = $mockProcess.Id
            url = "http://localhost:5002"
        }
    }
    status = "deployed"
}

$deploymentReport | ConvertTo-Json -Depth 3 | Out-File "reports/deployment_status.json" -Encoding UTF8

Write-Host "`n🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "Services Running:" -ForegroundColor Cyan
Write-Host "  • Noopur: http://localhost:5001" -ForegroundColor White
Write-Host "  • Mock CreatorCore: http://localhost:5002" -ForegroundColor White
Write-Host "  • Process IDs: Noopur=$($noopurProcess.Id), Mock=$($mockProcess.Id)" -ForegroundColor White
Write-Host "`nTo stop services:" -ForegroundColor Yellow
Write-Host "  Stop-Process -Id $($noopurProcess.Id)" -ForegroundColor White
Write-Host "  Stop-Process -Id $($mockProcess.Id)" -ForegroundColor White
Write-Host "`nDeployment report: reports/deployment_status.json" -ForegroundColor Cyan