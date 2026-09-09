# Customizable E-Commerce Management Platform
## Complete Implementation Plan for a 3-Week, 2-Person Industrial Attachment Project

**Project type:** Full-stack web application  
**Frontend:** Next.js + TypeScript + Tailwind CSS  
**Backend:** FastAPI + Python  
**Database:** PostgreSQL  
**ORM:** SQLAlchemy  
**Migrations:** Alembic  
**Authentication:** JWT  
**Containerization:** Docker / Docker Compose  
**Version control:** Git + GitHub

---

## 1. Purpose of This Document

This document is the implementation specification for a customizable e-commerce platform to be developed during a three-week industrial attachment by a two-person team.

It is intentionally written so that a coding agent such as Codex can use it as the project's working specification.

The implementation should prioritize:

1. A working end-to-end e-commerce flow.
2. Clean separation between frontend and backend.
3. Secure authentication and authorization.
4. A useful admin dashboard.
5. Store-level customization.
6. A manageable scope that can realistically be completed in three weeks.
7. Clean Git-based team collaboration.
8. Documentation and reproducible setup.

Do **not** expand the scope until the MVP is fully working.

---

# 2. Ambiguity Resolutions & Technical Risk Mitigations

This section resolves open questions and mitigates technical risks identified during planning. All implementers must follow these resolutions unless explicitly overridden.

## 2.1 Initial Admin Bootstrap

The public registration endpoint must **only** create `CUSTOMER` accounts. The first admin account must be created via the development seed script (`backend/scripts/seed.py`) or a one-time protected CLI command. Do **not** expose an admin registration endpoint. In production, the deployer must run the seed script once to create the initial admin.

## 2.2 StoreSettings Singleton Enforcement

Enforce singleton behavior at two layers:
1. **Database**: Add a unique check constraint ensuring only one row exists (e.g., a dummy unique column or a dedicated singleton table pattern).
2. **Service layer**: The `store.py` service must return a default configuration object if no record exists, and the admin update endpoint must create the row on first write.

## 2.3 Order Status State Machine

Define exact allowed transitions to prevent nonsensical state changes:

```text
PENDING  → CONFIRMED
PENDING  → CANCELLED
CONFIRMED → PROCESSING
PROCESSING → SHIPPED
SHIPPED → DELIVERED
CONFIRMED → CANCELLED
PROCESSING → CANCELLED
```

Any transition not in this graph must return `400 Bad Request`. `CANCELLED` and `DELIVERED` are terminal states. Once an order is `CANCELLED` or `DELIVERED`, no further status changes are permitted.

When transitioning to `CANCELLED` from any non-terminal state, the backend must restore reserved stock within the same transaction.

## 2.4 Featured Products Selection

Featured products are selected by admin via a boolean `is_featured` flag on the `Product` model. The homepage displays products where `is_featured = true`, limited to the first 8 ordered by creation date descending. No separate featured-products CRUD is required.

## 2.5 WhatsApp Number Format & Validation

Store the WhatsApp number in **E.164 format** without spaces or punctuation (e.g., `8801712345678`). Backend validation:
- Required field.
- Regex: `^\+?[1-9]\d{6,14}$` (allows optional leading `+`, then 7–15 digits, no leading zero after country code).
- Reject if the number is too short or contains non-digit characters (except optional leading `+`).

Frontend display may format the number for readability, but the stored and API-returned value must be the normalized E.164 form.

## 2.6 Pagination Defaults

- Default `limit`: `12`
- Maximum `limit`: `100`
- Minimum `page`: `1`
- If `page` or `limit` are out of bounds, return `422 Validation Error`.

## 2.7 Testing Frameworks

Use these exact frameworks to avoid ambiguity:
- **Backend**: `pytest` + `httpx` (async test client) + `pytest-asyncio`
- **Frontend**: `Vitest` + `@testing-library/react` + `@testing-library/jest-dom`
- **E2E**: Manual checklist (see Section 42); automated E2E is P2.

## 2.8 Image Upload Storage

For MVP, use **local filesystem storage** served from a dedicated `media/` directory inside the backend container. Docker Compose must mount a volume for `media/` so uploads persist across container restarts. Store only the relative path or filename in `image_url`. If uploads are implemented later, validate file type (`image/jpeg`, `image/png`, `image/webp`) and file size (max 2 MB). Never store binary images in PostgreSQL.

## 2.9 Next.js State Management

Use **Zustand** for client-side global state (cart, auth). Because the project uses Next.js App Router, all Zustand stores must be wrapped in `"use client"` directives. Do not use React Context for global state unless the state is truly local to a single component subtree.

## 2.10 WhatsApp Message Wording

Standardize the pre-filled WhatsApp message to ensure consistency:

```
Hello, I want to buy/inquire about this product:

Product: <product name>
Product ID: <product id>
Price: ৳<price>
Quantity: <quantity>
Product URL: <absolute product page URL>

Please let me know the availability and purchase process.
```

The currency symbol `৳` is used as an example; the exact symbol may be adjusted based on store locale, but the message structure must remain consistent.

## 2.11 JWT Storage Strategy

Use **httpOnly cookies** for JWT storage. This mitigates XSS attacks compared to `localStorage`. The backend must set the access token as an httpOnly cookie on login/register. The frontend must not store tokens in `localStorage` or `sessionStorage`. CSRF protection must be implemented using double-submit cookies or same-site cookie attributes.

## 2.12 WhatsApp Flow Failure Modes

If the backend order creation succeeds but the frontend fails to open WhatsApp (e.g., URL generation error, browser block), the customer must see a clear error message with the order ID and a manual fallback link to WhatsApp. The pending order remains in the system. The frontend must not silently swallow this error.

## 2.13 Stock Reservation Expiry

To prevent indefinite stock reservation, implement an `expires_at` timestamp on `Order` (default: 7 days from creation). A scheduled backend task (or manual admin action) must automatically cancel expired `PENDING` orders and restore stock. For MVP, a simple background task using FastAPI's `BackgroundTasks` or a lightweight scheduler is sufficient.

## 2.14 Concurrent Test Reliability

Write the concurrency test using `asyncio.gather` with two simultaneous API calls in the same event loop. Use a single database transaction per request and verify:
- Exactly one request returns `201 Created`.
- The other returns `409 Conflict`.
- Final stock is `0` (not negative).
- Exactly one `Order` and one `OrderItem` exist.

Run this test in isolation (mark it with a custom pytest marker) to reduce flakiness in CI.

## 2.15 Docker Networking

In Docker Compose:
- Backend service name: `backend`
- Frontend service name: `frontend`
- Database service name: `db`

