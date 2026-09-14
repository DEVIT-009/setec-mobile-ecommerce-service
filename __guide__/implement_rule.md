# 📐 Development Architecture Rules

> **Standard Reference Implementation**: `Category` (`interface/category`, `application/category`, `domain/category`, `infrastructure/persistence/.../category_*`)

This document defines the strict, non-negotiable architectural rules for the **SETEC eCommerce Service**. All developers and AI assistants must adhere to these rules when creating, modifying, or refactoring features.

---

## 1. Architectural Layers & Dependency Flow

The system follows **Clean / Hexagonal Architecture (Ports and Adapters)**.

```
[ Interface Layer ] (HTTP, URLs, ViewSets, Serializers, Controller Mappers)
        │
        ▼
[ Application Layer ] (Service Facades, Service Factories / DI)
        │
        ▼
[ Domain Layer ] (Entities, Service Interfaces, Repository Ports, Domain Exceptions)
        ▲
        │
[ Infrastructure Layer ] (ORM Models, Persistence Mappers, Repository Implementations)
```

### Dependency Rules:
1. **Inward Dependency Flow**: Dependencies point inwards toward the Domain.
2. **Domain Purity**: The Domain layer is pure Python (`dataclasses`, `typing`, `abc`, `uuid`, `datetime`). It **MUST NEVER** import from Django, DRF, or any outer layer (`application`, `interface`, `infrastructure`).
3. **No Direct ORM in Views or Facades**: Only Repository Implementations in `infrastructure/persistence/repository/` may query the database via Django ORM.
4. **Service Segregation**: A feature's view must interact with its **own** dedicated service facade (e.g., Tag views use `TagServiceInterface`, Category views use `CategoryServiceInterface`). Never cross-map to unrelated domain facades.
5. **Application may import Interface Mapper**: The `ServiceFacade` (Application layer) **may** import `ControllerMapper` from the Interface layer to convert domain entities to response dicts. This is the only permitted upward import.

---

## 2. Cross-Layer Data Mapping Lifecycle

Data transformations across layers must follow this exact sequence:

```
1. HTTP Request (JSON)
      │
      ▼  [DRF Serializer: CategoryRequest / CategoryPartialRequest]
2. Validated Dict (`serializer.validated_data`)
      │
      ▼  [Controller Mapper: CategoryControllerMapper.from_request()]  ← called inside ServiceFacade
3. Domain Entity (`domain.category.entity.Category`)
      │
      ▼  [Persistence Mapper: CategoryPersistenceMapper.to_model()]
4. Django ORM Model (`infrastructure.persistence.models.category_model.Category`)
      │
      ▼  [Database Query / Save via Repository Implementation]
5. Django ORM Model
      │
      ▼  [Persistence Mapper: CategoryPersistenceMapper.from_entity()]
6. Domain Entity (`domain.category.entity.Category`)
      │
      ▼  [Controller Mapper: CategoryControllerMapper.to_response()]   ← called inside ServiceFacade
7. Response Dataclass (`CategoryResponse`) serialized to Dict via `asdict()`
      │
      ▼  [Shared: ResponseHandler.api_success / api_created / api_list / api_no_content]
8. HTTP Response (Standard JSON format: `{ "data": ..., "meta": ..., "errors": [] }`)
```

### When each mapper is called:
| Mapper | Method | Location Called | Purpose |
|---|---|---|---|
| **Request Serializer** | `is_valid(raise_exception=True)` | `ViewSet` (Interface) | Validates HTTP payload before passing into application layer. |
| **Controller Mapper** | `from_request(validated_data)` | `ServiceFacade` (Application) | Converts validated dict into a clean Domain Entity. |
| **Persistence Mapper** | `to_model(domain, model_instance=None)` | `RepositoryImpl` (Infrastructure) | Converts Domain Entity to Django ORM Model for DB insert/update. |
| **Persistence Mapper** | `from_entity(model_instance)` | `RepositoryImpl` (Infrastructure) | Converts ORM Model instance back into pure Domain Entity. |
| **Controller Mapper** | `to_response(domain_entity)` | `ServiceFacade` (Application) | Converts Domain Entity into client response dict (via `asdict(ResponseDTO)`). |
| **ResponseHandler** | `api_success`, `api_created`, `api_list`, `api_no_content` | `ViewSet` (Interface) | Formats final HTTP response envelope and status code. |

> **Note**: `from_request` and `to_response` are NEVER called directly in the ViewSet. They are called inside the ServiceFacade, keeping the ViewSet thin.

