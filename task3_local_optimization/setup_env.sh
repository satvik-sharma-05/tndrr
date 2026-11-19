#!/bin/bash
# Setup script for Task 3 - Local Model Optimization
echo "========================================"
echo "Setting up Task 3 Environment"
echo "========================================"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv_task3

# Activate and install dependencies
echo "Installing dependencies..."
source venv_task3/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Task 3 environment setup complete!"
echo "========================================"
echo ""
echo "To activate: source venv_task3/bin/activate"
echo "To deactivate: deactivate"
