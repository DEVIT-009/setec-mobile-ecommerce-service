---
name: setec-testing
description: Adds and runs SETEC Django tests for facades, repositories, APIs, RBAC, and ecommerce workflows. Use for regression coverage, test failures, or verifying a feature; follows the existing unittest and Django TestCase setup.
---

# SETEC testing

Read `others/rule.md` and the affected source before adapting tests. All commands run from the repository root. Use the existing `.venv/bin/python` when available; no pytest dependency or configuration is established in this project.

## Existing suites

- `infrastructure/persistence/tests.py`: `HexagonalArchitectureTestSuite` builds users, store, category, product, variant, and address fixtures; exercises facades, cart checkout, review validation, and address/API behavior.
- `infrastructure/persistence/tests_rbac.py`: `PublicEndpointAccessTest`, `AdminEndpointAccessTest`, and `MultiRoleAccessTest` exercise route access using Django's test client and JWTs from `JwtUtil.generate_token_for_ecom`.
- These are examples, not proof that the baseline passes. `BackwardCompatibilityAliasTest` expects old bare routes that conflict with the no-alias rule and current routing. Diagnose and report that mismatch; do not restore forbidden aliases merely to satisfy stale tests.

## Choose the smallest useful test

- Entity, mapper, or facade decisions: use `unittest`/Django `SimpleTestCase` and injected fake or mock repository ports when no database is needed. Assert output and business effects, not just that one method calls another.
- Repository and integrated facade behavior: use `django.test.TestCase` with real related fixtures. Let models generate formatted IDs; use UUIDs only for UUID-backed resources. Verify audit actors, uniqueness, soft deletion, ownership, and round-trip mapping as applicable.
- API behavior: use Django's test client with real routes and JWT headers. Assert status plus relevant response fields. Cover guest/customer/admin/multi-role access, wrong-owner access, invalid payloads, PATCH omission versus explicit null, and public visibility.
- Transaction/locking changes: use `TransactionTestCase` and an appropriate database backend. SQLite results do not establish PostgreSQL row-lock behavior. Test rollback and collision invariants for sequence or checkout changes.
- Keep external services stubbed. Class-level ViewSet service instances are created at import time; patch the bound service or its dependencies rather than assuming patching the factory later replaces it.

Example adapted from the RBAC suite:

```python
token = JwtUtil.generate_token_for_ecom(self.admin_user)
response = self.client.get(
    '/api/v1/admin/categories/',
    HTTP_AUTHORIZATION=f'Bearer {token}',
)
self.assertEqual(response.status_code, 200, msg=response.content)
self.assertIn('data', response.json())
```

## Run and interpret

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py test infrastructure.persistence.tests_rbac.PublicEndpointAccessTest --verbosity 2
.venv/bin/python manage.py test infrastructure.persistence.tests infrastructure.persistence.tests_rbac --verbosity 2
```

Start with the affected test method/class; broaden to both suites for shared or cross-layer changes. These are reusable commands, not a claim that they passed during skill creation.

Before database tests, verify the configured backend and test-database target without printing credentials. Django creates and removes a test database; use a dedicated development/test configuration and ensure it cannot reuse production data. Do not run against an unknown external database or add `--keepdb` to conceal schema drift.

For schema changes, inspect migration drift with `manage.py makemigrations persistence --dry-run --check` and verify migration behavior on the intended test database. A successful `manage.py check` does not verify database connectivity or all model/migration behavior.

Report the commands run, results, and blockers. Separate pre-existing test/route drift from regressions introduced by the task; never claim unexecuted tests passed.
