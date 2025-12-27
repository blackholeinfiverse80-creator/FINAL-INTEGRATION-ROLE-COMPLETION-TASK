# Core Integrator Dockerfile
# Multi-stage build for production deployment

FROM python:3.14-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional runtime dependencies
RUN pip install --no-cache-dir \
    flask==3.1.2 \
    flask-sqlalchemy==3.1.1 \
    sentence-transformers==5.2.0 \
    scipy==1.16.3 \
    requests==2.32.5

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p db data reports logs htmlcov

# Set environment variables
ENV PYTHONPATH=/app
ENV INTEGRATOR_USE_NOOPUR=true
ENV NOOPUR_BASE_URL=http://noopur:5001
ENV DB_PATH=db/context.db
ENV NONCE_DB_PATH=db/nonce_store.db

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash integrator
RUN chown -R integrator:integrator /app
USER integrator

# Expose ports
EXPOSE 8000 5002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5002/system/health || exit 1

# Default command
CMD ["python", "main.py"]