---
name: setec-shared
description: Maintains SETEC shared JWT metadata, role checks, response and exception helpers, pagination, ID generation, and runtime configuration. Use when changing cross-feature utilities or integrating their existing contracts; not for routine endpoint scaffolding.
---

# SETEC shared contracts

Read `others/rule.md` and locate callers before changing a helper. All paths are repository-relative. Shared behavior affects multiple features; preserve existing signatures unless the task includes updating callers.

## Reuse the actual utilities

- `shared/metadata_handler/request_header_utillity.py` supplies `Metadata` and `metadata_handler`. Preserve the existing module spelling. It reads bearer tokens, parses comma-separated role claims, and validates sessions for session-bound tokens. Tokens without a session ID are currently accepted by this helper.
- `shared/permission_handler/permission_required.py` supplies `require_roles`, which accepts any matching role; it does not implement a separate fine-grained permission check. Endpoint admin checks use metadata from the outer metadata decorator.
- `shared/security/jwt_authentication.py` is the configured DRF authenticator; `shared/security/jwt_util.py` creates/decodes tokens. SimpleJWT is installed but is not the configured default authenticator. Trace both DRF authentication and metadata processing for auth changes.
- `shared/responseutils/response_handler.py` provides the `api_*` success helpers and older response helpers. New ecommerce endpoints use `api_*`; do not globally rewrite legacy consumers incidentally.
- `shared/exceptionalhandler/exceptional_handler.py` handles serializer validation and other exceptions differently. `BaseAPIException` is DRF-backed and stores `status_code`, `error_code`, and `detail`. Do not assume every error is formatted like an `api_error()` response.
- `shared/pagination/api_paging.py` parses page/page_size, defaults to 1/20, clamps size to 1–100, and handles invalid input. Use its values consistently for query slicing and `ResponseHandler.api_list` metadata.
- `shared/id_generator/id_generator.py` is a database-backed utility despite its shared location. Test it with database transaction semantics rather than treating it as pure string formatting.

Example of shared pagination use:

```python
paging = ApiPaging.from_request(request)
# Pass paging['page'] and paging['page_size'] to the feature service.
# Pass the returned items and unsliced total to ResponseHandler.api_list.
```

## Runtime and integrations

- `_config/settings.py` loads `.env` with django-environ. Required keys include `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `FRONTEND_URL`, and `DATABASE_URL`; preserve secrets outside code and skills.
- `FRONTEND_URL` is parsed as a list and feeds both allowed CORS origins and trusted CSRF origins. Credentials are enabled. Do not replace the origin list with allow-all as a routine frontend integration fix.
- `requirements.txt` pins Django 5.0.1, DRF 3.16.1, django-environ, CORS headers, PyJWT, Cloudinary, Gunicorn, and database drivers. `requirement.txt` also exists and differs; inspect which install command the workflow uses before updating dependencies. The generated settings header is not the runtime version authority.
- `application/upload/upload_service_facade.py` signs Cloudinary upload parameters using settings. Stub external integrations in tests and never expose the API secret in responses or fixtures.
- No repository CI configuration or pytest setup was found during skill creation. Use the established Django checks/tests; recheck the repository before assuming that remains true.

For shared changes, test representative consumers plus the affected helper's edge cases: invalid/expired tokens, revoked sessions, multiple roles, malformed paging, or exception serialization as appropriate.
