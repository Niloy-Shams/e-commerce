# Customizable E-Commerce Platform

Full spec: [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md).

## Stack

- **Frontend:** Next.js (App Router) + TypeScript + Tailwind CSS + Zustand
- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** PostgreSQL
- **Local dev:** Docker Compose

## Quick start

```bash
# 1. Clone and enter the repo
git clone https://github.com/CUET-Synesis-IT/ecommerce_project.git
cd ecommerce_project

# 2. Set up environment files (defaults work out of the box for Docker)
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 3. Start everything with Docker Compose
docker compose up --build
```

Then open:

- Frontend: <http://localhost:3000>
- Backend Swagger docs: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/v1/health>

Stop with `Ctrl+C`, or `docker compose down` to also remove containers
(add `-v` to also wipe the database volume).

### Frontend API URL

`frontend/.env.local` defaults to `http://backend:8000/api/v1` so the Next.js
container can reach the FastAPI container via Docker service name.
For local development outside Docker, override it to `http://localhost:8000/api/v1`.

## Running without Docker (optional)

**Backend:**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# point DATABASE_URL at localhost instead of "db" in backend/.env
uvicorn app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Database migrations (Alembic)

```bash
cd backend
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Run this inside the backend container (`docker compose exec backend alembic ...`)
or locally with `DATABASE_URL` pointed at `localhost`.

## Tests

```bash
cd backend
pytest
```

## Project structure

```text
backend/app/
  core/        - settings, security (hashing/JWT), shared dependencies
  db/          - SQLAlchemy engine/session, declarative Base
  models/      - SQLAlchemy models
  schemas/     - Pydantic request/response schemas
  api/v1/      - versioned routers (health check implemented, rest are stubs)
  services/    - business logic
frontend/
  app/         - Next.js App Router pages
  components/  - shared UI components
  lib/         - API client, auth helper, utils
  store/       - Zustand stores (cart)
  types/       - shared TypeScript types
```

## Current status

Phase 1 (scaffolding) complete:
- Docker Compose with PostgreSQL, FastAPI backend, and Next.js frontend
- Environment configuration for Docker and local development
- FastAPI app with CORS and `/api/v1/health` endpoint
- Next.js app with Tailwind CSS, TypeScript, and Zustand
- SQLAlchemy models for all entities with plan-complete field coverage:
  - `User` (UUID PK, email unique, password_hash, CUSTOMER/ADMIN role)
  - `Category` (name unique, description)
  - `Product` (Numeric price, stock with CHECK constraints, category FK, is_featured)
  - `Order` (status enum, shipping fields, **expires_at** for pending-order expiry)
  - `OrderItem` (snapshots product price at purchase time)
  - `StoreSettings` (**whatsapp_number** with E.164 validation, **singleton_key** unique constraint)
- Alembic migrations configured; model registry fixed to avoid circular imports
- Pydantic schemas implemented for `StoreSettings` and `Order` with validation
- Backend tests pass (`pytest`): 12 tests covering model metadata and schema validation

Everything under `TODO` comments — auth endpoints, product/category/order APIs,
services, and all customer/admin UI — is intentionally unimplemented
scaffolding. Follow `IMPLEMENTATION_PLAN.md` section 45 (Implementation
Sequence) and section 43 (Git strategy) for what to build next and how to
branch it.

## Git workflow

Branch off `develop`, one feature per branch (`feature/auth`, `feature/products`,
etc.), open a PR back into `develop`, and merge into `main` only for releases.
Don't commit directly to `main`. See `IMPLEMENTATION_PLAN.md` section 43 for
the full branching model and commit message convention.
