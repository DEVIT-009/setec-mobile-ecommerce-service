# ID Strategy Enhancement

## 1. Objective

Replace the current UUID-based identifiers for the listed eCommerce entities with human-readable, business-formatted identifiers.

The formatted identifier itself will be the model's **primary key**. No additional internal numeric `id` or separate `public_id` field is required.

All formatted identifiers use lowercase prefixes.

---

## 2. ID Strategy

### 2.1 Formatted IDs

Entities that use a formatted identifier will use:

```python
id = models.CharField(
    max_length=<appropriate_length>,
    primary_key=True,
    editable=False,
)
```

The identifier must be generated automatically by the application/database-safe mechanism and must not be manually entered by API clients.

Examples:

```text
prod-000001
vrn-000001
opt-000001
```

### 2.2 Numeric IDs

Entities explicitly defined as numeric IDs will use an auto-incrementing integer primary key:

```python
id = models.BigAutoField(primary_key=True)
```

The following entities use numeric IDs:

```text
Favorite
Search History
```

---

## 3. Complete ID Mapping

| Entity | ID Format | Django Type | Example | Sequence Rule |
|---|---|---|---|---|
| Product | `prod-000001` | `CharField` PK | `prod-000001` | Global increment |
| Product Variant | `vrn-000001` | `CharField` PK | `vrn-000001` | Global increment |
| Variant Option | `opt-000001` | `CharField` PK | `opt-000001` | Global increment |
| Product Image | `pimg-000001` | `CharField` PK | `pimg-000001` | Global increment |
| Product Tag | `tag-000001` | `CharField` PK | `tag-000001` | Global increment |
| Category | `cat-000001` | `CharField` PK | `cat-000001` | Global increment |
| Store | `str-000001` | `CharField` PK | `str-000001` | Global increment |
| Cart | `cart-000001` | `CharField` PK | `cart-000001` | Global increment |
| Cart Item | `citm-000001` | `CharField` PK | `citm-000001` | Global increment |
| Order | `ord-YYYYMMDD-0001` | `CharField` PK | `ord-20260920-0001` | Reset daily |
| Order Item | `oitm-000001` | `CharField` PK | `oitm-000001` | Global increment |
| Order Status Log | `ordst-000001` | `CharField` PK | `ordst-000001` | Global increment |
| Address | `adr-000001` | `CharField` PK | `adr-000001` | Global increment |
| Shipment | `ship-000001` | `CharField` PK | `ship-000001` | Global increment |
| Shipment Event | `shpev-000001` | `CharField` PK | `shpev-000001` | Global increment |
| Review | `rvw-000001` | `CharField` PK | `rvw-000001` | Global increment |
| Favorite | `1, 2, 3...` | `BigAutoField` PK | `1` | Global increment |
| Conversation | `conv-000001` | `CharField` PK | `conv-000001` | Global increment |
| Message | `msg-000001` | `CharField` PK | `msg-000001` | Global increment |
| Ticket | `tck-000001` | `CharField` PK | `tck-000001` | Global increment |
| Ticket Message | `tmsg-000001` | `CharField` PK | `tmsg-000001` | Global increment |
| Notification | `ntf-000001` | `CharField` PK | `ntf-000001` | Global increment |
| Search History | `1, 2, 3...` | `BigAutoField` PK | `1` | Global increment |
| Legal Document | `legdoc-01` | `CharField` PK | `legdoc-01` | Defined sequence |
| Legal Acceptance | `lacc-000001` | `CharField` PK | `lacc-000001` | Global increment |

---

## 4. Prefix Rules

All prefixes must be lowercase and consistent.

```text
prod-    Product
vrn-     Product Variant
opt-     Variant Option
pimg-    Product Image
tag-     Product Tag
cat-     Category
str-     Store
cart-    Cart
citm-    Cart Item
ord-     Order
oitm-    Order Item
ordst-   Order Status Log
adr-     Address
ship-    Shipment
shpev-   Shipment Event
rvw-     Review
conv-    Conversation
msg-     Message
tck-     Ticket
tmsg-    Ticket Message
ntf-     Notification
legdoc-  Legal Document
lacc-    Legal Acceptance
```

---

## 5. Order ID Rules

Orders are the only entity whose sequence resets based on the calendar date.

Format:

```text
ord-YYYYMMDD-NNNN
```

Example for September 20, 2026:

```text
ord-20260920-0001
ord-20260920-0002
ord-20260920-0003
```

On the next day, the sequence resets:

```text
ord-20260921-0001
ord-20260921-0002
ord-20260921-0003
```

The daily sequence must be generated atomically and safely under concurrent requests.

Do **not** generate the sequence using:

```python
Order.objects.filter(...).count() + 1
```

because concurrent order creation can produce duplicate numbers.

---

## 6. Order Item ID Rules

Order Item IDs are completely independent from Order IDs.

Format:

```text
oitm-NNNNNN
```

Example:

```text
oitm-000001
oitm-000002
oitm-000003
oitm-000004
```

