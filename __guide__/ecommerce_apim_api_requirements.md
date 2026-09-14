# SETEC eCommerce API Requirements for APIM

Source inputs:
- Database schema: `ecommerce_postgresql_schema.sql`
- Design reference: Kutuku eCommerce Mobile App UI Kit in Figma
- Frontend target: Flutter web/mobile customer app
- Future target: admin site, included for planning but not yet finalized

Figma access note: the shared Figma page confirms the Kutuku eCommerce mobile UI kit direction. Detailed frame names were not available from the public browser view, so screen-level needs are inferred from the mobile eCommerce design scope and confirmed against the database schema.

## 1. Purpose

This document defines the API surface required for the first Kutuku-style eCommerce frontend implementation and future admin portal. It is intended as a request to the APIM/backend team to build, expose, secure, and document REST APIs based on the PostgreSQL schema.

The first implementation should stay simple and avoid over-engineering. The API should support customer shopping flows first, with basic notifications and customer-to-admin messaging. Payment implementation is intentionally deferred to a later phase.

## 1.1 First Implementation Direction

- Build only the APIs needed for the initial Flutter customer experience and simple admin support.
- Keep the UI/API behavior clean, predictable, and easy to integrate with Django.
- Include basic in-app notifications for order updates, promotions, and future payment status events.
- Include basic customer-to-admin conversations with message history and read/unread status.
- Skip payment processing and saved payment method management for now.
- Use Cloudinary for image storage. The backend should store Cloudinary URLs and metadata, not image files.
- Keep endpoint and data model structure flexible so notification, message, payment, and admin features can grow later.

## 2. Frontend Scope

### 2.1 Customer Flutter Web/Mobile App

The customer app needs APIs for:

- Account registration, login, logout, session management, and profile editing
- Home/catalog browsing using categories, stores, products, tags, images, and variants
- Product search, filters, product details, favorites, ratings, and reviews
- Cart creation, cart item management, checkout preparation, and order placement
- Address book and default shipping address selection
- Order history, order detail, shipment tracking, and order status timeline
- Customer/admin conversations with message history and read/unread status
- Basic in-app notifications
- Legal document viewing and legal acceptance capture
- Security settings such as two-factor and biometric preference flags

### 2.2 Admin Site, Included for Planning

The admin site is not finalized yet, but APIM should plan API permissions and routing for:

- User management
- Store management
- Category management
- Product, image, variant, tag, and inventory moderation
- Order and shipment operations
- Payment and refund operations in a later phase
- Review moderation
- Notification publishing
- Support ticket handling
- Legal document publishing and versioning
- Reporting/search history access where permitted

Admin APIs may be implemented later, but the authorization model should not block adding them.

## 3. API Standards

Base path:

```text
/api/v1
```

Response format:

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

