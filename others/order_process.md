# Complete Order Flow and Implementation Status

This document separates the intended customer-to-delivery process from what the backend currently implements.

## Status legend

- ✅ **Implemented** — the route and core backend behavior exist.
- ⚠️ **Partial** — some code exists, but the step is manual, incomplete, or unsafe for a complete production flow.
- ❌ **Missing** — the required backend process does not exist.
- 👤 **Customer action**
- ⚙️ **System action**
- 🛠️ **Admin or fulfillment action**
- 📦 **Order status**
- 🚚 **Shipment status**
- 💳 **Payment status**

## Main order flow

### 1. Customer browses and selects a product

**Flag: ✅ Implemented**

👤 The customer reads the public product catalog and selects a product or variant.

Relevant public product routes are mounted below /api/v1/public/.

This is a selection step only. Adding the product to the cart happens in the next step.

### 2. Customer adds the product to the cart

**Flag: ✅ Implemented**

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

Current behavior:

- The backend creates an active cart when the customer has none.
- Adding the same product and variant again increases its quantity.
- The backend copies the current product or variant price into the cart item.
- A variant must belong to the selected product.
- New items are selected by default.

### 3. Customer updates quantity and selected items

**Flag: ✅ Implemented**

~~~http
PATCH /api/v1/customer/cart/items/{cart_item_id}/
~~~

Use this route to change quantity or is_selected.

~~~http
POST /api/v1/customer/cart/select-all/
DELETE /api/v1/customer/cart/items/{cart_item_id}/
~~~

Only selected, non-deleted items are included when the order is placed.

### 4. Customer selects a delivery address

**Flag: ⚠️ Partial**

List existing addresses:

~~~http
GET /api/v1/customer/addresses/
~~~

Create an address:

~~~http
POST /api/v1/customer/addresses/
~~~

The address routes work, and order placement requires shipping_address_id.

Current gap: checkout assigns the address ID but does not explicitly verify that the address belongs to the authenticated customer and is still active.

### 5. Customer requests checkout preview

**Flag: ⚠️ Partial**

~~~http
POST /api/v1/customer/cart/checkout-preview/
~~~

~~~json
{
  "shipping_address_id": "adr-000001"
}
~~~

Current calculation:

~~~text
subtotal = sum(selected item price snapshot * quantity)
shipping = 0.00
discount = 0.00
tax      = 0.00
total    = subtotal
currency = USD
~~~

The preview exists, but it does not calculate real shipping, discounts, promotions, or tax. It also does not reserve inventory.

### 6. Customer places the order

**Flag: ⚠️ Partial**

~~~http
POST /api/v1/customer/orders/
~~~

~~~json
{
  "cart_id": "cart-000001",
  "shipping_address_id": "adr-000001",
  "idempotency_key": "one-key-for-this-checkout-attempt"
}
~~~

Implemented system actions:

1. Find the authenticated customer's active cart.
2. Load selected cart items.
3. Lock selected product-variant rows.
4. Validate that each tracked variant is active and has enough stock.
5. Decrease ProductVariant.stock_quantity.
6. Mark a variant out_of_stock when its quantity reaches zero.
7. Group cart items by store.
8. Create one order per store.
9. Create immutable order-item snapshots.
10. Create the first status-history record.
11. Mark the cart checked_out.
12. Soft-delete processed cart items.
13. Commit stock, order, history, and cart changes in one database transaction.

Multi-store checkout returns an array because one checkout may create several orders.

Current gaps:

- idempotency_key is required but is not persisted or enforced.
- Retrying after an uncertain response can create duplicate orders.
- Product prices are not revalidated during order placement.
- Products without variants are allowed but have no stock tracking.

### 7. Order becomes pending

**Flag: ✅ Implemented**

📦 **Order status: pending**

Every new order starts as pending. The backend records:

~~~text
from_status: null
to_status: pending
note: Order placed via cart checkout
~~~

At this point, variant stock has already been decreased. In the current simple design, that decrease acts as the inventory reservation.

### 8. Customer completes payment

**Flag: ✅ Implemented with an internal mock provider**

Complete payment:

~~~http
POST /api/v1/customer/orders/payment/
~~~

