-- ============================================================
-- Ecommerce Customer Domain Data Insertion Script
-- Target: Tables used with Customer domain & lifecycle
-- File: insert_2_script.sql
-- Minimum rows per table: 5
-- ============================================================

BEGIN;

-- ============================================================
-- Table: public.users (Staff, Sellers, and 5 Dedicated Customers)
-- ============================================================

INSERT INTO public."users" ("id", "email", "phone_number", "password_hash", "first_name", "last_name", "avatar_url", "role", "status", "email_verified_at", "phone_verified_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0001-000000000001', 'dara.customer@cust.test', '+85599000001', 'argon2id$cust$hash1', 'Dara', 'Rath', 'https://images.example.com/customers/dara.jpg', 'customer', 'active', '2026-01-10 08:00:00+00', '2026-01-10 08:05:00+00', '2026-01-10 08:00:00+00', NULL, '2026-01-10 08:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0001-000000000002', 'chenda.customer@cust.test', '+85599000002', 'argon2id$cust$hash2', 'Chenda', 'Sam', 'https://images.example.com/customers/chenda.jpg', 'customer', 'active', '2026-01-11 09:00:00+00', '2026-01-11 09:05:00+00', '2026-01-11 09:00:00+00', NULL, '2026-01-11 09:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0001-000000000003', 'sreyneang.customer@cust.test', '+85599000003', 'argon2id$cust$hash3', 'Sreyneang', 'Heng', 'https://images.example.com/customers/sreyneang.jpg', 'customer', 'active', '2026-01-12 10:00:00+00', '2026-01-12 10:05:00+00', '2026-01-12 10:00:00+00', NULL, '2026-01-12 10:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0001-000000000004', 'vutha.customer@cust.test', '+85599000004', 'argon2id$cust$hash4', 'Vutha', 'Sok', 'https://images.example.com/customers/vutha.jpg', 'customer', 'active', '2026-01-13 11:00:00+00', '2026-01-13 11:05:00+00', '2026-01-13 11:00:00+00', NULL, '2026-01-13 11:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0001-000000000005', 'linda.customer@cust.test', '+85599000005', 'argon2id$cust$hash5', 'Linda', 'Mom', 'https://images.example.com/customers/linda.jpg', 'customer', 'active', '2026-01-14 12:00:00+00', '2026-01-14 12:05:00+00', '2026-01-14 12:00:00+00', NULL, '2026-01-14 12:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0002-000000000001', 'merchant.apple@cust.test', '+85599000011', 'argon2id$seller$hash1', 'Steve', 'Seller', 'https://images.example.com/merchants/apple.png', 'seller', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0002-000000000002', 'merchant.nike@cust.test', '+85599000012', 'argon2id$seller$hash2', 'Phil', 'Seller', 'https://images.example.com/merchants/nike.png', 'seller', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0002-000000000003', 'merchant.sony@cust.test', '+85599000013', 'argon2id$seller$hash3', 'Akio', 'Seller', 'https://images.example.com/merchants/sony.png', 'seller', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0002-000000000004', 'merchant.zara@cust.test', '+85599000014', 'argon2id$seller$hash4', 'Amancio', 'Seller', 'https://images.example.com/merchants/zara.png', 'seller', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0002-000000000005', 'merchant.anker@cust.test', '+85599000015', 'argon2id$seller$hash5', 'Steven', 'Seller', 'https://images.example.com/merchants/anker.png', 'seller', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0003-000000000001', 'support.desk@cust.test', '+85599000021', 'argon2id$staff$hash1', 'Sophea', 'Support', 'https://images.example.com/staff/support.png', 'support', 'active', '2026-01-01 00:00:00+00', '2026-01-01 00:05:00+00', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_profiles (Customer Personal Profiles)
-- ============================================================

INSERT INTO public."user_profiles" ("id", "user_id", "date_of_birth", "gender", "preferred_language", "marketing_opt_in", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0004-000000000001', 'c0000000-0000-0000-0001-000000000001', '1994-04-18', 'male', 'en', TRUE, '2026-01-10 08:00:00+00', NULL, '2026-01-10 08:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0004-000000000002', 'c0000000-0000-0000-0001-000000000002', '1996-08-25', 'female', 'km', TRUE, '2026-01-11 09:00:00+00', NULL, '2026-01-11 09:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0004-000000000003', 'c0000000-0000-0000-0001-000000000003', '1998-11-03', 'female', 'en', FALSE, '2026-01-12 10:00:00+00', NULL, '2026-01-12 10:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0004-000000000004', 'c0000000-0000-0000-0001-000000000004', '1991-01-15', 'male', 'km', TRUE, '2026-01-13 11:00:00+00', NULL, '2026-01-13 11:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0004-000000000005', 'c0000000-0000-0000-0001-000000000005', '2000-06-30', 'female', 'en', TRUE, '2026-01-14 12:00:00+00', NULL, '2026-01-14 12:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_addresses (Customer Shipping & Billing Addresses)
-- ============================================================

INSERT INTO public."user_addresses" ("id", "user_id", "label", "recipient_name", "phone_number", "address_line_1", "address_line_2", "city", "state", "postal_code", "country_code", "latitude", "longitude", "is_default", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0005-000000000001', 'c0000000-0000-0000-0001-000000000001', 'Home', 'Dara Rath', '+85599000001', 'Borey Peng Huoth #88, St Polar', 'Sangkat Nirouth, Khan Chbar Ampov', 'Phnom Penh', 'Phnom Penh', '121201', 'KH', 11.5312, 104.9543, TRUE, '2026-01-10 08:30:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-01-10 08:30:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0005-000000000002', 'c0000000-0000-0000-0001-000000000002', 'Condo', 'Chenda Sam', '+85599000002', 'The Bridge Condo, Floor 24, Unit 2410', 'Tonle Bassac, Khan Chamkarmon', 'Phnom Penh', 'Phnom Penh', '12301', 'KH', 11.5492, 104.9331, TRUE, '2026-01-11 09:30:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-01-11 09:30:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0005-000000000003', 'c0000000-0000-0000-0001-000000000003', 'Office', 'Sreyneang Heng', '+85599000003', 'Vattanac Capital Tower, Floor 18', 'Preah Monivong Blvd, Sangkat Wat Phnom', 'Phnom Penh', 'Phnom Penh', '120211', 'KH', 11.5724, 104.9208, TRUE, '2026-01-12 10:30:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-01-12 10:30:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0005-000000000004', 'c0000000-0000-0000-0001-000000000004', 'Residence', 'Vutha Sok', '+85599000004', 'Villa 42, St 598', 'Toul Kork, Khan Toul Kork', 'Phnom Penh', 'Phnom Penh', '121502', 'KH', 11.5856, 104.8962, TRUE, '2026-01-13 11:30:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-01-13 11:30:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0005-000000000005', 'c0000000-0000-0000-0001-000000000005', 'Apartment', 'Linda Mom', '+85599000005', 'St 310, No 25B', 'BKK2, Khan Chamkarmon', 'Phnom Penh', 'Phnom Penh', '12303', 'KH', 11.5471, 104.9192, TRUE, '2026-01-14 12:30:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-01-14 12:30:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_security_settings (Customer 2FA and Biometrics)
-- ============================================================

INSERT INTO public."user_security_settings" ("id", "user_id", "two_factor_enabled", "biometric_enabled", "last_password_changed_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0006-000000000001', 'c0000000-0000-0000-0001-000000000001', TRUE, TRUE, '2026-01-10 08:00:00+00', '2026-01-10 08:00:00+00', NULL, '2026-01-10 08:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0006-000000000002', 'c0000000-0000-0000-0001-000000000002', TRUE, TRUE, '2026-01-11 09:00:00+00', '2026-01-11 09:00:00+00', NULL, '2026-01-11 09:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0006-000000000003', 'c0000000-0000-0000-0001-000000000003', FALSE, TRUE, '2026-01-12 10:00:00+00', '2026-01-12 10:00:00+00', NULL, '2026-01-12 10:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0006-000000000004', 'c0000000-0000-0000-0001-000000000004', FALSE, FALSE, '2026-01-13 11:00:00+00', '2026-01-13 11:00:00+00', NULL, '2026-01-13 11:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0006-000000000005', 'c0000000-0000-0000-0001-000000000005', TRUE, FALSE, '2026-01-14 12:00:00+00', '2026-01-14 12:00:00+00', NULL, '2026-01-14 12:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.user_sessions (Customer Logged-In Sessions)
-- ============================================================

INSERT INTO public."user_sessions" ("id", "user_id", "device_name", "ip_address", "user_agent", "last_seen_at", "revoked_at", "created_at") VALUES
    ('c0000000-0000-0000-0007-000000000001', 'c0000000-0000-0000-0001-000000000001', 'iPhone 15 Pro', '103.14.200.12', 'EcomApp/3.0.1 (iOS 17.5; Build 2201)', '2026-03-15 14:00:00+00', NULL, '2026-03-01 08:00:00+00'),
    ('c0000000-0000-0000-0007-000000000002', 'c0000000-0000-0000-0001-000000000002', 'Samsung Galaxy Z Fold 5', '103.14.200.15', 'EcomApp/3.0.1 (Android 14; OneUI 6.1)', '2026-03-15 15:30:00+00', NULL, '2026-03-02 09:00:00+00'),
    ('c0000000-0000-0000-0007-000000000003', 'c0000000-0000-0000-0001-000000000003', 'MacBook Air M3', '103.14.200.22', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) Safari/605.1.15', '2026-03-15 16:20:00+00', NULL, '2026-03-03 10:00:00+00'),
    ('c0000000-0000-0000-0007-000000000004', 'c0000000-0000-0000-0001-000000000004', 'Xiaomi 14 Ultra', '103.14.200.31', 'EcomApp/3.0.1 (Android 14; HyperOS)', '2026-03-15 17:10:00+00', NULL, '2026-03-04 11:00:00+00'),
    ('c0000000-0000-0000-0007-000000000005', 'c0000000-0000-0000-0001-000000000005', 'iPad Pro 11 M4', '103.14.200.45', 'Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X)', '2026-03-15 18:45:00+00', NULL, '2026-03-05 12:00:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.categories (Product Categories)
-- ============================================================

INSERT INTO public."categories" ("id", "parent_id", "name", "slug", "icon_url", "image_url", "sort_order", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0008-000000000001', NULL, 'Smart Devices', 'cust-smart-devices', 'https://img.test/cat/devices.svg', 'https://img.test/cat/devices.jpg', 1, 'active', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0008-000000000002', 'c0000000-0000-0000-0008-000000000001', 'Smartphones', 'cust-smartphones', 'https://img.test/cat/smartphones.svg', 'https://img.test/cat/smartphones.jpg', 2, 'active', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0008-000000000003', 'c0000000-0000-0000-0008-000000000001', 'Wearables', 'cust-wearables', 'https://img.test/cat/wearables.svg', 'https://img.test/cat/wearables.jpg', 3, 'active', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0008-000000000004', NULL, 'Sportswear', 'cust-sportswear', 'https://img.test/cat/sportswear.svg', 'https://img.test/cat/sportswear.jpg', 4, 'active', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0008-000000000005', 'c0000000-0000-0000-0008-000000000004', 'Running Shoes', 'cust-running-shoes', 'https://img.test/cat/shoes.svg', 'https://img.test/cat/shoes.jpg', 5, 'active', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.stores (Stores Where Customers Shop)
-- ============================================================

INSERT INTO public."stores" ("id", "owner_id", "name", "slug", "description", "logo_url", "banner_url", "status", "rating_average", "rating_count", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0009-000000000001', 'c0000000-0000-0000-0002-000000000001', 'iStore Authorized', 'cust-istore-authorized', 'Authorized Apple flagship retailer', 'https://img.test/stores/apple.png', 'https://img.test/stores/apple_bg.jpg', 'active', 4.95, 310, '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0009-000000000002', 'c0000000-0000-0000-0002-000000000002', 'Nike Performance Store', 'cust-nike-performance', 'Official athletics apparel and footwear', 'https://img.test/stores/nike.png', 'https://img.test/stores/nike_bg.jpg', 'active', 4.88, 240, '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0009-000000000003', 'c0000000-0000-0000-0002-000000000003', 'Sony Audio Experience', 'cust-sony-audio', 'Premium noise cancellation headphones and soundbars', 'https://img.test/stores/sony.png', 'https://img.test/stores/sony_bg.jpg', 'active', 4.91, 180, '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0009-000000000004', 'c0000000-0000-0000-0002-000000000004', 'Zara Modern Chic', 'cust-zara-chic', 'Contemporary trending outfits and streetwear', 'https://img.test/stores/zara.png', 'https://img.test/stores/zara_bg.jpg', 'active', 4.76, 150, '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0009-000000000005', 'c0000000-0000-0000-0002-000000000005', 'Anker Power Station', 'cust-anker-power', 'Leading fast charging tech and portable powerbanks', 'https://img.test/stores/anker.png', 'https://img.test/stores/anker_bg.jpg', 'active', 4.89, 420, '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.tags (Catalog Tags)
-- ============================================================

INSERT INTO public."tags" ("id", "name", "slug") VALUES
    ('c0000000-0000-0000-0010-000000000001', 'Top Rated', 'cust-top-rated'),
    ('c0000000-0000-0000-0010-000000000002', 'Customer Choice', 'cust-choice'),
    ('c0000000-0000-0000-0010-000000000003', 'Express Delivery', 'cust-express-delivery'),
    ('c0000000-0000-0000-0010-000000000004', 'Free Warranty', 'cust-free-warranty'),
    ('c0000000-0000-0000-0010-000000000005', 'Eco Friendly', 'cust-eco-friendly')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.products (Products Available to Customers)
-- ============================================================

INSERT INTO public."products" ("id", "store_id", "category_id", "name", "slug", "description", "base_price", "compare_at_price", "currency", "sku", "status", "rating_average", "rating_count", "sold_count", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0011-000000000001', 'c0000000-0000-0000-0009-000000000001', 'c0000000-0000-0000-0008-000000000002', 'iPhone 16 Pro 256GB Black Titanium', 'iphone-16-pro-256', 'Latest flagship smartphone with A18 Pro chip', 1099.0, 1199.0, 'USD', 'SKU-IP16P-256', 'active', 4.92, 110, 350, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0011-000000000002', 'c0000000-0000-0000-0009-000000000002', 'c0000000-0000-0000-0008-000000000005', 'Nike Air Zoom Pegasus 41 Running Shoe', 'nike-air-zoom-pegasus-41', 'Responsive daily road running shoes with ReactX foam', 130.0, 150.0, 'USD', 'SKU-PEG41-BLK', 'active', 4.85, 95, 210, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0011-000000000003', 'c0000000-0000-0000-0009-000000000003', 'c0000000-0000-0000-0008-000000000003', 'Sony WH-1000XM5 Noise Canceling Headphones', 'sony-wh-1000xm5-silver', 'Industry-leading wireless active noise cancelling headphones', 399.99, 449.99, 'USD', 'SKU-WH1000XM5-SLV', 'active', 4.94, 280, 520, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0011-000000000004', 'c0000000-0000-0000-0009-000000000004', 'c0000000-0000-0000-0008-000000000004', 'Zara Textured Knit Crewneck Sweater', 'zara-textured-knit-sweater', 'Soft touch lightweight crewneck sweater in relaxed fit', 59.9, 79.9, 'USD', 'SKU-ZARA-KNIT-M', 'active', 4.7, 45, 130, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0011-000000000005', 'c0000000-0000-0000-0009-000000000005', 'c0000000-0000-0000-0008-000000000001', 'Anker Prime 20,000mAh Power Bank (200W)', 'anker-prime-20000-200w', 'Multi-device ultra fast charging power bank with smart display', 129.99, 149.99, 'USD', 'SKU-ANK-P200W', 'active', 4.88, 160, 480, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_variants (Customer Product Variants)
-- ============================================================

INSERT INTO public."product_variants" ("id", "product_id", "sku", "name", "price", "stock_quantity", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0012-000000000001', 'c0000000-0000-0000-0011-000000000001', 'SKU-IP16P-256-BLK-TI', 'Black Titanium / 256GB', 1099.0, 75, 'active', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0012-000000000002', 'c0000000-0000-0000-0011-000000000002', 'SKU-PEG41-US10', 'Black/White / US 10', 130.0, 50, 'active', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0012-000000000003', 'c0000000-0000-0000-0011-000000000003', 'SKU-WH1000XM5-SLV-STD', 'Platinum Silver', 399.99, 60, 'active', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0012-000000000004', 'c0000000-0000-0000-0011-000000000004', 'SKU-ZARA-KNIT-BEG-M', 'Oatmeal Beige / Size M', 59.9, 45, 'active', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0012-000000000005', 'c0000000-0000-0000-0011-000000000005', 'SKU-ANK-P200W-BLK', 'Matte Carbon', 129.99, 120, 'active', '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_images (Product Image Catalog)
-- ============================================================

INSERT INTO public."product_images" ("id", "product_id", "image_url", "alt_text", "sort_order", "is_primary", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0013-000000000001', 'c0000000-0000-0000-0011-000000000001', 'https://img.test/products/ip16p_main.jpg', 'iPhone 16 Pro Main Angle', 1, TRUE, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0013-000000000002', 'c0000000-0000-0000-0011-000000000002', 'https://img.test/products/peg41_main.jpg', 'Nike Pegasus 41 Running Shoe', 1, TRUE, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0013-000000000003', 'c0000000-0000-0000-0011-000000000003', 'https://img.test/products/xm5_main.jpg', 'Sony WH-1000XM5 Silver', 1, TRUE, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0013-000000000004', 'c0000000-0000-0000-0011-000000000004', 'https://img.test/products/zara_knit.jpg', 'Zara Knit Crewneck Front', 1, TRUE, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0013-000000000005', 'c0000000-0000-0000-0011-000000000005', 'https://img.test/products/anker200w.jpg', 'Anker Power Bank Display', 1, TRUE, '2026-01-05 00:00:00+00', NULL, '2026-01-05 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_tags (Product Tags Mapping)
-- ============================================================

INSERT INTO public."product_tags" ("id", "product_id", "tag_id") VALUES
    ('c0000000-0000-0000-0014-000000000001', 'c0000000-0000-0000-0011-000000000001', 'c0000000-0000-0000-0010-000000000001'),
    ('c0000000-0000-0000-0014-000000000002', 'c0000000-0000-0000-0011-000000000002', 'c0000000-0000-0000-0010-000000000002'),
    ('c0000000-0000-0000-0014-000000000003', 'c0000000-0000-0000-0011-000000000003', 'c0000000-0000-0000-0010-000000000003'),
    ('c0000000-0000-0000-0014-000000000004', 'c0000000-0000-0000-0011-000000000004', 'c0000000-0000-0000-0010-000000000004'),
    ('c0000000-0000-0000-0014-000000000005', 'c0000000-0000-0000-0011-000000000005', 'c0000000-0000-0000-0010-000000000005')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.variant_options (Variant Options Specification)
-- ============================================================

INSERT INTO public."variant_options" ("id", "product_variant_id", "name", "value") VALUES
    ('c0000000-0000-0000-0015-000000000001', 'c0000000-0000-0000-0012-000000000001', 'Finish', 'Black Titanium'),
    ('c0000000-0000-0000-0015-000000000002', 'c0000000-0000-0000-0012-000000000002', 'Shoe Size', 'US 10'),
    ('c0000000-0000-0000-0015-000000000003', 'c0000000-0000-0000-0012-000000000003', 'Color', 'Platinum Silver'),
    ('c0000000-0000-0000-0015-000000000004', 'c0000000-0000-0000-0012-000000000004', 'Size', 'M'),
    ('c0000000-0000-0000-0015-000000000005', 'c0000000-0000-0000-0012-000000000005', 'Color', 'Matte Carbon')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.legal_documents (Legal Agreements for Customers)
-- ============================================================

INSERT INTO public."legal_documents" ("id", "type", "title", "version", "content", "published_at", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0016-000000000001', 'terms', 'Customer Purchase Terms', 'v2.1', 'Binding agreement for online consumer purchases, checkout warranties, and dispute settlement.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0016-000000000002', 'privacy', 'Customer Data Protection Notice', 'v2.1', 'Information on how customer personal info, delivery coordinates, and payment tokens are processed.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0016-000000000003', 'refund_policy', 'Customer Returns and Chargeback Policy', 'v2.1', 'Rules governing 30-day money-back guarantee, defect claims, and courier pickup.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0016-000000000004', 'shipping_policy', 'Customer Delivery Policy', 'v2.1', 'Standard delivery commitments, doorstep signature requirements, and loss protection.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL),
    ('c0000000-0000-0000-0016-000000000005', 'terms', 'Mobile Loyalty & Rewards Terms', 'v1.0', 'Terms and conditions regarding reward cashback points, vouchers, and membership tiers.', '2026-01-01 00:00:00+00', 'published', '2026-01-01 00:00:00+00', NULL, '2026-01-01 00:00:00+00', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.carts (Shopping Carts for Customers)
-- ============================================================

INSERT INTO public."carts" ("id", "user_id", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0017-000000000001', 'c0000000-0000-0000-0001-000000000001', 'active', '2026-03-01 10:00:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-01 10:00:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0017-000000000002', 'c0000000-0000-0000-0001-000000000002', 'active', '2026-03-02 11:15:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-02 11:15:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0017-000000000003', 'c0000000-0000-0000-0001-000000000003', 'checked_out', '2026-03-03 14:00:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-03 14:30:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0017-000000000004', 'c0000000-0000-0000-0001-000000000004', 'checked_out', '2026-03-04 15:40:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-04 16:00:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0017-000000000005', 'c0000000-0000-0000-0001-000000000005', 'active', '2026-03-05 18:20:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 18:20:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.cart_items (Items Added to Customer Carts)
-- ============================================================

INSERT INTO public."cart_items" ("id", "cart_id", "product_id", "product_variant_id", "quantity", "unit_price_snapshot", "is_selected", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0018-000000000001', 'c0000000-0000-0000-0017-000000000001', 'c0000000-0000-0000-0011-000000000001', 'c0000000-0000-0000-0012-000000000001', 1, 1099.0, TRUE, '2026-03-01 10:05:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-01 10:05:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0018-000000000002', 'c0000000-0000-0000-0017-000000000002', 'c0000000-0000-0000-0011-000000000002', 'c0000000-0000-0000-0012-000000000002', 1, 130.0, TRUE, '2026-03-02 11:20:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-02 11:20:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0018-000000000003', 'c0000000-0000-0000-0017-000000000003', 'c0000000-0000-0000-0011-000000000003', 'c0000000-0000-0000-0012-000000000003', 1, 399.99, TRUE, '2026-03-03 14:05:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-03 14:05:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0018-000000000004', 'c0000000-0000-0000-0017-000000000004', 'c0000000-0000-0000-0011-000000000004', 'c0000000-0000-0000-0012-000000000004', 2, 59.9, TRUE, '2026-03-04 15:45:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-04 15:45:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0018-000000000005', 'c0000000-0000-0000-0017-000000000005', 'c0000000-0000-0000-0011-000000000005', 'c0000000-0000-0000-0012-000000000005', 1, 129.99, TRUE, '2026-03-05 18:25:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 18:25:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.orders (Customer Placed Orders)
-- ============================================================

INSERT INTO public."orders" ("id", "order_number", "user_id", "store_id", "shipping_address_id", "status", "subtotal_amount", "shipping_amount", "discount_amount", "tax_amount", "total_amount", "currency", "placed_at", "cancelled_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0019-000000000001', 'CUST-ORD-2026-0001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0009-000000000001', 'c0000000-0000-0000-0005-000000000001', 'delivered', 1099.0, 0.0, 50.0, 0.0, 1049.0, 'USD', '2026-03-01 10:30:00+00', NULL, '2026-03-01 10:30:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-03 14:00:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0019-000000000002', 'CUST-ORD-2026-0002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0009-000000000002', 'c0000000-0000-0000-0005-000000000002', 'delivered', 130.0, 5.0, 0.0, 0.0, 135.0, 'USD', '2026-03-02 12:00:00+00', NULL, '2026-03-02 12:00:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-04 16:30:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0019-000000000003', 'CUST-ORD-2026-0003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0009-000000000003', 'c0000000-0000-0000-0005-000000000003', 'shipped', 399.99, 0.0, 20.0, 0.0, 379.99, 'USD', '2026-03-03 14:30:00+00', NULL, '2026-03-03 14:30:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-04 09:00:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0019-000000000004', 'CUST-ORD-2026-0004', 'c0000000-0000-0000-0001-000000000004', 'c0000000-0000-0000-0009-000000000004', 'c0000000-0000-0000-0005-000000000004', 'processing', 119.8, 4.0, 0.0, 0.0, 123.8, 'USD', '2026-03-04 16:00:00+00', NULL, '2026-03-04 16:00:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-05 08:30:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0019-000000000005', 'CUST-ORD-2026-0005', 'c0000000-0000-0000-0001-000000000005', 'c0000000-0000-0000-0009-000000000005', 'c0000000-0000-0000-0005-000000000005', 'paid', 129.99, 3.5, 10.0, 0.0, 123.49, 'USD', '2026-03-05 18:30:00+00', NULL, '2026-03-05 18:30:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 18:35:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.order_items (Items Purchased by Customers)
-- ============================================================

INSERT INTO public."order_items" ("id", "order_id", "product_id", "product_variant_id", "product_name_snapshot", "variant_name_snapshot", "sku_snapshot", "unit_price", "quantity", "line_total", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0020-000000000001', 'c0000000-0000-0000-0019-000000000001', 'c0000000-0000-0000-0011-000000000001', 'c0000000-0000-0000-0012-000000000001', 'iPhone 16 Pro 256GB Black Titanium', 'Black Titanium / 256GB', 'SKU-IP16P-256-BLK-TI', 1099.0, 1, 1099.0, '2026-03-01 10:30:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-01 10:30:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0020-000000000002', 'c0000000-0000-0000-0019-000000000002', 'c0000000-0000-0000-0011-000000000002', 'c0000000-0000-0000-0012-000000000002', 'Nike Air Zoom Pegasus 41 Running Shoe', 'Black/White / US 10', 'SKU-PEG41-US10', 130.0, 1, 130.0, '2026-03-02 12:00:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-02 12:00:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0020-000000000003', 'c0000000-0000-0000-0019-000000000003', 'c0000000-0000-0000-0011-000000000003', 'c0000000-0000-0000-0012-000000000003', 'Sony WH-1000XM5 Noise Canceling Headphones', 'Platinum Silver', 'SKU-WH1000XM5-SLV-STD', 399.99, 1, 399.99, '2026-03-03 14:30:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-03 14:30:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0020-000000000004', 'c0000000-0000-0000-0019-000000000004', 'c0000000-0000-0000-0011-000000000004', 'c0000000-0000-0000-0012-000000000004', 'Zara Textured Knit Crewneck Sweater', 'Oatmeal Beige / Size M', 'SKU-ZARA-KNIT-BEG-M', 59.9, 2, 119.8, '2026-03-04 16:00:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-04 16:00:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0020-000000000005', 'c0000000-0000-0000-0019-000000000005', 'c0000000-0000-0000-0011-000000000005', 'c0000000-0000-0000-0012-000000000005', 'Anker Prime 20,000mAh Power Bank (200W)', 'Matte Carbon', 'SKU-ANK-P200W-BLK', 129.99, 1, 129.99, '2026-03-05 18:30:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 18:30:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.order_status_history (Customer Order Status Timeline)
-- ============================================================

INSERT INTO public."order_status_history" ("id", "order_id", "from_status", "to_status", "changed_by_id", "note", "created_at") VALUES
    ('c0000000-0000-0000-0021-000000000001', 'c0000000-0000-0000-0019-000000000001', 'pending', 'confirmed', 'c0000000-0000-0000-0001-000000000001', 'Customer placed order with ABA PayWay', '2026-03-01 10:32:00+00'),
    ('c0000000-0000-0000-0021-000000000002', 'c0000000-0000-0000-0019-000000000001', 'confirmed', 'shipped', 'c0000000-0000-0000-0002-000000000001', 'Order packed and assigned to courier', '2026-03-02 08:30:00+00'),
    ('c0000000-0000-0000-0021-000000000003', 'c0000000-0000-0000-0019-000000000001', 'shipped', 'delivered', 'c0000000-0000-0000-0002-000000000001', 'Successfully delivered to customer Dara Rath', '2026-03-03 14:00:00+00'),
    ('c0000000-0000-0000-0021-000000000004', 'c0000000-0000-0000-0019-000000000002', 'pending', 'paid', 'c0000000-0000-0000-0001-000000000002', 'Customer paid via Visa Card', '2026-03-02 12:02:00+00'),
    ('c0000000-0000-0000-0021-000000000005', 'c0000000-0000-0000-0019-000000000003', 'pending', 'shipped', 'c0000000-0000-0000-0002-000000000003', 'Shipped via express delivery', '2026-03-04 09:00:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.shipments (Shipments Dispatched to Customers)
-- ============================================================

INSERT INTO public."shipments" ("id", "order_id", "carrier_name", "tracking_number", "status", "shipped_at", "delivered_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0022-000000000001', 'c0000000-0000-0000-0019-000000000001', 'Kerry Express', 'CUST-TRK-9001', 'delivered', '2026-03-02 08:30:00+00', '2026-03-03 14:00:00+00', '2026-03-01 16:00:00+00', 'c0000000-0000-0000-0002-000000000001', '2026-03-03 14:00:00+00', 'c0000000-0000-0000-0002-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0022-000000000002', 'c0000000-0000-0000-0019-000000000002', 'J&T Express', 'CUST-TRK-9002', 'delivered', '2026-03-03 09:00:00+00', '2026-03-04 16:30:00+00', '2026-03-02 14:00:00+00', 'c0000000-0000-0000-0002-000000000002', '2026-03-04 16:30:00+00', 'c0000000-0000-0000-0002-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0022-000000000003', 'c0000000-0000-0000-0019-000000000003', 'DHL Express', 'CUST-TRK-9003', 'in_transit', '2026-03-04 09:00:00+00', NULL, '2026-03-03 16:00:00+00', 'c0000000-0000-0000-0002-000000000003', '2026-03-04 09:00:00+00', 'c0000000-0000-0000-0002-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0022-000000000004', 'c0000000-0000-0000-0019-000000000004', 'Flash Express', 'CUST-TRK-9004', 'packed', NULL, NULL, '2026-03-05 09:00:00+00', 'c0000000-0000-0000-0002-000000000004', '2026-03-05 09:00:00+00', 'c0000000-0000-0000-0002-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0022-000000000005', 'c0000000-0000-0000-0019-000000000005', 'Ninja Van', 'CUST-TRK-9005', 'pending', NULL, NULL, '2026-03-05 19:00:00+00', 'c0000000-0000-0000-0002-000000000005', '2026-03-05 19:00:00+00', 'c0000000-0000-0000-0002-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.shipment_events (Customer Tracking Checkpoint Events)
-- ============================================================

INSERT INTO public."shipment_events" ("id", "shipment_id", "status", "location", "description", "event_time", "created_at") VALUES
    ('c0000000-0000-0000-0023-000000000001', 'c0000000-0000-0000-0022-000000000001', 'packed', 'Merchant Warehouse', 'Electronic items securely bubbled and packaged', '2026-03-01 17:00:00+00', '2026-03-01 17:00:00+00'),
    ('c0000000-0000-0000-0023-000000000002', 'c0000000-0000-0000-0022-000000000001', 'in_transit', 'Kerry Gateway Hub', 'Scanned at transit dispatch facility', '2026-03-02 09:00:00+00', '2026-03-02 09:00:00+00'),
    ('c0000000-0000-0000-0023-000000000003', 'c0000000-0000-0000-0022-000000000001', 'out_for_delivery', 'Chbar Ampov Local Hub', 'Courier on route to deliver package', '2026-03-03 09:30:00+00', '2026-03-03 09:30:00+00'),
    ('c0000000-0000-0000-0023-000000000004', 'c0000000-0000-0000-0022-000000000001', 'delivered', 'Customer Doorstep', 'Package delivered and OTP verified', '2026-03-03 14:00:00+00', '2026-03-03 14:00:00+00'),
    ('c0000000-0000-0000-0023-000000000005', 'c0000000-0000-0000-0022-000000000003', 'in_transit', 'DHL Air Freight Center', 'Customs clearance completed and departed hub', '2026-03-04 11:30:00+00', '2026-03-04 11:30:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.favorites (Customer Saved Wishlists / Favorites)
-- ============================================================

INSERT INTO public."favorites" ("id", "user_id", "product_id", "created_at", "deleted_at") VALUES
    ('c0000000-0000-0000-0024-000000000001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0011-000000000003', '2026-02-01 10:00:00+00', NULL),
    ('c0000000-0000-0000-0024-000000000002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0011-000000000001', '2026-02-02 11:00:00+00', NULL),
    ('c0000000-0000-0000-0024-000000000003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0011-000000000002', '2026-02-03 12:00:00+00', NULL),
    ('c0000000-0000-0000-0024-000000000004', 'c0000000-0000-0000-0001-000000000004', 'c0000000-0000-0000-0011-000000000005', '2026-02-04 13:00:00+00', NULL),
    ('c0000000-0000-0000-0024-000000000005', 'c0000000-0000-0000-0001-000000000005', 'c0000000-0000-0000-0011-000000000004', '2026-02-05 14:00:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.search_history (Customer Search Activity)
-- ============================================================

INSERT INTO public."search_history" ("id", "user_id", "query", "filters_json", "result_count", "created_at") VALUES
    ('c0000000-0000-0000-0025-000000000001', 'c0000000-0000-0000-0001-000000000001', 'apple iphone 16 titanium', '{"brand": "Apple", "min_ram": "8GB"}', 18, '2026-03-01 09:00:00+00'),
    ('c0000000-0000-0000-0025-000000000002', 'c0000000-0000-0000-0001-000000000002', 'pegasus 41 marathon size 10', '{"brand": "Nike", "category": "cust-running-shoes"}', 9, '2026-03-02 10:15:00+00'),
    ('c0000000-0000-0000-0025-000000000003', 'c0000000-0000-0000-0001-000000000003', 'sony over ear wireless anc', '{"max_price": 450, "anc": true}', 14, '2026-03-03 11:20:00+00'),
    ('c0000000-0000-0000-0025-000000000004', 'c0000000-0000-0000-0001-000000000004', 'zara knitted warm sweater', '{"gender": "unisex", "size": "M"}', 22, '2026-03-04 12:45:00+00'),
    ('c0000000-0000-0000-0025-000000000005', 'c0000000-0000-0000-0001-000000000005', 'anker 200w high wattage portable battery', '{"capacity": "20000mah"}', 7, '2026-03-05 14:00:00+00')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.conversations (Customer Direct Chat with Stores)
-- ============================================================

INSERT INTO public."conversations" ("id", "customer_id", "store_id", "order_id", "status", "last_message_at", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0026-000000000001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0009-000000000001', 'c0000000-0000-0000-0019-000000000001', 'closed', '2026-03-03 14:30:00+00', '2026-03-01 10:45:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-03 14:30:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0026-000000000002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0009-000000000002', 'c0000000-0000-0000-0019-000000000002', 'open', '2026-03-04 17:00:00+00', '2026-03-02 12:15:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-04 17:00:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0026-000000000003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0009-000000000003', 'c0000000-0000-0000-0019-000000000003', 'open', '2026-03-04 10:00:00+00', '2026-03-03 15:00:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-04 10:00:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0026-000000000004', 'c0000000-0000-0000-0001-000000000004', 'c0000000-0000-0000-0009-000000000004', 'c0000000-0000-0000-0019-000000000004', 'open', '2026-03-05 09:15:00+00', '2026-03-04 16:30:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-05 09:15:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0026-000000000005', 'c0000000-0000-0000-0001-000000000005', 'c0000000-0000-0000-0009-000000000005', 'c0000000-0000-0000-0019-000000000005', 'open', '2026-03-05 19:00:00+00', '2026-03-05 18:40:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 19:00:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.messages (Chat Messages Exchanged with Customers)
-- ============================================================

INSERT INTO public."messages" ("id", "conversation_id", "sender_id", "message_type", "body", "attachment_url", "read_at", "created_at", "deleted_at") VALUES
    ('c0000000-0000-0000-0027-000000000001', 'c0000000-0000-0000-0026-000000000001', 'c0000000-0000-0000-0001-000000000001', 'text', 'Hi! Could you please ensure the iPhone comes with the genuine Apple 1-year warranty sticker on the box?', NULL, '2026-03-01 10:50:00+00', '2026-03-01 10:45:00+00', NULL),
    ('c0000000-0000-0000-0027-000000000002', 'c0000000-0000-0000-0026-000000000001', 'c0000000-0000-0000-0002-000000000001', 'text', 'Absolutely Dara! All our units are 100% factory sealed with official distributor warranty cards.', NULL, '2026-03-01 11:00:00+00', '2026-03-01 10:55:00+00', NULL),
    ('c0000000-0000-0000-0027-000000000003', 'c0000000-0000-0000-0026-000000000002', 'c0000000-0000-0000-0001-000000000002', 'text', 'Hello Nike store, will US 10 fit true to size for daily 5k jogs?', NULL, '2026-03-02 12:30:00+00', '2026-03-02 12:15:00+00', NULL),
    ('c0000000-0000-0000-0027-000000000004', 'c0000000-0000-0000-0026-000000000003', 'c0000000-0000-0000-0001-000000000003', 'text', 'Does this Sony headset include the airplane dual adapter in the carrying case?', NULL, '2026-03-03 15:10:00+00', '2026-03-03 15:00:00+00', NULL),
    ('c0000000-0000-0000-0027-000000000005', 'c0000000-0000-0000-0026-000000000004', 'c0000000-0000-0000-0001-000000000004', 'text', 'Can I request gift wrapping for the Zara sweater?', NULL, NULL, '2026-03-04 16:30:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.notifications (In-App Push Notifications for Customers)
-- ============================================================

INSERT INTO public."notifications" ("id", "user_id", "type", "title", "body", "data", "read_at", "status", "created_at", "deleted_at") VALUES
    ('c0000000-0000-0000-0028-000000000001', 'c0000000-0000-0000-0001-000000000001', 'order', 'Order Delivered Successfully', 'Your order #CUST-ORD-2026-0001 has been delivered to your home.', '{"order_id": "c0000000-0000-0000-0019-000000000001"}', '2026-03-03 14:05:00+00', 'sent', '2026-03-03 14:00:00+00', NULL),
    ('c0000000-0000-0000-0028-000000000002', 'c0000000-0000-0000-0001-000000000002', 'order', 'Package In Transit', 'Nike Pegasus 41 is now out for delivery with J&T Express.', '{"tracking_code": "CUST-TRK-9002"}', '2026-03-04 09:30:00+00', 'sent', '2026-03-04 09:00:00+00', NULL),
    ('c0000000-0000-0000-0028-000000000003', 'c0000000-0000-0000-0001-000000000003', 'promotion', 'Flash Sale: 15% Off All Electronics', 'Special customer appreciation voucher code TECH15 valid until midnight.', '{"promo_code": "TECH15"}', NULL, 'sent', '2026-03-05 08:00:00+00', NULL),
    ('c0000000-0000-0000-0028-000000000004', 'c0000000-0000-0000-0001-000000000004', 'order', 'Order Processing Started', 'Zara store is preparing your order #CUST-ORD-2026-0004.', '{"order_id": "c0000000-0000-0000-0019-000000000004"}', '2026-03-05 08:35:00+00', 'sent', '2026-03-05 08:30:00+00', NULL),
    ('c0000000-0000-0000-0028-000000000005', 'c0000000-0000-0000-0001-000000000005', 'security', 'Security Checkup Complete', 'Two-factor authentication is active on your customer account.', '{"type": "security_status"}', '2026-03-05 19:00:00+00', 'sent', '2026-03-05 18:30:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.support_tickets (Customer Support Help Desk Tickets)
-- ============================================================

INSERT INTO public."support_tickets" ("id", "user_id", "order_id", "subject", "category", "status", "priority", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0029-000000000001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0019-000000000001', 'Electronic VAT Tax Receipt Request', 'order', 'resolved', 'normal', '2026-03-03 15:00:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-03 16:30:00+00', 'c0000000-0000-0000-0003-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0029-000000000002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0019-000000000002', 'Shoe Size Fit Inquiry and Exchange Window', 'delivery', 'resolved', 'low', '2026-03-04 17:00:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-04 18:00:00+00', 'c0000000-0000-0000-0003-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0029-000000000003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0019-000000000003', 'Expedited International Courier Tracking Help', 'delivery', 'open', 'high', '2026-03-04 10:00:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-04 10:00:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0029-000000000004', 'c0000000-0000-0000-0001-000000000004', NULL, 'How to link Bakong KHQR for one-tap checkout', 'payment', 'resolved', 'normal', '2026-03-05 10:00:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-05 11:20:00+00', 'c0000000-0000-0000-0003-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0029-000000000005', 'c0000000-0000-0000-0001-000000000005', NULL, 'Voucher code applied twice inquiry', 'payment', 'open', 'normal', '2026-03-05 19:15:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 19:15:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.support_ticket_messages (Customer Support Messages)
-- ============================================================

INSERT INTO public."support_ticket_messages" ("id", "ticket_id", "sender_id", "body", "attachment_url", "created_at", "deleted_at") VALUES
    ('c0000000-0000-0000-0030-000000000001', 'c0000000-0000-0000-0029-000000000001', 'c0000000-0000-0000-0001-000000000001', 'Hello, please send the official invoice with company name for tax declaration.', NULL, '2026-03-03 15:00:00+00', NULL),
    ('c0000000-0000-0000-0030-000000000002', 'c0000000-0000-0000-0029-000000000001', 'c0000000-0000-0000-0003-000000000001', 'Attached is your digital tax invoice with company stamp.', 'https://invoices.test/inv-cust-001.pdf', '2026-03-03 16:30:00+00', NULL),
    ('c0000000-0000-0000-0030-000000000003', 'c0000000-0000-0000-0029-000000000002', 'c0000000-0000-0000-0001-000000000002', 'The Nike shoes fit great! Wanted to verify that returns are valid for 30 days if unused.', NULL, '2026-03-04 17:00:00+00', NULL),
    ('c0000000-0000-0000-0030-000000000004', 'c0000000-0000-0000-0029-000000000002', 'c0000000-0000-0000-0003-000000000001', 'Yes Chenda, you have a full 30-day exchange period as an active rewards member.', NULL, '2026-03-04 18:00:00+00', NULL),
    ('c0000000-0000-0000-0030-000000000005', 'c0000000-0000-0000-0029-000000000003', 'c0000000-0000-0000-0001-000000000003', 'DHL tracking shows cleared customs, can we schedule evening delivery?', NULL, '2026-03-04 10:00:00+00', NULL)
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.legal_acceptances (Customer Terms & Privacy Acceptances)
-- ============================================================

INSERT INTO public."legal_acceptances" ("id", "user_id", "legal_document_id", "accepted_at", "ip_address") VALUES
    ('c0000000-0000-0000-0031-000000000001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0016-000000000001', '2026-01-10 08:05:00+00', '103.14.200.12'),
    ('c0000000-0000-0000-0031-000000000002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0016-000000000001', '2026-01-11 09:05:00+00', '103.14.200.15'),
    ('c0000000-0000-0000-0031-000000000003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0016-000000000002', '2026-01-12 10:05:00+00', '103.14.200.22'),
    ('c0000000-0000-0000-0031-000000000004', 'c0000000-0000-0000-0001-000000000004', 'c0000000-0000-0000-0016-000000000003', '2026-01-13 11:05:00+00', '103.14.200.31'),
    ('c0000000-0000-0000-0031-000000000005', 'c0000000-0000-0000-0001-000000000005', 'c0000000-0000-0000-0016-000000000004', '2026-01-14 12:05:00+00', '103.14.200.45')
ON CONFLICT DO NOTHING;


-- ============================================================
-- Table: public.product_reviews (Verified Customer Reviews)
-- ============================================================

INSERT INTO public."product_reviews" ("id", "user_id", "product_id", "order_item_id", "rating", "title", "body", "status", "created_at", "created_by_id", "updated_at", "updated_by_id", "deleted_at", "deleted_by_id") VALUES
    ('c0000000-0000-0000-0032-000000000001', 'c0000000-0000-0000-0001-000000000001', 'c0000000-0000-0000-0011-000000000001', 'c0000000-0000-0000-0020-000000000001', 5, 'Worth every penny - outstanding phone', 'Super smooth 120Hz display, battery easily lasts two full days with heavy usage. Quick delivery!', 'published', '2026-03-04 10:00:00+00', 'c0000000-0000-0000-0001-000000000001', '2026-03-04 10:00:00+00', 'c0000000-0000-0000-0001-000000000001', NULL, NULL),
    ('c0000000-0000-0000-0032-000000000002', 'c0000000-0000-0000-0001-000000000002', 'c0000000-0000-0000-0011-000000000002', 'c0000000-0000-0000-0020-000000000002', 5, 'Best running shoes I have owned', 'The ReactX foam has so much spring. Great arch support for flat feet. 10/10 recommend.', 'published', '2026-03-05 11:30:00+00', 'c0000000-0000-0000-0001-000000000002', '2026-03-05 11:30:00+00', 'c0000000-0000-0000-0001-000000000002', NULL, NULL),
    ('c0000000-0000-0000-0032-000000000003', 'c0000000-0000-0000-0001-000000000003', 'c0000000-0000-0000-0011-000000000003', 'c0000000-0000-0000-0020-000000000003', 5, 'Top tier noise cancellation', 'Blocks out office chatter completely. Microphone quality for calls is pristine.', 'published', '2026-03-05 14:00:00+00', 'c0000000-0000-0000-0001-000000000003', '2026-03-05 14:00:00+00', 'c0000000-0000-0000-0001-000000000003', NULL, NULL),
    ('c0000000-0000-0000-0032-000000000004', 'c0000000-0000-0000-0001-000000000004', 'c0000000-0000-0000-0011-000000000004', 'c0000000-0000-0000-0020-000000000004', 4, 'Cozy knitwear and true to color', 'The oatmeal color matches photos perfectly. Slightly long in the sleeves but very stylish.', 'published', '2026-03-05 16:30:00+00', 'c0000000-0000-0000-0001-000000000004', '2026-03-05 16:30:00+00', 'c0000000-0000-0000-0001-000000000004', NULL, NULL),
    ('c0000000-0000-0000-0032-000000000005', 'c0000000-0000-0000-0001-000000000005', 'c0000000-0000-0000-0011-000000000005', 'c0000000-0000-0000-0020-000000000005', 5, 'Incredible charging speed for MacBook', 'Charged my laptop to 80% in 35 minutes. Digital battery display is super handy.', 'published', '2026-03-05 20:00:00+00', 'c0000000-0000-0000-0001-000000000005', '2026-03-05 20:00:00+00', 'c0000000-0000-0000-0001-000000000005', NULL, NULL)
ON CONFLICT DO NOTHING;

COMMIT;
