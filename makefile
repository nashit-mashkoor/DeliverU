# DeliverU Makefile

.PHONY: help format lint dev test migrate build-backend build-frontend up-backend up-frontend up down logs

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Backend Commands
# =============================================================================

backend-format: ## Format backend code with ruff
	cd backend && uv run ruff format .
	cd backend && uv run ruff check --select I --fix .

backend-lint: ## Run backend linting and type checking
	cd backend && uv run ruff check .
	cd backend && uv run ruff format . --diff
	cd backend && uv run mypy .

backend-dev: ## Start backend development server
	cd backend && uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8504

backend-migrate: ## Run database migrations
	cd backend && uv run alembic upgrade head

backend-migration: ## Create a new migration (usage: make backend-migration msg="migration message")
	cd backend && uv run alembic revision --autogenerate -m "$(msg)"

backend-test: ## Run backend tests
	cd backend && uv run pytest -v

backend-test-cov: ## Run backend tests with coverage
	cd backend && uv run pytest --cov=backend --cov-report=html

backend-install: ## Install backend dependencies
	cd backend && uv sync

backend-build: ## Build backend Docker image
	docker compose build app worker

backend-up: ## Start backend services only
	docker compose up -d redis postgres pgbouncer minio minio-init app worker

# =============================================================================
# Frontend Commands
# =============================================================================

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

frontend-dev: ## Start frontend development server
	cd frontend && npm run dev

frontend-build: ## Build frontend Docker image
	docker compose build frontend

frontend-up: ## Start frontend service only
	docker compose up -d frontend

# =============================================================================
# Full Stack Commands
# =============================================================================

format: backend-format ## Format all code
lint: backend-lint ## Lint all code
dev: backend-dev ## Start development servers (backend only, use frontend-dev separately)

migrate: backend-migrate ## Run database migrations
migration: backend-migration ## Create a new migration (usage: make migration msg="message")
test: backend-test ## Run all tests
test-cov: backend-test-cov ## Run tests with coverage

install: backend-install frontend-install ## Install all dependencies

build: backend-build frontend-build ## Build all Docker images
build-backend: backend-build ## Build backend Docker images
build-frontend: frontend-build ## Build frontend Docker image

up: ## Start all services
	docker compose up -d

up-backend: backend-up ## Start backend services only
up-frontend: frontend-up ## Start frontend service only

down: ## Stop all services
	docker compose down

logs: ## View all logs
	docker compose logs -f

logs-backend: ## View backend logs
	docker compose logs -f app worker

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

# =============================================================================
# Setup
# =============================================================================

setup: ## Initial project setup
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
	fi
	cd backend && uv sync
	cd frontend && npm install
	@echo "Setup complete! Edit .env with your settings, then run 'make up' to start services."