~~~json
{
  "idempotency_key": "one-key-for-this-payment-attempt",
  "order_ids": [
    "ord-20261024-0001",
    "ord-20261024-0002"
  ]
}
~~~

Use one request for every order returned by the same multi-store checkout. The order IDs must be unique, belong to the authenticated customer, be pending, and use the same currency.

Read the order payment:

~~~http
GET /api/v1/customer/orders/{order_id}/payment/
~~~

Current internal behavior:

1. Validate that order_ids is not empty and contains no duplicates.
2. Verify every order belongs to the authenticated customer.
3. Lock all orders in a stable order to prevent concurrent payment completion.
4. Return the existing payment batch when the same key and same order set are retried.
5. Reject the key if it was previously used with a different order set.
6. Accept the batch only when every order is pending and unpaid.
7. Use each order's server-side total and currency; the customer cannot submit an amount.
8. Create one payment batch for the combined total.
9. Create one child payment record per order for cancellation and refund tracking.
10. Use `simulate_outcome` to mark the batch and child payments `succeeded` or `failed` (`succeeded` is the default).
11. Store provider references and either `paid_at` or `failure_reason`.

The older single-order endpoint remains available for compatibility:

~~~http
POST /api/v1/customer/orders/{order_id}/payment/
~~~

💳 **Payment status: succeeded**

This provider moves no real money. The payment module isolates the temporary behavior so a real provider can replace it later.

### 9. System confirms the order after payment

**Flag: ✅ Implemented automatically by the internal payment service**

📦 **Order status: confirmed**

Successful internal payment automatically:

1. Changes every order in the batch from pending to confirmed.
2. Adds an order-status-history entry to every order.
3. Returns the succeeded batch and its per-order payment records.
4. Includes the matching child payment in each later order-detail response.

The history note is Payment succeeded via internal payment service.

An admin can also change the status manually:

~~~http
PATCH /api/v1/admin/orders/{order_id}/status/
~~~

~~~json
{
  "status": "confirmed",
  "note": "Order manually confirmed"
}
~~~

The automatic payment route is the correct path for customer payment. A manual admin confirmation does not verify payment.

### 10. Store prepares the order

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Marks that store staff are finding, checking, and preparing the ordered products.

🛠️ Admin or store starts preparing products.
📦 **Order status: processing**

An admin starts preparation through the dedicated route:

~~~http
PATCH /api/v1/admin/orders/{order_id}/processing
~~~

~~~json
{
  "note": "Store started preparing the products"
}
~~~

The backend requires the current order status to be confirmed, changes it to processing, and writes one status-history record. Repeating the route after the order is already processing returns the current order without creating duplicate history.

There is still no seller-facing route, preparation task record, or detailed packing workflow.

### 11. Shipment is created

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Creates the package record that will hold the carrier, tracking number, and delivery progress.

🛠️ Admin or store creates a shipment.
🚚 **Shipment status: pending**

~~~http
POST /api/v1/admin/orders/{order_id}/shipments
~~~

~~~json
{
  "note": "Shipment created for fulfillment"
}
~~~

The order must be processing. The backend creates one pending shipment and one pending shipment event. Repeating the request returns the existing shipment instead of creating another one.

### 12. Products are packed

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Marks that the products have been placed in their delivery packaging and are ready for pickup.

🚚 **Shipment status: packed**

~~~http
PATCH /api/v1/admin/shipments/{shipment_id}/packed
~~~

~~~json
{
  "note": "Products packed and ready for pickup"
}
~~~

The shipment must be pending. The backend changes it to packed and records a packed shipment event. Repeating the request does not create duplicate events.

### 13. Package is handed to the carrier

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Records that the store has given the package to the delivery company and tracking has started.

📦 **Order status: shipped**
🚚 **Shipment status: in_transit**

~~~http
PATCH /api/v1/admin/shipments/{shipment_id}/handoff
~~~

~~~json
{
  "carrier_name": "DHL Express",
  "tracking_number": "DHL-123456",
  "location": "Phnom Penh warehouse",
  "note": "Package handed to carrier"
}
~~~

The shipment must be packed and its order must be processing. The backend saves the carrier and tracking number, sets shipped_at, changes the shipment to in_transit, records an event, changes the order to shipped, and records order status history. Repeating the request does not duplicate events or history.

