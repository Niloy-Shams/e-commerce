"""
TODO (feature/orders): the checkout transaction lives here - see
IMPLEMENTATION_PLAN.md section 11. Must run inside a single DB transaction:
validate products -> verify stock -> price from DB -> compute total ->
create Order -> create OrderItems -> decrease stock -> commit (or roll back
everything on any failure).
"""
