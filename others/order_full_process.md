# Complete Order Process

This document describes the order flow currently implemented by this service: cart preparation, checkout, order creation, order history, cancellation, admin fulfillment, and shipment tracking.

The canonical URLs below come from the mounted Django routes. Customer routes use the /api/v1/customer/ prefix. Some older documentation and OpenAPI entries omit /customer/ and should not be treated as the runtime route source of truth.

## 1. Actors and authentication

- Customer: manages a cart, places orders, views owned orders, cancels eligible orders, and views tracking.
- Admin: lists all orders, reads any order, and updates fulfillment status.
- Backend: groups selected items by store, creates order snapshots, and records status changes.

All routes in this document require:

~~~http
Authorization: Bearer <access_token>
Content-Type: application/json
~~~

Admin routes also require the admin role.

Successful object/mutation responses use:

~~~json
{
  "data": {},
  "meta": { "request_id": null },
  "errors": []
}
~~~

List responses additionally contain page, page_size, total, and has_next in meta.

## 2. End-to-end flow

~~~mermaid
flowchart TD
    A[Customer signs in] --> B[Select shipping address]
    B --> C[Add products to cart]
    C --> D[Select items and update quantities]
    D --> E[Request checkout preview]
    E --> F[POST customer/orders]
    F --> G{Items from multiple stores?}
    G -- No --> H[Create one pending order]
    G -- Yes --> I[Create one pending order per store]
    H --> J[Snapshot items and create pending history]
    I --> J
    J --> K[Mark cart checked_out]
    K --> L[Orders appear in customer history]
    L --> M{Next action}
    M -- Customer cancels --> N[Status becomes cancelled]
    M -- Admin fulfills --> O[Admin updates status]
    O --> P[Create status-history entry]
    P --> Q[Shipment tracking]
    Q --> R[Delivered]
~~~

## 3. Customer checkout

### Step 1: Prepare a shipping address

The order request requires a shipping_address_id. Address routes are mounted under:

- GET /api/v1/customer/addresses/
- POST /api/v1/customer/addresses/
- GET /api/v1/customer/addresses/{address_id}/
- PATCH /api/v1/customer/addresses/{address_id}/
- DELETE /api/v1/customer/addresses/{address_id}/
- POST or PATCH /api/v1/customer/addresses/{address_id}/default/

The frontend should require the customer to select or create an address before placing an order.

### Step 2: Get or create the active cart

~~~http
GET /api/v1/customer/cart/
~~~

If the customer has no active cart, the backend creates one. The result contains the cart ID, status, active items, and totals.

### Step 3: Add a product

~~~http
POST /api/v1/customer/cart/items/
~~~

~~~json
{
  "product_id": "prod-000001",
  "product_variant_id": "vrn-000001",
  "quantity": 2
}
~~~

product_variant_id is optional; quantity must be at least 1.

Current behavior:

- A missing product returns 404 PRODUCT_NOT_FOUND.
- The current product or variant price is copied to unit_price_snapshot.
- Adding the same product/variant again increases its quantity.
- A new item is selected by default.

### Step 4: Update selected items

Update a quantity or selection:

~~~http
PATCH /api/v1/customer/cart/items/{cart_item_id}/
~~~

~~~json
{
  "quantity": 3,
  "is_selected": true
}
~~~

Remove an item:

~~~http
DELETE /api/v1/customer/cart/items/{cart_item_id}/
~~~

Select or deselect all:

~~~http
POST /api/v1/customer/cart/select-all/
~~~

~~~json
{
  "selected": true
}
~~~

Only selected, non-deleted items are converted into orders.

### Step 5: Preview checkout

~~~http
POST /api/v1/customer/cart/checkout-preview/
~~~

~~~json
{
  "shipping_address_id": "adr-000001"
}
~~~

The response contains cart_id, shipping_address_id, and totals based on selected items.

Current total calculation:

~~~text
subtotal = sum(unit_price_snapshot * quantity)
shipping = 0.00
discount = 0.00
tax      = 0.00
total    = subtotal
currency = USD
~~~

Preview does not reserve inventory and does not create an order.

### Step 6: Place the order

~~~http
POST /api/v1/customer/orders/
~~~

All three fields are currently required:

