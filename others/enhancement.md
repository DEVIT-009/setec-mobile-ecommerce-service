# Current State

### What already works for multi-role (no changes needed)

| Layer | Status |
|-------|--------|
| `JwtUtil.generate_token_for_ecom(roles=[...])` | ✅ Supports comma-joined roles in JWT |
| `JwtUtil.extract_roles(token)` | ✅ Splits CSV → `List[str]` |
| `Metadata.roles: List[str]` | ✅ Populated from JWT at request time |
| `@require_roles("admin")` decorator | ✅ Checks `any(role in required for role in user_roles)` |

These layers were **already written anticipating multi-role** — they just aren't fed real data yet.

---

### What is the core bottleneck

**The database and everything below the JWT layer is single-role only:**

| Layer | Problem |
|-------|---------|
| **DB `users.role`** | Single `ENUM` column — one value per user |
| **`EcomUser.role`** (ORM) | Plain `CharField`, no M2M to a role table |
| **`User` domain entity** | `role: str = "customer"` — a string, not a list |
| **`AuthServiceFacade.login()`** | Calls `_generate_token(user)` with no `roles=` arg → only `user.role` (single) embedded |
| **`AuthServiceFacade.register()`** | Hard-codes `role='customer'` |
| **`update_admin_user()`** | Sets one `role` field only |

---

### The gap in one line

> **Login reads `user.role` (single string) and puts it in the JWT. Everything above the JWT already supports multi-role lists. So the full data path from DB → JWT → decorator is single-role at the bottom and multi-role at the top — the two halves just need to be connected.**

The detailed artifact with a full flow diagram and layer-by-layer table is linked above. When you're ready to plan the enhancement, just say the word.

Ran command: `python manage.py runserver`
Ran command: `agy`
Viewed ecommerce_postgresql_schema.sql:627-657
Ran command: `git add .`
Ran command: `git commit -m "improve id"`
Ran command: `git push origin dev`

# Desired State
