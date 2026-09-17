-- ============================================================
-- Ecommerce Platform Data Insertion Script (Public Schema)
-- Tables included: 31
-- Minimum rows per table: 5
-- ============================================================

BEGIN;

-- ============================================================
-- Table: public.legacy_users (at least 5 rows)
-- ============================================================

INSERT INTO public."legacy_users" ("id", "last_login", "first_name", "last_name", "username", "email", "password", "bio", "avatar", "phone_number", "phone_code", "status", "is_staff", "is_superuser", "created_by", "updated_by", "deleted_by", "created_at", "updated_at", "deleted_at") VALUES
    ('00000000-0000-0000-0001-000000000001', '2026-03-01 08:30:00+00', 'Alice', 'Admin', 'legacy_admin', 'legacy_admin@ecom.test', 'pbkdf2_sha256$260000$seedpasswordhash1', 'Lead system administrator', 'https://images.example.com/avatar/legacy1.jpg', '+15550001001', '+1', TRUE, TRUE, TRUE, NULL, NULL, NULL, '2026-01-01 00:00:00+00', '2026-03-01 08:30:00+00', NULL),
    ('00000000-0000-0000-0001-000000000002', '2026-03-02 09:15:00+00', 'Bob', 'Manager', 'legacy_bob', 'legacy_bob@ecom.test', 'pbkdf2_sha256$260000$seedpasswordhash2', 'Regional store manager', 'https://images.example.com/avatar/legacy2.jpg', '+15550001002', '+1', TRUE, TRUE, FALSE, 'legacy_admin', NULL, NULL, '2026-01-02 00:00:00+00', '2026-03-02 09:15:00+00', NULL),
    ('00000000-0000-0000-0001-000000000003', '2026-03-03 10:45:00+00', 'Charlie', 'Seller', 'legacy_charlie', 'legacy_charlie@ecom.test', 'pbkdf2_sha256$260000$seedpasswordhash3', 'Verified marketplace merchant', 'https://images.example.com/avatar/legacy3.jpg', '+15550001003', '+1', TRUE, FALSE, FALSE, 'legacy_admin', NULL, NULL, '2026-01-03 00:00:00+00', '2026-03-03 10:45:00+00', NULL),
    ('00000000-0000-0000-0001-000000000004', '2026-03-04 11:20:00+00', 'Diana', 'Buyer', 'legacy_diana', 'legacy_diana@ecom.test', 'pbkdf2_sha256$260000$seedpasswordhash4', 'Frequent customer', 'https://images.example.com/avatar/legacy4.jpg', '+15550001004', '+1', TRUE, FALSE, FALSE, NULL, NULL, NULL, '2026-01-04 00:00:00+00', '2026-03-04 11:20:00+00', NULL),
    ('00000000-0000-0000-0001-000000000005', '2026-03-05 14:00:00+00', 'Evan', 'Staff', 'legacy_evan', 'legacy_evan@ecom.test', 'pbkdf2_sha256$260000$seedpasswordhash5', 'Support specialist', 'https://images.example.com/avatar/legacy5.jpg', '+15550001005', '+1', TRUE, TRUE, FALSE, 'legacy_admin', NULL, NULL, '2026-01-05 00:00:00+00', '2026-03-05 14:00:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.users (at least 5 rows)
-- ============================================================

INSERT INTO public."users" ("id", "email", "phone_number", "password_hash", "first_name", "last_name", "avatar_url", "role", "status", "email_verified_at", "phone_verified_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0002-000000000001', 'seed.admin@ecom.test', '+85512000001', 'argon2id$seed$adminpasswordhash', 'Sokha', 'Chan', 'https://images.example.com/users/admin.png', 'admin', 'active', '2026-01-01 01:00:00+00', '2026-01-01 01:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0002-000000000002', 'seed.techseller@ecom.test', '+85512000002', 'argon2id$seed$seller1hash', 'Vireak', 'Meas', 'https://images.example.com/users/seller1.png', 'seller', 'active', '2026-01-02 02:00:00+00', '2026-01-02 02:05:00+00', '2026-01-02 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-02 00:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0002-000000000003', 'seed.fashionseller@ecom.test', '+85512000003', 'argon2id$seed$seller2hash', 'Bopha', 'Keo', 'https://images.example.com/users/seller2.png', 'seller', 'active', '2026-01-03 03:00:00+00', '2026-01-03 03:05:00+00', '2026-01-03 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-03 00:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0002-000000000004', 'seed.customer1@ecom.test', '+85512000004', 'argon2id$seed$cust1hash', 'Dara', 'Rath', 'https://images.example.com/users/cust1.png', 'customer', 'active', '2026-01-04 04:00:00+00', '2026-01-04 04:05:00+00', '2026-01-04 00:00:00+00', NULL, '2026-01-04 00:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0002-000000000005', 'seed.customer2@ecom.test', '+85512000005', 'argon2id$seed$cust2hash', 'Chenda', 'Sam', 'https://images.example.com/users/cust2.png', 'customer', 'active', '2026-01-05 05:00:00+00', '2026-01-05 05:05:00+00', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0002-000000000006', 'seed.support@ecom.test', '+85512000006', 'argon2id$seed$supporthash', 'Piseth', 'Lim', 'https://images.example.com/users/support.png', 'support', 'active', '2026-01-06 06:00:00+00', '2026-01-06 06:05:00+00', '2026-01-06 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-06 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.tags (at least 5 rows)
-- ============================================================

INSERT INTO public."tags" ("id", "name", "slug") VALUES
    ('00000000-0000-0000-0003-000000000001', 'Electronics', 'electronics'),
    ('00000000-0000-0000-0003-000000000002', 'Fashion', 'fashion'),
    ('00000000-0000-0000-0003-000000000003', 'Wireless', 'wireless'),
    ('00000000-0000-0000-0003-000000000004', 'Best Seller', 'best-seller'),
    ('00000000-0000-0000-0003-000000000005', 'New Arrival', 'new-arrival')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_profiles (at least 5 rows)
-- ============================================================

INSERT INTO public."user_profiles" ("id", "user_id", "date_of_birth", "gender", "preferred_language", "marketing_opt_in", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0004-000000000001', '00000000-0000-0000-0002-000000000001', '1990-05-15', 'female', 'en', TRUE, '2026-01-01 01:00:00+00', NULL, '2026-01-01 01:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0004-000000000002', '00000000-0000-0000-0002-000000000002', '1988-10-20', 'male', 'en', FALSE, '2026-01-02 02:00:00+00', NULL, '2026-01-02 02:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0004-000000000003', '00000000-0000-0000-0002-000000000003', '1995-03-12', 'female', 'km', TRUE, '2026-01-03 03:00:00+00', NULL, '2026-01-03 03:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0004-000000000004', '00000000-0000-0000-0002-000000000004', '1992-07-28', 'male', 'km', TRUE, '2026-01-04 04:00:00+00', NULL, '2026-01-04 04:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0004-000000000005', '00000000-0000-0000-0002-000000000005', '1997-12-04', 'female', 'en', FALSE, '2026-01-05 05:00:00+00', NULL, '2026-01-05 05:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_addresses (at least 5 rows)
-- ============================================================

INSERT INTO public."user_addresses" ("id", "user_id", "label", "recipient_name", "phone_number", "address_line_1", "address_line_2", "city", "state", "postal_code", "country_code", "latitude", "longitude", "is_default", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0005-000000000001', '00000000-0000-0000-0002-000000000004', 'Home', 'Dara Rath', '+85512000004', '#123 St 2004', 'Sangkat Teuk Thla, Khan Sen Sok', 'Phnom Penh', 'Phnom Penh', '120802', 'KH', 11.5564, 104.8872, TRUE, '2026-01-10 09:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-01-10 09:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0005-000000000002', '00000000-0000-0000-0002-000000000004', 'Office', 'Dara Rath', '+85512000004', 'Exchange Square, Floor 8', 'St 106, Wat Phnom', 'Phnom Penh', 'Phnom Penh', '120211', 'KH', 11.5721, 104.9213, FALSE, '2026-01-11 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-01-11 10:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0005-000000000003', '00000000-0000-0000-0002-000000000005', 'Apartment', 'Chenda Sam', '+85512000005', '#45B Mao Tse Toung Blvd', 'BKK3, Khan Chamkarmon', 'Phnom Penh', 'Phnom Penh', '12304', 'KH', 11.5458, 104.9189, TRUE, '2026-01-12 11:00:00+00', '00000000-0000-0000-0002-000000000005', '2026-01-12 11:00:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0005-000000000004', '00000000-0000-0000-0002-000000000002', 'Store Warehouse', 'Vireak Meas', '+85512000002', 'National Road 4, Km 18', 'Preah Sihanouk Avenue', 'Phnom Penh', 'Kandal', '140101', 'KH', 11.5124, 104.8105, TRUE, '2026-01-13 14:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-13 14:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0005-000000000005', '00000000-0000-0000-0002-000000000003', 'Boutique HQ', 'Bopha Keo', '+85512000003', 'St 51, Corner St 302', 'BKK1', 'Phnom Penh', 'Phnom Penh', '12302', 'KH', 11.5512, 104.9278, TRUE, '2026-01-14 15:30:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-14 15:30:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_security_settings (at least 5 rows)
-- ============================================================

INSERT INTO public."user_security_settings" ("id", "user_id", "two_factor_enabled", "biometric_enabled", "last_password_changed_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0006-000000000001', '00000000-0000-0000-0002-000000000001', TRUE, TRUE, '2026-01-01 01:00:00+00', '2026-01-01 01:00:00+00', NULL, '2026-01-01 01:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0006-000000000002', '00000000-0000-0000-0002-000000000002', TRUE, FALSE, '2026-01-02 02:00:00+00', '2026-01-02 02:00:00+00', NULL, '2026-01-02 02:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0006-000000000003', '00000000-0000-0000-0002-000000000003', FALSE, TRUE, '2026-01-03 03:00:00+00', '2026-01-03 03:00:00+00', NULL, '2026-01-03 03:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0006-000000000004', '00000000-0000-0000-0002-000000000004', FALSE, FALSE, '2026-01-04 04:00:00+00', '2026-01-04 04:00:00+00', NULL, '2026-01-04 04:00:00+00', NULL, NULL, NULL),
    ('00000000-0000-0000-0006-000000000005', '00000000-0000-0000-0002-000000000005', TRUE, TRUE, '2026-01-05 05:00:00+00', '2026-01-05 05:00:00+00', NULL, '2026-01-05 05:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_sessions (at least 5 rows)
-- ============================================================

INSERT INTO public."user_sessions" ("id", "user_id", "device_name", "ip_address", "user_agent", "last_seen_at", "revoked_at", "created_at") VALUES
    ('00000000-0000-0000-0007-000000000001', '00000000-0000-0000-0002-000000000001', 'MacBook Pro M2', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', '2026-03-10 12:00:00+00', NULL, '2026-03-01 08:00:00+00'),
    ('00000000-0000-0000-0007-000000000002', '00000000-0000-0000-0002-000000000002', 'iPhone 15 Pro', '192.168.1.102', 'MobileEcommerceApp/2.4.1 (iOS 17.4)', '2026-03-11 14:20:00+00', NULL, '2026-03-02 09:30:00+00'),
    ('00000000-0000-0000-0007-000000000003', '00000000-0000-0000-0002-000000000003', 'iPad Air 5th Gen', '192.168.1.103', 'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X)', '2026-03-12 16:15:00+00', NULL, '2026-03-03 10:15:00+00'),
    ('00000000-0000-0000-0007-000000000004', '00000000-0000-0000-0002-000000000004', 'Samsung Galaxy S24', '192.168.1.104', 'MobileEcommerceApp/2.4.1 (Android 14)', '2026-03-13 18:00:00+00', NULL, '2026-03-04 11:00:00+00'),
    ('00000000-0000-0000-0007-000000000005', '00000000-0000-0000-0002-000000000005', 'Windows PC Chrome', '192.168.1.105', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0', '2026-03-14 20:45:00+00', NULL, '2026-03-05 15:20:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.categories (at least 5 rows)
-- ============================================================

INSERT INTO public."categories" ("id", "parent_id", "name", "slug", "icon_url", "image_url", "sort_order", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0008-000000000001', NULL, 'Consumer Electronics', 'seed-consumer-electronics', 'https://images.example.com/icons/electronics.svg', 'https://images.example.com/categories/electronics.jpg', 1, 'active', '2026-01-01 02:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 02:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0008-000000000002', '00000000-0000-0000-0008-000000000001', 'Smartphones & Tablets', 'seed-smartphones-tablets', 'https://images.example.com/icons/phones.svg', 'https://images.example.com/categories/phones.jpg', 2, 'active', '2026-01-01 02:10:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 02:10:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0008-000000000003', '00000000-0000-0000-0008-000000000001', 'Audio & Headphones', 'seed-audio-headphones', 'https://images.example.com/icons/audio.svg', 'https://images.example.com/categories/audio.jpg', 3, 'active', '2026-01-01 02:20:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 02:20:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0008-000000000004', NULL, 'Fashion & Apparel', 'seed-fashion-apparel', 'https://images.example.com/icons/fashion.svg', 'https://images.example.com/categories/fashion.jpg', 4, 'active', '2026-01-01 02:30:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 02:30:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0008-000000000005', '00000000-0000-0000-0008-000000000004', 'Footwear & Sneakers', 'seed-footwear-sneakers', 'https://images.example.com/icons/shoes.svg', 'https://images.example.com/categories/shoes.jpg', 5, 'active', '2026-01-01 02:40:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 02:40:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.stores (at least 5 rows)
-- ============================================================

INSERT INTO public."stores" ("id", "owner_id", "name", "slug", "description", "logo_url", "banner_url", "status", "rating_average", "rating_count", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0009-000000000001', '00000000-0000-0000-0002-000000000002', 'TechZone Official', 'seed-techzone-official', 'Premium authentic electronics, gadgets and mobile accessories', 'https://images.example.com/stores/techzone_logo.png', 'https://images.example.com/stores/techzone_banner.jpg', 'active', 4.85, 120, '2026-01-05 08:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-05 08:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0009-000000000002', '00000000-0000-0000-0002-000000000003', 'Urban Thread Boutique', 'seed-urban-thread-boutique', 'Modern urban lifestyle fashion, streetwear and formal apparel', 'https://images.example.com/stores/urban_logo.png', 'https://images.example.com/stores/urban_banner.jpg', 'active', 4.7, 85, '2026-01-06 09:30:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-06 09:30:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0009-000000000003', '00000000-0000-0000-0002-000000000002', 'SmartSound Audio', 'seed-smartsound-audio', 'High-fidelity audiophile gear, earbuds, and home studio sound', 'https://images.example.com/stores/sound_logo.png', 'https://images.example.com/stores/sound_banner.jpg', 'active', 4.9, 210, '2026-01-07 10:15:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-07 10:15:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0009-000000000004', '00000000-0000-0000-0002-000000000003', 'SoleStyle Kicks', 'seed-solestyle-kicks', 'Designer footwear, running sneakers, and casual slip-ons', 'https://images.example.com/stores/sole_logo.png', 'https://images.example.com/stores/sole_banner.jpg', 'active', 4.65, 60, '2026-01-08 11:45:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-08 11:45:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0009-000000000005', '00000000-0000-0000-0002-000000000002', 'Prime Gadgetry', 'seed-prime-gadgetry', 'Smart home devices, IoT hardware, and computing accessories', 'https://images.example.com/stores/gadget_logo.png', 'https://images.example.com/stores/gadget_banner.jpg', 'active', 4.75, 95, '2026-01-09 13:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-09 13:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.carts (at least 5 rows)
-- ============================================================

INSERT INTO public."carts" ("id", "user_id", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0010-000000000001', '00000000-0000-0000-0002-000000000004', 'active', '2026-02-01 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-01 10:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0010-000000000002', '00000000-0000-0000-0002-000000000005', 'active', '2026-02-02 11:30:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-02 11:30:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0010-000000000003', '00000000-0000-0000-0002-000000000004', 'checked_out', '2026-02-03 14:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-03 15:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0010-000000000004', '00000000-0000-0000-0002-000000000005', 'checked_out', '2026-02-04 16:20:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-04 17:00:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0010-000000000005', '00000000-0000-0000-0002-000000000004', 'abandoned', '2026-01-20 08:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-01-22 08:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.search_history (at least 5 rows)
-- ============================================================

INSERT INTO public."search_history" ("id", "user_id", "query", "filters_json", "result_count", "created_at") VALUES
    ('00000000-0000-0000-0011-000000000001', '00000000-0000-0000-0002-000000000004', 'wireless noise cancelling headphones', '{"category": "seed-audio-headphones", "price_max": 350}', 12, '2026-02-10 10:15:00+00'),
    ('00000000-0000-0000-0011-000000000002', '00000000-0000-0000-0002-000000000004', 'flagship smartphone 256gb', '{"category": "seed-smartphones-tablets"}', 8, '2026-02-11 11:20:00+00'),
    ('00000000-0000-0000-0011-000000000003', '00000000-0000-0000-0002-000000000005', 'running sneakers breathable', '{"category": "seed-footwear-sneakers", "rating_min": 4}', 15, '2026-02-12 14:05:00+00'),
    ('00000000-0000-0000-0011-000000000004', '00000000-0000-0000-0002-000000000005', 'oversized graphic hoodie', '{"category": "seed-fashion-apparel"}', 24, '2026-02-13 16:40:00+00'),
    ('00000000-0000-0000-0011-000000000005', NULL, 'portable bluetooth speaker waterproof', '{"price_max": 100}', 19, '2026-02-14 19:10:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.notifications (at least 5 rows)
-- ============================================================

INSERT INTO public."notifications" ("id", "user_id", "type", "title", "body", "data", "read_at", "status", "created_at", "deleted_at") VALUES
    ('00000000-0000-0000-0012-000000000001', '00000000-0000-0000-0002-000000000004', 'order', 'Order Confirmed', 'Your order #ORD-2026-0001 has been confirmed by the store.', '{"order_number": "ORD-2026-0001"}', '2026-02-15 10:05:00+00', 'sent', '2026-02-15 10:00:00+00', NULL),
    ('00000000-0000-0000-0012-000000000002', '00000000-0000-0000-0002-000000000004', 'order', 'Package In Transit', 'Shipment for order #ORD-2026-0001 is on the way.', '{"tracking_number": "TRK-2026-8801"}', NULL, 'sent', '2026-02-16 11:30:00+00', NULL),
    ('00000000-0000-0000-0012-000000000003', '00000000-0000-0000-0002-000000000005', 'promotion', 'Flash Weekend Sale', 'Enjoy 20% off all audio products this weekend with code FLASH20.', '{"coupon": "FLASH20"}', '2026-02-17 09:15:00+00', 'sent', '2026-02-17 08:00:00+00', NULL),
    ('00000000-0000-0000-0012-000000000004', '00000000-0000-0000-0002-000000000005', 'security', 'New Login Detected', 'Your account was accessed from a new device (Windows PC).', '{"ip": "192.168.1.105"}', NULL, 'sent', '2026-02-18 15:45:00+00', NULL),
    ('00000000-0000-0000-0012-000000000005', '00000000-0000-0000-0002-000000000002', 'system', 'Payout Processed', 'Your merchant weekly payout of $1,420.50 has been transferred.', '{"payout_id": "PO-9912"}', '2026-02-19 12:00:00+00', 'sent', '2026-02-19 10:00:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.legal_documents (at least 5 rows)
-- ============================================================

INSERT INTO public."legal_documents" ("id", "type", "title", "version", "content", "published_at", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0013-000000000001', 'terms', 'Terms of Service', 'v1.0', 'General terms and conditions for buyers and merchants using the platform.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0013-000000000002', 'terms', 'Terms of Service', 'v2.0', 'Updated terms including cross-border merchant compliance and arbitration clauses.', '2026-02-01 00:00:00+00', 'published', '2026-02-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-02-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0013-000000000003', 'privacy', 'Privacy & Cookie Policy', 'v1.0', 'Details on personal data processing, telemetry collection, and GDPR compliance.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0013-000000000004', 'refund_policy', 'Customer Return & Refund Policy', 'v1.0', 'Full reimbursement rules, 14-day return window, and damaged goods exchange.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0013-000000000005', 'shipping_policy', 'Logistics & Shipping Standards', 'v1.0', 'Estimated transit times, domestic delivery rates, and courier partner guidelines.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', '2026-01-01 00:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.products (at least 5 rows)
-- ============================================================

INSERT INTO public."products" ("id", "store_id", "category_id", "name", "slug", "description", "base_price", "compare_at_price", "currency", "sku", "status", "rating_average", "rating_count", "sold_count", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0009-000000000001', '00000000-0000-0000-0008-000000000002', 'UltraPhone 15 Pro Max 256GB', 'ultraphone-15-pro-max', 'Next-gen titanium smartphone with A17 pro chip and 5x optical zoom', 1199.0, 1299.0, 'USD', 'SKU-UP15PM-256', 'active', 4.9, 48, 150, '2026-01-15 09:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-15 09:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0014-000000000002', '00000000-0000-0000-0009-000000000003', '00000000-0000-0000-0008-000000000003', 'AeroSound Pro ANC Wireless Earbuds', 'aerosound-pro-anc', 'True wireless stereo earbuds with 45dB active noise cancellation', 189.99, 229.99, 'USD', 'SKU-ASP-ANC-01', 'active', 4.8, 92, 320, '2026-01-16 10:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-16 10:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0014-000000000003', '00000000-0000-0000-0009-000000000002', '00000000-0000-0000-0008-000000000004', 'Heritage Heavyweight Oversized Hoodie', 'heritage-heavyweight-hoodie', '480 GSM organic cotton french terry hoodie with relaxed silhouette', 75.0, 95.0, 'USD', 'SKU-HHH-BLK-01', 'active', 4.7, 35, 110, '2026-01-17 11:00:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-17 11:00:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0014-000000000004', '00000000-0000-0000-0009-000000000004', '00000000-0000-0000-0008-000000000005', 'Apex Runner Nitro Cushion Sneakers', 'apex-runner-nitro', 'Ultralight marathon running shoes with responsive nitrogen foam sole', 140.0, 160.0, 'USD', 'SKU-ARN-RUN-42', 'active', 4.65, 29, 85, '2026-01-18 12:00:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-18 12:00:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0014-000000000005', '00000000-0000-0000-0009-000000000005', '00000000-0000-0000-0008-000000000001', 'OmniCharge 100W GaN Fast Charger', 'omnicharge-100w-gan', 'Compact 4-port fast wall charger with dual USB-C PD 3.0 support', 49.99, 65.0, 'USD', 'SKU-OC-100W-GAN', 'active', 4.85, 64, 450, '2026-01-19 13:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-19 13:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.orders (at least 5 rows)
-- ============================================================

INSERT INTO public."orders" ("id", "order_number", "user_id", "store_id", "shipping_address_id", "status", "subtotal_amount", "shipping_amount", "discount_amount", "tax_amount", "total_amount", "currency", "placed_at", "cancelled_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0015-000000000001', 'ORD-2026-0001', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000001', '00000000-0000-0000-0005-000000000001', 'delivered', 1199.0, 10.0, 50.0, 0.0, 1159.0, 'USD', '2026-02-15 10:00:00+00', NULL, '2026-02-15 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-17 15:00:00+00', '00000000-0000-0000-0002-000000000001', NULL, NULL),
    ('00000000-0000-0000-0015-000000000002', 'ORD-2026-0002', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000003', '00000000-0000-0000-0005-000000000001', 'shipped', 189.99, 5.0, 0.0, 0.0, 194.99, 'USD', '2026-02-18 11:30:00+00', NULL, '2026-02-18 11:30:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-19 09:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0015-000000000003', 'ORD-2026-0003', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0009-000000000002', '00000000-0000-0000-0005-000000000003', 'paid', 75.0, 4.0, 10.0, 0.0, 69.0, 'USD', '2026-02-20 14:15:00+00', NULL, '2026-02-20 14:15:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-20 14:20:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0015-000000000004', 'ORD-2026-0004', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0009-000000000004', '00000000-0000-0000-0005-000000000003', 'processing', 140.0, 5.0, 0.0, 0.0, 145.0, 'USD', '2026-02-22 16:45:00+00', NULL, '2026-02-22 16:45:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-23 08:30:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0015-000000000005', 'ORD-2026-0005', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000005', '00000000-0000-0000-0005-000000000002', 'pending', 49.99, 3.0, 0.0, 0.0, 52.99, 'USD', '2026-02-24 18:00:00+00', NULL, '2026-02-24 18:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-24 18:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.legal_acceptances (at least 5 rows)
-- ============================================================

INSERT INTO public."legal_acceptances" ("id", "user_id", "legal_document_id", "accepted_at", "ip_address") VALUES
    ('00000000-0000-0000-0016-000000000001', '00000000-0000-0000-0002-000000000001', '00000000-0000-0000-0013-000000000001', '2026-01-01 01:00:00+00', '192.168.1.101'),
    ('00000000-0000-0000-0016-000000000002', '00000000-0000-0000-0002-000000000002', '00000000-0000-0000-0013-000000000001', '2026-01-02 02:00:00+00', '192.168.1.102'),
    ('00000000-0000-0000-0016-000000000003', '00000000-0000-0000-0002-000000000003', '00000000-0000-0000-0013-000000000003', '2026-01-03 03:00:00+00', '192.168.1.103'),
    ('00000000-0000-0000-0016-000000000004', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0013-000000000001', '2026-01-04 04:00:00+00', '192.168.1.104'),
    ('00000000-0000-0000-0016-000000000005', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0013-000000000004', '2026-01-05 05:00:00+00', '192.168.1.105')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_images (at least 5 rows)
-- ============================================================

INSERT INTO public."product_images" ("id", "product_id", "image_url", "alt_text", "sort_order", "is_primary", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0017-000000000001', '00000000-0000-0000-0014-000000000001', 'https://images.example.com/products/phone_front.jpg', 'UltraPhone 15 Pro Front View', 1, TRUE, '2026-01-15 09:10:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-15 09:10:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0017-000000000002', '00000000-0000-0000-0014-000000000002', 'https://images.example.com/products/earbuds_case.jpg', 'AeroSound Pro Case and Pods', 1, TRUE, '2026-01-16 10:10:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-16 10:10:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0017-000000000003', '00000000-0000-0000-0014-000000000003', 'https://images.example.com/products/hoodie_black.jpg', 'Heritage Hoodie Model Front', 1, TRUE, '2026-01-17 11:10:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-17 11:10:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0017-000000000004', '00000000-0000-0000-0014-000000000004', 'https://images.example.com/products/sneaker_side.jpg', 'Apex Runner Side Profile', 1, TRUE, '2026-01-18 12:10:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-18 12:10:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0017-000000000005', '00000000-0000-0000-0014-000000000005', 'https://images.example.com/products/charger_ports.jpg', 'OmniCharge 100W Ports Layout', 1, TRUE, '2026-01-19 13:10:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-19 13:10:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_variants (at least 5 rows)
-- ============================================================

INSERT INTO public."product_variants" ("id", "product_id", "sku", "name", "price", "stock_quantity", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0018-000000000001', '00000000-0000-0000-0014-000000000001', 'SKU-UP15PM-256-BLK', 'Natural Titanium / 256GB', 1199.0, 50, 'active', '2026-01-15 09:15:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-15 09:15:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0018-000000000002', '00000000-0000-0000-0014-000000000001', 'SKU-UP15PM-512-BLU', 'Blue Titanium / 512GB', 1399.0, 30, 'active', '2026-01-15 09:15:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-15 09:15:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0018-000000000003', '00000000-0000-0000-0014-000000000002', 'SKU-ASP-ANC-WHT', 'Matte White', 189.99, 100, 'active', '2026-01-16 10:15:00+00', '00000000-0000-0000-0002-000000000002', '2026-01-16 10:15:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0018-000000000004', '00000000-0000-0000-0014-000000000003', 'SKU-HHH-BLK-L', 'Washed Black / Size L', 75.0, 40, 'active', '2026-01-17 11:15:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-17 11:15:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0018-000000000005', '00000000-0000-0000-0014-000000000004', 'SKU-ARN-RUN-42-RED', 'Solar Red / EU 42', 140.0, 25, 'active', '2026-01-18 12:15:00+00', '00000000-0000-0000-0002-000000000003', '2026-01-18 12:15:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_tags (at least 5 rows)
-- ============================================================

INSERT INTO public."product_tags" ("id", "product_id", "tag_id") VALUES
    ('00000000-0000-0000-0019-000000000001', '00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0003-000000000001'),
    ('00000000-0000-0000-0019-000000000002', '00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0003-000000000004'),
    ('00000000-0000-0000-0019-000000000003', '00000000-0000-0000-0014-000000000002', '00000000-0000-0000-0003-000000000003'),
    ('00000000-0000-0000-0019-000000000004', '00000000-0000-0000-0014-000000000003', '00000000-0000-0000-0003-000000000002'),
    ('00000000-0000-0000-0019-000000000005', '00000000-0000-0000-0014-000000000004', '00000000-0000-0000-0003-000000000005')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.favorites (at least 5 rows)
-- ============================================================

INSERT INTO public."favorites" ("id", "user_id", "product_id", "created_at", "deleted_at") VALUES
    ('00000000-0000-0000-0020-000000000001', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000001', '2026-02-05 10:00:00+00', NULL),
    ('00000000-0000-0000-0020-000000000002', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000002', '2026-02-06 11:30:00+00', NULL),
    ('00000000-0000-0000-0020-000000000003', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0014-000000000003', '2026-02-07 14:15:00+00', NULL),
    ('00000000-0000-0000-0020-000000000004', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0014-000000000004', '2026-02-08 16:45:00+00', NULL),
    ('00000000-0000-0000-0020-000000000005', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000005', '2026-02-09 18:20:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.order_status_history (at least 5 rows)
-- ============================================================

INSERT INTO public."order_status_history" ("id", "order_id", "from_status", "to_status", "changed_by_id", "note", "created_at") VALUES
    ('00000000-0000-0000-0021-000000000001', '00000000-0000-0000-0015-000000000001', 'pending', 'confirmed', '00000000-0000-0000-0002-000000000001', 'Payment confirmed via ABA PayWay gateway', '2026-02-15 10:05:00+00'),
    ('00000000-0000-0000-0021-000000000002', '00000000-0000-0000-0015-000000000001', 'confirmed', 'processing', '00000000-0000-0000-0002-000000000002', 'Items picked and packed at warehouse', '2026-02-15 14:00:00+00'),
    ('00000000-0000-0000-0021-000000000003', '00000000-0000-0000-0015-000000000001', 'processing', 'shipped', '00000000-0000-0000-0002-000000000002', 'Handed over to J&T Express courier', '2026-02-16 09:30:00+00'),
    ('00000000-0000-0000-0021-000000000004', '00000000-0000-0000-0015-000000000001', 'shipped', 'delivered', '00000000-0000-0000-0002-000000000001', 'Recipient signed and confirmed delivery', '2026-02-17 15:00:00+00'),
    ('00000000-0000-0000-0021-000000000005', '00000000-0000-0000-0015-000000000002', 'pending', 'paid', '00000000-0000-0000-0002-000000000004', 'Customer paid via Credit Card', '2026-02-18 11:35:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.shipments (at least 5 rows)
-- ============================================================

INSERT INTO public."shipments" ("id", "order_id", "carrier_name", "tracking_number", "status", "shipped_at", "delivered_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0022-000000000001', '00000000-0000-0000-0015-000000000001', 'J&T Express', 'TRK-2026-8801', 'delivered', '2026-02-16 09:30:00+00', '2026-02-17 15:00:00+00', '2026-02-15 14:30:00+00', '00000000-0000-0000-0002-000000000002', '2026-02-17 15:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0022-000000000002', '00000000-0000-0000-0015-000000000002', 'Kerry Express', 'TRK-2026-8802', 'in_transit', '2026-02-19 09:00:00+00', NULL, '2026-02-18 16:00:00+00', '00000000-0000-0000-0002-000000000002', '2026-02-19 09:00:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL),
    ('00000000-0000-0000-0022-000000000003', '00000000-0000-0000-0015-000000000003', 'Flash Express', 'TRK-2026-8803', 'packed', NULL, NULL, '2026-02-21 10:00:00+00', '00000000-0000-0000-0002-000000000003', '2026-02-21 10:00:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0022-000000000004', '00000000-0000-0000-0015-000000000004', 'DHL Express', 'TRK-2026-8804', 'pending', NULL, NULL, '2026-02-23 09:15:00+00', '00000000-0000-0000-0002-000000000003', '2026-02-23 09:15:00+00', '00000000-0000-0000-0002-000000000003', NULL, NULL),
    ('00000000-0000-0000-0022-000000000005', '00000000-0000-0000-0015-000000000005', 'Ninja Van', 'TRK-2026-8805', 'pending', NULL, NULL, '2026-02-24 18:30:00+00', '00000000-0000-0000-0002-000000000002', '2026-02-24 18:30:00+00', '00000000-0000-0000-0002-000000000002', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.conversations (at least 5 rows)
-- ============================================================

INSERT INTO public."conversations" ("id", "customer_id", "store_id", "order_id", "status", "last_message_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0023-000000000001', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000001', '00000000-0000-0000-0015-000000000001', 'closed', '2026-02-17 15:30:00+00', '2026-02-15 11:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-17 15:30:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0023-000000000002', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000003', '00000000-0000-0000-0015-000000000002', 'open', '2026-02-19 10:20:00+00', '2026-02-18 12:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-19 10:20:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0023-000000000003', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0009-000000000002', '00000000-0000-0000-0015-000000000003', 'open', '2026-02-20 15:00:00+00', '2026-02-20 14:30:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-20 15:00:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0023-000000000004', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0009-000000000004', NULL, 'open', '2026-02-21 16:10:00+00', '2026-02-21 16:00:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-21 16:10:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0023-000000000005', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0009-000000000005', NULL, 'archived', '2026-01-25 09:00:00+00', '2026-01-24 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-01-25 09:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.support_tickets (at least 5 rows)
-- ============================================================

INSERT INTO public."support_tickets" ("id", "user_id", "order_id", "subject", "category", "status", "priority", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0024-000000000001', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0015-000000000001', 'Inquire about AppleCare warranty registration', 'other', 'resolved', 'normal', '2026-02-16 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-17 11:00:00+00', '00000000-0000-0000-0002-000000000006', NULL, NULL),
    ('00000000-0000-0000-0024-000000000002', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0015-000000000002', 'Request express courier tracking update', 'delivery', 'open', 'high', '2026-02-19 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-19 10:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0024-000000000003', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0015-000000000003', 'Size exchange request for hoodie', 'order', 'pending', 'normal', '2026-02-21 11:00:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-21 14:00:00+00', '00000000-0000-0000-0002-000000000006', NULL, NULL),
    ('00000000-0000-0000-0024-000000000004', '00000000-0000-0000-0002-000000000005', NULL, 'Payment card 3DS verification failed', 'payment', 'closed', 'urgent', '2026-02-22 09:00:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-22 10:30:00+00', '00000000-0000-0000-0002-000000000006', NULL, NULL),
    ('00000000-0000-0000-0024-000000000005', '00000000-0000-0000-0002-000000000004', NULL, 'How to enable 2FA biometric login', 'account', 'resolved', 'low', '2026-02-23 15:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-23 16:20:00+00', '00000000-0000-0000-0002-000000000006', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.variant_options (at least 5 rows)
-- ============================================================

INSERT INTO public."variant_options" ("id", "product_variant_id", "name", "value") VALUES
    ('00000000-0000-0000-0025-000000000001', '00000000-0000-0000-0018-000000000001', 'Color', 'Natural Titanium'),
    ('00000000-0000-0000-0025-000000000002', '00000000-0000-0000-0018-000000000002', 'Color', 'Blue Titanium'),
    ('00000000-0000-0000-0025-000000000003', '00000000-0000-0000-0018-000000000003', 'Color', 'Matte White'),
    ('00000000-0000-0000-0025-000000000004', '00000000-0000-0000-0018-000000000004', 'Size', 'L'),
    ('00000000-0000-0000-0025-000000000005', '00000000-0000-0000-0018-000000000005', 'Shoe Size', 'EU 42')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.cart_items (at least 5 rows)
-- ============================================================

INSERT INTO public."cart_items" ("id", "cart_id", "product_id", "product_variant_id", "quantity", "unit_price_snapshot", "is_selected", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0026-000000000001', '00000000-0000-0000-0010-000000000001', '00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0018-000000000001', 1, 1199.0, TRUE, '2026-02-01 10:05:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-01 10:05:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0026-000000000002', '00000000-0000-0000-0010-000000000001', '00000000-0000-0000-0014-000000000005', NULL, 2, 49.99, TRUE, '2026-02-01 10:10:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-01 10:10:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0026-000000000003', '00000000-0000-0000-0010-000000000002', '00000000-0000-0000-0014-000000000002', '00000000-0000-0000-0018-000000000003', 1, 189.99, TRUE, '2026-02-02 11:35:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-02 11:35:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0026-000000000004', '00000000-0000-0000-0010-000000000002', '00000000-0000-0000-0014-000000000003', '00000000-0000-0000-0018-000000000004', 1, 75.0, TRUE, '2026-02-02 11:40:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-02 11:40:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0026-000000000005', '00000000-0000-0000-0010-000000000002', '00000000-0000-0000-0014-000000000004', '00000000-0000-0000-0018-000000000005', 1, 140.0, FALSE, '2026-02-02 11:45:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-02 11:45:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.order_items (at least 5 rows)
-- ============================================================

INSERT INTO public."order_items" ("id", "order_id", "product_id", "product_variant_id", "product_name_snapshot", "variant_name_snapshot", "sku_snapshot", "unit_price", "quantity", "line_total", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0027-000000000001', '00000000-0000-0000-0015-000000000001', '00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0018-000000000001', 'UltraPhone 15 Pro Max 256GB', 'Natural Titanium / 256GB', 'SKU-UP15PM-256-BLK', 1199.0, 1, 1199.0, '2026-02-15 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-15 10:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0027-000000000002', '00000000-0000-0000-0015-000000000002', '00000000-0000-0000-0014-000000000002', '00000000-0000-0000-0018-000000000003', 'AeroSound Pro ANC Wireless Earbuds', 'Matte White', 'SKU-ASP-ANC-WHT', 189.99, 1, 189.99, '2026-02-18 11:30:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-18 11:30:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0027-000000000003', '00000000-0000-0000-0015-000000000003', '00000000-0000-0000-0014-000000000003', '00000000-0000-0000-0018-000000000004', 'Heritage Heavyweight Oversized Hoodie', 'Washed Black / Size L', 'SKU-HHH-BLK-L', 75.0, 1, 75.0, '2026-02-20 14:15:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-20 14:15:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0027-000000000004', '00000000-0000-0000-0015-000000000004', '00000000-0000-0000-0014-000000000004', '00000000-0000-0000-0018-000000000005', 'Apex Runner Nitro Cushion Sneakers', 'Solar Red / EU 42', 'SKU-ARN-RUN-42-RED', 140.0, 1, 140.0, '2026-02-22 16:45:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-22 16:45:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0027-000000000005', '00000000-0000-0000-0015-000000000005', '00000000-0000-0000-0014-000000000005', NULL, 'OmniCharge 100W GaN Fast Charger', 'Default', 'SKU-OC-100W-GAN', 49.99, 1, 49.99, '2026-02-24 18:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-24 18:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.shipment_events (at least 5 rows)
-- ============================================================

INSERT INTO public."shipment_events" ("id", "shipment_id", "status", "location", "description", "event_time", "created_at") VALUES
    ('00000000-0000-0000-0028-000000000001', '00000000-0000-0000-0022-000000000001', 'packed', 'Phnom Penh Central Hub', 'Package packed and shipment label generated', '2026-02-15 15:00:00+00', '2026-02-15 15:00:00+00'),
    ('00000000-0000-0000-0028-000000000002', '00000000-0000-0000-0022-000000000001', 'in_transit', 'Sen Sok Sorting Center', 'Departed facility towards destination city', '2026-02-16 10:00:00+00', '2026-02-16 10:00:00+00'),
    ('00000000-0000-0000-0028-000000000003', '00000000-0000-0000-0022-000000000001', 'out_for_delivery', 'Khan Sen Sok Delivery Station', 'Out for delivery with courier rider Sothea', '2026-02-17 08:30:00+00', '2026-02-17 08:30:00+00'),
    ('00000000-0000-0000-0028-000000000004', '00000000-0000-0000-0022-000000000001', 'delivered', 'Customer Residence', 'Delivered and signed by recipient Dara Rath', '2026-02-17 15:00:00+00', '2026-02-17 15:00:00+00'),
    ('00000000-0000-0000-0028-000000000005', '00000000-0000-0000-0022-000000000002', 'in_transit', 'Daun Penh Distribution Center', 'Shipment scanned into transit conveyor', '2026-02-19 11:15:00+00', '2026-02-19 11:15:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.messages (at least 5 rows)
-- ============================================================

INSERT INTO public."messages" ("id", "conversation_id", "sender_id", "message_type", "body", "attachment_url", "read_at", "created_at", "deleted_at") VALUES
    ('00000000-0000-0000-0029-000000000001', '00000000-0000-0000-0023-000000000001', '00000000-0000-0000-0002-000000000004', 'text', 'Hello, is the 256GB Natural Titanium phone currently in stock?', NULL, '2026-02-15 11:05:00+00', '2026-02-15 11:00:00+00', NULL),
    ('00000000-0000-0000-0029-000000000002', '00000000-0000-0000-0023-000000000001', '00000000-0000-0000-0002-000000000002', 'text', 'Yes Dara! We have sealed units ready for same-day dispatch.', NULL, '2026-02-15 11:10:00+00', '2026-02-15 11:08:00+00', NULL),
    ('00000000-0000-0000-0029-000000000003', '00000000-0000-0000-0023-000000000002', '00000000-0000-0000-0002-000000000004', 'text', 'Hi SmartSound, does this model support multipoint Bluetooth?', NULL, '2026-02-18 12:10:00+00', '2026-02-18 12:00:00+00', NULL),
    ('00000000-0000-0000-0029-000000000004', '00000000-0000-0000-0023-000000000002', '00000000-0000-0000-0002-000000000002', 'text', 'Yes, you can pair up to 2 devices simultaneously seamlessly.', NULL, '2026-02-18 12:15:00+00', '2026-02-18 12:12:00+00', NULL),
    ('00000000-0000-0000-0029-000000000005', '00000000-0000-0000-0023-000000000003', '00000000-0000-0000-0002-000000000005', 'text', 'Could you provide measurements for the Size L hoodie chest width?', NULL, NULL, '2026-02-20 14:30:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.support_ticket_messages (at least 5 rows)
-- ============================================================

INSERT INTO public."support_ticket_messages" ("id", "ticket_id", "sender_id", "body", "attachment_url", "created_at", "deleted_at") VALUES
    ('00000000-0000-0000-0030-000000000001', '00000000-0000-0000-0024-000000000001', '00000000-0000-0000-0002-000000000004', 'Hi, I just received my UltraPhone. Can you send me the official tax invoice for warranty registration?', NULL, '2026-02-16 10:00:00+00', NULL),
    ('00000000-0000-0000-0030-000000000002', '00000000-0000-0000-0024-000000000001', '00000000-0000-0000-0002-000000000006', 'Hello Dara, I have attached your official VAT tax invoice PDF. You can upload this directly to the Apple portal.', 'https://invoices.example.com/inv-2026-0001.pdf', '2026-02-16 11:30:00+00', NULL),
    ('00000000-0000-0000-0030-000000000003', '00000000-0000-0000-0024-000000000002', '00000000-0000-0000-0002-000000000004', 'The tracking code TRK-2026-8802 is showing in transit for 2 days without scan. Could you check with Kerry?', NULL, '2026-02-19 10:00:00+00', NULL),
    ('00000000-0000-0000-0030-000000000004', '00000000-0000-0000-0024-000000000003', '00000000-0000-0000-0002-000000000005', 'I received the Size L hoodie but it runs too oversized for me. Can I exchange for Size M?', NULL, '2026-02-21 11:00:00+00', NULL),
    ('00000000-0000-0000-0030-000000000005', '00000000-0000-0000-0024-000000000003', '00000000-0000-0000-0002-000000000006', 'Sure Chenda! Please keep all tags attached and our courier will swap with Size M tomorrow.', NULL, '2026-02-21 14:00:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_reviews (at least 5 rows)
-- ============================================================

INSERT INTO public."product_reviews" ("id", "user_id", "product_id", "order_item_id", "rating", "title", "body", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('00000000-0000-0000-0031-000000000001', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000001', '00000000-0000-0000-0027-000000000001', 5, 'Incredible camera and battery life!', 'The titanium frame feels noticeably lighter in hand. 5x telephoto is super sharp. Delivered fast by TechZone!', 'published', '2026-02-18 10:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-18 10:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0031-000000000002', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000002', '00000000-0000-0000-0027-000000000002', 5, 'Best noise cancellation under $200', 'Comfortable for all-day zoom meetings and airplane flights. Deep punchy bass without distortion.', 'published', '2026-02-20 16:30:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-20 16:30:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL),
    ('00000000-0000-0000-0031-000000000003', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0014-000000000003', '00000000-0000-0000-0027-000000000003', 4, 'High quality heavyweight fabric', 'Super warm and thick 480gsm cotton. Runs slightly large so size down if you prefer fitted look.', 'published', '2026-02-22 18:00:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-22 18:00:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0031-000000000004', '00000000-0000-0000-0002-000000000005', '00000000-0000-0000-0014-000000000004', '00000000-0000-0000-0027-000000000004', 5, 'Great cushioning for daily 10k runs', 'The nitrogen foam absorbs road impact well. Highly breathable mesh upper keeps feet cool in hot weather.', 'published', '2026-02-24 19:20:00+00', '00000000-0000-0000-0002-000000000005', '2026-02-24 19:20:00+00', '00000000-0000-0000-0002-000000000005', NULL, NULL),
    ('00000000-0000-0000-0031-000000000005', '00000000-0000-0000-0002-000000000004', '00000000-0000-0000-0014-000000000005', '00000000-0000-0000-0027-000000000005', 5, 'Charges my laptop and phone fast together', 'Very compact GaN charger. It stays cool even when outputting max 100W power.', 'published', '2026-02-25 12:00:00+00', '00000000-0000-0000-0002-000000000004', '2026-02-25 12:00:00+00', '00000000-0000-0000-0002-000000000004', NULL, NULL)
ON CONFLICT DO NOTHING;

COMMIT;
