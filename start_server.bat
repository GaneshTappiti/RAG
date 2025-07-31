@echo off
REM Windows batch script to run the AI Tool Prompt Generator development server
REM This script helps avoid Flask socket errors on Windows

echo 🚀 AI Tool Prompt Generator - Development Server
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Using system Python.
    echo 💡 Consider creating a virtual environment: python -m venv .venv
    echo.
)

REM Check if required packages are installed
python -c "import flask" 2>NUL
if errorlevel 1 (
    echo ❌ Flask not found. Installing required packages...
    pip install flask python-dotenv langchain-google-genai
    if errorlevel 1 (
        echo ❌ Failed to install packages. Please check your internet connection.
        pause
        exit /b 1
    )
)

REM Set environment variables for better Windows compatibility
set FLASK_ENV=development
set FLASK_DEBUG=1
set PYTHONPATH=%CD%

echo 🔧 Environment configured
echo 🌐 Starting server on http://127.0.0.1:5000
echo 💡 Press Ctrl+C to stop the server
echo.

REM Run the server with error handling
python run_dev_server.py --host 127.0.0.1 --port 5000

if errorlevel 1 (
    echo.
    echo ❌ Server failed to start. Trying fallback...
    echo.
    python app.py
)

echo.
echo 🛑 Server stopped
pause
