#!/bin/sh
set -e

echo "Running Alembic migrations..."
max_attempts=20
attempt=1

until uv run alembic upgrade head; do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "ERROR: Alembic migrations failed after ${max_attempts} attempts!"
        exit 1
    fi

    echo "Migration attempt ${attempt} failed, retrying in 3 seconds..."
    attempt=$((attempt + 1))
    sleep 3
done

echo "Migrations completed successfully."
echo "Starting DeliverU application server..."
exec uv run uvicorn backend.main:app --host 0.0.0.0 --port 8504 --workers 4