---

## 3. Interface Layer Rules (`interface/<feature>/`)

### 3.1. ViewSet Requirement (NO APIView)
- All views **MUST** inherit from `rest_framework.viewsets.ViewSet`.
- **NEVER** use `rest_framework.views.APIView` or generic class-based views (`generics.*`).

### 3.2. View File Naming by Access Scope
Every view file name **MUST** reflect its access scope. There are exactly **three** valid scopes:

| Scope | File Name | Auth | Who Can Access |
|---|---|---|---|
| **Public** | `<feature>_public_view.py` | ❌ None | Guests, customers, admins |
| **Customer** | `<feature>_customer_view.py` | ✅ Customer JWT | Logged-in customers (and admins acting as customers) |
| **Admin** | `<feature>_admin_view.py` | ✅ JWT + `admin` role | Admins only |

#### Rules:
- **Create only the files that the feature actually needs.** A pure customer-scoped feature needs only `<feature>_customer_view.py`. A feature with both public and admin operations needs exactly `<feature>_public_view.py` + `<feature>_admin_view.py`.
- **Mixed public + customer** (no admin): `<feature>_public_view.py` + `<feature>_customer_view.py`.
- **Mixed public + admin**: `<feature>_public_view.py` + `<feature>_admin_view.py`.
- **Mixed customer + admin** (no public read): `<feature>_customer_view.py` + `<feature>_admin_view.py`.
- **All three tiers active**: `<feature>_public_view.py` + `<feature>_customer_view.py` + `<feature>_admin_view.py`.
- ❌ **Never create** `<feature>_view.py` — this is the legacy pattern and is **forbidden**.
- ❌ **Never create deprecated shim files** (e.g., `store_view.py` re-exporting another class). Once a view is refactored, the old file must be **deleted immediately** — no compat wrappers.
- ❌ **Never use the wrong scope name** — a customer-scoped view named `<feature>_view.py` or `<feature>_public_view.py` violates this rule.

#### Examples:
- ✅ `category_admin_view.py` + `category_public_view.py` → Admin + Public feature (2 files).
- ✅ `address_customer_view.py` → Customer-only feature (1 file).
- ✅ `legal_document_view.py`... ❌ No — must be `legal_document_public_view.py` + `legal_document_customer_view.py`.
- ❌ `address_view.py` → forbidden legacy naming.
- ❌ `store_admin_view.py` + `store_public_view.py` + `store_view.py` → extra `store_view.py` violates this rule.

### 3.3. Single Class Per View File Rule
- **Each view file MUST contain ONLY ONE ViewSet class.**
- ❌ **Do NOT** put `AdminListView` and `AdminDetailView` in the same file or split list/detail into separate classes. A ViewSet handles `list`, `create`, `retrieve`, `update`, `partial_update`, and `destroy` inside a single class.

### 3.4. ViewSet Structure & Decorators

**Admin ViewSet** (full CRUD, role-protected):
```python
from rest_framework import viewsets
from rest_framework.request import Request

from application.category.factory.category_service_factory import category_service_factory
from domain.category.exception.category_exception import CategoryException
from domain.category.service.category_service import CategoryServiceInterface
from interface.category.serializer.request.category_request import CategoryRequest, CategoryPartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class CategoryAdminView(viewsets.ViewSet):
    # Service injected at class level via factory, typed to interface (not implementation)
    category_service: CategoryServiceInterface = category_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        result = self.category_service.list_admin()
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        serializer = CategoryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.create(serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, category_id=None, *, metadata: Metadata):
        # UUID path parameter only — slug lookup uses retrieve_by_slug
        if category_id is None:
            raise CategoryException.not_found()
        result = self.category_service.get_by_id(str(category_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        # Slug as QUERY PARAMETER: GET /admin/categories/search/?slug=<slug>
        # No path parameter — slug is NEVER a path parameter for write operations
        slug = request.query_params.get('slug')
        if not slug:
            raise CategoryException.not_found("Slug query parameter is required")
        result = self.category_service.get_admin(slug)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, category_id=None, *, metadata: Metadata):
        # Write operations ONLY accept UUID path parameter — never slug
        if category_id is None:
            raise CategoryException.not_found()
        serializer = CategoryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.update(str(category_id), serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        serializer = CategoryPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.update(str(category_id), serializer.validated_data, partial=True, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        self.category_service.soft_delete(str(category_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
```

