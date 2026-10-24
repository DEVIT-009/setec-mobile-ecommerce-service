---
name: setec-business-logic
description: Implements SETEC use-case logic, domain entities and ports, service facades, and dependency factories. Use for validation, ownership, cart and order behavior, or service-contract changes without putting business logic into views.
---

# SETEC business logic

Read `others/rule.md`, then the target service interface, facade, repository port, and factory. Paths are repository-relative.

## Boundaries and contracts

- Entities are plain dataclasses with typed defaults; mutable collections use `field(default_factory=list)`. Keep entities, repository ports, and service ABCs free of Django and outer-layer imports.
- Facades implement domain service ABCs, receive repository interfaces through constructors, and return dictionaries/lists through controller mappers. Application imports of interface controller mappers are explicitly allowed here.
- Repository ports exchange domain entities or primitives; read misses usually return `None`. Facades turn misses into semantic feature exceptions. Audit-enabled writes pass `actor_id` through to the repository.
- Reuse feature exceptions such as `CategoryException.not_found()` and `.invalid_parent()`. These existing exceptions inherit `shared.exceptionalhandler.base_api_exception.BaseAPIException`; do not duplicate the error hierarchy to enforce hypothetical domain purity.
- Factories wire concrete adapters and return service interfaces. Do not import models or run queries from a new facade. Existing auth-facade ORM access is a deviation, not the preferred pattern.

## Implement a use case

1. Establish required fields, uniqueness, ownership, relationship validity, and permitted state transitions from the request and existing behavior.
2. Add matching service and repository signatures only when needed; update the facade, implementation, factory, and callers together.
3. For create, validate through repository reads, map validated data to a domain entity, persist, then map the saved entity to a response.
4. For PATCH, fetch the existing entity and change only fields present in the input. Distinguish missing keys from explicit `None`, `False`, or zero. Uniqueness checks on update exclude the current ID.
5. Keep multi-write database atomicity inside a repository operation. Extract complex facade logic into private helpers, without moving ORM into the facade.

Real update pattern from `application/category/category_service_facade.py`:

```python
existing = self.repo.get_by_id(category_id)
if not existing:
    raise CategoryException.not_found()
if 'parent_id' in data:
    # Validate a nonempty parent and reject self-parenting before assigning.
    existing.parent_id = data['parent_id']
saved = self.repo.update(existing, actor_id=actor_id)
return CategoryControllerMapper.to_response(saved)
```

## Ecommerce-specific references

- `application/cart/cart_service_facade.py`: combines cart and product ports, snapshots prices using `Decimal`, and scopes item lookup to the user's cart. Keep money calculations decimal; serialize monetary values according to existing DTOs.
- `application/category/category_service_facade.py`: uniqueness checks, parent lookup, partial updates, and tree helpers. Self-parent rejection is present; do not assume arbitrary ancestor cycles are already rejected.
- `application/order/order_service_facade.py` and `infrastructure/persistence/repository/order_repository_impl.py`: checkout groups selected items by store, snapshots order items, writes status history, and closes the cart within a transaction.
- Checkout accepts `idempotency_key` but the repository currently does not use it. Do not describe retries as idempotent or inventory as reserved without implementing and verifying those behaviors when requested.
- User ownership and state transitions must be verified for the specific operation; an interface parameter alone is not evidence that the repository enforces it.

Test facade decisions with injected fake/mock ports; use database tests for transactional behavior and persistence effects.
