#!/bin/bash

# Terminate script on first error
set -e

echo "Initializing environment setup for macOS/Linux..."

# Check for python3 availability
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 command not found. Ensure Python 3.9+ is installed."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment: venv"
fi

# Activate and update package manager
source venv/bin/activate
python3 -m pip install --upgrade pip

# Install dependencies from manifest
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies successfully installed."
else
    echo "Warning: requirements.txt not detected. Skipping installation."
fi

echo "Setup finalized. Activate the environment with: source venv/bin/activate"