`NEXT_PUBLIC_API_URL` in the frontend must resolve to `http://backend:8000` (the Docker service name), **not** `localhost`. For local development outside Docker, developers may override this in `.env.local` to `http://localhost:8000`.

---

## 2.16 Safe Implementation Sequence

The original sequence in Section 45 placed high-risk backend features late. The revised sequence front-loads risk and validates integration early:

```text
1. Freeze requirements
         ↓
2. Create Git repository (main + develop)
         ↓
3. Design architecture + database schema
         ↓
4. Create project skeleton (folders, docker-compose, .env.example)
         ↓
5. Setup Docker services (PostgreSQL, backend, frontend)
         ↓
6. Setup FastAPI + health check + CORS
         ↓
7. Setup Next.js + Tailwind + global layout
         ↓
8. Implement SQLAlchemy models + Alembic migrations
         ↓
9. Create seed data script (admin, categories, products, store settings)
         ↓
10. Implement authentication API + JWT + password hashing
         ↓
11. Implement authorization dependencies (get_current_user, require_admin, require_customer)
         ↓
12. Implement category API
         ↓
13. Implement product API (public browse + admin CRUD)
         ↓
14. Implement store settings API
         ↓
15. Implement order API WITH transactional stock protection (FOR UPDATE)
         ↓
16. Add concurrent stock test + cancellation stock-restore test
         ↓
17. Test all backend APIs via Swagger
         ↓
18. Build frontend auth UI (login, register)
         ↓
19. Build product listing + details + cart
         ↓
20. Build checkout + WhatsApp purchase flow
         ↓
21. Build customer order pages
         ↓
22. Build admin dashboard + product/category/order management
         ↓
23. Build store customization UI
         ↓
24. Connect dynamic store branding
         ↓
25. Run end-to-end critical flow test
         ↓
26. Security review + error handling polish
         ↓
27. Full backend tests + frontend type checks
         ↓
28. Responsive UI polish
         ↓
29. Complete README + docs
         ↓
30. Deployment + production testing
         ↓
31. Final demo preparation
```

**Critical rule**: Do not build frontend checkout or WhatsApp flow (steps 20) until the backend order API (step 15) and its concurrency tests (step 16) are passing. This prevents building on a broken or unsafe foundation.

---

# 2. Product Vision

The application has two main user experiences:

### Customer

A customer can:

- Browse products.
- Search products.
- Filter and sort products.
- View product details.
- Register and log in.
- Add products to a cart.
- Change cart quantities.
- Checkout.
- Place an order.
- View order history.
- View order details and status.

### Administrator

An administrator can:

- Log in securely.
- View dashboard statistics.
- Create/update/delete products.
- Manage categories.
- Manage product stock.
- View customers.
- View orders.
- Change order status.
- Configure store information and branding.

### Customization

The administrator can configure:

- Store name.
- Store description.
- Logo.
- Homepage banner.
- Primary color.
- Secondary color.
- Contact information.
- WhatsApp number for product purchase inquiries.
- Featured products.

The same codebase should therefore be usable for different stores.

---

# 3. Scope

## 3.1 Must-Have Features

These are mandatory:

- User registration.
- User login.
- JWT authentication.
- Customer/admin roles.
- Product CRUD.
- Category CRUD.
- Product browsing.
- Product search.
- Product filtering.
- Product sorting.
- Product details.
- Shopping cart.
- Checkout.
- Order creation.
- Order history.
- Order status management.
- Admin dashboard.
- Customer management/read-only list.
- Store customization.
- Responsive UI.
- API validation.
- Authorization.
- Error handling.
- Database migrations.
- Docker-based local development.
- Basic testing.
- Deployment-ready configuration.
- README documentation.

## 3.2 Explicitly Out of Scope for MVP

Do not implement these unless the MVP is complete and there is significant remaining time:

- Real payment gateway.
- Online payment processing.

Instead, product purchase inquiries will be initiated through the store WhatsApp number configured in StoreSettings.
- Multi-vendor marketplace.
- Seller accounts.
- Delivery partner integration.
- GPS delivery tracking.
- Real-time chat.
- AI recommendations.
- AI chatbot.
- Complex coupon engine.
- Loyalty points.
- Advanced warehouse management.
- Complex analytics.
- Microservice architecture.
- Real-time notifications.
- Social login.
- Multi-language support.

These can be documented under "Future Enhancements."

---

# 4. Architecture

Use a simple three-layer architecture.

```text
                         ┌──────────────────────┐
                         │       Customer       │
                         │       Browser        │
                         └──────────┬───────────┘
                                    │
                                    │ HTTPS / HTTP
                                    ▼
                         ┌──────────────────────┐
                         │       Next.js        │
                         │      Frontend        │
                         │                      │
                         │ Customer UI          │
                         │ Admin UI             │
                         │ Cart State           │
                         └──────────┬───────────┘
                                    │
                              REST / JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       Backend        │
                         │                      │
                         │ Auth                 │
                         │ Business Logic       │
                         │ Validation           │
                         │ Authorization        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PostgreSQL      │
                         │       Database       │
                         └──────────────────────┘
```

The frontend must never directly access PostgreSQL.

All business operations go through FastAPI.

---

# 5. Recommended Repository Structure

Use a monorepo:

```text
customizable-ecommerce/
│
├── frontend/
├── backend/
├── docker-compose.yml
├── .gitignore
├── .env.example
├── README.md
└── docs/
    ├── architecture.md
    ├── database.md
    ├── api.md
    └── screenshots/
```

## Backend structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   └── base.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── store_settings.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── store_settings.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── categories.py
│   │           ├── products.py
│   │           ├── orders.py
│   │           ├── admin.py
│   │           └── store.py
│   │
│   └── services/
│       ├── auth.py
│       ├── product.py
│       ├── order.py
│       └── store.py
│
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Frontend structure

```text
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── loading.tsx
│   ├── not-found.tsx
│   │
│   ├── login/
│   ├── register/
│   ├── products/
│   ├── product/
│   │   └── [id]/
│   ├── cart/
│   ├── checkout/
│   ├── orders/
│   │   ├── page.tsx
│   │   └── [id]/
│   │
│   └── admin/
│       ├── page.tsx
│       ├── products/
│       ├── categories/
│       ├── orders/
│       ├── customers/
│       └── settings/
│
├── components/
│   ├── layout/
│   ├── products/
│   ├── cart/
│   ├── orders/
│   ├── admin/
│   └── ui/
│
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   └── utils.ts
│
├── store/
│   └── cart-store.ts
│
├── types/
│   ├── product.ts
│   ├── order.ts
│   ├── user.ts
│   └── store.ts
│
└── public/
```