### 14. Carrier tracking events are recorded

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Shows where the package was scanned or moved so the customer can follow its journey.

~~~http
POST /api/v1/admin/shipments/{shipment_id}/events
~~~

~~~json
{
  "location": "Phnom Penh sorting center",
  "description": "Package scanned at sorting center",
  "event_time": "2026-10-24T14:30:00Z"
}
~~~

The shipment must be in_transit or out_for_delivery. If event_time is omitted, the backend uses the current time. The event records the shipment's current status and does not change that status.

The customer can read shipment information through:

~~~http
GET /api/v1/customer/orders/{order_id}/shipments/
GET /api/v1/customer/shipments/{shipment_id}/
GET /api/v1/customer/shipments/{shipment_id}/events/
~~~

The create, pack, handoff, out-for-delivery, and delivery-confirmation routes also create their own events automatically.

Customer shipment-detail and event routes verify ownership through the shipment's order.

### 15. Package is out for delivery

**Flag: ✅ Implemented for admins**

**Real-world purpose:** Marks that a courier has the package and is taking it to the customer's address that day.

🚚 **Shipment status: out_for_delivery**

~~~http
PATCH /api/v1/admin/shipments/{shipment_id}/out-for-delivery
~~~

~~~json
{
  "location": "Phnom Penh delivery hub",
  "note": "Courier is delivering the package"
}
~~~

The shipment must be in_transit and its order must be shipped. The backend changes the shipment to out_for_delivery and creates an event. The order remains shipped. Repeating the request does not duplicate the event.

### 16. Customer receives the product

**Flag: ✅ Implemented as customer confirmation**

**Real-world purpose:** Lets the customer acknowledge that the package physically arrived and was received.

👤 The customer physically receives the product.

~~~http
POST /api/v1/customer/shipments/{shipment_id}/confirm-delivery
~~~

~~~json
{
  "note": "Product received in good condition"
}
~~~

The shipment must belong to the customer and be out_for_delivery. This is a simple receipt confirmation; signature, photo, one-time code, and carrier webhook verification are not implemented.

### 17. Order and shipment become delivered

**Flag: ✅ Implemented automatically after customer confirmation**

**Real-world purpose:** Closes the fulfillment process and records that the store's delivery responsibility is complete.

🚚 **Shipment status: delivered**
📦 **Order status: delivered**

Customer confirmation changes the shipment to delivered, sets delivered_at, and creates a delivered event. When every active shipment for the order is delivered, the backend changes the order from shipped to delivered and writes order status history. Repeating confirmation returns the delivered shipment without duplicate events or history.

Automatic customer notification is still not implemented.

## Customer cancellation flow

### Customer requests cancellation

**Flag: ✅ Implemented**

Cancellation is allowed only while the order is pending or confirmed:

~~~http
POST /api/v1/customer/orders/{order_id}/cancel/
~~~

Implemented actions:

1. Verify the order belongs to the customer.
2. Lock the order.
3. Restore stock for its product variants.
4. Change an out_of_stock variant back to active after stock is restored.
5. Change the order status to cancelled.
6. Set cancelled_at.
7. Add a status-history record with note Cancelled by customer.

📦 **Order status: cancelled**

### Cancel or refund payment

**Flag: ✅ Implemented for the internal mock payment**

Cancelling a confirmed order changes its child payment to refunded and records refunded_at. A batch becomes partially_refunded while another child payment remains succeeded, then refunded after every child payment is refunded. This is a logical refund only; no real funds are moved.

## Admin cancellation and failure flow

**Flag: ✅ Implemented**

**Real-world purpose:** Cancellation records a deliberate stop, while failure records that payment or fulfillment could not be completed.

~~~http
PATCH /api/v1/admin/orders/{order_id}/cancel
PATCH /api/v1/admin/orders/{order_id}/failed
~~~

~~~json
{
  "note": "Reason for cancelling or failing the order"
}
~~~

Both routes accept only pending, confirmed, or processing orders. They restore reserved variant stock, logically refund a succeeded internal payment, and write status history. Repeating the same route returns the current order without restoring stock or writing history twice. Terminal and shipped orders return `409 ORDER_INVALID_STATUS_TRANSITION`.

