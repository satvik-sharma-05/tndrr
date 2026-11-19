@echo off
REM Setup script for Task 2 - RAG from Scratch
echo ========================================
echo Setting up Task 2 Environment
echo ========================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv_task2

REM Activate and install dependencies
echo Installing dependencies...
call venv_task2\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Task 2 environment setup complete!
echo ========================================
echo.
echo To activate: call venv_task2\Scripts\activate.bat
echo To deactivate: deactivate
