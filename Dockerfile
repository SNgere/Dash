# Builder stage
FROM python:3.13-slim AS builder

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only dependency files first to leverage caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install application
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Clean up unnecessary files to reduce image size
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true \
    && find /app -type f -name "*.pyc" -delete \
    && find /app -type f -name "*.pyo" -delete \
    && find /app -type f -name ".DS_Store" -delete \
    && find /app -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Final stage
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Create non-root user for security
RUN addgroup --system --gid 1001 appuser \
    && adduser --system --uid 1001 --gid 1001 --disabled-password appuser

# Set working directory
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder --chown=appuser:appuser /app /app

# Switch to non-root user
USER appuser

# Run the dash application by default
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]


