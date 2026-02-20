#!/bin/bash
# Quick setup script for researchers
# Run from project root: bash scripts/setup.sh

set -e
echo "=== AI Pipeline Setup ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required. Install from https://www.python.org/downloads/"
    exit 1
fi

echo "Python: $(python3 --version)"

# Create virtual environment (recommended)
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
    echo "Please edit .env and add your OPENAI_API_KEY"
else
    echo ".env already exists"
fi

# Generate sample data if needed
if [ ! -f "data/training_data_sample.xlsx" ]; then
    echo "Generating sample data..."
    python scripts/generate_sample_data.py
fi

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  Run bash scripts/run_web.sh (or manually: source .venv/bin/activate then python web_interface/app.py)"
echo "  Open http://127.0.0.1:5001 in your browser"
echo "  Enter your OpenAI API key in the web form"
echo ""
