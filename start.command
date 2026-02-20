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

source .venv/bin/activate
echo "Starting web server at http://127.0.0.1:5001"
echo "(Browser will open automatically. Press Ctrl+C to stop the server.)"
# Open browser after 2 seconds (gives server time to start)
(sleep 2 && open http://127.0.0.1:5001) &
python web_interface/app.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Server stopped. Check the error above."
    read -p "Press Enter to close..."
    exit 1
fi
