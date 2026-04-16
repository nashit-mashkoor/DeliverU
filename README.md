# MyApp - Full-Stack Platform Template

A production-ready full-stack platform template with FastAPI backend, React frontend, and containerized infrastructure.

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
   cd template-app
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start all services:
   ```bash
   make up
   # or: docker compose up -d
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
make dev

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
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
deliveru/
├── backend/                  # Backend application
│   ├── main.py              # FastAPI entry point
│   ├── constants.py         # Configuration
│   ├── broker.py            # TaskIQ broker
│   ├── database/            # Database layer
│   │   ├── models.py        # SQLModel models
│   │   └── crud.py          # Base CRUD operations
│   ├── modules/             # Feature modules
│   │   ├── auth/            # Authentication
│   │   ├── items/           # Example CRUD module
│   │   └── jobs/            # Background jobs
│   ├── services/            # Shared services
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
└── restart.sh              # Quick restart script
```

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