**Public ViewSet** (read-only, no authentication required):
```python
class CategoryPublicView(viewsets.ViewSet):
    """Public category ViewSet (guest access)."""

    category_service: CategoryServiceInterface = category_service_factory()

    @metadata_handler(required_user_id=False)    # No @require_roles for public endpoints
    def list(self, request: Request, *, metadata: Metadata):
        result = self.category_service.list_active()
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve(self, request: Request, category_id=None, *, metadata: Metadata):
        # UUID path parameter only
        if category_id is None:
            raise CategoryException.not_found()
        result = self.category_service.get_by_id(str(category_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        # Slug as QUERY PARAMETER: GET /public/categories/search/?slug=<slug>
        slug = request.query_params.get('slug')
        if not slug:
            raise CategoryException.not_found("Slug query parameter is required")
        result = self.category_service.get_by_slug(slug)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)    # Custom non-standard action is allowed
    def tree(self, request: Request, *, metadata: Metadata):
        result = self.category_service.get_tree()
        return ResponseHandler.api_success(result)
```

**Decorator & Signature Rules:**
- **Decorator order**: `@metadata_handler(...)` outermost, `@require_roles(...)` inside.
- **Method signature**: Always include `*, metadata: Metadata` as keyword-only parameter.
- **Public endpoints**: Use `@metadata_handler(required_user_id=False)` — **NO** `@require_roles`.
- **Admin endpoints**: Use `@metadata_handler(required_user_id=True)` AND `@require_roles("admin")`.
- **Payload Validation**: Always validate `request.data` using the appropriate `<Feature>Request(data=request.data)` serializer and call `serializer.is_valid(raise_exception=True)`. **Never** pass raw `request.data` to the service.
- **ID Guard**: Before any write operation on a resource, guard against missing `category_id` by raising `CategoryException.not_found()` if it is `None`.

### 3.5. Serializers, DTOs & Mappers

**Request Serializers** (`interface/<feature>/serializer/request/<feature>_request.py`):
- Inherit from `rest_framework.serializers.Serializer` (**NOT** `ModelSerializer`).
- Define `<Feature>Request` for full creates/updates (all required fields are `required=True` by default).
- Define `<Feature>PartialRequest` with `required=False` on **all** fields for `patch` updates.
- Both classes live in the **same** file.
- `ChoiceField` with explicit `choices` list for enum-type fields (e.g., `status`).

```python
class CategoryRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(choices=["active", "inactive"], default="active", required=False)

class CategoryPartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(max_length=255, required=False)
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(choices=["active", "inactive"], required=False)
```

**Response DTO** (`interface/<feature>/serializer/response/<feature>_response.py`):
- Plain Python `@dataclass`.
- Typed fields representing what the frontend receives.
- May include a `to_dict()` helper, but the Controller Mapper **MUST** use `dataclasses.asdict()` for serialization.
- IDs are `Optional[str]` (converted from UUID to string before populating the DTO).

**Controller Mapper** (`interface/<feature>/serializer/mapper/<feature>_controller_mapper.py`):
- A plain class with **static methods only** — never instantiated.
- Required static methods:
  - `from_request(validated_data: Dict[str, Any]) -> DomainEntity` — builds Domain Entity from validated dict.
  - `to_response(entity: DomainEntity) -> Dict[str, Any]` — returns `asdict(ResponseDTO(...))`.
  - `to_list_response(entities: List[DomainEntity]) -> List[Dict[str, Any]]` — calls `to_response` for each item.
- UUID-to-string conversion (`str(entity.id) if entity.id else None`) is done **here**, not in the domain or repository.

### 3.6. URL Routing (`interface/<feature>/url/<feature>_url.py`)

#### ✅ One URL File Per Feature
- Each feature **MUST have exactly ONE URL file**: `interface/<feature>/url/<feature>_url.py`.
- ❌ **Never split** into `<feature>_admin_url.py`, `<feature>_public_url.py`, or any other split. All routes live in the **single** `<feature>_url.py` file.
- ❌ **Never leave old split URL files** as dead code. If a legacy `_admin_url.py` or `_public_url.py` existed during refactoring, it **must be deleted** once the unified `_url.py` is in place.
- ✅ **Correct**: `interface/category/url/category_url.py` → 1 file containing all routes.
- ❌ **Wrong**: `interface/store/url/store_url.py` + `store_admin_url.py` + `store_public_url.py` → 3 files.
- Included in root `_config/urls.py` as: `path('api/v1/', include('interface.<feature>.url.<feature>_url'))`.

