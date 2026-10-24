---
name: setec-feature
description: Implements end-to-end features in setec_ecom_service across domain contracts, application facades, persistence adapters, and HTTP interfaces. Use for new features or changes spanning multiple layers; use the focused sibling skills for single-layer tasks.
---

# SETEC feature implementation

Read `others/rule.md` before implementation. Paths below are relative to the repository root. Use Category as the structural reference, but check its current implementation and the discrepancies below before copying it.

## Workflow

1. Trace the closest existing feature from `_config/urls.py` through its ViewSet, factory, facade, domain contracts, repository, and both mappers. Inspect affected callers and tests before changing a signature.
2. Define the domain dataclass in `domain/<feature>/entity/`, repository ABC in `ports/`, service ABC in `service/`, and semantic exceptions in `exception/`. Repository contracts return domain entities; service contracts return response dictionaries/lists.
3. Implement persistence under `infrastructure/persistence/{models,mapper,repository}/`. Keep queries and database transactions there. Use [setec-persistence](../setec-persistence/SKILL.md) for schema and repository work.
4. Implement the facade in `application/<feature>/<feature>_service_facade.py`, injecting repository interfaces. The factory in `factory/` wires concrete adapters and returns the service interface. Use [setec-business-logic](../setec-business-logic/SKILL.md) for use-case rules.
5. Add request serializers, response dataclasses, controller mapper, scoped ViewSets, and explicit URL mappings under `interface/<feature>/`. Use [setec-api](../setec-api/SKILL.md) for HTTP details.
6. Reuse shared authentication, response, pagination, and exception helpers; consult [setec-shared](../setec-shared/SKILL.md) when changing those contracts. Verify behavior with [setec-testing](../setec-testing/SKILL.md).
7. Update `openapi.yaml` and relevant integration documentation when the requested change alters the public contract; compare them with executable routes rather than assuming they are current.

## Actual reference chain

- `interface/category/view/category_admin_view.py` validates requests and calls its own service interface.
- `application/category/factory/category_service_factory.py` injects **both** category and product repositories into `CategoryServiceFacade`.
- `application/category/category_service_facade.py` coordinates uniqueness, parent validation, and controller mapping.
- `infrastructure/persistence/repository/category_repository_impl.py` owns queries and persistence mapping.
- `interface/category/serializer/mapper/category_controller_mapper.py` uses `asdict(CategoryResponse(...))`.

## Rules versus existing code

- The rules prescribe UUIDs, but Category/Product and many other resources now use formatted string IDs. Their models, migrations, ID generator, and routes agree on that contract. Preserve it; do not introduce UUID validation for `cat-000001`. User IDs still use UUIDs.
- The rules contradict themselves about split URL files. For new features, prefer Category's single scoped URL module. Preserve existing route composition for focused changes; do not silently reorganize unrelated routes or add compatibility aliases.
- Domain entities and ports stay framework-free. Existing domain exceptions deliberately inherit the DRF-backed `BaseAPIException`, an explicit exception to the rule document's broad purity statement.
- Auth has direct ORM access in its facade, and shared helpers also query models. These are existing boundary deviations, not templates for new business features.
- The explicit `force_insert=True` requirement in the rules still applies to new create implementations, even though Category currently uses plain `save()`.

Keep changes within the requested feature. Existing legacy files do not authorize a repository-wide cleanup.
