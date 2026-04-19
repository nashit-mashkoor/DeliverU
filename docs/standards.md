# DeliverU Coding Standards

This document defines the default coding conventions for the DeliverU backend.

## Core Principles

- Prefer explicit code over hidden behavior.
- Keep changes small and local to the owning module.
- Keep business rules out of generic helpers and model base classes.
- Use migration-driven schema changes only.

## Backend Structure

New backend modules should follow this shape:

```text
modules/<feature>/
  <feature>_controller.py
  <feature>_service.py
  <feature>_repository.py
  <feature>_dto.py
```

- `controller`: FastAPI routes, request parsing, response models, dependencies.
- `service`: business logic, authorization/resource checks, workflow, transaction ownership.
- `repository`: SQLModel queries and persistence only.
- `dto`: request and response schemas.

Shared infrastructure belongs in:

- `backend/database/`: models, session, seed, Alembic integration.
- `backend/services/security.py`: password hashing, JWT helpers, auth guards.

## Layer Rules

Controller rules:

- Do not query the database directly.
- Do not contain business logic.
- Pass the request-scoped session to the service.

Service rules:

- Own business rules and state transitions.
- Own `commit()` for write operations.
- Do not create database sessions directly.

Repository rules:

- Only interact with the database.
- Do not call `commit()` or `rollback()`.
- Do not raise `HTTPException` for business rules.

## Database Rules

- Use one request-scoped session from `get_db`.
- Pass the same session through `controller -> service -> repository`.
- New code should use explicit SQLModel queries in repositories.
- Do not add new usage of generic `EasyModel` CRUD helpers like `filter()` or `update_by_id()`.
- Keep list endpoints paginated in SQL, not in Python.
- Add deterministic ordering for list queries.

## Auth and Permissions

- Shared auth and JWT helpers live in `backend/services/security.py`.
- Module-specific auth flows live in `backend/modules/auth/`.
- Role checks can live in FastAPI dependencies.
- Resource ownership and business permission checks belong in the service layer.

## Error Handling

- Prefer domain errors for reusable business failures.
- Use `HTTPException` for request/authentication boundary failures.
- Do not hide failures inside generic helpers.

## Naming Conventions

- Use `*_controller.py`, `*_service.py`, `*_repository.py`, and `*_dto.py`.
- Keep repository methods explicit: `get_user_by_email`, `list_customer_orders`, `create_order`.
- Prefer action-based service methods: `place_order`, `change_password`, `deactivate_user`.

## Testing

- Add or update pytest coverage for every new endpoint or business flow.
- Prefer refactors that preserve existing behavior and tests.
- Run targeted tests for the touched module before finishing work.
