#!/bin/sh
set -e

echo "Running Alembic migrations..."
if ! uv run alembic upgrade head; then
    echo "ERROR: Alembic migrations failed!"
    exit 1
fi

echo "Ensuring database tables exist..."
if ! uv run python -c "import asyncio; from backend.database.crud import init_models; asyncio.run(init_models())"; then
    echo "ERROR: Database initialization failed!"
    exit 1
fi

echo "Migrations completed successfully."
echo "Starting MyApp application server..."
exec uv run uvicorn backend.main:app --host 0.0.0.0 --port 8504 --workers 4