#### Route Prefix Convention

Three first-class URL tiers exist. Every route **MUST** fall into exactly one:

| Tier | Prefix | Auth Required | Who can access |
|---|---|---|---|
| **Public** | `public/<feature>/...` | ❌ None | Guests, customers, admins |
| **Customer** | `customer/<feature>/...` | ✅ Valid customer JWT | Logged-in customers (and admins acting as customers) |
| **Admin** | `admin/<feature>/...` | ✅ JWT + `admin` role | Admins only |

- **Admin routes** MUST be prefixed with `admin/<feature>/...`
- **Public routes** MUST be prefixed with `public/<feature>/...`
- **Customer-only routes** MUST be prefixed with `customer/<feature>/...`
- ❌ **Never register bare `<feature>/...` routes** (e.g., `categories/`, `users/`). These are forbidden.
- ❌ **No backward-compatibility aliases** without a prefix. If a client uses the wrong URL, update the client — do not add a compat route.
- ❌ **Do NOT duplicate** a route across tiers. If a route is public, it lives **only** in `public/`. If it requires a customer login, it lives **only** in `customer/`. Never register the same endpoint under both.

##### When to use `customer/<feature>/...`
A route belongs under `customer/` when **all** of the following are true:
1. The view uses `@metadata_handler(required_user_id=True)`.
2. The resource is owned by or scoped to the currently logged-in user (not an admin managing other users).
3. The action is not publicly readable by unauthenticated guests.

##### Mixed-auth features (some actions public, some customer-only)
When a feature has **both** public actions and customer-only actions, split into two URL files:
- `interface/<feature>/url/<feature>_public_url.py` → public actions → registered under `api/v1/public/<feature>/`
- `interface/<feature>/url/<feature>_customer_url.py` → customer-only actions → registered under `api/v1/customer/<feature>/`

> **Example**: `legal-documents` — `GET /public/legal-documents/` (list/latest) is public; `POST /customer/legal-documents/<id>/accept/` requires a customer JWT.

```python
# interface/legal_document/url/legal_document_url.py  (public)
urlpatterns = [
    path('', LegalDocumentListView.as_view({'get': 'list'}), name='public-legal-document-list'),
    path('<str:type>/latest/', LegalDocumentLatestView.as_view({'get': 'retrieve'}), name='public-legal-document-latest'),
]

# interface/legal_document/url/legal_document_customer_url.py  (customer-only)
urlpatterns = [
    path('<uuid:legal_document_id>/accept/', LegalDocumentAcceptView.as_view({'post': 'accept'}), name='customer-legal-document-accept'),
]
```

```python
# _config/urls.py
path('api/v1/public/legal-documents/',   include('interface.legal_document.url.legal_document_url')),
path('api/v1/customer/legal-documents/', include('interface.legal_document.url.legal_document_customer_url')),
```

##### Full list of customer-scoped features (registered in `_config/urls.py`)
```python
path('api/v1/customer/users/',           include('interface.user.url.user_url')),
path('api/v1/customer/addresses/',       include('interface.address.url.address_url')),
path('api/v1/customer/orders/',          include('interface.order.url.order_url')),
path('api/v1/customer/shipments/',       include('interface.shipment.url.shipment_url')),
path('api/v1/customer/search-history/',  include('interface.search_history.url.search_history_url')),
path('api/v1/customer/favorites/',       include('interface.favorite.url.favorite_url')),
path('api/v1/customer/cart/',            include('interface.cart.url.cart_url')),
path('api/v1/customer/conversations/',   include('interface.conversation.url.conversation_url')),
path('api/v1/customer/messages/',        include('interface.conversation.url.message_url')),
path('api/v1/customer/notifications/',   include('interface.notification.url.notification_url')),
path('api/v1/customer/support/',         include('interface.support_ticket.url.support_ticket_url')),
path('api/v1/customer/legal-documents/', include('interface.legal_document.url.legal_document_customer_url')),
path('api/v1/customer/uploads/',         include('interface.upload.url.upload_url')),
```

##### Exceptions (not under `customer/`)
| Route | Why it stays outside `customer/` |
|---|---|
| `/api/v1/auth/` | Auth is its own namespace; register/login/forgot-password are public; logout/me are customer-scoped but kept together for discoverability. |
| `/api/v1/home/` | Home feed is public by design (`required_user_id=False, optional_user_id=True`). User ID is optional — it personalises the feed when present but is not required. |


