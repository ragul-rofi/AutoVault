# Use an official lightweight Python 3.12 image
FROM python:3.12-slim

# Set environment variables to optimize Python container execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Set working directory in container
WORKDIR /app

# Install system packages required for compiling potential C dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Create a non-privileged user and adjust permissions for security hardening
RUN useradd -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 5000 for the Flask backend
EXPOSE 5000

# Start Gunicorn WSGI server binding to all network interfaces on port 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
