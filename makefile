# DeliverU Makefile

.PHONY: infra infra-storage all down dev-backend dev-frontend migrate migration

infra:
	docker compose --profile infra up -d

infra-storage:
	docker compose --profile infra --profile storage up -d

all:
	docker compose --profile infra --profile storage --profile app --profile worker --profile web up -d

down:
	docker compose down

dev-backend:
	cd backend && \
	set -a && . ../.env && set +a && \
	DATABASE_URL=postgresql+asyncpg://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@localhost:5432/$${POSTGRES_DB} \
	REDIS_HOST=localhost \
	REDIS_URL=redis://:$${REDIS_PASSWORD}@localhost:$${REDIS_PORT} \
	MINIO_ENDPOINT=localhost:9000 \
	uv run alembic upgrade head && \
	DATABASE_URL=postgresql+asyncpg://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@localhost:5432/$${POSTGRES_DB} \
	REDIS_HOST=localhost \
	REDIS_URL=redis://:$${REDIS_PASSWORD}@localhost:$${REDIS_PORT} \
	MINIO_ENDPOINT=localhost:9000 \
	uv run uvicorn backend.main:app --host 0.0.0.0 --port 8504 --reload

migrate:
	cd backend && \
	set -a && . ../.env && set +a && \
	DATABASE_URL=postgresql+asyncpg://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@localhost:5432/$${POSTGRES_DB} \
	REDIS_HOST=localhost \
	REDIS_URL=redis://:$${REDIS_PASSWORD}@localhost:$${REDIS_PORT} \
	MINIO_ENDPOINT=localhost:9000 \
	uv run alembic upgrade head

migration:
	cd backend && \
	set -a && . ../.env && set +a && \
	DATABASE_URL=postgresql+asyncpg://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@localhost:5432/$${POSTGRES_DB} \
	REDIS_HOST=localhost \
	REDIS_URL=redis://:$${REDIS_PASSWORD}@localhost:$${REDIS_PORT} \
	MINIO_ENDPOINT=localhost:9000 \
	uv run alembic revision --autogenerate -m "$(msg)"

dev-frontend:
	cd frontend && VITE_API_URL=http://localhost:8504 npm run dev
