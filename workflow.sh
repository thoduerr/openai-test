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
log "Executing agent.py with arguments: $1"

# python3 agent.py workflow-test manager
python3 agent.py $1 architect
python3 agent.py $1 programmer
python3 agent.py $1 quality
python3 agent.py $1 programmer
python3 agent.py $1 quality
python3 agent.py $1 programmer

log "Script completed successfully."

new_filename="topic_$1/$(date '+%Y-%m-%d-%H%M%S')_last_answer.md"
mv topic_$1/last_answer.md $new_filename
log "Renamed: topic_$1/last_answer.md to $new_filename"