List response format:

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 0,
    "has_next": false
  },
  "errors": []
}
```

Error format:

```json
{
  "data": null,
  "meta": {
    "request_id": "string"
  },
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Human-readable message",
      "field": "email"
    }
  ]
}
```

Required API behavior:

- Use JSON request and response bodies.
- Use UUID strings for entity IDs.
- Use ISO 8601 timestamps for date/time fields.
- Use lowercase enum values exactly as defined in the database.
- Support soft-deleted rows by excluding `deleted_at IS NOT NULL` from normal customer responses.
- Include `request_id` in all error responses.
- Support pagination on all list endpoints.
- Support sorting where useful, especially products, orders, reviews, notifications, and admin lists.
- Support idempotency keys for checkout, order placement, and status-changing admin actions.

## 3.1 API Access Scope and Routing Contract

Every endpoint MUST belong to exactly one access scope. The scope is part of the API contract and must be explicit in the endpoint tables.

| Scope | Prefix | Authentication | Purpose |
|---|---|---|---|
| **Public** | `/api/v1/public/...` | None | Guest/customer/admin-readable catalog and published content |
| **Customer** | `/api/v1/customer/...` | Customer JWT | Data owned by or scoped to the currently authenticated customer |
| **Seller** | `/api/v1/seller/...` | Seller JWT + `seller` role | Seller-owned store/catalog/operations |
| **Admin** | `/api/v1/admin/...` | JWT + `admin` role | Platform-wide administration |
| **Auth** | `/api/v1/auth/...` | Endpoint-specific | Authentication and account verification flows |
| **Home** | `/api/v1/home/...` | Optional | Public home feed; may personalize when a valid user is present |

### Scope Rules

- **Public** is for resources that guests can read without authentication.
- **Customer** is for resources belonging to the current customer, including profile, addresses, cart, orders, favorites, search history, notifications, conversations, support tickets, and legal acceptance.
- **Seller** is reserved for seller-owned operations. Seller APIs are planned but are not part of the Phase 1 customer MVP unless explicitly implemented.
- **Admin** is for platform-wide management and moderation.
- `/auth/` remains a separate namespace because registration, login, verification, password recovery, logout, refresh, and current-user authentication concerns are cross-cutting authentication operations.
- `/home/` remains a public exception because the home feed can be requested without a user ID and can optionally personalize when a user is authenticated.
- **Never create bare feature routes** such as `/api/v1/products/`, `/api/v1/orders/`, or `/api/v1/users/`.
- An endpoint must not be duplicated across access scopes.
- If a resource has both public and authenticated operations, the operations must be placed in their appropriate scopes rather than exposing the same endpoint in multiple scopes.

### Identifier Convention

Use one identifier convention consistently across the API:

- UUID-based resource access uses a UUID path parameter:
  - `GET /api/v1/public/products/{product_id}/`
  - `PATCH /api/v1/admin/products/{product_id}/`
  - `DELETE /api/v1/customer/addresses/{address_id}/`
- Slug lookup MUST use a dedicated `/search/` endpoint with a query parameter:
  - `GET /api/v1/public/products/search/?slug=<product_slug>`
  - `GET /api/v1/public/categories/search/?slug=<category_slug>`
  - `GET /api/v1/public/stores/search/?slug=<store_slug>`
- **Slug MUST NOT be a path parameter.**
- Write operations (`POST`, `PUT`, `PATCH`, `DELETE`) MUST NOT use slugs as resource identifiers.
- ID-based `GET retrieve` also uses UUID path parameters.
- Static paths such as `/tree/`, `/search/`, `/images/`, `/variants/`, and `/options/` must be registered before parameterized UUID paths.

### Product / Variant / Option Resource Structure

Product-related resources follow this hierarchy:

```text
/public/products/
/public/products/search/?slug=<product_slug>
/public/products/{product_id}/
/public/products/{product_id}/images/
/public/products/{product_id}/variants/
/public/products/variants/search/?product_id=<product_id>
/public/products/variants/{variant_id}/
/public/products/variants/options/search/?product_id=<product_id>&variant_id=<variant_id>
/public/products/variants/options/{option_id}/
```

The same resource hierarchy is used under `/admin/` for administrative management:

```text
/admin/products/
/admin/products/search/?slug=<product_slug>
/admin/products/{product_id}/
/admin/products/{product_id}/images/
/admin/products/{product_id}/variants/
/admin/products/variants/search/?product_id=<product_id>
/admin/products/variants/{variant_id}/
/admin/products/variants/options/search/?product_id=<product_id>&variant_id=<variant_id>
/admin/products/variants/options/{option_id}/
```

`product_id`, `variant_id`, and `option_id` are query parameters only for collection/search endpoints where filtering by a parent resource is required. They are UUID path parameters when directly retrieving or mutating an individual resource.

## 4. Authentication and Authorization

Authentication:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/refresh`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/verify-email`
- `POST /auth/verify-phone`
- `GET /auth/me`

Authorization roles:

- `customer`: shopping, profile, address, cart, order, review, support, notifications
- `seller`: own store, own catalog, own orders, own conversations
- `support`: support tickets, conversations, limited order visibility
- `admin`: platform-wide management

Token requirements:

- Use Bearer token authorization.
- Refresh tokens must be revocable through `user_sessions`.
- Block access when `users.status` is `blocked` or `inactive`.
- Restrict pending users based on backend policy, at minimum allowing verification flows.

## 5. Core Customer APIs

### 5.1 Customer — Users and Profile

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/users/me` | Get current user account, profile, security settings, and default address summary |
| PATCH | `/customer/users/me` | Update first name, last name, avatar, phone, and profile preferences |
| GET | `/customer/users/me/profile` | Get extended profile details |
| PATCH | `/customer/users/me/profile` | Update date of birth, gender, preferred language, and marketing preference |
| GET | `/customer/users/me/security-settings` | Get two-factor, biometric, and password change state |
| PATCH | `/customer/users/me/security-settings` | Update security preference flags |
| GET | `/customer/users/me/sessions` | List current user's active and revoked sessions |
| POST | `/customer/users/me/sessions/{session_id}/revoke` | Revoke one session |