## Payment failure flow

**Flag: ✅ Implemented in the internal payment simulator**

Intended flow:

~~~text
Order: pending
→ Payment: failed
→ Restore stock
→ Order: failed
~~~

To test a failed multi-order payment:

~~~http
POST /api/v1/customer/orders/payment/
~~~

~~~json
{
  "idempotency_key": "one-key-for-this-failed-attempt",
  "order_ids": [
    "ord-20261024-0001",
    "ord-20261024-0002"
  ],
  "simulate_outcome": "failed",
  "failure_reason": "Mock card declined"
}
~~~

The operation atomically marks the payment batch and every child payment failed, stores the reason, restores each order's reserved variant stock, changes every order to failed, and writes status history. Retrying the same key and order set returns the original failed batch without repeating stock restoration. This simulates failure only; there is no real provider decline or webhook yet.

## Inventory flow

**Flag: ✅ Implemented as a simple variant-stock design**

The project intentionally uses ProductVariant.stock_quantity without a separate inventory feature.

Checkout behavior:

~~~text
Lock variant rows
→ Add requested quantities per variant
→ Validate active status and available quantity
→ Decrease stock
→ Mark out_of_stock when quantity becomes zero
~~~

Failure response:

~~~text
HTTP 409
code: INSUFFICIENT_STOCK
product_variant_id: affected variant
requested_quantity: requested units
available_quantity: available units
~~~

Restoration behavior:

- Customer cancellation restores variant stock.
- Admin cancellation restores variant stock once.
- Admin failed status restores variant stock once.
- A restored out_of_stock variant becomes active unless it was deleted.

Current limitations:

- Products without a variant are not stock-tracked.
- Pending orders have no expiration time.
- An abandoned pending order continues holding deducted stock.
- There is no stock movement ledger or audit history.
- Refunds and returns do not automatically add stock.
- Admin status transitions can still create stock inconsistencies.

## Customer order-history flow

### List orders

**Flag: ✅ Implemented**

~~~http
GET /api/v1/customer/orders/?page=1&page_size=20
~~~

Returns only the authenticated customer's orders, newest first.

### Read order details

**Flag: ✅ Implemented**

~~~http
GET /api/v1/customer/orders/{order_id}/
~~~

The route checks customer ownership.

### Read status history

**Flag: ⚠️ Partial**

~~~http
GET /api/v1/customer/orders/{order_id}/status-history/
~~~

The chronological history is implemented, but the repository lookup does not currently filter by the authenticated customer. A logged-in customer who knows another order ID may be able to read that timeline.

### Read order shipments

**Flag: ✅ Implemented**

~~~http
GET /api/v1/customer/orders/{order_id}/shipments/
~~~

This route verifies order ownership and returns the shipment created by the admin fulfillment flow.

## Current end-to-end boundary

The currently working business flow is:

~~~text
✅ Product selection
→ ✅ Cart management
→ ⚠️ Address selection
→ ⚠️ Checkout preview
→ ⚠️ Place order
→ ✅ Stock decrease
→ ✅ Order pending
→ ✅ Internal payment succeeded
→ ✅ Order confirmed
→ ✅ Order processing
→ ✅ Shipment pending
→ ✅ Shipment packed
→ ✅ Carrier handoff
→ ✅ Shipment in transit
→ ✅ Order shipped
→ ✅ Carrier checkpoints
→ ✅ Shipment out for delivery
→ ✅ Customer confirms receipt
→ ✅ Shipment delivered
→ ✅ Order delivered
~~~

The simple internal customer-to-delivery flow is now implemented through delivered. Real payment, carrier integration, proof of delivery, and automatic notifications remain future work.

## Recommended implementation order

1. Validate shipping-address ownership during checkout.
2. Persist and enforce idempotency keys.
3. Define one order-status enum and allowed transition map.
4. Add pending-order expiration and stock restoration.
5. Replace internal_mock with a real payment provider and webhook processing.
6. Add real payment failure and retry behavior.
7. Add signature, photo, or one-time-code proof of delivery if required.
8. Add automatic customer notifications.
9. Secure the direct order status-history route by customer ownership.

