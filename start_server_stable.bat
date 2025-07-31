@echo off
REM Windows batch script to run the AI Tool Prompt Generator with stable configuration
REM This script avoids Flask socket errors on Windows

echo 🚀 AI Tool Prompt Generator - Stable Mode
echo.

REM Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Using system Python.
)

REM Set environment variables for better Windows compatibility
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=%CD%

echo 🔧 Environment configured for Windows
echo 🌐 Starting server on http://127.0.0.1:5000
echo 🔒 Running in stable mode (no auto-reload)
echo 💡 Press Ctrl+C to stop the server
echo.

REM Try multiple server configurations in order of preference
echo ⚡ Attempting to start stable development server...
python run_dev_server.py --no-reload --host 127.0.0.1 --port 5000

if errorlevel 1 (
    echo.
    echo ❌ Development server failed. Trying app.py with no-reload...
    echo.
    python app.py --no-reload
)

if errorlevel 1 (
    echo.
    echo ❌ Flask server failed. Trying production server...
    echo.
    python run_prod_server.py --host 127.0.0.1 --port 5000
)

echo.
echo 🛑 Server stopped
pause