### 5.2 Customer — Addresses

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/addresses` | List saved addresses for the current user |
| POST | `/customer/addresses` | Create a saved address |
| GET | `/customer/addresses/{address_id}` | Get one address |
| PATCH | `/customer/addresses/{address_id}` | Update one address |
| DELETE | `/customer/addresses/{address_id}` | Soft-delete one address |
| POST | `/customer/addresses/{address_id}/default` | Set default active address |

Required validation:

- `country_code` must be a 2-character country code.
- Latitude must be between `-90` and `90`.
- Longitude must be between `-180` and `180`.
- Only one active default address per user.

### 5.3 Public — Catalog, Stores, Categories, and Tags

| Method | Path | Purpose |
|---|---|---|
| GET | `/home` | Return home-screen content: featured categories, stores, products, promotions if available |
| GET | `/public/categories` | List active categories with optional parent filtering |
| GET | `/public/categories/tree` | Return category hierarchy |
| GET | `/public/categories/{slug}` | Get category detail |
| GET | `/public/stores` | List active stores |
| GET | `/public/stores/{slug}` | Get store detail with rating summary |
| GET | `/public/stores/{slug}/products` | List active products for one store |
| GET | `/public/tags` | List product tags |

### 5.4 Public — Products

| Method | Path | Purpose |
|---|---|---|
| GET | `/public/products` | List active products with search, category, store, tag, price, rating, and status filters |
| GET | `/public/products/{product_id}` | Get product detail |
| GET | `/public/products/search/?slug=<product_slug>` | Get product detail by store and product slug |
| GET | `/public/products/{product_id}/images` | Get ordered product images |
| GET | `/public/products/{product_id}/variants` | Get active variants and option values |
| GET | `/public/products/{product_id}/reviews` | List published reviews |

Product list filters:

- `q`
- `category_id`
- `store_id`
- `tag`
- `min_price`
- `max_price`
- `rating_min`
- `status`
- `sort`, allowed values: `newest`, `price_asc`, `price_desc`, `rating`, `sold`

Product response should include:

- Product fields from `products`
- Primary image from `product_images`
- Image gallery
- Store summary
- Category summary
- Variant summary
- Tags
- Rating average and rating count
- Current user's `is_favorite` value when authenticated

### 5.5 Customer — Search History

| Method | Path | Purpose |
|---|---|---|
| POST | `/customer/search-history` | Record a search query, filters, and result count |
| GET | `/customer/search-history` | List current user's recent searches |
| DELETE | `/customer/search-history/{search_id}` | Delete one search history item if supported |
| DELETE | `/customer/search-history` | Clear current user's search history if supported |

### 5.6 Customer — Favorites

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/favorites` | List current user's favorite products |
| POST | `/customer/favorites` | Add a product to favorites |
| DELETE | `/customer/favorites/{product_id}` | Remove a product from favorites |
| GET | `/public/products/{product_id}/favorite` | Return favorite state for current user |

### 5.7 Customer — Cart

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/cart` | Get current user's active cart with items and totals |
| POST | `/customer/cart/items` | Add product or variant to active cart |
| PATCH | `/customer/cart/items/{cart_item_id}` | Update quantity or selected state |
| DELETE | `/customer/cart/items/{cart_item_id}` | Soft-delete item from cart |
| POST | `/customer/cart/select-all` | Select or unselect all active cart items |
| POST | `/customer/cart/checkout-preview` | Return checkout totals using selected items and shipping address |

Cart requirements:

- Maintain one active cart per user.
- Use `unit_price_snapshot` when adding cart items.
- Prevent duplicate active cart item rows for the same product and variant.
- Only selected cart items should be included in checkout preview and order placement.

### 5.8 Customer — Payment Methods, Deferred

Payment implementation is skipped for the first release. Do not build saved payment method APIs yet.

The database includes `payment_methods` so the feature can be added later without changing the frontend architecture. When payment work starts, expected future endpoints are:

- `GET /payment-methods`
- `POST /payment-methods`
- `PATCH /payment-methods/{payment_method_id}`
- `DELETE /payment-methods/{payment_method_id}`
- `POST /payment-methods/{payment_method_id}/default`

Security requirement:

- Do not store raw card numbers or CVV.
- Store only provider token, brand, last four digits, and expiry metadata.

### 5.9 Customer — Orders and Checkout

| Method | Path | Purpose |
|---|---|---|
| POST | `/customer/orders` | Place an order from selected cart items |
| GET | `/customer/orders` | List current user's orders |
| GET | `/customer/orders/{order_id}` | Get order detail, items, shipment, and status history. Payment can be added later |
| POST | `/customer/orders/{order_id}/cancel` | Request or perform cancellation when allowed |
| GET | `/customer/orders/{order_id}/status-history` | List order status changes |

Order placement request:

```json
{
  "cart_id": "uuid",
  "shipping_address_id": "uuid",
  "idempotency_key": "string"
}
```

Order response should include:

- Order header and totals
- Order item snapshots
- Store summary
- Shipping address summary
- Payment summary only when payment is implemented in a later phase
- Shipment summary
- Status timeline

Checkout rules:

- Create order item snapshots for product name, variant name, SKU, unit price, quantity, and line total.
- Compute subtotal, shipping, discount, tax, and total server-side.
- Mark the cart as `checked_out` only after successful order creation.
- Set the initial order status to `pending` or `confirmed` according to backend policy.
- If selected cart items include products from multiple stores, create one order per store because the current schema has `store_id` at the order level.

### 5.10 Customer — Payments, Deferred

Payment APIs should not be part of the first implementation.

Keep the order response shape flexible enough to add payment status later. When payment is implemented, expected future endpoints are:

- `POST /orders/{order_id}/payments`
- `GET /orders/{order_id}/payments`
- `GET /payments/{payment_id}`
- `POST /payments/{payment_id}/confirm`

Payment statuses:

- `pending`
- `authorized`
- `captured`
- `failed`
- `refunded`
- `cancelled`

### 5.11 Customer — Shipments and Tracking

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/orders/{order_id}/shipments` | List shipments for an order |
| GET | `/customer/shipments/{shipment_id}` | Get shipment detail |
| GET | `/customer/shipments/{shipment_id}/events` | Get ordered tracking events |

Shipment statuses:

- `pending`
- `packed`
- `in_transit`
- `out_for_delivery`
- `delivered`
- `failed`
- `returned`

### 5.12 Customer — Reviews

| Method | Path | Purpose |
|---|---|---|
| POST | `/customer/products/{product_id}/reviews` | Create product review |
| PATCH | `/customer/reviews/{review_id}` | Update own pending or published review if allowed |
| DELETE | `/customer/reviews/{review_id}` | Soft-delete own review |
| GET | `/customer/users/me/reviews` | List current user's reviews |

Review rules:

- Rating must be from `1` to `5`.
- Customer can optionally review by `order_item_id`.
- Only one active review per user per order item.
- Public product pages should show only `published` reviews.

### 5.13 Customer — Conversations and Messages

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/conversations` | List current user's conversations |
| POST | `/customer/conversations` | Start a basic customer-to-admin conversation with optional order context |
| GET | `/customer/conversations/{conversation_id}` | Get conversation detail |
| PATCH | `/customer/conversations/{conversation_id}` | Close or archive a conversation if allowed |
| GET | `/customer/conversations/{conversation_id}/messages` | List messages |
| POST | `/customer/conversations/{conversation_id}/messages` | Send text or attachment message |
| POST | `/customer/messages/{message_id}/read` | Mark message as read |

Message rules:

- First implementation should support customer-to-admin conversation only. Store/seller messaging can be added later.
- `message_type` can be `text`, `image`, or `system`.
- A message must include `body`, `attachment_url`, or be a `system` message.
- Conversation list should include `last_message_at`, last message preview, and unread count for the current user.
- Message history should support pagination by newest or oldest message.
- Read/unread state can use `messages.read_at` for the first implementation.
- Attachments, if enabled, should use Cloudinary URLs.

### 5.14 Customer — Notifications

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/notifications` | List current user's notifications |
| GET | `/customer/notifications/unread-count` | Return unread notification count |
| POST | `/customer/notifications/{notification_id}/read` | Mark one notification as read |
| POST | `/customer/notifications/read-all` | Mark all current user's notifications as read |
| DELETE | `/customer/notifications/{notification_id}` | Soft-delete one notification |

Notification types:

- `order`
- `promotion`
- `message`
- `system`
- `security`

Notification rules:

