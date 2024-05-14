#!/bin/bash

# Function to log messages with timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $@"
}

# Function to check if a command exists
ensure_command() {
    command -v "$1" >/dev/null 2>&1 || { log "Error: $1 is not installed"; exit 1; }
}

# Main script starts here
log "Starting script..."

# Check for Python installation
ensure_command python3

# Check if main.py exists
if [ ! -f "agent.py" ]; then
    log "Error: agent.py does not exist in the current directory"
    exit 1
fi

# Run the Python script with all passed arguments
log "Executing agent.py with arguments: $@"
python3 agent.py "$@" || { log "Error: agent.py failed to execute"; exit 1; }

log "Script completed successfully."