#### General URL Rules
- Explicitly map ViewSet actions using `.as_view({http_method: action_name})`.
- **Standard actions**: `list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`.
- **Custom (non-standard) actions** (e.g., `tree`, `retrieve_by_slug`): map directly using `.as_view({'get': 'tree'})` — no `@action` decorator needed when routing manually.
- Route names follow pattern: `<scope>-<resource>-<action>` (e.g., `admin-category-list-create`, `public-category-tree`).

#### Path Parameter vs Query Parameter Rules:
- **UUID path parameter** (`<uuid:category_id>`): used for all **write operations** (`PUT`, `PATCH`, `DELETE`) and ID-based `GET retrieve`.
- **Slug is NEVER a path parameter**. Slug lookups are always via **query parameter** on a dedicated `/search/` endpoint: `GET /public/categories/search/?slug=<slug>`.
- Write operations (`PUT`, `PATCH`, `DELETE`) **only** accept UUID path parameters — never slug.

```python
from django.urls import path
from interface.category.view.category_admin_view import CategoryAdminView
from interface.category.view.category_public_view import CategoryPublicView

urlpatterns = [
    # Admin routes — prefix: admin/<feature>/
    path('admin/categories/', CategoryAdminView.as_view({'get': 'list', 'post': 'create'}), name='admin-category-list-create'),
    path('admin/categories/search/', CategoryAdminView.as_view({'get': 'retrieve_by_slug'}), name='admin-category-search'),  # ?slug=
    path('admin/categories/<uuid:category_id>/', CategoryAdminView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='admin-category-detail'),

    # Public routes — prefix: public/<feature>/
    path('public/categories/', CategoryPublicView.as_view({'get': 'list'}), name='public-category-list'),
    path('public/categories/tree/', CategoryPublicView.as_view({'get': 'tree'}), name='public-category-tree'),
    path('public/categories/search/', CategoryPublicView.as_view({'get': 'retrieve_by_slug'}), name='public-category-search'),  # ?slug=
    path('public/categories/<uuid:category_id>/', CategoryPublicView.as_view({'get': 'retrieve'}), name='public-category-detail'),
]
```

> **Order matters**: Register static paths (e.g., `public/categories/tree/`, `public/categories/search/`) **before** parameterized paths (e.g., `public/categories/<uuid:category_id>/`) to prevent Django from trying to match the static segment as a UUID.

---



## 4. Application Layer Rules (`application/<feature>/`)

### 4.1. Service Facade (`<feature>_service_facade.py`)
- Implements the Domain Service Interface:
  ```python
  class CategoryServiceFacade(CategoryServiceInterface):
      def __init__(self, repo: CategoryRepositoryInterface):
          self.repo = repo
  ```
- **Coordinates business use-cases**: Enforces uniqueness, validates hierarchical relationships, coordinates domain logic.
- Calls `ControllerMapper.from_request(...)` to convert validated data into a Domain Entity.
- Calls `ControllerMapper.to_response(...)` / `to_list_response(...)` before returning to the ViewSet.
- Returns Python primitives (`Dict[str, Any]`, `List[Dict[str, Any]]`) to the View — **never** Domain Entities.
- **NEVER** imports `django.db`, ORM models, or issues raw queries.
- **Private helpers** (`_method_name`): Complex internal logic (e.g., finding by id-or-slug, recursive tree building) MUST be extracted into private helper methods prefixed with `_`.

**Partial Update Pattern** — mutate the fetched entity, then save:
```python
def update(self, resource_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
    existing = self.repo.get_by_id(resource_id)
    if not existing:
        raise FeatureException.not_found()

    # Only update fields present in data (when partial=True)
    if 'name' in data:
        existing.name = data['name']
    if 'slug' in data:
        new_slug = data['slug']
        if new_slug != existing.slug:
            if self.repo.exists_by_slug(new_slug, exclude_id=existing.id):
                raise FeatureException.already_exists(...)
            existing.slug = new_slug

    saved = self.repo.update(existing, actor_id=actor_id)
    return ControllerMapper.to_response(saved)
```

**Business validation sequence for `create`**:
1. Validate required fields from `data` (raise domain exception if missing).
2. Check uniqueness (slug, name, etc.) via `repo.exists_by_*`.
3. Validate relational integrity (e.g., parent exists) via `repo.get_by_id`.
4. Call `ControllerMapper.from_request(data)` to build the entity.
5. Call `repo.create(entity, actor_id=actor_id)`.
6. Return `ControllerMapper.to_response(saved)`.

