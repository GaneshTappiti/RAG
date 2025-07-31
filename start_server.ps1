# PowerShell script to run the AI Tool Prompt Generator development server
# This script helps avoid Flask socket errors on Windows

Write-Host "🚀 AI Tool Prompt Generator - Development Server" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
$venvPaths = @(".\.venv\Scripts\Activate.ps1", ".\venv\Scripts\Activate.ps1")
$venvFound = $false

foreach ($venvPath in $venvPaths) {
    if (Test-Path $venvPath) {
        Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
        & $venvPath
        $venvFound = $true
        break
    }
}

if (-not $venvFound) {
    Write-Host "⚠️  No virtual environment found. Using system Python." -ForegroundColor Yellow
    Write-Host "💡 Consider creating a virtual environment: python -m venv .venv" -ForegroundColor Cyan
    Write-Host ""
}

# Check if required packages are installed
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask not found"
    }
} catch {
    Write-Host "❌ Flask not found. Installing required packages..." -ForegroundColor Red
    pip install flask python-dotenv langchain-google-genai
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install packages. Please check your internet connection." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Set environment variables for better Windows compatibility
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:PYTHONPATH = Get-Location

Write-Host "🔧 Environment configured" -ForegroundColor Green
Write-Host "🌐 Starting server on http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "💡 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the server with error handling
try {
    python run_dev_server.py --host 127.0.0.1 --port 5000
} catch {
    Write-Host ""
    Write-Host "❌ Server failed to start. Trying fallback..." -ForegroundColor Red
    Write-Host ""
    python app.py
}

Write-Host ""
Write-Host "🛑 Server stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"
