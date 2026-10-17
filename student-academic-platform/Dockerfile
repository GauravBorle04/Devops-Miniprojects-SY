# Base operating environment: official lightweight Python 3.11 slim image
FROM python:3.11-slim

# Environment variables for optimized container execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Dedicated application directory
WORKDIR /app

# Install curl (needed by the HEALTHCHECK) and clean apt caches
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Layer caching: copy only requirements first to optimize rebuild times
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project source code into the container
COPY . .

# Security best practice: run the application as a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose internal application port
EXPOSE 5000

# Healthcheck probe to monitor container health
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Launch the application
CMD ["python", "run.py"]
