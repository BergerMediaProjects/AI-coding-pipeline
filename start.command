#!/bin/bash
# Double-click to start the AI Pipeline web interface (Mac)
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found."
    echo "Please run setup first: open Terminal, cd to this folder, and run: bash scripts/setup.sh"
    echo "Or install Docker and run: docker-compose up"
    read -p "Press Enter to close..."
    exit 1
fi

open http://127.0.0.1:5001
source .venv/bin/activate
exec python web_interface/app.py