The sequence:

- does not reset daily
- does not reset for each order
- does not contain the order number
- is globally incrementing

Example:

```text
ord-20260920-0001
    ├── oitm-000001
    └── oitm-000002

ord-20260920-0002
    └── oitm-000003

ord-20260921-0001
    ├── oitm-000004
    └── oitm-000005
```

The relationship between an Order and its Order Items is still maintained through the normal foreign key.

---

## 7. ID Generation Requirements

Formatted IDs must be generated automatically.

API clients must not be allowed to choose or modify generated IDs during normal create operations.

For global sequences, the generation mechanism must be safe under concurrent requests.

For daily Order sequences, the sequence must be scoped by the order date and generated atomically.

Do not use record counting to generate IDs:

```python
Model.objects.count() + 1
```

or:

```python
Model.objects.filter(...).count() + 1
```

because deletion and concurrent requests can cause duplicate identifiers.

---

## 8. Model Relationship Changes

Because the formatted identifier is the actual primary key, Django foreign keys will reference the corresponding `CharField` primary key.

Example:

```python
class Product(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False,
    )
```

A related model can reference it normally:

```python
class ProductImage(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
```

No separate:

```text
numeric id
public_id
product_code
```

field is required when the formatted ID itself is the primary key.

---

## 9. API URL Changes

Current UUID URL parameters must be changed to string parameters where applicable.

For example:

### Before

```text
/api/v1/public/products/<uuid:product_id>/
```

### After

```text
/api/v1/public/products/<str:product_id>/
```

Example request:

```text
/api/v1/public/products/prod-000001/
```

The same change applies to all formatted IDs:

```text
/variants/<str:variant_id>/
/categories/<str:category_id>/
/stores/<str:store_id>/
/customer/orders/<str:order_id>/
/customer/cart/items/<str:cart_item_id>/
/customer/addresses/<str:address_id>/
/customer/shipments/<str:shipment_id>/
/customer/conversations/<str:conversation_id>/
/customer/messages/<str:message_id>/
/customer/notifications/<str:notification_id>/
/customer/search-history/<str:search_id>/
/admin/legal-documents/<str:legal_document_id>/
```

Numeric IDs such as Favorite and Search History can continue to use an integer URL converter where appropriate.

---

## 10. Existing UUID Usage to Migrate

The current project uses UUIDs across the following areas:

### Catalog & Products

- Product
- Product Variant
- Variant Option
- Product Image
- Product Tag

### Categories

- Category

### Stores / Merchants

- Store

### Cart

- Cart
- Cart Item

### Orders

- Order
- Order Item
- Order Status History

### Customer Addresses

- Address

### Shipments & Tracking

- Shipment
- Shipment Event

### Reviews

- Review
- Purchase verification through Order Item

### Favorites

- Favorite
- Product reference in Favorite endpoints

### Live Chat & Messaging

- Conversation
- Message

### Support Tickets

- Ticket
- Ticket Message

### Notifications

- Notification

### Search History

- Search Entry

### Legal Documents

- Legal Document
- Legal Acceptance

User identifiers are excluded from this enhancement unless explicitly changed separately.

---

## 11. Migration Requirements

The migration must update:

1. Django model primary key definitions.
2. Foreign key definitions and relationships.
3. Serializers.
4. Repository/database queries.
5. Use cases and domain logic where IDs are handled.
6. URL patterns and path converters.
7. Views/controllers.
8. API request validation.
9. API response schemas.
10. Tests and fixtures.
11. Existing database records, if migration is performed against existing data.
12. Any documentation or examples containing UUID identifiers.

Existing UUID values must not be blindly converted into the new formatted IDs. A deterministic migration strategy must generate valid new IDs and update all dependent foreign-key references consistently.

---

## 12. Validation Requirements

Formatted IDs must follow their entity-specific format.

Examples:

```text
prod-000001     ✓
prod-000002     ✓
PROD-000001     ✗
product-000001  ✗
prod-1          ✗
```

Order IDs:

```text
ord-20260920-0001  ✓
ord-20260920-0002  ✓
ord-20260921-0001  ✓
```

Invalid examples:

```text
ORD-20260920-0001     ✗
ord-2026-09-20-0001   ✗
ord-20260920-1        ✗
```

The generated ID must be unique.

---

## 13. Final Design

The final ID architecture is:

```text
Formatted business ID
        │
        └── Actual database primary key
              │
              ├── CharField for prefixed IDs
              │
              └── BigAutoField for numeric IDs
```

There is **no additional internal numeric ID** and **no separate public ID field** for entities using formatted IDs.

### Examples

```text
Product
    prod-000001

Variant
    vrn-000001

Product Image
    pimg-000001

Order
    ord-20260920-0001

Order Item
    oitm-000001

Order Status Log
    ordst-000001

Shipment Event
    shpev-000001

Ticket Message
    tmsg-000001

Legal Acceptance
    lacc-000001
```

This is the final identifier strategy to implement across the project.
