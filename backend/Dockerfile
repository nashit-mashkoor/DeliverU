# Stage 1: Builder
FROM python:3.12-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc g++ make \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY uv.lock pyproject.toml /app/

COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/

RUN uv sync --no-group dev

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /bin/uvx /bin/uvx

COPY start.sh /app/scripts/start.sh

RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app/scripts && \
    chmod +x /app/scripts/start.sh

USER root

COPY . /app/backend/
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

RUN chown -R appuser:appuser /app/backend /app/alembic.ini /app/alembic && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app/logs

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8504 \
    PYTHONPATH="/app" \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 8504

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8504/health || exit 1

CMD ["/app/scripts/start.sh"]

