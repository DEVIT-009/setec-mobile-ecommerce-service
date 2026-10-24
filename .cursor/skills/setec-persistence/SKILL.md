---
name: setec-persistence
description: Implements SETEC database models, repository adapters, persistence mappers, migrations, and transactional operations. Use for ORM queries, schema changes, soft deletion, generated IDs, or database performance work.
---

# SETEC persistence

Read `others/rule.md`, the affected models and migrations, and their repository ports. Paths below are repository-relative. Database settings come from `DATABASE_URL`; do not infer the active engine solely from installed database drivers.

## Models and identity

- Models belong in `infrastructure/persistence/models/<feature>_model.py`, with explicit `db_table`, relevant indexes, and existing feature-specific constraints/audit relationships.
- `infrastructure/persistence/models/__init__.py` exports registered models; `PersistenceConfig.ready()` also imports model-named modules. Inspect aggregate model modules and re-export files before creating a duplicate class.
- Category/Product and many commerce models have `CharField` primary keys generated in `save()` via `shared/id_generator/id_generator.py`. `EcomUser` retains a UUID primary key. Match the model, FK, port, serializer, and URL types; the old blanket UUID rule is stale for formatted IDs.
- Reuse the sequence generator and `IdSequence` for formatted IDs. It uses atomic transactions and row locking; do not replace it with `count()+1` or `max()+1`. Do not reset sequences as a routine migration step.

## Repository and mapper behavior

- Implement the domain repository ABC; keep business-feature ORM queries in repository adapters. Read misses return `None`; update/delete misses raise the feature's semantic exception.
- Use `deleted_at__isnull=True` for soft-deletable resources. Public reads also need the applicable active/published status; admin reads may include inactive rows. Some models, such as Tag, have different deletion semantics: inspect fields before copying filters.
- Keep ownership filters in the actual query, e.g. Order lookup combines `id`, `user_id`, and `deleted_at__isnull=True`.
- Persistence mappers are static: `from_entity(orm_model)` means ORM to domain; `to_model(domain, model_instance=None)` means domain to ORM. Return `None` for a missing input in `from_entity`. Use FK `_id` fields to avoid extra queries and serialize IDs to strings at boundaries.
- Audit actor fields belong to the repository. For nullable fields, distinguish omitted PATCH values in the facade and explicitly assign `None` in the mapper when clearing is intended. Category's current truthy-only parent assignment is not a reliable clearing template.
- Follow the rule's INSERT requirement for new create paths even where existing code differs:

```python
model = CategoryPersistenceMapper.to_model(category)
if actor_id:
    model.created_by_id = actor_id
    model.updated_by_id = actor_id
model.save(force_insert=True)
return CategoryPersistenceMapper.from_entity(model)
```

Updates and soft deletion use ordinary `save()` on fetched rows; `objects.create()` is already INSERT-only. Preserve explicit create-or-update semantics where the port defines them.

## Transactions and schema workflow

- Use `transaction.atomic()` for operations such as order checkout and status/history updates. Atomicity alone does not provide idempotency or prevent concurrent lost updates; use constraints/locks when the requested invariant needs them.
- Fetch related objects with `select_related`/`prefetch_related` where mapping would otherwise issue repeated queries. Count paginated querysets before slicing and apply deterministic ordering.
- Use Django migrations under `infrastructure/persistence/migrations/`; the app label is `persistence`. SQL files under `others/sql/` are references, not a substitute for migration state.
- For a schema task, inspect `makemigrations persistence --dry-run --check`, generate a focused migration, and review its operations and dependencies. Do not regenerate the initial migration or include unrelated drift.
- Apply migrations only against the intended development/test database as part of the authorized task; do not run seed SQL or production data changes merely to inspect a feature.

Examples: `infrastructure/persistence/repository/category_repository_impl.py`, `infrastructure/persistence/mapper/category_persistence_mapper.py`, and `infrastructure/persistence/repository/order_repository_impl.py`. Test collisions, soft-delete visibility, nullable updates, ownership, and rollback where affected.
