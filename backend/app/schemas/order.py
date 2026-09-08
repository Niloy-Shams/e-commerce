"""
TODO (feature/orders): Pydantic schemas for Order/OrderItem, matching
IMPLEMENTATION_PLAN.md sections 11-12.

- OrderItemIn: product_id, quantity  (client only sends this - never price)
- OrderCreate: items: list[OrderItemIn], shipping_name, shipping_phone, shipping_address
- OrderItemOut: product_id, name, quantity, price
- OrderOut: id, user_id, total_amount, shipping_*, status, items, created_at, updated_at
- OrderStatusUpdate: status  (admin only, validate transitions)
"""