### 4.2. Factory (`application/<feature>/factory/<feature>_service_factory.py`)
- Exports a **single factory function** returning the **interface** type (not the concrete class).
- Wires the concrete infrastructure repository implementation into the application facade.
```python
def category_service_factory() -> CategoryServiceInterface:
    repo = CategoryRepositoryInterfaceImpl()
    return CategoryServiceFacade(repo)
```
- Called at **class level** in the ViewSet (`service = factory()`), creating one instance per server process.

---

## 5. Domain Layer Rules (`domain/<feature>/`)

### 5.1. Entity (`domain/<feature>/entity/<feature>.py`)
- Pure Python `@dataclass` with `from dataclasses import dataclass, field`.
- All fields have sensible defaults (`None` or empty string / 0 / list).
- IDs typed as `Optional[str] = None` (stored as strings, not `uuid.UUID`).
- **Audit fields** (`created_at`, `updated_at`, `deleted_at`) typed as `Optional[datetime] = None` — always present on entities that support soft deletion.
- **Nested/relationship fields** (e.g., `children: List['FeatureName'] = field(default_factory=list)`) are allowed for tree or aggregated representations, defaulting to empty list.
- **Zero** external framework imports — only `uuid`, `datetime`, `dataclasses`, `typing`.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Category:
    id: Optional[str] = None
    parent_id: Optional[str] = None
    name: str = ""
    slug: str = ""
    sort_order: int = 0
    status: str = "active"
    children: List['Category'] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
```

### 5.2. Service Interface (`domain/<feature>/service/<feature>_service.py`)
- Abstract base class inheriting from `abc.ABC`.
- All methods decorated with `@abstractmethod`.
- Methods return **primitives** (`Dict[str, Any]`, `List[Dict[str, Any]]`, `None`) — not Domain Entities. This is the contract the View depends on.
- Write methods accept `actor_id: Optional[str] = None` for audit purposes.
- Beyond standard CRUD, define any domain-specific query methods (e.g., `get_tree()`, `get_admin()`, `get_by_slug()`).

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class CategoryServiceInterface(ABC):
    @abstractmethod
    def list_active(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def get_tree(self) -> List[Dict[str, Any]]: pass
    @abstractmethod
    def create(self, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def update(self, resource_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]: pass
    @abstractmethod
    def soft_delete(self, resource_id: str, actor_id: Optional[str] = None) -> None: pass
```

### 5.3. Repository Interface / Port (`domain/<feature>/ports/<feature>_repository.py`)
- Abstract base class inheriting from `abc.ABC`.
- Operates strictly on **Domain Entities** — parameters and return types are Domain Entities or primitives (`str`, `bool`, `Optional[Entity]`, `List[Entity]`), **never** ORM models.
- **Read methods** return `Optional[DomainEntity]` (return `None` if not found — **do not raise** exceptions).
- **Existence check methods** (`exists_by_slug`, `exists_by_name`): return `bool`, accept optional `exclude_id` for uniqueness checks during updates.
- **Write methods** (`create`, `update`) accept `actor_id: Optional[str] = None` and return the saved Domain Entity.
- **Soft delete** accepts `actor_id: Optional[str] = None` and returns `None`.

```python
class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[Category]: pass
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Category]: pass
    @abstractmethod
    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool: pass
    @abstractmethod
    def create(self, category: Category, actor_id: Optional[str] = None) -> Category: pass
    @abstractmethod
    def update(self, category: Category, actor_id: Optional[str] = None) -> Category: pass
    @abstractmethod
    def soft_delete(self, category_id: str, actor_id: Optional[str] = None) -> None: pass
```

### 5.4. Domain Exceptions (`domain/<feature>/exception/<feature>_exception.py`)
- Inherits from `shared.exceptionalhandler.base_api_exception.BaseAPIException`.
- Provides **semantic factory class methods** named after business scenarios (not HTTP codes).
- **Exception code format**: `SCREAMING_SNAKE_CASE` prefixed with the feature name (e.g., `CATEGORY_NOT_FOUND`, `CATEGORY_ALREADY_EXISTS`).
- **Always supply a sensible default message** in the class method signature.
- Exceptions are raised in the **ServiceFacade** and in the **RepositoryImpl** (for write operations that find the record missing). **Never** raised in the Domain Entity or PersistenceMapper.

```python
from rest_framework import status
from shared.exceptionalhandler.base_api_exception import BaseAPIException

class CategoryException(BaseAPIException):
    @classmethod
    def not_found(cls, message: str = "Category not found"):
        return cls.create(status.HTTP_404_NOT_FOUND, message, "CATEGORY_NOT_FOUND")

    @classmethod
    def already_exists(cls, message: str = "Category already exists"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "CATEGORY_ALREADY_EXISTS")

    @classmethod
    def invalid_parent(cls, message: str = "Invalid parent category"):
        return cls.create(status.HTTP_400_BAD_REQUEST, message, "INVALID_PARENT_CATEGORY")
```

---

## 6. Infrastructure Layer Rules (`infrastructure/persistence/`)

### 6.1. Django ORM Model (`models/<feature>_model.py`)
- Primary key is always a UUID: `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`.
- Explicit `db_table` in `class Meta` (plural snake_case, e.g., `'categories'`).
- **Soft deletion** via `deleted_at = models.DateTimeField(null=True, blank=True)`.
- **Audit relationships** (`created_by`, `updated_by`, `deleted_by`) link to `EcomUser` with `related_name='+'` (no reverse accessor needed).
- **Status fields** use `STATUS_CHOICES` list defined at the top of the class.
- **Self-referencing FK** for tree structures: `parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')`.
- `class Meta` should include database **indexes** for frequently filtered fields.
- Include a `__str__` method returning a meaningful string representation (e.g., `self.name`).

```python
class Category(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(EcomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'categories'
        indexes = [models.Index(fields=['status']), models.Index(fields=['parent'])]

    def __str__(self):
        return self.name
```

### 6.2. Persistence Mapper (`mapper/<feature>_persistence_mapper.py`)
- A plain class with **static methods only** — never instantiated.
- Method naming convention:
  - `from_entity(entity: Optional[OrmModel]) -> Optional[DomainEntity]` — converts ORM Model → Domain Entity. *(Note: parameter is named `entity` but refers to the ORM model instance.)*
  - `to_model(domain: DomainEntity, model_instance: Optional[OrmModel] = None) -> OrmModel` — converts Domain Entity → ORM Model. When `model_instance` is provided (update), it mutates the existing model; when `None` (create), it creates a new model instance.
- **UUID-to-string**: Cast UUIDs to `str` (`str(entity.id)`) in `from_entity`.
- **FK parent_id** handling: Access `entity.parent_id` (not `entity.parent.id`) to avoid extra DB queries.
- **NEVER** raises exceptions — silently returns `None` if input is `None`.
- **Does NOT map audit fields** on `to_model` (those are set by the Repository Implementation, not the mapper). `from_entity` **does** map audit datetime fields to the domain entity.

```python
class CategoryPersistenceMapper:
    @staticmethod
    def from_entity(entity: Optional[CategoryModel]) -> Optional[Category]:
        if entity is None:
            return None
        return Category(
            id=str(entity.id),
            parent_id=str(entity.parent_id) if entity.parent_id else None,
            name=entity.name,
            slug=entity.slug,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: Category, model_instance: Optional[CategoryModel] = None) -> CategoryModel:
        model = model_instance or CategoryModel()
        if domain.parent_id:
            model.parent_id = domain.parent_id
        model.name = domain.name
        model.slug = domain.slug
        model.status = domain.status
        return model
```

### 6.3. Repository Implementation (`repository/<feature>_repository_impl.py`)
- Class name convention: `<Feature>RepositoryInterfaceImpl` (e.g., `CategoryRepositoryInterfaceImpl`).
- Implements `<Feature>RepositoryInterface`.
- Encapsulates **ALL** Django ORM queries (`.filter(...)`, `.create(...)`, `.save(...)`, `.exclude(...)`).
- **Module-level `_is_uuid` helper** — always include to prevent DB errors on malformed UUID lookups:
  ```python
  def _is_uuid(val: str) -> bool:
      try:
          uuid.UUID(str(val))
          return True
      except (ValueError, AttributeError, TypeError):
          return False
  ```
- **Soft-delete filter**: All read queries **must** include `deleted_at__isnull=True` unless explicitly querying deleted records.
- **Read methods** (`get_by_id`, `get_by_slug`) return `None` if not found — **do NOT raise** here.
- **Write methods** (`update`, `soft_delete`) raise `<Feature>Exception.not_found()` if the record is missing at the point of mutation.
- **Actor audit fields** (`created_by_id`, `updated_by_id`, `deleted_by_id`): set directly on the model in the repository (not in the mapper):
  ```python
  if actor_id:
      model.created_by_id = actor_id
      model.updated_by_id = actor_id
  model.save()
  ```