The exact structure may be adjusted if needed, but the separation of concerns should remain.

---

# 6. Database Design

## 6.1 User

Fields:

```text
id              UUID / integer primary key
name            string
email           string unique, not null
password_hash   string not null
role            enum: CUSTOMER | ADMIN
created_at      timestamp
updated_at      timestamp
```

Rules:

- Email must be unique.
- Never store plaintext passwords.
- Default role is CUSTOMER.
- Admin creation should not be publicly exposed through registration. The first admin is created via the development seed script. No public or customer-facing endpoint may set `role=ADMIN`.

---

## 6.2 Category

```text
id              primary key
name            string unique
description     nullable string
created_at      timestamp
updated_at      timestamp
```

Relationship:

```text
Category 1 ──────── * Product
```

---

## 6.3 Product

```text
id              primary key
name            string
description     text
price           numeric/decimal
stock           integer
image_url       nullable string
category_id     foreign key
is_featured     boolean
created_at      timestamp
updated_at      timestamp
```

Rules:

- Price >= 0.
- Stock >= 0.
- Category must exist.
- Deleting a category must not silently create invalid products.
- Product price should use Decimal/Numeric rather than floating-point money calculations.
- Featured products: `is_featured = true` marks a product as featured. The homepage shows up to 8 featured products ordered by creation date descending. Admin toggles this flag in the product form.

---

## 6.4 Order

```text
id                  primary key
user_id             foreign key
total_amount        numeric/decimal
shipping_name       string
shipping_phone      string
shipping_address    text
status              enum
expires_at          nullable timestamp
created_at          timestamp
updated_at          timestamp
```

Order statuses:

```text
PENDING
CONFIRMED
PROCESSING
SHIPPED
DELIVERED
CANCELLED
```

State machine (allowed transitions):

```text
PENDING  → CONFIRMED
PENDING  → CANCELLED
CONFIRMED → PROCESSING
PROCESSING → SHIPPED
SHIPPED → DELIVERED
CONFIRMED → CANCELLED
PROCESSING → CANCELLED
```

Any transition not in this graph returns `400 Bad Request`. `CANCELLED` and `DELIVERED` are terminal. Once reached, no further status changes are permitted.

`expires_at` defaults to 7 days from creation for `PENDING` orders. A background task must cancel expired pending orders and restore stock.

---

## 6.5 OrderItem

```text
id              primary key
order_id        foreign key
product_id      foreign key
quantity        integer
price           numeric/decimal
```

Important:

`price` represents the product price at the time the order was placed.

Do not calculate historical order totals from the current Product.price.

Relationship:

```text
Order 1 ──────── * OrderItem
Product 1 ───── * OrderItem
```

---

## 6.6 StoreSettings

Only one store settings record is required for MVP.

```text
id                  primary key
store_name          string
description         nullable text
logo_url            nullable string
banner_url          nullable string
primary_color       string
secondary_color     string
contact_email       nullable string
contact_phone       nullable string
whatsapp_number     string not null
address             nullable text
updated_at          timestamp
```

Use a singleton-style record. Enforce at the database layer (e.g., a unique constraint on a dummy singleton key) and at the service layer. The backend must provide a default configuration if no settings record exists.

## 6.7 Singleton Enforcement

The `StoreSettings` table must contain exactly one row. Implementation approach:
1. Add a unique column `singleton_key` with a fixed value (e.g., `'default'`).
2. The service `get_store_settings()` returns the existing row or creates a default row if none exists.
3. The admin `PUT` endpoint updates the single row; it must not allow creation of a second row.

---

# 7. Backend API Specification

Prefix all APIs with:

```text
/api/v1
```

Use REST conventions.

---

## 7.1 Health Check

```http
GET /api/v1/health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 8. Authentication API

## Register

```http
POST /api/v1/auth/register
```

Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password"
}
```

Response should return safe user information.

Never return the password or password hash.

---

## Login

```http
POST /api/v1/auth/login
```

Accept email and password.

Return:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "name": "...",
    "email": "...",
    "role": "CUSTOMER"
  }
}
```

The backend must also set the access token as an **httpOnly cookie** with `SameSite=Strict`. The JSON body response is kept for initial client hydration, but subsequent requests rely on the cookie.

---

## Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

Returns the authenticated user.

---

# 9. Category API

## Public

```http
GET /api/v1/categories
GET /api/v1/categories/{id}
```

## Admin

```http
POST /api/v1/categories
PUT /api/v1/categories/{id}
DELETE /api/v1/categories/{id}
```

Only ADMIN can mutate categories.

---

# 10. Product API

## Public

```http
GET /api/v1/products
GET /api/v1/products/{id}
```

Support query parameters:

```text
search
category_id
min_price
max_price
sort
page
limit
```

Pagination defaults and limits:
- `page`: minimum `1`, default `1`
- `limit`: minimum `1`, default `12`, maximum `100`

Example:

```text
GET /api/v1/products?search=phone&category_id=2&sort=price_asc&page=1&limit=12
```

Supported sorting:

```text
price_asc
price_desc
newest
name_asc
name_desc
```

Implement pagination.

Response should contain:

```json
{
  "items": [],
  "page": 1,
  "limit": 12,
  "total": 50,
  "pages": 5
}
```

## Admin

```http
POST /api/v1/products
PUT /api/v1/products/{id}
DELETE /api/v1/products/{id}
```

Validate all fields on the backend.

---

# 11. Order API

The application will not process online payments. An application order represents a **purchase request/reservation** that can be followed up through WhatsApp.

For the primary purchase flow, the customer selects a quantity and uses `Message to Buy on WhatsApp`. The frontend should first ask the backend to create a pending purchase request. If the request succeeds, the frontend opens WhatsApp with a pre-filled message containing the generated order/request ID and product information.

This design is important for stock consistency: the backend can atomically validate and reserve stock before the customer is sent to WhatsApp.

## Customer

```http
POST /api/v1/orders
GET /api/v1/orders
GET /api/v1/orders/{id}
```

The backend must:

1. Authenticate the customer.
2. Validate every product.
3. Verify stock.
4. Read current product prices from the database.
5. Calculate the total on the backend.
6. Create Order.
7. Create OrderItems.
8. Decrease stock.
9. Commit everything transactionally.

Do not trust:

- Product prices from frontend.
- Total amount from frontend.
- User ID from frontend.

The authenticated user's ID must be used.

---

# 12. Admin Order API

```http
GET /api/v1/admin/orders
GET /api/v1/admin/orders/{id}
PATCH /api/v1/admin/orders/{id}/status
```

Only ADMIN can access these endpoints.

Status transitions must follow the state machine defined in Section 6.4. When a PENDING purchase request is cancelled/rejected, the backend must restore the quantities reserved by that request exactly once, within a transaction.

At minimum, prevent nonsensical changes such as moving a CANCELLED order back into normal processing unless explicitly supported.

---

# 13. Customer API

Admin-only:

```http
GET /api/v1/admin/customers
GET /api/v1/admin/customers/{id}
```

Customer information should not expose password hashes or sensitive internal data.

---

# 14. Store Customization API

## Public

```http
GET /api/v1/store/settings
```

## Admin

```http
PUT /api/v1/admin/store/settings
```

The public endpoint should return only information required by the frontend.

---

# 15. Authentication and Authorization

Implement JWT-based authentication.

Backend responsibilities:

```text
Login
  ↓
Verify password
  ↓
Create JWT
  ↓
Set JWT as httpOnly cookie
  ↓
Frontend sends cookie automatically
  ↓
API requests include cookie
```

**JWT Storage**: Store the access token in an **httpOnly, SameSite=Strict cookie**. Do **not** store tokens in `localStorage` or `sessionStorage`. This mitigates XSS. Implement CSRF protection using a double-submit cookie pattern or same-site attributes.

Create reusable backend dependencies:

```text
get_current_user()
require_customer()
require_admin()
```

Authorization rules:

| Action | Guest | Customer | Admin |
|---|---:|---:|---:|
| Browse products | Yes | Yes | Yes |
| Search products | Yes | Yes | Yes |
| Add to cart | No* | Yes | Yes |
| Place order | No | Yes | Yes |
| View own orders | No | Yes | Yes |
| Manage products | No | No | Yes |
| Manage categories | No | No | Yes |
| Manage orders | No | No | Yes |
| Manage store settings | No | No | Yes |
| View customers | No | No | Yes |

\* The cart can be allowed for guests on the frontend, but checkout requires login.

---

# 16. Frontend Implementation

## 16.1 Global Layout

Create:

- Navbar.
- Footer.
- Main content container.
- Responsive navigation.
- Store branding from StoreSettings.

Navbar:

```text
Logo | Home | Products | Categories | Search | Cart | Account
```

For admins, show:

```text
Admin Dashboard
```

---

# 17. Homepage

Homepage sections:

1. Hero/banner.
2. Store description.
3. Featured products.
4. Categories.
5. Call-to-action.
6. Footer.

All store-specific information must come from the backend rather than hardcoded values.

---

# 18. Product Listing

Implement:

- Product cards.
- Search.
- Category filter.
- Price filter.
- Sorting.
- Pagination.
- Loading state.
- Empty state.
- Error state.

Product card:

```text
Image
Name
Category
Price
Stock status
View Details
Add to Cart
```

Do not allow adding unavailable/out-of-stock products.

---

# 19. Product Details

Show:

- Product image.
- Name.
- Description.
- Category.
- Price.
- Available stock.
- Quantity selector.
- Add to Cart.

Validate quantity against available stock on the frontend for good UX, but perform the authoritative check again on the backend during checkout.

---

# 20. Cart

Use **Zustand** for client-side cart state. Because the project uses Next.js App Router, the cart store file must include the `"use client"` directive at the top. Do not use React Context for global cart state.

Cart item:

```text
product_id
name
price
image_url
quantity
```

Cart functionality:

- Add item.
- Remove item.
- Increase quantity.
- Decrease quantity.
- Clear cart.
- Calculate subtotal.
- Display item count.

The frontend cart is not authoritative for price or stock.

At checkout, FastAPI must re-read product information.

---

# 21. Checkout

Checkout page:

```text
Order Summary

Customer Name
Phone
Shipping Address

[Place Order]
```

On submission:

```text
Frontend
   ↓
POST /api/v1/orders
   ↓
FastAPI validates cart
   ↓
Creates order
   ↓
Returns order
   ↓
Frontend clears cart
   ↓
Redirect to order details
```

Prevent duplicate submissions using loading state.

---

# 22. Customer Orders

Pages:

```text
/orders
/orders/[id]
```

Order list:

```text
Order ID
Date
Total
Status
View
```

Order details:

```text
Order information
Shipping information
Products
Quantity
Price
Total
Status
```

Display status using a visual timeline where practical.

---

# 23. Admin Dashboard

Route:

```text
/admin
```

Dashboard cards:

```text
Total Products
Total Customers
Total Orders
Total Sales
```

Also display:

- Recent orders.
- Order status summary.
- Featured/best-selling products if easy to calculate.

Do not build advanced analytics.

---

# 24. Admin Product Management

Routes:

```text
/admin/products
/admin/products/new
/admin/products/[id]/edit
```

Features:

- List products.
- Search products.
- Add product.
- Edit product.
- Delete product.
- Set stock.
- Set price.
- Select category.
- Mark featured.

Use reusable forms.

---

# 25. Admin Category Management

Route:

```text
/admin/categories
```

Features:

- List categories.
- Add.
- Edit.
- Delete.

Before deleting a category, handle products belonging to it safely.

Prefer blocking deletion when products still reference the category and displaying a clear message.

---

# 26. Admin Order Management

Route:

```text
/admin/orders
/admin/orders/[id]
```

Features:

- List orders.
- Search/filter if time permits.
- View order.
- Change status.
- View customer and shipping information.

---

# 27. Admin Customer Management

Route:

```text
/admin/customers
```

Display:

- Name.
- Email.
- Registration date.
- Number of orders if easy to calculate.

No customer password or password hash should ever be shown.

---

# 28. Admin Store Customization

Route:

```text
/admin/settings
```

Form:

```text
Store Name
Description
Logo URL / upload
Banner URL / upload
Primary Color
Secondary Color
Contact Email
Contact Phone
Address
```

Save using:

```http
PUT /api/v1/admin/store/settings
```

After saving, refresh the public store configuration.

---

# 29. WhatsApp Purchase Flow

Because a real payment gateway will not be implemented in the MVP, the platform will use WhatsApp as the purchase/inquiry channel.

The store administrator must configure a WhatsApp number in `StoreSettings`.

## 29.1 StoreSettings field

Add:

```text
whatsapp_number    string not null
```

Store the number in a normalized E.164 form without spaces or punctuation (e.g., `8801712345678`). Backend validation:
- Required field.
- Regex: `^\+?[1-9]\d{6,14}$`
- Reject if too short or contains invalid characters.
Frontend display may format for readability, but the stored and API-returned value must be normalized E.164.

## 29.2 Product page

Every product detail page should contain a primary action such as:

```text
[Message to Buy on WhatsApp]
```

When the customer presses it:

1. Retrieve the configured store WhatsApp number.
2. Generate a pre-filled WhatsApp message containing the product details.
3. Open the WhatsApp chat for the configured number.

The application should use the standard WhatsApp click-to-chat URL mechanism rather than attempting to send the message through a WhatsApp API.

Before opening WhatsApp, the frontend should create a pending purchase request through the backend. The backend response should provide the order/request ID. The generated WhatsApp message should include this ID so that the store owner can match the WhatsApp conversation with the application record.

Recommended flow:

```text
Product Page
    ↓
Select quantity
    ↓
Message to Buy on WhatsApp
    ↓
POST /api/v1/orders
    ↓
Backend validates + locks stock + creates PENDING order
    ↓
Success → return order ID
    ↓
Generate WhatsApp message
    ↓
Open WhatsApp chat
```

If order creation fails because stock is no longer available, WhatsApp must not be opened and the customer should see an out-of-stock message.

Standardized WhatsApp pre-filled message:

```
Hello, I want to buy/inquire about this product:

Product: <product name>
Product ID: <product id>
Price: ৳<price>
Quantity: <quantity>
Product URL: <absolute product page URL>

Please let me know the availability and purchase process.
```

**Failure handling**: If the backend order creation succeeds but the frontend fails to open WhatsApp, display a clear error with the order ID and a manual fallback link. Do not silently swallow the error.

## 29.3 Quantity

The product page should allow the customer to select a desired quantity before pressing the WhatsApp purchase button.

The generated message should include the selected quantity.

If the requested quantity exceeds currently displayed stock, the UI should warn the customer and prevent the WhatsApp action until a valid quantity is selected.

However, the displayed stock is only informational at this stage. Because the actual purchase is completed outside the application, stock cannot be permanently reserved merely by opening WhatsApp.

## 29.4 Stock and WhatsApp limitation

The WhatsApp button represents a purchase request/inquiry, not a completed transaction.

The WhatsApp chat itself does **not** reserve stock. The application creates the pending purchase request and reserves/decreases the relevant stock **before** opening WhatsApp.

The application must clearly distinguish:

```text
Purchase Request / Stock Reserved
```

from:

```text
Payment Completed / Order Completed
```

No payment is claimed to have been completed by the application. The store owner completes the commercial transaction through the WhatsApp conversation or another offline method.

For MVP simplicity, a successful pending purchase request may reduce available stock immediately. If the owner rejects/cancels the request, the admin cancellation operation must restore the reserved quantity.

Add `expires_at` to the `Order` model (default: 7 days from creation for `PENDING` orders). A background task must automatically cancel expired pending orders and restore stock exactly once.

## 29.5 Store settings API

The public store settings response may expose the WhatsApp number or a safe WhatsApp chat URL required by the frontend.

Admin can update it through:

```http
PUT /api/v1/admin/store/settings
```

The customer-facing frontend should not hardcode the number.

---

# 30. Concurrent Stock Handling and Race Conditions

A critical business requirement is preventing overselling when multiple customers attempt to purchase the same product concurrently.

Example:

```text
Product stock = 1

Customer A requests quantity = 1
Customer B requests quantity = 1

Only ONE request may successfully reserve/decrease the stock.
The other request must fail with an out-of-stock response.
```

## 30.1 Where the protection is required

The stock check must be performed in the FastAPI backend inside a database transaction. This applies to the pending purchase request created immediately before the WhatsApp chat is opened.

Do not rely only on frontend checks such as:

```text
if stock >= quantity:
    allow purchase
```

Two customers can read the same stock value before either update is committed. This creates a race condition.

## 30.2 Recommended implementation

Use a PostgreSQL transaction with row-level locking for the product rows involved in an order.

Conceptually:

```text
BEGIN TRANSACTION
        ↓
SELECT product FOR UPDATE
        ↓
Read current stock
        ↓
Check requested quantity
        ↓
If insufficient → ROLLBACK + 409/400 error
        ↓
If sufficient
        ↓
Create OrderItem
        ↓
Decrease stock
        ↓
Create/complete Order
        ↓
COMMIT
```

With SQLAlchemy, use the database transaction and a row lock such as `SELECT ... FOR UPDATE` (`with_for_update()`) when loading the product for an order.

The lock must be held until the transaction commits or rolls back.

## 30.3 Example

Initial state:

```text
Product A
stock = 1
```

Two requests arrive almost simultaneously:

```text
Request A ──┐
            ├── PostgreSQL
Request B ──┘
```

Request A obtains the row lock first:

```text
A locks Product A
A sees stock = 1
A needs quantity = 1
A creates order
A changes stock 1 → 0
A commits
```

Request B then obtains the lock:

```text
B locks Product A
B sees stock = 0
B needs quantity = 1
B rejects request
B rolls back
```

Therefore:

```text
Customer A → SUCCESS
Customer B → OUT OF STOCK
```

There must never be a final state of `stock = -1`. If an administrator cancels/rejects a pending purchase request, the reserved quantity must be restored exactly once.

## 30.4 Atomic conditional update

A second acceptable implementation is an atomic database update such as:

```sql
UPDATE products
SET stock = stock - :quantity
WHERE id = :product_id
  AND stock >= :quantity;
```

Then check the affected-row count:

```text
1 row updated → stock successfully reserved/decreased
0 rows updated → insufficient stock / product unavailable
```

If this approach is used, order creation and stock modification must still be handled transactionally so that a failed order does not leave stock incorrectly reduced.

For this project, row-level locking is recommended because it is straightforward to explain in the industrial attachment report and demonstrates transaction/concurrency handling clearly.

## 30.5 Multiple products in one order

If an order contains multiple products:

1. Start one database transaction.
2. Validate the request.
3. Load all required product rows with locks.
4. Acquire locks in a deterministic order, preferably sorted by product ID.
5. Validate all stock quantities.
6. Calculate the total from database prices.
7. Create the order and order items.
8. Decrease stock for every product.
9. Commit only if every item succeeds.

If any item has insufficient stock:

```text
ROLLBACK
```

The entire order should fail rather than partially reducing stock.

Sorting product IDs before acquiring multiple row locks also reduces the risk of deadlocks between concurrent multi-product orders.

## 30.6 HTTP response

When stock is insufficient, return a clear response such as:

```http
409 Conflict
```

Example:

```json
{
  "detail": "Insufficient stock for Wireless Headphone. Available: 0, requested: 1."
}
```

The frontend should display a user-friendly message and refresh the product/cart stock information.

## 30.7 Testing concurrency

Add a backend test specifically for this scenario. Write the test using `asyncio.gather` with two simultaneous API calls in the same event loop. Use a single database transaction per request and verify:
- Exactly one request returns `201 Created`.
- The other returns `409 Conflict`.
- Final stock is `0` (not negative).
- Exactly one `Order` and one `OrderItem` exist.

Mark this test with a custom pytest marker (e.g., `@pytest.mark.concurrency`) so it can be run in isolation and skipped in flaky CI environments if necessary.

Test setup:

```text
Product stock = 1
```

Send two purchase requests concurrently, each requesting quantity 1.

Expected result:

```text
One request  → success
One request  → 409 Conflict / insufficient stock
Final stock  → 0
Successful orders → 1
```

The test should verify that:

- Both requests cannot succeed.
- Stock never becomes negative.
- Only one successful order/order item is created.
- The failed request receives a clear error.

This is a high-priority business-logic test.

## 30.8 Important distinction with WhatsApp

The concurrency protection described above applies when the application itself creates an order and decreases/reserves stock.

The WhatsApp button itself is only the communication mechanism. The application creates the pending purchase request immediately before opening WhatsApp so that stock can be protected against concurrent purchase requests.

The application does not need WhatsApp Business API/webhooks for the MVP. It only uses the standard click-to-chat URL with a pre-filled message.

If the business later requires automatic confirmation of payment or automatic synchronization with WhatsApp messages, a WhatsApp Business API/webhook integration would be required. That is outside the MVP.

---

# 31. Image Strategy

For the first implementation, use `image_url` with **local filesystem storage**. Create a `media/` directory inside the backend container. Docker Compose must mount a named volume to `backend/media/` so uploads persist across container restarts. Store only the relative path or filename in `image_url`. Serve uploaded files via a dedicated FastAPI static route (e.g., `/media/{filename}`).

If time permits, implement image uploads with the following rules:
- Validate file type: `image/jpeg`, `image/png`, `image/webp`.
- Validate file size: max 2 MB.
- Store the resulting relative path.
- Never store large binary images directly in PostgreSQL.

---

# 32. API Client in Next.js

Create one centralized API client.

For example:

```text
lib/api.ts
```

It should handle:

- Base API URL.
- HTTP methods.
- JSON parsing.
- Authentication headers.
- Common error handling.

Avoid scattering raw `fetch()` calls throughout every component.

Organize API functions logically:

```text
authApi
productsApi
categoriesApi
ordersApi
adminApi
storeApi
```

---

# 33. Environment Variables

Frontend:

```text
NEXT_PUBLIC_API_URL=
```

Backend:

```text
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
CORS_ORIGINS=
```

Never commit real secrets.

Provide:

```text
.env.example
```

with placeholders.

---

# 34. Docker

Use Docker Compose for local development.

Services:

```text
frontend
backend
db
```

At minimum, PostgreSQL should run through Docker.

Docker Compose service names:
- `db` — PostgreSQL
- `backend` — FastAPI
- `frontend` — Next.js

Networking:
- Frontend must call backend using the Docker service name: `NEXT_PUBLIC_API_URL=http://backend:8000`.
- For local development outside Docker, override in `.env.local` to `http://localhost:8000`.
- Backend must listen on `0.0.0.0:8000` inside the container.

Example conceptual setup:

```text
docker-compose.yml

services:
  db:
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/ecommerce
    volumes:
      - backend_media:/app/media

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

volumes:
  postgres_data:
  backend_media:
```

Make sure the project can be started using a documented command sequence.

Do not make Docker unnecessarily complicated.

---

# 35. Database Migrations

Use Alembic.

Workflow:

```text
Modify SQLAlchemy model
        ↓
Create migration
        ↓
Review migration
        ↓
Run migration
        ↓
Test database
```

Do not manually modify the production schema.

Document migration commands in README.

---

# 36. Seed Data

Create a development seed mechanism.

Seed:

- One admin account (created by seed script, never via public registration).
- Several customer accounts if useful.
- 4–6 categories.
- 15–30 products.
- Store settings.

Use fake/demo data only.

Never put real credentials in the repository.

Document how to create/reset seed data.

## 36.1 Admin Bootstrap

Because public registration only creates `CUSTOMER` accounts, the seed script must create the initial `ADMIN` account. Document the exact command (e.g., `python scripts/seed.py`) and warn developers not to commit real credentials.

---

# 37. Error Handling

Backend should return appropriate HTTP status codes.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
```

Frontend should translate common API errors into user-friendly messages.

Examples:

```text
Invalid email or password.
You do not have permission to perform this action.
Product is out of stock.
The requested product was not found.
Unable to place the order. Please try again.
```

---

# 38. Validation Rules

Backend validation is authoritative.

### User

- Valid email.
- Password minimum length.
- Name required.

### Product

- Name required.
- Price >= 0.
- Stock >= 0.
- Valid category.

### Order

- Quantity > 0.
- Product exists.
- Product is available.
- Requested quantity <= stock.
- Shipping information required.

### Store

- Store name required.
- Colors should be validated as valid color values where possible.

---

# 39. Security Requirements

Implement at minimum:

- Password hashing.
- JWT authentication.
- Role-based authorization.
- Backend validation.
- CORS configuration.
- No password exposure.
- No password hash exposure.
- No trusting frontend totals.
- No trusting frontend user IDs.
- Parameterized/ORM database queries.
- Environment-based secrets.
- Appropriate HTTP status codes.

Do not log passwords or tokens.

---

# 40. Frontend UX Requirements

Every major data-driven page should handle:

```text
Loading
Success
Empty
Error
```

Examples:

### Product loading

Show skeleton/spinner.

### Empty search

```text
No products found.
```

### Empty cart

```text
Your cart is empty.
[Continue Shopping]
```

### No orders

```text
You haven't placed any orders yet.
```

Make the UI responsive for:

- Desktop.
- Tablet.
- Mobile.

---

# 41. Testing Strategy

Use these exact frameworks:
- **Backend**: `pytest` + `httpx` (async test client) + `pytest-asyncio`
- **Frontend**: `Vitest` + `@testing-library/react` + `@testing-library/jest-dom`
- **E2E**: Manual checklist (see Section 42); automated E2E is P2.

## Backend unit/API tests

Test:

### Authentication

- Register.
- Duplicate email.
- Login.
- Wrong password.
- Current user.
- Unauthorized request.

### Authorization

- Customer cannot access admin endpoints.
- Admin can access admin endpoints.

### Products

- List.
- Detail.
- Create.
- Update.
- Delete.
- Invalid category.
- Invalid price/stock.

### Orders

- Valid order.
- Invalid product.
- Insufficient stock.
- Correct total.
- Correct stock reduction.
- Customer can only access own orders.
- Admin can access all orders.
- Status update.

### Concurrent stock

Test:

```text
Initial stock = 1
Request A quantity = 1
Request B quantity = 1
Both submitted concurrently
```

Expected:

```text
One request succeeds and creates PENDING order
One request receives 409 Conflict
Final available stock = 0
No negative stock
Only one successful reservation/order
```

Also test cancellation:

```text
Cancel successful pending order
        ↓
Reserved quantity restored
        ↓
Stock becomes 1
```

### Store

- Public settings.
- Admin update.
- Unauthorized update blocked.

---

# 42. Critical End-to-End Test

This is the most important test.

```text
1. Open store
2. Browse products
3. Search product
4. Open product details
5. Add product to cart
6. Increase quantity
7. Login/register
8. Select quantity
9. Click Message to Buy on WhatsApp
10. Verify pending purchase request is created and stock is reserved
11. Verify WhatsApp opens with the configured number and pre-filled message
12. Login as admin
13. Open admin dashboard
14. Verify order appears
15. Change status to CONFIRMED
16. Change status to PROCESSING
17. Change status to SHIPPED
18. Change status to DELIVERED
19. Login as customer
20. Verify updated status
```

The project should not be considered complete until this flow works.

---

# 43. Git Strategy for Two Developers

Use:

```text
main
└── develop
    ├── feature/auth
    ├── feature/products
    ├── feature/cart
    ├── feature/orders
    ├── feature/admin
    └── feature/customization
```

Recommended process:

```text
Create branch
    ↓
Implement one feature
    ↓
Run tests
    ↓
Commit
    ↓
Push
    ↓
Pull Request
    ↓
Review
    ↓
Merge into develop
```

Do not directly work on `main`.

Use meaningful commits:

```text
feat: add product CRUD API
feat: implement customer cart
fix: prevent order creation with insufficient stock
feat: add store customization
refactor: centralize API client
docs: update setup instructions
```

---

# 44. Team Responsibilities

## Developer 1 — Backend Lead

Primary:

- FastAPI.
- PostgreSQL.
- SQLAlchemy.
- Alembic.
- Authentication.
- Authorization.
- Product APIs.
- Category APIs.
- Order APIs.
- Store APIs.

Secondary:

- Backend tests.
- API documentation.
- Deployment support.

## Developer 2 — Frontend Lead

Primary:

- Next.js.
- TypeScript.
- Tailwind CSS.
- Customer UI.
- Cart.
- Checkout.
- Admin dashboard.
- Admin forms.
- Customization UI.

Secondary:

- Frontend testing.
- Responsive design.
- Deployment support.

## Shared

Both should understand:

- Database design.
- API contracts.
- Git workflow.
- Authentication flow.
- Deployment.
- Testing.
- Final presentation.

Do not wait until the end to integrate frontend and backend.

---

# 45. Implementation Sequence

Follow this exact high-level order. The revised sequence front-loads high-risk backend work and validates integration before building dependent frontend features.

```text
1. Freeze requirements
         ↓
2. Create Git repository (main + develop)
         ↓
3. Design architecture + database schema
         ↓
4. Create project skeleton (folders, docker-compose, .env.example)
         ↓
5. Setup Docker services (PostgreSQL, backend, frontend)
         ↓
6. Setup FastAPI + health check + CORS
         ↓
7. Setup Next.js + Tailwind + global layout
         ↓
8. Implement SQLAlchemy models + Alembic migrations
         ↓
9. Create seed data script (admin, categories, products, store settings)
         ↓
10. Implement authentication API + JWT + password hashing
         ↓
11. Implement authorization dependencies (get_current_user, require_admin, require_customer)
         ↓
12. Implement category API
         ↓
13. Implement product API (public browse + admin CRUD)
         ↓
14. Implement store settings API
         ↓
15. Implement order API WITH transactional stock protection (FOR UPDATE)
         ↓
16. Add concurrent stock test + cancellation stock-restore test
         ↓
17. Test all backend APIs via Swagger
         ↓
18. Build frontend auth UI (login, register)
         ↓
19. Build product listing + details + cart
         ↓
20. Build checkout + WhatsApp purchase flow
         ↓
21. Build customer order pages
         ↓
22. Build admin dashboard + product/category/order management
         ↓
23. Build store customization UI
         ↓
24. Connect dynamic store branding
         ↓
25. Run end-to-end critical flow test
         ↓
26. Security review + error handling polish
         ↓
27. Full backend tests + frontend type checks
         ↓
28. Responsive UI polish
         ↓
29. Complete README + docs
         ↓
30. Deployment + production testing
         ↓
31. Final demo preparation
```

**Critical rule**: Do not build frontend checkout or WhatsApp flow (steps 20) until the backend order API (step 15) and its concurrency tests (step 16) are passing. This prevents building on a broken or unsafe foundation.

---

# 46. Definition of Done

The MVP is complete only when all of the following are true:

## Customer

- [ ] Customer can register.
- [ ] Customer can log in.
- [ ] Customer can browse products.
- [ ] Customer can search.
- [ ] Customer can filter.
- [ ] Customer can sort.
- [ ] Customer can view product details.
- [ ] Customer can add products to cart.
- [ ] Customer can modify cart.
- [ ] Customer can checkout.
- [ ] Customer can place an order.
- [ ] Customer can view order history.
- [ ] Customer can view order status.

## Admin

- [ ] Admin login works.
- [ ] Admin dashboard works.
- [ ] Admin can create products.
- [ ] Admin can edit products.
- [ ] Admin can delete products.
- [ ] Admin can manage categories.
- [ ] Admin can view customers.
- [ ] Admin can view orders.
- [ ] Admin can update order status.
- [ ] Admin can modify store settings.

## Customization

- [ ] Store name is dynamic.
- [ ] Store description is dynamic.
- [ ] Logo is dynamic.
- [ ] Banner is dynamic.
- [ ] Theme colors are dynamic.
- [ ] Contact information is dynamic.
- [ ] Featured products are configurable.
- [ ] WhatsApp purchase number is configurable.
- [ ] Product page has a Message to Buy on WhatsApp action.
- [ ] Generated WhatsApp message contains product details and selected quantity.

## Technical

- [ ] PostgreSQL works.
- [ ] Alembic migrations work.
- [ ] API documentation works.
- [ ] Authentication is protected.
- [ ] Admin routes are protected.
- [ ] Passwords are hashed.
- [ ] Backend validates input.
- [ ] Order totals are calculated server-side.
- [ ] Stock is validated server-side.
- [ ] Stock updates are concurrency-safe using a database transaction and row-level locking or an atomic conditional update.
- [ ] Concurrent stock test passes: only one customer can succeed when stock is sufficient for only one request.
- [ ] Errors are handled.
- [ ] Environment variables are documented.
- [ ] Docker setup works.
- [ ] README is complete.
- [ ] Critical end-to-end flow works.

---

# 47. Priority System

If time becomes limited, implement according to this priority.

## P0 — Absolutely Required

```text
Authentication
Products
Categories
Cart
Checkout
Orders
Admin product management
Admin order management
Basic customization
WhatsApp purchase inquiry
Concurrent stock protection
```

## P1 — Important

```text
Search
Filtering
Sorting
Dashboard statistics
Customer management
Responsive UI
Seed data
Testing
```

## P2 — Only If Time Allows

```text
Image uploads
Advanced analytics
Better animations
Advanced search
Order filtering
Product reviews
Wishlist
```

Do not start P2 features while P0 features are unfinished.

---

# 48. Suggested Final Demonstration

The final presentation should tell one complete story.

## Part 1 — Customer

Show:

```text
Homepage
    ↓
Products
    ↓
Search/filter
    ↓
Product details
    ↓
Cart
    ↓
Login
    ↓
Checkout
    ↓
Order
```

## Part 2 — Admin

Then:

```text
Admin Login
    ↓
Dashboard
    ↓
Products
    ↓
Orders
    ↓
Open customer's order
    ↓
Update status
```

## Part 3 — WhatsApp Purchase Inquiry

Show the product page and press:

```text
Message to Buy on WhatsApp
```

Verify that WhatsApp opens for the configured store number with a pre-filled product message.

## Part 4 — Customization

Finally:

```text
Admin Settings
    ↓
Change Store Name
    ↓
Change Logo/Banner
    ↓
Change Theme Color
    ↓
Save
    ↓
Open Customer Store
    ↓
Show changes
```

This demonstrates the complete system and makes the customization feature obvious.

---

# 49. Documentation Requirements

Prepare these documents:

## README.md

Include:

- Project description.
- Features.
- Architecture.
- Tech stack.
- Prerequisites.
- Environment variables.
- Installation.
- Docker setup.
- Database migration.
- Seed data.
- Running frontend.
- Running backend.
- API documentation.
- Test commands.

## docs/architecture.md

Include:

- System architecture.
- Frontend/backend interaction.
- Authentication flow.
- Order flow.

## docs/database.md

Include:

- ER diagram.
- Tables.
- Relationships.
- Constraints.

## docs/api.md

Include:

- Endpoint list.
- Authentication requirements.
- Request examples.
- Response examples.

---

# 50. Coding-Agent Instructions

When using Codex or another coding agent, do not ask it to build the entire application in one prompt.

Use incremental implementation.

A good sequence is:

### Prompt 1

```text
Read IMPLEMENTATION_PLAN.md. Do not implement anything yet.

Analyze the requirements, identify ambiguities or technical risks,
and propose the initial repository structure and implementation sequence.

Do not add features outside the specified MVP.
```

### Prompt 2

```text
Implement Phase 1 of the implementation plan:
project scaffolding, Docker/PostgreSQL, FastAPI, Next.js,
environment configuration, and basic health checks.

Follow IMPLEMENTATION_PLAN.md exactly.

After implementation, run the relevant checks and report:
1. files changed
2. commands executed
3. results
4. remaining issues
```

Then continue feature by feature.

### For each feature

Tell the agent:

```text
Implement the Product API according to IMPLEMENTATION_PLAN.md.

Requirements:
- Follow the existing architecture.
- Do not change unrelated modules.
- Add validation.
- Add tests.
- Update documentation if necessary.
- Run tests/lint/type checks.
- Do not mark the task complete unless the checks pass.

At the end, report changed files, tests run, and any known limitations.
```

This approach is much safer than asking an agent:

```text
Build the entire e-commerce website.
```

---

# 51. Important Coding-Agent Rules

When implementing the WhatsApp purchase flow, follow these rules:

1. Do not hardcode the store WhatsApp number anywhere in the frontend.
2. Read the number from StoreSettings/API data.
3. Use a standard WhatsApp click-to-chat URL with a URL-encoded message.
4. Do not claim that the application completed a payment.
5. Create the pending purchase request before opening WhatsApp so stock can be protected.
6. The backend must calculate price and validate stock.
7. Use a PostgreSQL transaction with row-level locking (`FOR UPDATE`) or an equivalent atomic conditional update.
8. Never allow stock to become negative.
9. If a pending request is cancelled/rejected, restore its reserved quantities exactly once.
10. Add a concurrency test demonstrating that two simultaneous requests cannot both reserve the final unit.


Give the coding agent these permanent rules:

1. Read `IMPLEMENTATION_PLAN.md` before making architectural decisions.
2. Do not introduce features outside the MVP without approval.
3. Do not replace the chosen stack.
4. Do not expose secrets.
5. Do not store plaintext passwords.
6. Do not trust frontend order totals.
7. Do not trust frontend stock information.
8. Validate all important operations on the backend.
9. Keep frontend and backend API contracts synchronized.
10. Add tests for important business logic.
11. Do not rewrite working code unnecessarily.
12. Keep commits small and meaningful.
13. Run tests after significant changes.
14. Fix errors before moving to the next major feature.
15. Prefer simple implementations because the project has a three-week deadline.

---

# 52. Final Project Outcome

The final system should provide this complete flow:

```text
                         ADMIN
                           │
                           ▼
                  ┌─────────────────┐
                  │ Admin Dashboard │
                  └───────┬─────────┘
                          │
             ┌────────────┼─────────────┐
             ▼            ▼             ▼
         Products     Categories    Store Settings
             │                          │
             └────────────┬─────────────┘
                          │
                          ▼
                  CUSTOMIZED STORE
                          │
                          ▼
                     CUSTOMER
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
              Browse            Search
                 │                 │
                 └────────┬────────┘
                          ▼
                       Product
                          │
                          ▼
                         Cart
                          │
                          ▼
                       Checkout
                          │
                          ▼
                        Purchase Request
                          │
                          ├──────────────► WhatsApp chat
                          │
                          ▼
                   Admin manages it
                          │
                          ▼
                   Status updated
                          │
                          ▼
                Customer sees status
```

This is the **target architecture and implementation scope**. Once this flow works reliably, the project is strong enough for a three-week industrial attachment. Additional features should only be considered after this entire flow is functional.
