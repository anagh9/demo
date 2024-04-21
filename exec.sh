#!/bin/bash

# Detect the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    VENV_DIR="venv"
    ACTIVATE_PATH="$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    VENV_DIR="venv"
    ACTIVATE_PATH="$VENV_DIR/bin/activate"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    VENV_DIR="venv"
    ACTIVATE_PATH="$VENV_DIR/Scripts/activate.bat"
else
    echo "Unsupported operating system"
    exit 1
fi

# Check if the virtual environment exists and delete it if it does
if [ -d "$VENV_DIR" ]; then
    echo "Deleting existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create a new virtual environment
echo "Creating a new virtual environment..."
python -m venv "$VENV_DIR"

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$ACTIVATE_PATH"

# Install dependencies (if needed)
# pip install -r requirements.txt

echo "Installing requirements..."
pip install -r requirements.txt


# Run the Django server
echo "Running Django server..."
python manage.py runserver
