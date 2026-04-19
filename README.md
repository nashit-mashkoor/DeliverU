# DeliverU - Full-Stack Delivery Platform

DeliverU is a production-ready full-stack delivery platform with a FastAPI backend, React frontend, and containerized infrastructure.

## Features

- 🚀 **FastAPI Backend** - Async Python web framework
- ⚛️ **React Frontend** - Vite-powered with React Router
- 🔐 **JWT Authentication** - Access & refresh tokens
- 🗄️ **PostgreSQL** - Primary database with SQLModel ORM
- 📦 **Redis** - Caching and background job broker
- 💾 **MinIO** - S3-compatible object storage
- 🔄 **TaskIQ** - Background job processing
- 🐳 **Docker** - Full containerization with compose
- 📝 **Alembic** - Database migrations

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ with uv
- Node.js 20+ (for frontend development)

### Setup

1. Clone and enter the project:
   ```bash
   cd DeliverU
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   # Edit values if needed
   ```

3. Start all services:
   ```bash
   make all
   # or: make infra   (infra only)
   ```

4. Access the application:
   - Frontend: http://localhost:8503
   - Backend API: http://localhost:8504
   - API Docs: http://localhost:8504/docs (admin/password)
   - MinIO Console: http://localhost:9001 (minioadmin/minioadmin)

## Development

### Backend Development

```bash
# Install dependencies
uv sync

# Start development server
make dev-backend

# Use a specific env file
ENV_FILE=.env.dev make dev-backend

# Run linting
make lint

# Format code
make format
```

### Database Migrations

```bash
# Create a new migration
make migration msg="Add new table"

# Apply migrations
make migrate

# Seed one complete dev bootstrap set
make seed
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Environment Files

- Use a single env file: `.env` (copy from `.env.example`).
- Update all variables in `.env` as your single source of truth.
- Local app commands use `DATABASE_URL`, `REDIS_URL`, `MINIO_ENDPOINT`.
- Docker app/worker use `DOCKER_DATABASE_URL`, `DOCKER_REDIS_URL`, `DOCKER_MINIO_ENDPOINT` from the same `.env`.
- PgBouncer uses `PGBOUNCER_DATABASE_URL` from the same `.env`.
- You can still override with `ENV_FILE=/path/to/file` for any Make target.
- Seed defaults can be overridden with env vars such as `SEED_ADMIN_EMAIL`, `SEED_CUSTOMER_EMAIL`, `SEED_DRIVER_EMAIL`, and `SEED_DEFAULT_PASSWORD`.

## Project Structure

```
deliveru/
├── backend/                  # Backend application
│   ├── main.py              # FastAPI entry point
│   ├── constants.py         # Configuration
│   ├── database/            # Database layer
│   │   ├── models.py        # SQLModel models
│   │   ├── crud.py          # Base CRUD operations
│   │   └── seed.py          # Dev seed bootstrap script
│   ├── modules/             # Feature modules
│   │   ├── auth/            # Authentication
│   │   ├── items/           # Legacy sample module (kept inactive during migration)
│   │   └── jobs/            # Background jobs
│   ├── services/            # Shared and runtime services
│   │   ├── auth.py          # Authentication helpers
│   │   └── runtime/         # Broker and Redis runtime clients
│   ├── utils/               # Utilities
│   ├── alembic/            # Database migrations
│   ├── alembic.ini          # Alembic configuration
│   ├── Dockerfile           # Backend container
│   ├── pyproject.toml        # Python dependencies
│   └── uv.lock              # Locked dependencies
├── frontend/                # React frontend
│   ├── src/
│   │   ├── services/        # API services
│   │   ├── context/         # React contexts
│   │   ├── components/      # UI components
│   │   └── pages/           # Page components
│   ├── Dockerfile           # Frontend container
│   └── nginx.conf           # Nginx configuration
├── docker-compose.yml       # Infrastructure
├── makefile                 # Build and deployment commands
└── scripts/
    ├── seed.sh              # DB seed wrapper script
    └── restart.sh          # Quick restart script
```

## Frontend Design System

The frontend follows the Neon Control Room visual system described in `docs/design.md`. Keep additions aligned to the shared typography, color, motion, and component rules so the landing page and authenticated app remain cohesive.

## Adding New Features

### Adding a New Module

1. Create module directory: `backend/modules/myfeature/`
2. Add files following the pattern:
   - `__init__.py`
   - `myfeature_dto.py` - Request/Response models
   - `myfeature_service.py` - Business logic
   - `myfeature_controller.py` - API endpoints
3. Register router in `backend/main.py`
4. Add database models if needed in `backend/database/models.py`
5. Create migration: `make migration msg="Add myfeature"`

### Adding Background Jobs

1. Add job function in `backend/modules/jobs/`
2. Use `@broker.task()` decorator
3. Call with `await my_task.kiq(args...)`

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT
