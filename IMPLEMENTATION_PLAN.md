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

# 2. Product Vision

Build a reusable e-commerce application that can be configured for a small business without changing the application source code.

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
- Admin creation should not be publicly exposed through registration.

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
address             nullable text
updated_at          timestamp
```

Use a singleton-style record.

The backend should provide a default configuration if no settings record exists.

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

Status transitions should be validated.

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
Frontend stores authentication state
  ↓
API requests include Bearer token
```

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

Use a lightweight client-side state solution such as Zustand or React Context.

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

# 29. Image Strategy

For the first implementation, use `image_url`.

Do not make image uploading a blocker.

The initial product form can accept an image URL.

If time permits, implement image uploads using a suitable object/image storage provider.

If upload is implemented:

- Validate file type.
- Validate file size.
- Store the resulting URL.
- Never store large binary images directly in PostgreSQL.

---

# 30. API Client in Next.js

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

# 31. Environment Variables

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

# 32. Docker

Use Docker Compose for local development.

Recommended services:

```text
frontend
backend
db
```

At minimum, PostgreSQL should run through Docker.

Example conceptual setup:

```text
docker-compose.yml

services:
  db:
    postgres

  backend:
    FastAPI

  frontend:
    Next.js
```

Make sure the project can be started using a documented command sequence.

Do not make Docker unnecessarily complicated.

---

# 33. Database Migrations

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

# 34. Seed Data

Create a development seed mechanism.

Seed:

- One admin account.
- Several customer accounts if useful.
- 4–6 categories.
- 15–30 products.
- Store settings.

Use fake/demo data only.

Never put real credentials in the repository.

Document how to create/reset seed data.

---

# 35. Error Handling

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

# 36. Validation Rules

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

# 37. Security Requirements

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

# 38. Frontend UX Requirements

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

# 39. Testing Strategy

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

### Store

- Public settings.
- Admin update.
- Unauthorized update blocked.

---

# 40. Critical End-to-End Test

This is the most important test.

```text
1. Open store
2. Browse products
3. Search product
4. Open product details
5. Add product to cart
6. Increase quantity
7. Login/register
8. Checkout
9. Place order
10. Verify order exists
11. Login as admin
12. Open admin dashboard
13. Verify order appears
14. Change status to CONFIRMED
15. Change status to PROCESSING
16. Change status to SHIPPED
17. Change status to DELIVERED
18. Login as customer
19. Verify updated status
```

The project should not be considered complete until this flow works.

---

# 41. Git Strategy for Two Developers

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

# 42. Team Responsibilities

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

# 43. Implementation Sequence

Follow this exact high-level order.

```text
1. Freeze requirements
        ↓
2. Create Git repository
        ↓
3. Design architecture
        ↓
4. Design database
        ↓
5. Create project skeleton
        ↓
6. Setup Docker/PostgreSQL
        ↓
7. Setup FastAPI
        ↓
8. Setup Next.js
        ↓
9. Configure environment variables
        ↓
10. Implement SQLAlchemy models
        ↓
11. Implement Alembic migrations
        ↓
12. Create seed data
        ↓
13. Implement authentication
        ↓
14. Implement authorization
        ↓
15. Implement category API
        ↓
16. Implement product API
        ↓
17. Test APIs with Swagger/Postman
        ↓
18. Build global Next.js layout
        ↓
19. Build authentication UI
        ↓
20. Build product listing
        ↓
21. Build product details
        ↓
22. Integrate product APIs
        ↓
23. Implement cart
        ↓
24. Implement checkout
        ↓
25. Implement order API
        ↓
26. Build customer order pages
        ↓
27. Build admin product management
        ↓
28. Build admin category management
        ↓
29. Build admin order management
        ↓
30. Build customer management
        ↓
31. Build admin dashboard
        ↓
32. Implement store settings API
        ↓
33. Build customization UI
        ↓
34. Connect dynamic store branding
        ↓
35. Add image handling if time permits
        ↓
36. Security review
        ↓
37. Backend tests
        ↓
38. Frontend tests/manual QA
        ↓
39. End-to-end testing
        ↓
40. Responsive UI polishing
        ↓
41. Deployment
        ↓
42. Production testing
        ↓
43. Documentation
        ↓
44. Final demo preparation
```

---

# 44. Definition of Done

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
- [ ] Errors are handled.
- [ ] Environment variables are documented.
- [ ] Docker setup works.
- [ ] README is complete.
- [ ] Critical end-to-end flow works.

---

# 45. Priority System

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

# 46. Suggested Final Demonstration

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

## Part 3 — Customization

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

# 47. Documentation Requirements

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

# 48. Coding-Agent Instructions

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

# 49. Important Coding-Agent Rules

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

# 50. Final Project Outcome

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
                        Order
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
