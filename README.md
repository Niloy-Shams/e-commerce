# Customizable E-Commerce Platform

Full spec: [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md). This README covers
day-to-day setup only.

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

# 2. Set up environment files (defaults work out of the box for local dev)
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 3. Start everything
docker compose up --build
```

Then open:

- Frontend: <http://localhost:3000> (should show a green "Backend reachable" status)
- Backend Swagger docs: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/v1/health>

Stop everything with `Ctrl+C`, or `docker compose down` to also remove containers
(add `-v` to also wipe the database volume).

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
  models/      - SQLAlchemy models (implemented)
  schemas/     - Pydantic request/response schemas (TODO per feature)
  api/v1/      - versioned routers (health check implemented, rest are stubs)
  services/    - business logic (TODO per feature)
frontend/
  app/         - Next.js App Router pages
  components/  - shared UI components (TODO per feature)
  lib/         - API client, auth helper, utils
  store/       - Zustand stores (cart)
  types/       - shared TypeScript types
```

## Current status

Phase 1 (scaffolding) complete: Docker Compose, FastAPI + Next.js skeletons,
environment configuration, database models, and an end-to-end health check
(frontend calls backend calls confirms connectivity) all work.

Everything under `TODO` comments — auth, product/category/order endpoints,
schemas, services, and all customer/admin UI — is intentionally unimplemented
scaffolding. Follow `IMPLEMENTATION_PLAN.md` section 43 (Implementation
Sequence) and section 41 (Git strategy) for what to build next and how to
branch it.

## Git workflow

Branch off `develop`, one feature per branch (`feature/auth`, `feature/products`,
etc.), open a PR back into `develop`, and merge into `main` only for releases.
Don't commit directly to `main`. See `IMPLEMENTATION_PLAN.md` section 41 for
the full branching model and commit message convention.