~~~json
{
  "cart_id": "cart-000001",
  "shipping_address_id": "adr-000001",
  "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

Frontend rules:

- Generate one key for each new checkout attempt.
- Reuse the same key when retrying the same request after a timeout.
- Disable the Place Order button during the request.
- Treat response data as an array because one checkout may create multiple orders.

The backend uses a database transaction and:

1. Finds an active cart belonging to the authenticated customer.
2. Loads selected, non-deleted items.
3. Returns 400 CART_EMPTY if the cart is unavailable or nothing is selected.
4. Groups items by the product's store.
5. Creates one order per store group.
6. Generates an ID such as ord-20261023-0001.
7. Sets each new order to pending.
8. Copies product name, variant name, SKU, unit price, quantity, and line total into order-item snapshots.
9. Adds a history row from null to pending with note Order placed via cart checkout.
10. Marks the cart checked_out.
11. Soft-deletes the processed selected items.
12. Commits all order and cart changes together.

If items come from three stores, the response contains three independent orders.

Example response shape:

~~~json
{
  "data": [
    {
      "id": "ord-20261023-0001",
      "order_number": "ord-20261023-0001",
      "status": "pending",
      "subtotal_amount": "90.00",
      "shipping_amount": "0.00",
      "discount_amount": "0.00",
      "tax_amount": "0.00",
      "total_amount": "90.00",
      "currency": "USD",
      "store": {
        "id": "str-000001",
        "name": "Example Store"
      },
      "shipping_address_id": "adr-000001",
      "items": [],
      "payment": null,
      "shipments": [],
      "status_history": [
        {
          "id": "ordst-000001",
          "from_status": null,
          "to_status": "pending",
          "note": "Order placed via cart checkout",
          "created_at": "2026-10-23T10:00:00+00:00"
        }
      ]
    }
  ],
  "meta": { "request_id": null },
  "errors": []
}
~~~

### Step 7: Start the next cart

After checkout, the old cart is checked_out. Calling GET /api/v1/customer/cart/ again creates a new active cart.

## 4. Customer order history

### List the customer's orders

~~~http
GET /api/v1/customer/orders/?page=1&page_size=20
~~~

The backend limits results to the authenticated customer and sorts newest first. Use this for the My Orders screen.

Each summary contains order ID/number, status, total, currency, store, item count, and placed time. The customer route currently has no server-side status filter.

### Read one order

~~~http
GET /api/v1/customer/orders/{order_id}/
~~~

The backend checks that the order belongs to the authenticated customer. Use this for item snapshots, price breakdown, address ID, and status history.

### Read the status timeline

~~~http
GET /api/v1/customer/orders/{order_id}/status-history/
~~~

History is sorted oldest first. A history row is created when:

- Checkout creates an order: null to pending.
- A customer cancels: pending or confirmed to cancelled.
- An admin changes fulfillment status: old status to new status.

Example:

~~~json
{
  "data": [
    {
      "id": "ordst-000001",
      "from_status": null,
      "to_status": "pending",
      "note": "Order placed via cart checkout",
      "created_at": "2026-10-23T10:00:00+00:00"
    },
    {
      "id": "ordst-000002",
      "from_status": "pending",
      "to_status": "confirmed",
      "note": "Order accepted",
      "created_at": "2026-10-23T10:10:00+00:00"
    }
  ],
  "meta": { "request_id": null },
  "errors": []
}
~~~

## 5. Customer cancellation

~~~http
POST /api/v1/customer/orders/{order_id}/cancel/
~~~

Cancellation succeeds only when the order belongs to the customer and its current status is pending or confirmed.

On success, the backend:

1. Changes status to cancelled.
2. Sets cancelled_at.
3. Adds a history row with note Cancelled by customer.
4. Returns the updated order.

Important errors:

- Unknown/unowned order: 404 ORDER_NOT_FOUND.
- Ineligible status: 400 ORDER_CANNOT_CANCEL.

The frontend should display Cancel only for pending and confirmed, while still handling a backend rejection in case the status changed concurrently.

## 6. Admin fulfillment

List and filter orders:

~~~http
GET /api/v1/admin/orders/?user_id={user_id}&status={status}&store_id={store_id}&page=1&page_size=20
~~~

Read an order:

~~~http
GET /api/v1/admin/orders/{order_id}/
~~~

Change status:

~~~http
PATCH /api/v1/admin/orders/{order_id}/status/
~~~

~~~json
{
  "status": "processing",
  "note": "Payment verified; preparing items"
}
~~~

Every update records the old status, new status, admin actor, optional note, and time.

Intended happy path:

~~~text
pending -> confirmed -> processing -> shipped -> delivered
~~~

Alternative outcomes are cancelled, refunded, and failed. This state machine is recommended but not currently enforced by the repository.

## 7. Shipment tracking

Customer routes:

~~~http
GET /api/v1/customer/orders/{order_id}/shipments/
GET /api/v1/customer/shipments/{shipment_id}/
GET /api/v1/customer/shipments/{shipment_id}/events/
~~~

Shipment statuses defined by the model:

~~~text
pending -> packed -> in_transit -> out_for_delivery -> delivered
~~~

Exceptional outcomes are failed and returned.

Admin routes intended for shipment management:

~~~http
GET /api/v1/admin/shipments/
GET /api/v1/admin/shipments/{shipment_id}/
PATCH /api/v1/admin/shipments/{shipment_id}/
~~~

Admin shipment implementation is currently incomplete; see section 10.

## 8. Payment

Payment is not implemented.

- There is no payment route, model, repository, or payment workflow.
- Order responses always contain "payment": null.
- Checkout creates pending orders without charging the customer.
- Shipping, discount, and tax are always zero.

A 201 response means an order was created; it does not mean payment succeeded. A future integration should include payment intent creation, provider confirmation/webhooks, idempotent recording, failures, refunds, and controlled payment-related order transitions.

## 9. Frontend orchestration checklist

1. Authenticate and store the access token securely.
2. Fetch or create the active cart.
3. Add items and let the customer select what to buy.
4. Require a shipping address.
5. Request checkout preview and display its totals.
6. Generate one idempotency key for the attempt.
7. Submit the order once and prevent double taps.
8. Save every returned order ID.
9. Show an order-success page listing all created orders.
10. Refresh the customer order list.
11. Fetch detail and status history when an order opens.
12. Show cancellation only for pending or confirmed.
13. Fetch shipments separately for tracking.
14. After an uncertain timeout, never retry with a new key.
15. On 401, follow the application's refresh/login flow.

## 10. Current implementation gaps and blockers

These issues were found by comparing the routes, serializers, models, repositories, and integration guide.

### Critical blockers

1. Idempotency is not enforced. The field is required but ignored by the repository. A retry can create duplicate orders if the first transaction committed but its response was lost.

2. Shipping-address ownership is not validated at checkout. The backend assigns the foreign key without explicitly confirming it belongs to the authenticated customer and is active.

3. Status-history authorization is incomplete. The customer service ignores user_id when loading history, so a logged-in user may be able to request another order's timeline if its ID is known.

4. Shipment authorization is incomplete. Shipment detail and events require login but do not verify ownership through the shipment's order.

### Workflow gaps

5. Admin status transitions are unrestricted; terminal orders can be moved backward.

6. Status definitions disagree. The model contains paid but not failed, while the request serializer contains failed but not paid.

7. Updating an order to its current status still creates a redundant history row.

8. Admin shipment views call list_admin and update methods that are absent from the current shipment service/repository. No implemented shipment or shipment-event creation flow exists.

9. Order detail always maps shipments to an empty array; clients must call the separate shipments route.

10. Checkout performs no stock validation, reservation, or deduction.

11. Final prices are not revalidated; order creation uses the cart's stored price snapshot.

12. There is no shipping-fee, promotion, discount, or tax engine.

13. The shipping address is not snapshotted. The order stores a nullable foreign key, so immutable delivery details are not preserved.

14. Some documentation uses /api/v1/orders/ and UUID order IDs, while runtime uses /api/v1/customer/orders/ and ord-YYYYMMDD-NNNN identifiers.

## 11. Recommended status rules

Before production, enforce a transition map similar to:

~~~text
pending    -> confirmed | cancelled | failed
confirmed  -> processing | cancelled | refunded
processing -> shipped | cancelled | refunded | failed
shipped    -> delivered | returned
delivered  -> refunded
cancelled  -> terminal
refunded   -> terminal
failed     -> terminal
~~~

Exact transitions depend on the future payment design. Each accepted transition should be transactional, reject stale updates, write exactly one history row, and trigger any required notification or inventory action.

## 12. Recommended acceptance tests

- One-store checkout creates one order and one initial history row.
- Multi-store checkout creates one order per store atomically.
- Empty/deselected cart returns 400 CART_EMPTY.
- A customer cannot use another customer's cart or address.
- Reusing an idempotency key returns the original result.
- A failure during creation rolls back all orders and cart changes.
- Customer list, detail, history, and shipment routes enforce ownership.
- Cancellation works only for allowed statuses and records one history row.
- Invalid admin transitions are rejected.
- Inventory is reserved or deducted exactly once.
- Payment success, failure, timeout, refund, and webhook replay are idempotent.
- Shipment creation and checkpoints are visible only to the owning customer.
- Order item and address snapshots remain unchanged after later edits.

