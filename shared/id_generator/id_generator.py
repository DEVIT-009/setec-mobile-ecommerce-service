"""
Atomic, concurrent-safe ID generator for eCommerce entities.

Global sequences:  prod-, vrn-, opt-, pimg-, tag-, cat-, str-, cart-, citm-,
                   oitm-, ordst-, adr-, ship-, shpev-, rvw-, conv-, msg-,
                   tck-, tmsg-, ntf-, lacc-

Daily sequence:    ord-YYYYMMDD-  (resets each calendar day)
Special:           legdoc-  uses 2-digit padding (legdoc-01)
"""
from __future__ import annotations

import re
from datetime import date
from django.db import transaction
from django.utils import timezone

# ---------------------------------------------------------------------------
# Prefix registry
# ---------------------------------------------------------------------------
GLOBAL_PREFIXES: dict[str, str] = {
    "product":          "prod",
    "variant":          "vrn",
    "option":           "opt",
    "product_image":    "pimg",
    "tag":              "tag",
    "category":         "cat",
    "store":            "str",
    "cart":             "cart",
    "cart_item":        "citm",
    "order_item":       "oitm",
    "order_status_log": "ordst",
    "address":          "adr",
    "shipment":         "ship",
    "shipment_event":   "shpev",
    "review":           "rvw",
    "conversation":     "conv",
    "message":          "msg",
    "ticket":           "tck",
    "ticket_message":   "tmsg",
    "notification":     "ntf",
    "legal_document":   "legdoc",
    "legal_acceptance": "lacc",
}

# Entities that use 2-digit padding (e.g. legdoc-01)
SHORT_SEQUENCE_PREFIXES: set[str] = {"legdoc"}

# ---------------------------------------------------------------------------
# Validation patterns
# ---------------------------------------------------------------------------
_GLOBAL_PATTERN = re.compile(r'^[a-z]+-\d{6}$')
_ORDER_PATTERN  = re.compile(r'^ord-\d{8}-\d{4}$')
_LEGDOC_PATTERN = re.compile(r'^legdoc-\d{2}$')


def is_valid_formatted_id(prefix_key: str, value: str) -> bool:
    """Return True if *value* matches the expected format for *prefix_key*."""
    if prefix_key == "order":
        return bool(_ORDER_PATTERN.match(value))
    if prefix_key == "legal_document":
        return bool(_LEGDOC_PATTERN.match(value))
    prefix = GLOBAL_PREFIXES.get(prefix_key)
    if prefix is None:
        return False
    return bool(_GLOBAL_PATTERN.match(value)) and value.startswith(f"{prefix}-")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_sequence_model():
    """Lazy import to avoid circular imports at module load time."""
    from infrastructure.persistence.models.id_sequence_model import IdSequence
    return IdSequence


def _next_global(prefix_key: str) -> str:
    """
    Atomically increment the global counter for *prefix_key* and return a
    formatted identifier string.

    Uses SELECT FOR UPDATE to serialise concurrent writers.
    """
    IdSequence = _get_sequence_model()
    prefix = GLOBAL_PREFIXES[prefix_key]
    padding = 2 if prefix in SHORT_SEQUENCE_PREFIXES else 6

    with transaction.atomic():
        seq, _ = IdSequence.objects.select_for_update().get_or_create(
            sequence_key=prefix_key,
            defaults={"current_value": 0},
        )
        seq.current_value += 1
        seq.save(update_fields=["current_value"])
        return f"{prefix}-{seq.current_value:0{padding}d}"


def _next_order(order_date: date | None = None) -> str:
    """
    Atomically increment the *per-day* order counter and return an order ID
    in the format ``ord-YYYYMMDD-NNNN``.

    The counter resets automatically whenever *order_date* changes.
    """
    IdSequence = _get_sequence_model()
    today = order_date or timezone.localdate()
    sequence_key = f"order_{today.strftime('%Y%m%d')}"

    with transaction.atomic():
        seq, _ = IdSequence.objects.select_for_update().get_or_create(
            sequence_key=sequence_key,
            defaults={"current_value": 0},
        )
        seq.current_value += 1
        seq.save(update_fields=["current_value"])
        return f"ord-{today.strftime('%Y%m%d')}-{seq.current_value:04d}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_product_id() -> str:
    return _next_global("product")

def generate_variant_id() -> str:
    return _next_global("variant")

def generate_option_id() -> str:
    return _next_global("option")

def generate_product_image_id() -> str:
    return _next_global("product_image")

def generate_tag_id() -> str:
    return _next_global("tag")

def generate_category_id() -> str:
    return _next_global("category")

def generate_store_id() -> str:
    return _next_global("store")

def generate_cart_id() -> str:
    return _next_global("cart")

def generate_cart_item_id() -> str:
    return _next_global("cart_item")

def generate_order_id(order_date: date | None = None) -> str:
    return _next_order(order_date)

def generate_order_item_id() -> str:
    return _next_global("order_item")

def generate_order_status_log_id() -> str:
    return _next_global("order_status_log")

def generate_address_id() -> str:
    return _next_global("address")

def generate_shipment_id() -> str:
    return _next_global("shipment")

def generate_shipment_event_id() -> str:
    return _next_global("shipment_event")

def generate_review_id() -> str:
    return _next_global("review")

def generate_conversation_id() -> str:
    return _next_global("conversation")

def generate_message_id() -> str:
    return _next_global("message")

def generate_ticket_id() -> str:
    return _next_global("ticket")

def generate_ticket_message_id() -> str:
    return _next_global("ticket_message")

def generate_notification_id() -> str:
    return _next_global("notification")

def generate_legal_document_id() -> str:
    return _next_global("legal_document")

def generate_legal_acceptance_id() -> str:
    return _next_global("legal_acceptance")
