# Use Python 3.12 slim image
FROM python:3.12.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (dev extras include flake8 for `make lint`)
COPY requirements.txt requirements-dev.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copy project
COPY . /usr/src/app/

# Create dirs the app writes to and make entrypoint executable
RUN mkdir -p /usr/src/app/staticfiles /usr/src/app/logs \
    && chmod +x /usr/src/app/docker/entrypoint.sh

# Run as a non-root user
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/bash --create-home app \
    && chown -R app:app /usr/src/app
USER app

# Expose port
EXPOSE 8000

# run the application with ASGI (async)
ENTRYPOINT ["/usr/src/app/docker/entrypoint.sh"]
