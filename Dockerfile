# =============================================================================
# SQL Practice Questions Platform - Dockerfile
# =============================================================================
# This Dockerfile builds a containerized environment for the SQL Practice 
# Questions Platform, enabling local generation of practice problems and 
# running the platform in an isolated environment.
# =============================================================================

# Use official Python 3.11 slim image as base
FROM python:3.11-slim

# Set metadata labels
LABEL maintainer="SQL Practice Platform Team"
LABEL description="SQL Practice Questions Platform - Generate and practice SQL queries"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    APP_HOME=/app

# Create application directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY infra/ ./infra/
COPY Questions/ ./Questions/
COPY SQl_answer.py .
COPY README.md .
COPY PRODUCT_ROADMAP.md .

# Create necessary directories
RUN mkdir -p output logs users

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser ${APP_HOME}

# Switch to non-root user
USER appuser

# Default command to generate data and run the platform
CMD ["python", "SQl_answer.py"]

# Expose volume mount points
VOLUME ["/app/output", "/app/logs", "/app/users", "/app/Questions"]

# =============================================================================
# Usage Examples:
# 
# Build the image:
#   docker build -t sql-practice-platform .
#
# Run with default settings:
#   docker run --rm sql-practice-platform
#
# Run interactively:
#   docker run -it --rm sql-practice-platform /bin/bash
#
# Run with persistent data:
#   docker run -v ./output:/app/output -v ./users:/app/users sql-practice-platform
#
# Generate data only:
#   docker run --rm sql-practice-platform python -m infra.DataGenerator
# =============================================================================
