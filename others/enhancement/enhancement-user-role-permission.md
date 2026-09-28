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

# Desired State

## Desired State — Multi-Role RBAC

### 1. Remove unused Django default authentication/RBAC tables

The project does **not** use Django's default `auth_user` / `auth_group` authentication system.

Remove the unused default tables:

```text
auth_user
auth_group
auth_group_permissions
auth_user_groups
auth_user_user_permissions
auth_permission
```

Keep only Django infrastructure tables that are still required by the project, such as:

```text
django_migrations
django_content_type
django_session
django_admin_log
```

Do **not** replace the application's `users` table with `auth_user`.

The existing custom `users` table remains the application's single source of truth for users.

---

# 2. Multi-role user

### Current

```text
users
-----
id
email
...
role    ← single role
```

### Desired

Remove:

```text
users.role
```

A user can have **zero, one, or many roles** through a junction table.

```text
users
  │
  │ 1:N
  ▼
user_roles
  │
  │ N:1
  ▼
roles
```

Example:

```text
User: Devit
   │
   ├── customer
   ├── seller
   └── support
```

---

# 3. Role table

Create:

```text
roles
-----
id
name
slug
description
created_at
updated_at
```

Example:

```text
id | name     | slug
---+----------+---------
1  | Customer | customer
2  | Seller   | seller
3  | Support  | support
4  | Admin    | admin
```

`slug` should be unique.

---

# 4. User → Role relationship

Create:

```text
user_roles
----------
id
user_id
role_id
created_at
```

Relationships:

```text
users.id ─────< user_roles.user_id
roles.id ─────< user_roles.role_id
```

Add a unique constraint:

```text
UNIQUE(user_id, role_id)
```

This prevents assigning the same role to the same user twice.

---

# 5. Role → Permission relationship

Create:

```text
permissions
-----------
id
name
slug
description
created_at
updated_at
```

Example:

```text
product.create
product.update
product.delete
order.view
order.update
user.view
user.update
```

Then create:

```text
role_has_permissions
--------------------
id
role_id
permission_id
created_at
```

Relationships:

```text
roles.id ─────────< role_has_permissions.role_id
permissions.id ───< role_has_permissions.permission_id
```

Add:

```text
UNIQUE(role_id, permission_id)
```

---

# 6. Final database relationship

```text
┌──────────────┐
│    users     │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│  user_roles  │
└──────┬───────┘
       │
       │ N:1
       ▼
┌──────────────┐
│    roles     │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌────────────────────────┐
│ role_has_permissions   │
└───────────┬────────────┘
            │
            │ N:1
            ▼
┌────────────────┐
│  permissions   │
└────────────────┘
```

Conceptually:

```text
User
 └──< UserRole >── Role
                    └──< RoleHasPermission >── Permission
```

---

# 7. Authentication / JWT desired flow

The existing multi-role JWT functionality should remain.

The new source of roles becomes the database relationship:

```text
users
  ↓
user_roles
  ↓
roles
  ↓
AuthServiceFacade.login()
  ↓
roles = ["customer", "seller"]
  ↓
JWT
  ↓
Metadata.roles
  ↓
@require_roles(...)
```

For example:

```json
{
  "user_id": "uuid",
  "roles": [
    "customer",
    "seller"
  ]
}
```

`JwtUtil` should receive the roles from the user's role relationships rather than from:

```python
user.role
```

---

# 8. Final desired state

```text
                    ┌──────────────┐
                    │    users     │
                    │              │
                    │ id           │
                    │ email        │
                    │ password_hash│
                    │ status       │
                    │ ...          │
                    └──────┬───────┘
                           │
                           │
                    ┌──────▼───────┐
                    │  user_roles  │
                    │              │
                    │ user_id      │
                    │ role_id      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    roles     │
                    │              │
                    │ id           │
                    │ name         │
                    │ slug         │
                    └──────┬───────┘
                           │
                           │
               ┌───────────▼────────────┐
               │ role_has_permissions   │
               │                        │
               │ role_id                │
               │ permission_id          │
               └───────────┬────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ permissions  │
                    │              │
                    │ id           │
                    │ name         │
                    │ slug         │
                    └──────────────┘
```

### Key rules

1. `users` remains the application's user table.
2. Remove `users.role`.
3. One user can have multiple roles.
4. One role can belong to many users.
5. One role can have many permissions.
6. One permission can belong to many roles.
7. Duplicate `user_id + role_id` is forbidden.
8. Duplicate `role_id + permission_id` is forbidden.
9. JWT contains a list of roles.
10. Existing `Metadata.roles` and `@require_roles()` continue to work.
11. Role assignment is stored in the database, not as a comma-separated string.
12. Django's default `auth_user`/`auth_group` RBAC system is not the application's RBAC source of truth.