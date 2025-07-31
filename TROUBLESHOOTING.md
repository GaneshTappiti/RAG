# Flask Development Server Troubleshooting Guide

## Socket Error Solutions

The `OSError: [WinError 10038] An operation was attempted on something that is not a socket` error is common on Windows with Flask's development server. Here are several solutions:

## Quick Fixes

### 1. Use the New Development Server Script

```bash
# Use the robust development server
python run_dev_server.py

# Or use the Windows batch script
start_server.bat

# Or use PowerShell script
powershell -ExecutionPolicy Bypass -File start_server.ps1
```

### 2. Run with Different Configuration

```bash
# Disable auto-reload
python run_dev_server.py --no-reload

# Use different host
python run_dev_server.py --host localhost

# Use different port
python run_dev_server.py --port 5001
```

### 3. Manual Flask Configuration

```bash
# Set environment variables and run
set FLASK_ENV=development
set FLASK_DEBUG=0
python app.py
```

## Advanced Solutions

### 1. Kill Existing Processes

Sometimes the port is still in use:

```bash
# Windows Command Prompt
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# PowerShell
Get-NetTCPConnection -LocalPort 5000 | Stop-Process -Force
```

### 2. Use Production Server for Development

```bash
# Use Waitress instead of Flask dev server
python run_prod_server.py --host 127.0.0.1 --port 5000
```

### 3. Virtual Environment Issues

```bash
# Create fresh virtual environment
python -m venv fresh_venv
fresh_venv\Scripts\activate
pip install -r requirements.txt
python run_dev_server.py
```

## Common Causes

1. **File Watcher Issues**: Windows file system events can cause conflicts
2. **Port Conflicts**: Another process using port 5000
3. **Rapid Restarts**: Flask reloader starting before previous instance stops
4. **Virtual Environment**: Path or permission issues

## Prevention Tips

1. **Always stop server cleanly**: Use Ctrl+C instead of closing terminal
2. **Use localhost**: Prefer `127.0.0.1` over `0.0.0.0` on Windows
3. **Disable reload when needed**: Use `--no-reload` for testing
4. **Check ports**: Ensure port 5000 is available

## Environment Setup

### Required Environment Variables

```bash
# .env file
GOOGLE_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
```

### Verify Installation

```bash
# Check if all dependencies are installed
python -c "import flask, langchain_google_genai; print('All dependencies OK')"
```

## Alternative Development Methods

### 1. Use Docker (Recommended for Production)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run_prod_server.py"]
```

### 2. Use Streamlit Alternative

If Flask continues to have issues, the app includes Streamlit support:

```bash
streamlit run uiux_prompt_generator.py
```

## Still Having Issues?

1. **Check Python Version**: Ensure Python 3.8+ is installed
2. **Update Dependencies**: `pip install --upgrade flask werkzeug`
3. **Windows Defender**: Add project folder to exclusions
4. **Antivirus**: Temporarily disable real-time scanning
5. **Admin Rights**: Try running terminal as administrator

## Report Issues

If problems persist, please provide:

- Windows version
- Python version (`python --version`)
- Error log (full traceback)
- Virtual environment status
- Port availability (`netstat -an | findstr 5000`)
