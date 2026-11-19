@echo off
REM Setup script for Task 3 - Local Model Optimization
echo ========================================
echo Setting up Task 3 Environment
echo ========================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv_task3

REM Activate and install dependencies
echo Installing dependencies...
call venv_task3\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Task 3 environment setup complete!
echo ========================================
echo.
echo To activate: call venv_task3\Scripts\activate.bat
echo To deactivate: deactivate