- **Soft delete implementation**: set `model.deleted_at = timezone.now()` and optionally `model.deleted_by_id = actor_id`, then `model.save()`.
- Calls `PersistenceMapper` to convert between DB models and Domain Entities — never manually construct Domain Entities in the repository.
- **Ordering**: default ordering should be applied at query level (e.g., `.order_by('sort_order', 'name')`).

---

## 7. Summary Checklist for New / Refactored Features

| Step | Layer | File to Create / Check | Check Rule |
|---|---|---|---|
| 1 | Domain | `domain/<feat>/entity/<feat>.py` | Plain `@dataclass`, no ORM imports, audit datetime fields, `children` list if tree. |
| 2 | Domain | `domain/<feat>/exception/<feat>_exception.py` | Inherits `BaseAPIException`, semantic `@classmethod`s, `FEAT_ERROR_CODE` format. |
| 3 | Domain | `domain/<feat>/ports/<feat>_repository.py` | `ABC`, operates only with Domain Entities, read methods return `None` (no raise). |
| 4 | Domain | `domain/<feat>/service/<feat>_service.py` | `ABC`, returns primitives (Dict/List), `actor_id` on write methods. |
| 5 | Infrastructure | `infrastructure/persistence/models/<feat>_model.py` | UUID PK, soft delete, audit fields, `STATUS_CHOICES`, indexes, `__str__`. |
| 6 | Infrastructure | `infrastructure/persistence/mapper/<feat>_persistence_mapper.py` | Static `from_entity` and `to_model`, UUID→str cast, no exceptions. |
| 7 | Infrastructure | `infrastructure/persistence/repository/<feat>_repository_impl.py` | `_is_uuid` helper, `deleted_at__isnull=True` filter, actor fields set in repo. |
| 8 | Application | `application/<feat>/<feat>_service_facade.py` | Implements service interface, partial-update pattern, private helpers for complex logic. |
| 9 | Application | `application/<feat>/factory/<feat>_service_factory.py` | Single factory function returning interface type. |
| 10 | Interface | `interface/<feat>/serializer/request/<feat>_request.py` | `Serializer` (both `Request` and `PartialRequest` in same file). |
| 11 | Interface | `interface/<feat>/serializer/response/<feat>_response.py` | Plain `@dataclass` Response DTO, `Optional[str]` for IDs. |
| 12 | Interface | `interface/<feat>/serializer/mapper/<feat>_controller_mapper.py` | Static `from_request`, `to_response` (uses `asdict`), `to_list_response`. |
| 13 | Interface | `interface/<feat>/view/<feat>_public_view.py` | Only create if the feature has **public** (unauthenticated) endpoints. `ViewSet`, **exactly 1 class**, `@metadata_handler(required_user_id=False)`, no `@require_roles`. ❌ Do not create if feature is customer-only or admin-only. |
| 14 | Interface | `interface/<feat>/view/<feat>_customer_view.py` | Only create if the feature has **customer-scoped** endpoints. `ViewSet`, **exactly 1 class**, `@metadata_handler(required_user_id=True)`, no `@require_roles`. Service injected at class level. ❌ Do not create if feature has no customer-authenticated routes. |
| 15 | Interface | `interface/<feat>/view/<feat>_admin_view.py` | Only create if the feature has **admin** endpoints. `ViewSet`, **exactly 1 class**, `@metadata_handler(required_user_id=True)`, `@require_roles("admin")`. Service injected at class level. |
| 16 | Interface | `interface/<feat>/url/<feat>_url.py` | **Exactly 1 URL file** for features with a single tier. For mixed-auth features, use `<feat>_public_url.py` + `<feat>_customer_url.py`. Admin routes prefixed `admin/<feat>/`, public prefixed `public/<feat>/`, customer-only prefixed `customer/<feat>/`. **No bare `<feat>/` routes.** UUID path param only for writes; slug via `?slug=` query param on `/search/`. Static paths before parameterized paths. |
| 17 | Cleanup | (all layers) | Delete any legacy files: `<feat>_view.py`, `<feat>_admin_url.py`, `<feat>_public_url.py`. No deprecated shim files, no split URL files, no bare unscoped routes left on disk. |
