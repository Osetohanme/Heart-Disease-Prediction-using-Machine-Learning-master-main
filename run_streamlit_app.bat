@echo off
REM This batch file will find and run the Streamlit app from anywhere

echo ========================================
echo Starting Heart Disease Prediction App
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Navigate to the app directory
cd /d "%SCRIPT_DIR%Heart-Disease-Prediction-using-Machine-Learning-master"

REM Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo.
    echo Current directory: %CD%
    echo.
    echo Please make sure you're running this from the correct location.
    echo Expected location: Heart-Disease-Prediction-using-Machine-Learning-master\app.py
    pause
    exit /b 1
)

echo Found app.py in: %CD%
echo.
echo Starting Streamlit...
echo.

REM Run Streamlit using Python module
python -m streamlit run app.py

pause

