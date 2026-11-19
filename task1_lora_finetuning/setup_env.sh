#!/bin/bash
# Setup script for Task 1 - LoRA Fine-tuning
echo "========================================"
echo "Setting up Task 1 Environment"
echo "========================================"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv_task1

# Activate and install dependencies
echo "Installing dependencies..."
source venv_task1/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Task 1 environment setup complete!"
echo "========================================"
echo ""
echo "To activate: source venv_task1/bin/activate"
echo "To deactivate: deactivate"
