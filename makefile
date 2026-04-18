# DeliverU Makefile

.PHONY: infra infra-storage all down dev-backend dev-frontend migrate migration free-ports

ENV_FILE ?= .env
ENV_FILE_PATH := $(abspath $(ENV_FILE))
FREE_PORTS ?= 8504 8503 5432 6379 9000 9001 6432

infra:
	docker compose --env-file $(ENV_FILE_PATH) --profile infra up -d

infra-storage:
	docker compose --env-file $(ENV_FILE_PATH) --profile infra --profile storage up -d

all:
	docker compose --env-file $(ENV_FILE_PATH) --profile infra --profile storage --profile app --profile worker --profile web up -d --build

down:
	docker compose --env-file $(ENV_FILE_PATH) down

free-ports:
	@docker stop deliveru-app deliveru-frontend deliveru-worker deliveru-pgbouncer deliveru-postgres deliveru-minio deliveru-redis 2>/dev/null || true
	@fuser -k -n tcp $(FREE_PORTS) 2>/dev/null || true

dev-backend:
	cd backend && \
	set -a && . "$(ENV_FILE_PATH)" && set +a && \
	if [ "$$RUN_MIGRATIONS" = "1" ]; then \
		PYTHONPATH=$${PYTHONPATH:-..} uv run alembic upgrade head; \
	fi && \
	PYTHONPATH=$${PYTHONPATH:-..} uv run uvicorn backend.main:app --host 0.0.0.0 --port $${BACKEND_PORT:-8504} --reload

migrate:
	cd backend && \
	set -a && . "$(ENV_FILE_PATH)" && set +a && \
	PYTHONPATH=$${PYTHONPATH:-..} uv run alembic upgrade head

migration:
	cd backend && \
	set -a && . "$(ENV_FILE_PATH)" && set +a && \
	PYTHONPATH=$${PYTHONPATH:-..} uv run alembic revision --autogenerate -m "$(msg)"

dev-frontend:
	cd frontend && \
	set -a && . "$(ENV_FILE_PATH)" && set +a && \
	npm run dev
