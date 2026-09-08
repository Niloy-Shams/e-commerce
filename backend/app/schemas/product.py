"""
TODO (feature/products): Pydantic schemas for Product, matching
IMPLEMENTATION_PLAN.md section 10.

- ProductCreate / ProductUpdate: name, description, price (>=0), stock (>=0),
  image_url, category_id, is_featured
- ProductOut: all fields above plus id, created_at, updated_at
- ProductListResponse: items, page, limit, total, pages
  (for GET /api/v1/products with search/category_id/min_price/max_price/sort/page/limit)
"""
