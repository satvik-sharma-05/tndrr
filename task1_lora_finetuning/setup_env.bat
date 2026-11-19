@echo off
REM Setup script for Task 1 - LoRA Fine-tuning
echo ========================================
echo Setting up Task 1 Environment
echo ========================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv_task1

REM Activate and install dependencies
echo Installing dependencies...
call venv_task1\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Task 1 environment setup complete!
echo ========================================
echo.
echo To activate: call venv_task1\Scripts\activate.bat
echo To deactivate: deactivate
