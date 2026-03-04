# ---------------------------
# Builder Stage
# ---------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies (for mysqlclient, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv globally
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock /app/

# Sync → creates /app/.venv with everything (including alembic, uvicorn, etc.)
RUN uv sync --frozen --no-dev   # --no-dev usually wanted in prod

# Optional: if you want to install project editable in builder (for testing), but usually skip for prod

# ---------------------------
# Runtime Stage
# ---------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Important: activate venv by putting its bin first in PATH
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Runtime OS deps (mysql client lib + curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --system --group appuser

# Copy the virtual environment from builder (this brings alembic, uvicorn, etc.)
COPY --from=builder /app/.venv /app/.venv

# Copy application code (chown to non-root)
COPY --chown=appuser:appuser . /app

# Copy wait-for-it if it's not already in your repo root
# (assuming you have wait-for-it.sh in your project)
COPY --chown=appuser:appuser wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Your entrypoint
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]