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

### First-run database initialization

The first time you start the backend, create the database tables:

```bash
docker compose exec backend python -c "
from app.db.base import Base
from app.db.session import engine
from app.models import user, category, product, order, order_item, store_settings
Base.metadata.create_all(bind=engine)
print('Tables created')
"
```

### Creating an admin user

Public registration only creates `CUSTOMER` accounts. To access admin endpoints,
create an admin user with the seed script:

```bash
docker compose exec backend python scripts/seed.py
```

Default admin credentials:
- Email: `admin@example.com`
- Password: `admin123`

### Accessing admin endpoints in Swagger UI

1. Open `/docs`
2. Call `POST /auth/login` with the admin credentials.
   This sets an httpOnly cookie automatically.
3. Call `GET /admin/customers` or other admin endpoints.
   The cookie is sent automatically by the browser.

If you see `401`, refresh `/docs` and log in again.

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
  api/v1/      - versioned routers
  services/    - business logic
frontend/
  app/         - Next.js App Router pages
  components/  - shared UI components
  lib/         - API client, auth helper, utils
  store/       - Zustand stores (cart)
  types/       - shared TypeScript types
```

## Implemented backend APIs

The backend exposes the following `/api/v1` endpoints:

- `GET /health` — health check
- `POST /auth/register` — register a customer account
- `POST /auth/login` — login and receive JWT + httpOnly cookie
- `GET /auth/me` — get current authenticated user
- `GET /categories` — list categories (public)
- `GET /categories/{id}` — get category (public)
- `POST /categories` — create category (admin)
- `PUT /categories/{id}` — update category (admin)
- `DELETE /categories/{id}` — delete category (admin, blocked if products exist)
- `GET /products` — list products with search, filter, sort, pagination (public)
- `GET /products/{id}` — get product (public)
- `POST /products` — create product (admin)
- `PUT /products/{id}` — update product (admin)
- `DELETE /products/{id}` — delete product (admin)
- `POST /orders` — create order with transactional stock protection (customer)
- `GET /orders` — list own orders (customer)
- `GET /orders/{id}` — get own order (customer)
- `GET /admin/orders` — list all orders (admin)
- `GET /admin/orders/{id}` — get any order (admin)
- `PATCH /admin/orders/{id}/status` — update order status with state-machine validation (admin)
- `GET /admin/customers` — list all customers (admin)
- `GET /admin/customers/{id}` — get customer details (admin)
- `PUT /admin/store/settings` — update store settings (admin)
- `GET /store/settings` — get public store settings (public)

## Key backend features

- JWT authentication with httpOnly, SameSite=Strict cookies
- CSRF protection via double-submit cookie pattern (`GET /auth/csrf` + `X-CSRF-Token` header)
- Role-based authorization (`CUSTOMER` / `ADMIN`)
- Password hashing with bcrypt
- Order creation with `FOR UPDATE` row-level locking to prevent overselling
- Order status state machine with terminal states
- Automatic stock restoration on cancellation
- Store settings singleton with default fallback
- WhatsApp number E.164 validation
- Pagination with enforced bounds
- Backend tests: 67 passing

## Authentication and authorization

The backend uses **JWT tokens stored in httpOnly cookies** to avoid XSS risks from
`localStorage`/`sessionStorage`.

### Auth endpoints

- `GET /auth/csrf` — fetch a CSRF token (sets a non-httponly `csrf_token` cookie)
- `POST /auth/register` — register a `CUSTOMER` account
- `POST /auth/login` — login and receive JWT + httpOnly cookie
- `POST /auth/logout` — clear auth and CSRF cookies
- `GET /auth/me` — get current authenticated user

### CSRF flow

1. Call `GET /auth/csrf` to obtain a CSRF token and cookie.
2. Include the token in the `X-CSRF-Token` header for all state-changing requests
   (`POST`, `PUT`, `PATCH`, `DELETE`).
3. The backend validates that the header value matches the `csrf_token` cookie.

### Authorization rules

| Action | Guest | Customer | Admin |
|---|---:|---:|---:|
| Browse products | Yes | Yes | Yes |
| Search products | Yes | Yes | Yes |
| Place order | No | Yes | Yes |
| View own orders | No | Yes | Yes |
| Manage products | No | No | Yes |
| Manage categories | No | No | Yes |
| Manage orders | No | No | Yes |
| Manage store settings | No | No | Yes |
| View customers | No | No | Yes |

Reusable backend dependencies: `get_current_user()`, `require_customer()`, `require_admin()`.

## Current status

- Backend API specification, authentication, order, and admin APIs implemented
- All backend tests pass (`pytest`: 67 passed)
- Frontend UI remains to be built

## Git workflow

Branch off `develop`, one feature per branch (`feature/auth`, `feature/products`,
etc.), open a PR back into `develop`, and merge into `main` only for releases.
Don't commit directly to `main`. See `IMPLEMENTATION_PLAN.md` section 43 for
the full branching model and commit message convention.
