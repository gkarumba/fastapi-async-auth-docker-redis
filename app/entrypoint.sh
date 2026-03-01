#!/bin/sh
set -e

# Wait for MySQL
./wait-for-it.sh db:3306 --timeout=60 --strict -- echo "MySQL is up"

# Wait for Redis
./wait-for-it.sh redis:6379 --timeout=60 --strict -- echo "Redis is up"

# Run Alembic migrations
alembic upgrade head

# Start FastAPI
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload