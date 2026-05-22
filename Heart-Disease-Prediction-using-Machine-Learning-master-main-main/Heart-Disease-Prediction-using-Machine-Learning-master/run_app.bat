@echo off
REM Navigate to the directory containing this batch file
cd /d "%~dp0"

REM Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found in current directory!
    echo Current directory: %CD%
    echo.
    echo Please make sure this batch file is in the same folder as app.py
    pause
    exit /b 1
)

echo Starting Streamlit app...
echo Current directory: %CD%
echo.

REM Run Streamlit using Python module (works even if streamlit command isn't recognized)
python -m streamlit run app.py

pause

