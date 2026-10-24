---
name: setec-api
description: Adds or changes SETEC Django REST Framework endpoints, request validation, response mapping, scoped routes, and access controls. Use for HTTP contract work in interface; excludes repository implementation and business-rule design.
---

# SETEC APIs

Read `others/rule.md` and the affected feature's URL module plus `_config/urls.py`. All source paths here are repository-relative.

## Implement the HTTP boundary

- Use `viewsets.ViewSet`, one class per scope file: `<feature>_public_view.py`, `<feature>_customer_view.py`, or `<feature>_admin_view.py`. Create only needed scopes. Do not introduce APIView, generic views, ModelSerializer, or legacy unscoped view filenames.
- Inject the feature's factory result at class level, typed as its domain service interface. Keep per-request state out of that shared service instance.
- Validate with `Serializer` and `is_valid(raise_exception=True)`. Put full and partial request classes together; partial fields are optional and must not inject defaults for omitted values. Pass `validated_data` to the facade, never raw request data.
- Facades call `ControllerMapper.from_request()` and `to_response()`. Views do not perform domain mapping. Response DTOs are dataclasses; controller mappers serialize with `asdict()`.
- Public actions use `@metadata_handler(required_user_id=False)`. Customer actions require a user; admin actions additionally use `@require_roles("admin")`, inside the metadata decorator. Signatures include keyword-only `metadata: Metadata`.
- Obtain customer identity and audit actors from `metadata.user_id`. Pass the identity into ownership-aware service operations, not a client-supplied user ID.

Example from the Category admin pattern:

```python
@metadata_handler(required_user_id=True)
@require_roles("admin")
def create(self, request: Request, *, metadata: Metadata):
    serializer = CategoryRequest(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = self.category_service.create(
        serializer.validated_data, actor_id=metadata.user_id,
    )
    return ResponseHandler.api_created(result)
```

Imports live in `shared.metadata_handler.request_header_utillity` (retain that spelling), `shared.permission_handler`, and `shared.responseutils.response_handler`.

## Routes and response contracts

- Use explicit `.as_view({'get': 'list', 'post': 'create'})` mappings. Custom actions are mapped directly; no router or `@action` is required.
- Prefer one `<feature>_url.py` with public/customer/admin prefixes for new features. Existing features sometimes split modules or receive prefixes from root includes. Resolve the full path to avoid double prefixes; retain established routing when a task does not request migration.
- Category uses `<str:category_id>` because its IDs are formatted strings. Follow the actual model ID type, despite older UUID examples in the rules. Put static `search/` and `tree/` routes before string captures. Slug lookup is `search/?slug=...`; writes use resource IDs.
- Use `ResponseHandler.api_success`, `api_created`, `api_no_content`, and `api_list`. A 204 has no JSON body. Paginated lists take page/page_size from `ApiPaging.from_request()` and preserve the repository's total.
- Successful API responses use `{data, meta, errors}`. Existing exception responses do not uniformly use that envelope: inspect `shared/exceptionalhandler/exceptional_handler.py` and assert the actual error contract.
- Check guest/customer/admin access, another user's resource, invalid payloads, omitted PATCH fields, and inactive/deleted visibility. Public detail methods are not guaranteed to filter inactive records merely because list methods do.

Concrete references: `interface/category/url/category_url.py`, `interface/category/serializer/request/category_request.py`, `interface/category/serializer/mapper/category_controller_mapper.py`, and `interface/address/view/address_customer_view.py`.
