#!/bin/bash
# Run the web interface. Activates venv if needed.
# Usage: bash scripts/run_web.sh   OR   ./scripts/run_web.sh

cd "$(dirname "$(dirname "$(realpath "$0")")")"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run: bash scripts/setup.sh"
    exit 1
fi

# Activate venv and run
source .venv/bin/activate
exec python web_interface/app.py
