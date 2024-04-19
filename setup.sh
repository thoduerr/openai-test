#!/bin/bash

# Function to log messages with timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function to check if a command exists
ensure_command() {
    command -v "$1" >/dev/null 2>&1 || { log "Error: $1 is not installed"; exit 1; }
}

# Main script starts here
log "Starting script..."

# Assign working directory from first argument or use current directory if none provided
WORKING_DIRECTORY="${1:-$(pwd)}"
log "Setting WORKING_DIRECTORY to: $WORKING_DIRECTORY"

# Change to the working directory
if [ ! -d "$WORKING_DIRECTORY" ]; then
    log "Error: Directory does not exist - $WORKING_DIRECTORY"
    exit 1
fi
cd "$WORKING_DIRECTORY" || { log "Error: Failed to change directory to $WORKING_DIRECTORY"; exit 1; }

# Uncomment to update git repository
# log "Checking out main branch and pulling latest changes"
# ensure_command git
# git checkout main || { log "Error: Failed to checkout main branch"; exit 1; }
# git pull || { log "Error: Failed to pull latest changes"; exit 1; }

# Setup Python environment
log "Setting up Python virtual environment"
ensure_command python3
python3 -m venv .venv || { log "Error: Failed to create virtual environment"; exit 1; }
source .venv/bin/activate || { log "Error: Failed to activate virtual environment"; exit 1; }
python3 -m pip install --upgrade pip || { log "Error: Failed to upgrade pip"; exit 1; }

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || { log "Error: Failed to install required packages"; exit 1; }
else
    log "No requirements.txt found, skipping package installation."
fi

log "Setup completed successfully!"
echo "To activate the virtual environment, run 'source .venv/bin/activate'"