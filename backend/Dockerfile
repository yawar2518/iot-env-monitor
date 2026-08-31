# =============================================================
# IoT Environmental Monitoring — Django Backend
# =============================================================
# Build stage: installs dependencies
# Runtime: runs Daphne ASGI server
# =============================================================

FROM python:3.12-slim

# -------------------------------------------------------------
# Environment — Python behaviour inside container
# -------------------------------------------------------------

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Flush stdout/stderr immediately — critical for Docker log visibility
ENV PYTHONUNBUFFERED=1

# -------------------------------------------------------------
# System dependencies
# -------------------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required to compile psycopg2 C extensions
    libpq-dev \
    gcc \
    # Network debugging utilities — useful during development
    curl \
    # Clean up apt cache to keep image small
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------
# Working directory
# -------------------------------------------------------------

WORKDIR /app

# -------------------------------------------------------------
# Python dependencies
# Install requirements BEFORE copying application code.
# This caches the pip install layer separately from code changes.
# -------------------------------------------------------------

COPY requirements/ requirements/

# Install local requirements (includes base.txt via -r base.txt)
RUN pip install --upgrade pip && \
    pip install -r requirements/local.txt

# -------------------------------------------------------------
# Application code
# Copied last so code changes don't invalidate dependency cache.
# In development this layer is overridden by the volume mount in
# docker-compose.yml — changes are reflected instantly without rebuild.
# -------------------------------------------------------------

COPY . .

# -------------------------------------------------------------
# Non-root user — security best practice
# -------------------------------------------------------------

RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

# -------------------------------------------------------------
# Port
# -------------------------------------------------------------

EXPOSE 8000

# -------------------------------------------------------------
# Default command
# Overridden by docker-compose.yml for each service (django,
# celery worker, celery beat, mqtt_subscriber all use the same
# image but different commands).
# -------------------------------------------------------------

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]