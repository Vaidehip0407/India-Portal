FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Chrome for RPA
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    curl \
    wget \
    unzip \
    chromium \
    chromium-driver \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set display for headless Chrome
ENV DISPLAY=:99

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy RPA automation scripts
COPY ../rpa-automation /app/rpa-automation

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Create screenshots directory for RPA
RUN mkdir -p /tmp/dgvcl_screenshots

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
