-- ============================================================
-- ID Sequence Synchronization Script for eCommerce Platform
-- Target File: id_sequence.sql
-- Model Reference: infrastructure/persistence/models/id_sequence_model.py
-- Generator Reference: shared/id_generator/id_generator.py
-- ============================================================
-- Description:
--   Synchronizes the "id_sequences" table with current data across
--   all domain tables to prevent Primary Key collision when new
--   entities are created via the application's ID generator.
--
--   This script is IDEMPOTENT and can be executed at any time or
--   after executing manual raw SQL inserts (e.g., seed scripts).
--   It uses GREATEST(id_sequences.current_value, EXCLUDED.current_value)
--   so existing higher counters are never accidentally decreased.
-- ============================================================

BEGIN;

-- ============================================================
-- 1. Global Entity Sequences
-- ============================================================
-- Maps each sequence_key in shared/id_generator/id_generator.py
-- to the corresponding table and prefix:
--   product            -> products (prod-NNNNNN)
--   variant            -> product_variants (vrn-NNNNNN)
--   option             -> variant_options (opt-NNNNNN)
--   product_image      -> product_images (pimg-NNNNNN)
--   tag                -> tags & product_tags (tag-NNNNNN)
--   category           -> categories (cat-NNNNNN)
--   store              -> stores (str-NNNNNN)
--   cart               -> carts (cart-NNNNNN)
--   cart_item          -> cart_items (citm-NNNNNN)
--   order_item         -> order_items (oitm-NNNNNN)
--   order_status_log   -> order_status_history (ordst-NNNNNN)
--   address            -> user_addresses (adr-NNNNNN)
--   shipment           -> shipments (ship-NNNNNN)
--   shipment_event     -> shipment_events (shpev-NNNNNN)
--   review             -> reviews (rvw-NNNNNN)
--   conversation       -> conversations (conv-NNNNNN)
--   message            -> messages (msg-NNNNNN)
--   ticket             -> support_tickets (tck-NNNNNN)
--   ticket_message     -> support_ticket_messages (tmsg-NNNNNN)
--   notification       -> notifications (ntf-NNNNNN)
--   legal_document     -> legal_documents (legdoc-NN)
--   legal_acceptance   -> legal_acceptances (lacc-NNNNNN)
-- ============================================================

INSERT INTO public."id_sequences" ("sequence_key", "current_value")
VALUES
    ('product', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^prod-', ''), ''))::bigint FROM public."products" WHERE id ~ '^prod-\d+$'), 0)),
    ('variant', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^vrn-', ''), ''))::bigint FROM public."product_variants" WHERE id ~ '^vrn-\d+$'), 0)),
    ('option', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^opt-', ''), ''))::bigint FROM public."variant_options" WHERE id ~ '^opt-\d+$'), 0)),
    ('product_image', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^pimg-', ''), ''))::bigint FROM public."product_images" WHERE id ~ '^pimg-\d+$'), 0)),
    ('tag', GREATEST(
        COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^tag-', ''), ''))::bigint FROM public."tags" WHERE id ~ '^tag-\d+$'), 0),
        COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^tag-', ''), ''))::bigint FROM public."product_tags" WHERE id ~ '^tag-\d+$'), 0)
    )),
    ('category', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^cat-', ''), ''))::bigint FROM public."categories" WHERE id ~ '^cat-\d+$'), 0)),
    ('store', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^str-', ''), ''))::bigint FROM public."stores" WHERE id ~ '^str-\d+$'), 0)),
    ('cart', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^cart-', ''), ''))::bigint FROM public."carts" WHERE id ~ '^cart-\d+$'), 0)),
    ('cart_item', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^citm-', ''), ''))::bigint FROM public."cart_items" WHERE id ~ '^citm-\d+$'), 0)),
    ('order_item', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^oitm-', ''), ''))::bigint FROM public."order_items" WHERE id ~ '^oitm-\d+$'), 0)),
    ('order_status_log', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^ordst-', ''), ''))::bigint FROM public."order_status_history" WHERE id ~ '^ordst-\d+$'), 0)),
    ('address', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^adr-', ''), ''))::bigint FROM public."user_addresses" WHERE id ~ '^adr-\d+$'), 0)),
    ('shipment', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^ship-', ''), ''))::bigint FROM public."shipments" WHERE id ~ '^ship-\d+$'), 0)),
    ('shipment_event', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^shpev-', ''), ''))::bigint FROM public."shipment_events" WHERE id ~ '^shpev-\d+$'), 0)),
    ('review', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^rvw-', ''), ''))::bigint FROM public."reviews" WHERE id ~ '^rvw-\d+$'), 0)),
    ('conversation', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^conv-', ''), ''))::bigint FROM public."conversations" WHERE id ~ '^conv-\d+$'), 0)),
    ('message', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^msg-', ''), ''))::bigint FROM public."messages" WHERE id ~ '^msg-\d+$'), 0)),
    ('ticket', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^tck-', ''), ''))::bigint FROM public."support_tickets" WHERE id ~ '^tck-\d+$'), 0)),
    ('ticket_message', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^tmsg-', ''), ''))::bigint FROM public."support_ticket_messages" WHERE id ~ '^tmsg-\d+$'), 0)),
    ('notification', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^ntf-', ''), ''))::bigint FROM public."notifications" WHERE id ~ '^ntf-\d+$'), 0)),
    ('legal_document', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^legdoc-', ''), ''))::bigint FROM public."legal_documents" WHERE id ~ '^legdoc-\d+$'), 0)),
    ('legal_acceptance', COALESCE((SELECT MAX(NULLIF(regexp_replace(id, '^lacc-', ''), ''))::bigint FROM public."legal_acceptances" WHERE id ~ '^lacc-\d+$'), 0))
ON CONFLICT ("sequence_key")
DO UPDATE SET "current_value" = GREATEST(public."id_sequences"."current_value", EXCLUDED."current_value");

-- ============================================================
-- 2. Daily Order Sequences (order_YYYYMMDD)
-- ============================================================
-- Orders use per-day sequence format: ord-YYYYMMDD-NNNN
-- This query dynamically discovers all existing dates in the orders table
-- and sets each day's sequence to its maximum 4-digit number.
-- ============================================================

INSERT INTO public."id_sequences" ("sequence_key", "current_value")
SELECT
    'order_' || (regexp_match(id, '^ord-(\d{8})-\d{4}$'))[1] AS sequence_key,
    MAX((regexp_match(id, '^ord-\d{8}-(\d{4})$'))[1]::bigint) AS current_value
FROM public."orders"
WHERE id ~ '^ord-\d{8}-\d{4}$'
GROUP BY (regexp_match(id, '^ord-(\d{8})-\d{4}$'))[1]
ON CONFLICT ("sequence_key")
DO UPDATE SET "current_value" = GREATEST(public."id_sequences"."current_value", EXCLUDED."current_value");

COMMIT;

-- ============================================================
-- Verification: Display updated sequences
-- ============================================================
SELECT "sequence_key", "current_value"
FROM public."id_sequences"
ORDER BY "sequence_key";
