#!/bin/sh
set -e

# Wait for dependencies (your existing wait-for-it)
./wait-for-it.sh db:3306 --timeout=60 --strict -- echo "MySQL is up"
./wait-for-it.sh redis:6379 --timeout=60 --strict -- echo "Redis is up"

# Run migrations (now alembic is in PATH)
echo "Running Alembic migrations..."
alembic upgrade head

# Start server (direct call, no --reload in prod!)
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4   # adjust workers, log-config, etc.