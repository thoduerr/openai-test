# OpenAI Test

This project is a small Python application designed to interact with the OpenAI API. It facilitates the simulation of conversations by allowing users to define and switch roles easily. Each chat session is saved, enabling users to continue conversations seamlessly in subsequent sessions.

The application is particularly useful for developers and researchers who wish to test and explore the capabilities of the OpenAI API in generating text-based responses within predefined contexts. By setting up different roles, users can create diverse scenarios to better understand how the AI models respond to various conversational cues.

## Important Notice

To use this application, you must have an active OpenAI account with API access enabled. OpenAI requires a valid payment method to be linked to your account and a minimum balance of $5 to start using the API services. This setup ensures that you can make API requests without interruption during your testing and development activities.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a Linux or macOS machine. (Windows users might need to adjust scripts or use WSL.)
- You have installed Python 3.12.
- You have installed Bash (usually pre-installed on Linux and macOS).

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/thoduerr/openai-test
cd openai-test
```

To set up the project environment, run the following script:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "OPENAI_API_KEY=<your_api_key>" > .env
```

```bash
./setup.py && source .venv/bin/activate
```

This script will:

- Check if Python 3 is installed.
- Set up a Python virtual environment.
- Install required Python packages from `requirements.txt`.

Cleanup:

```bash
deactivate
rm -r .venv/
```

## Usage

To run the main application, use the following command:

```bash
./chat.sh <topic> <role>
```

Where:

- `<topic>` is the topic of the chat.
- `<role>` is the role you are simulating in the chat.

## Development

Ensure only required dependencies are saved.

```bash
pip3 install pipreqs
pipreqs . --ignore bin,etc,include,lib,lib64 --force
```