- First implementation should be basic in-app notifications only.
- Notifications should support order updates, promotions, message alerts, system notices, and future payment status updates.
- Notification list should include `type`, `title`, `body`, `data`, `read_at`, `status`, and `created_at`.
- Push notification delivery is not required for the first implementation unless separately requested.

### 5.15 Customer — Support Tickets

| Method | Path | Purpose |
|---|---|---|
| GET | `/customer/support/tickets` | List current user's support tickets |
| POST | `/customer/support/tickets` | Create a support ticket |
| GET | `/customer/support/tickets/{ticket_id}` | Get ticket detail |
| PATCH | `/customer/support/tickets/{ticket_id}` | Update ticket subject/status where allowed |
| GET | `/customer/support/tickets/{ticket_id}/messages` | List ticket messages |
| POST | `/customer/support/tickets/{ticket_id}/messages` | Add ticket message |

Ticket categories:

- `order`
- `payment`
- `delivery`
- `account`
- `other`

### 5.16 Public + Customer — Legal Documents

| Method | Path | Purpose |
|---|---|---|
| GET | `/public/legal-documents` | List published legal documents by type |
| GET | `/public/legal-documents/{type}/latest` | Get latest published legal document of a type |
| POST | `/customer/legal-documents/{legal_document_id}/accept` | Record current user's acceptance |
| GET | `/customer/users/me/legal-acceptances` | List current user's legal acceptances |

Legal types:

- `terms`
- `privacy`
- `refund_policy`
- `shipping_policy`

## 6. Admin and Seller Planning APIs

These endpoints should be protected by role-based permissions and can be implemented after customer APIs.

### 6.0 Seller Planning

Seller endpoints are planned separately from customer and admin APIs. They must use the `/seller/` prefix and require a valid seller JWT with the `seller` role.

Planned seller scope includes:

- Own store profile and settings
- Own products, images, variants, options, tags, and inventory
- Own order/shipment operations where permitted
- Seller-facing conversations when seller messaging is introduced

Seller APIs are not required for the Phase 1 customer MVP. Do not expose seller operations under `/customer/` or `/admin/`.

### 6.1 Admin Users

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/users` | Search and list users |
| GET | `/admin/users/{user_id}` | Get user detail |
| PATCH | `/admin/users/{user_id}` | Update role or status |
| POST | `/admin/users/{user_id}/block` | Block user |
| POST | `/admin/users/{user_id}/unblock` | Unblock user |

### 6.2 Admin Stores

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/stores` | List stores |
| POST | `/admin/stores` | Create store |
| PATCH | `/admin/stores/{store_id}` | Update store |
| POST | `/admin/stores/{store_id}/suspend` | Suspend store |
| POST | `/admin/stores/{store_id}/activate` | Activate store |

### 6.3 Admin Catalog

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/categories` | Manage category list |
| POST | `/admin/categories` | Create category |
| PATCH | `/admin/categories/{category_id}` | Update category |
| DELETE | `/admin/categories/{category_id}` | Soft-delete category |
| GET | `/admin/products` | Search all products |
| POST | `/admin/products` | Create product |
| PATCH | `/admin/products/{product_id}` | Update product |
| DELETE | `/admin/products/{product_id}` | Soft-delete product |
| POST | `/admin/products/{product_id}/images` | Add product image metadata |
| PATCH | `/admin/product-images/{image_id}` | Update image order, alt text, or primary flag |
| DELETE | `/admin/product-images/{image_id}` | Soft-delete image |
| POST | `/admin/products/{product_id}/variants` | Add variant |
| PATCH | `/admin/product-variants/{variant_id}` | Update variant |
| DELETE | `/admin/product-variants/{variant_id}` | Soft-delete variant |
| POST | `/admin/tags` | Create tag |
| PATCH | `/admin/tags/{tag_id}` | Update tag |

### 6.4 Admin Orders, Shipments, and Future Payments

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/orders` | Search all orders |
| GET | `/admin/orders/{order_id}` | Get full order detail |
| PATCH | `/admin/orders/{order_id}/status` | Change order status and write status history |
| GET | `/admin/payments` | Future phase: search payments |
| PATCH | `/admin/payments/{payment_id}/status` | Future phase: update payment status |
| GET | `/admin/shipments` | Search shipments |
| POST | `/admin/orders/{order_id}/shipments` | Create shipment |
| PATCH | `/admin/shipments/{shipment_id}` | Update carrier, tracking number, or status |
| POST | `/admin/shipments/{shipment_id}/events` | Add shipment tracking event |

### 6.5 Admin Reviews, Support, Notifications, and Legal

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/reviews` | Search and moderate reviews |
| PATCH | `/admin/reviews/{review_id}/status` | Publish or hide review |
| GET | `/admin/support/tickets` | List support tickets |
| PATCH | `/admin/support/tickets/{ticket_id}` | Update status, priority, or assignment when supported |
| POST | `/admin/notifications` | Create notification for one or many users |
| GET | `/admin/legal-documents` | List legal document versions |
| POST | `/admin/legal-documents` | Create legal document version |
| PATCH | `/admin/legal-documents/{legal_document_id}` | Update draft legal document |
| POST | `/admin/legal-documents/{legal_document_id}/publish` | Publish legal document |
| POST | `/admin/legal-documents/{legal_document_id}/archive` | Archive legal document |

## 7. Key Data Models for Frontend

### 7.1 Product Card

```json
{
  "id": "uuid",
  "name": "string",
  "slug": "string",
  "base_price": "12.00",
  "compare_at_price": "15.00",
  "currency": "USD",
  "primary_image_url": "https://...",
  "rating_average": 4.5,
  "rating_count": 20,
  "sold_count": 100,
  "status": "active",
  "store": {
    "id": "uuid",
    "name": "string",
    "slug": "string"
  },
  "is_favorite": false
}
```

### 7.2 Product Detail

```json
{
  "id": "uuid",
  "store": {},
  "category": {},
  "name": "string",
  "slug": "string",
  "description": "string",
  "base_price": "12.00",
  "compare_at_price": "15.00",
  "currency": "USD",
  "sku": "string",
  "status": "active",
  "rating_average": 4.5,
  "rating_count": 20,
  "sold_count": 100,
  "images": [],
  "variants": [],
  "tags": [],
  "is_favorite": false
}
```

### 7.3 Cart

```json
{
  "id": "uuid",
  "status": "active",
  "items": [
    {
      "id": "uuid",
      "product": {},
      "variant": {},
      "quantity": 1,
      "unit_price_snapshot": "12.00",
      "line_total": "12.00",
      "is_selected": true
    }
  ],
  "totals": {
    "selected_item_count": 1,
    "subtotal_amount": "12.00",
    "shipping_amount": "0.00",
    "discount_amount": "0.00",
    "tax_amount": "0.00",
    "total_amount": "12.00",
    "currency": "USD"
  }
}
```

### 7.4 Order Detail

```json
{
  "id": "uuid",
  "order_number": "string",
  "status": "pending",
  "subtotal_amount": "12.00",
  "shipping_amount": "0.00",
  "discount_amount": "0.00",
  "tax_amount": "0.00",
  "total_amount": "12.00",
  "currency": "USD",
  "placed_at": "2026-08-29T00:00:00Z",
  "items": [],
  "payment": null,
  "shipments": [],
  "status_history": []
}
```

## 8. APIM Requirements

APIM MUST treat the route prefixes above as the authorization boundary. APIM should not infer access scope from the HTTP method or resource name alone.


APIM should provide:

- Environment-based base URLs for development, staging, and production.
- API versioning through `/api/v1`.
- OpenAPI specification for all endpoints.
- JWT validation and role-based route policies.
- Rate limiting for authentication, search, cart mutation, checkout, reviews, and messages.
- Request/response logging with sensitive field masking.
- CORS configuration for Flutter web domains.
- Standard timeout and retry guidance for frontend.
- Request ID propagation to backend logs.
- Idempotency support on high-risk mutation endpoints such as order creation.
- Separate admin route policy group for `/admin/*`.

Recommended rate limits:

| Endpoint group | Suggested limit |
|---|---:|
| Auth login/register | 10 requests per minute per IP |
| Product/catalog reads | 120 requests per minute per user/IP |
| Search | 60 requests per minute per user/IP |
| Cart mutation | 60 requests per minute per user |
| Checkout/order creation | 10 requests per minute per user |
| Message/support creation | 30 requests per minute per user |
| Admin mutation | 60 requests per minute per admin |

## 9. File and Media Handling

Use Cloudinary for image and media storage. The backend/server should not store image files directly.

The schema stores Cloudinary URLs for images and attachments:

- `avatar_url`
- `logo_url`
- `banner_url`
- `image_url`
- `attachment_url`

Required Cloudinary-related APIs:

| Method | Path | Purpose |
|---|---|---|
| POST | `/uploads/cloudinary-signature` | Create a signed Cloudinary upload payload when frontend uploads directly to Cloudinary |
| POST | `/uploads/confirm` | Confirm uploaded Cloudinary asset and return URL, public ID, mime type, size, and usage type |

Upload requirements:

- Frontend may upload directly to Cloudinary using a backend-generated signature.
- Backend should persist only Cloudinary URL/public ID and related metadata.
- Product images, avatars, store logos, store banners, message attachments, and support attachments should all use the same Cloudinary flow.
- Keep transformation sizes simple for the first release, such as thumbnail, product card, and full detail image.

## 10. Frontend State and UX Requirements

The Flutter app needs APIs that are fast enough for mobile-style UI:

- Home screen should load with one API call where possible.
- Product card lists should include enough data to avoid extra calls per item.
- Product detail should include images, variants, tags, store summary, and favorite state.
- Cart endpoint should include calculated totals.
- Order detail should include items, shipment, and timeline together. Payment should remain `null` or omitted until the later payment phase.
- Notification unread count should be lightweight.
- APIs should support pull-to-refresh and infinite scroll.

## 11. APIM / Backend Decisions

The following decisions are confirmed by the APIM/backend team for the first implementation:

- **Checkout / Mixed-Store Cart:** The current database has `store_id` at the order level. Therefore, if a cart contains products from multiple stores, the backend will create one order per store during checkout. This keeps the current schema structure consistent.
- **Seller Site and Admin Site:** Treat the seller site and admin site as separate frontend applications/interfaces. The backend will maintain separate role-based permissions for `seller`, `support`, and `admin`.
- **Inventory:** `product_variants.stock_quantity` will be the source of truth for product inventory. No separate product-level inventory field is required for the first implementation.
- **Promotions, Coupons, Banners, and Delivery Fees:** These features are not part of the first implementation unless already supported by the existing schema. Do not introduce additional tables just for the initial MVP. They can be designed and added in a later phase.
- **Cloudinary Assets:** Use Cloudinary for image and media storage. The backend stores Cloudinary URLs, public IDs, and metadata rather than the actual image files. For the first implementation, use public URLs unless a specific security requirement later requires protected/signed URLs.
- **Legal Acceptance:** Legal acceptance will be handled according to the existing legal-document APIs. For the first implementation, do not block checkout with additional legal acceptance requirements unless the project requirements explicitly require it. Legal acceptance can be captured during registration/account flows.
- **Payment:** Payment is deferred completely from the first implementation. Do not implement payment processing, saved payment methods, payment tokens, or payment-provider integration yet. The API structure should remain flexible for a later payment phase.
- **Notifications:** Implement basic in-app notifications only for the first release. Push notifications, email notifications, and other delivery channels are not required at this stage.
- **Message / Conversation:** Implement a basic customer-to-admin conversation system with message history and read/unread status. Seller messaging and advanced real-time messaging features can be added later.

These decisions are intended to keep the first implementation small, stable, and easy for the Flutter frontend to integrate while leaving the API structure flexible for future expansion.

## 12. Launch Priority

### Phase 1: Customer MVP

- Auth and current user
- Profile and addresses
- Categories, stores, products, product detail
- Search and favorites
- Cart
- Checkout preview and order creation
- Orders and order detail
- Basic notifications
- Basic customer/admin conversations and message history
- Legal documents and acceptance

### Phase 2: Commerce Operations

- Shipment tracking
- Reviews
- Support tickets
- User sessions and security settings

### Phase 3: Admin/Seller

- Admin user/store/catalog management
- Order/shipment operations
- Review moderation
- Support queue
- Notification publishing
- Legal document publishing
- Payment integration and payment admin tools

## 13. Acceptance Criteria

The APIM delivery is considered ready for frontend integration when:

- OpenAPI documentation is available for every implemented endpoint, including its explicit access scope and authorization requirement.
- Auth token flow works in Flutter web/mobile.
- All response examples match actual API responses.
- All list endpoints support pagination.
- Product, cart, order, and notification responses include frontend-ready summary objects.
- Role-based access is enforced for customer, seller, support, and admin routes.
- Error responses use the agreed standard shape.
- Checkout/order creation supports idempotency.
- Soft-deleted data is hidden from customer-facing APIs.
- Staging endpoints are available for frontend integration testing.
