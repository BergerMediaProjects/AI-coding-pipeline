FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create required directories
RUN mkdir -p data/results data/log data/temp_uploads

EXPOSE 5001

# Run the web interface (no API key required at startup - user enters in UI)
CMD ["python", "web_interface/app.py"]
