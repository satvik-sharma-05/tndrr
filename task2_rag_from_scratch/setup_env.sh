#!/bin/bash
# Setup script for Task 2 - RAG from Scratch
echo "========================================"
echo "Setting up Task 2 Environment"
echo "========================================"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv_task2

# Activate and install dependencies
echo "Installing dependencies..."
source venv_task2/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Task 2 environment setup complete!"
echo "========================================"
echo ""
echo "To activate: source venv_task2/bin/activate"
echo "To deactivate: deactivate"
