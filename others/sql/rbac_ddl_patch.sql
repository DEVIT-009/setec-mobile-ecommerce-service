-- =============================================================
-- RBAC DDL Patch: Multi-role support
-- Removes users.role and adds roles / user_roles /
-- permissions / role_has_permissions tables.
-- =============================================================

-- 1. Drop unused Django auth tables (not used by this app)
DROP TABLE IF EXISTS public.auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS public.auth_user_groups CASCADE;
DROP TABLE IF EXISTS public.auth_group_permissions CASCADE;
DROP TABLE IF EXISTS public.auth_user CASCADE;
DROP TABLE IF EXISTS public.auth_group CASCADE;
DROP TABLE IF EXISTS public.auth_permission CASCADE;

-- 2. Create roles table
CREATE TABLE IF NOT EXISTS public.roles
(
    id          serial PRIMARY KEY,
    name        varchar(100)             NOT NULL,
    slug        varchar(120)             NOT NULL UNIQUE,
    description text,
    created_at  timestamp with time zone NOT NULL DEFAULT now(),
    updated_at  timestamp with time zone NOT NULL DEFAULT now()
);

-- 3. Create permissions table
CREATE TABLE IF NOT EXISTS public.permissions
(
    id          serial PRIMARY KEY,
    name        varchar(100)             NOT NULL,
    slug        varchar(120)             NOT NULL UNIQUE,
    description text,
    created_at  timestamp with time zone NOT NULL DEFAULT now(),
    updated_at  timestamp with time zone NOT NULL DEFAULT now()
);

-- 4. Create user_roles junction table
CREATE TABLE IF NOT EXISTS public.user_roles
(
    id         serial PRIMARY KEY,
    user_id    uuid    NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    role_id    integer NOT NULL REFERENCES public.roles (id) ON DELETE CASCADE,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT uq_user_role UNIQUE (user_id, role_id)
);

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON public.user_roles (user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON public.user_roles (role_id);

-- 5. Create role_has_permissions junction table
CREATE TABLE IF NOT EXISTS public.role_has_permissions
(
    id            serial PRIMARY KEY,
    role_id       integer NOT NULL REFERENCES public.roles (id) ON DELETE CASCADE,
    permission_id integer NOT NULL REFERENCES public.permissions (id) ON DELETE CASCADE,
    created_at    timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT uq_role_permission UNIQUE (role_id, permission_id)
);

CREATE INDEX IF NOT EXISTS idx_rhp_role_id ON public.role_has_permissions (role_id);
CREATE INDEX IF NOT EXISTS idx_rhp_permission_id ON public.role_has_permissions (permission_id);

-- 6. Seed default roles
INSERT INTO public.roles (name, slug, description)
VALUES
    ('Customer', 'customer', 'Regular buyer/customer.'),
    ('Seller',   'seller',   'Product seller / merchant.'),
    ('Support',  'support',  'Customer support agent.'),
    ('Admin',    'admin',    'Platform administrator.')
ON CONFLICT (slug) DO NOTHING;

-- 7. Seed default permissions
INSERT INTO public.permissions (name, slug)
VALUES
    ('Create Product', 'product.create'),
    ('Update Product', 'product.update'),
    ('Delete Product', 'product.delete'),
    ('View Order',     'order.view'),
    ('Update Order',   'order.update'),
    ('View User',      'user.view'),
    ('Update User',    'user.update')
ON CONFLICT (slug) DO NOTHING;

-- 8. Assign permissions to roles
-- seller
INSERT INTO public.role_has_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM public.roles r, public.permissions p
WHERE r.slug = 'seller'
  AND p.slug IN ('product.create', 'product.update', 'product.delete', 'order.view')
ON CONFLICT DO NOTHING;

-- support
INSERT INTO public.role_has_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM public.roles r, public.permissions p
WHERE r.slug = 'support'
  AND p.slug IN ('order.view', 'order.update', 'user.view')
ON CONFLICT DO NOTHING;

-- admin (all permissions)
INSERT INTO public.role_has_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM public.roles r, public.permissions p
WHERE r.slug = 'admin'
ON CONFLICT DO NOTHING;

-- 9. Migrate existing single-role data to user_roles
-- (Only if users.role column still exists — safe to run before column drop)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'role'
    ) THEN
        INSERT INTO public.user_roles (user_id, role_id)
        SELECT u.id, r.id
        FROM public.users u
        JOIN public.roles r ON r.slug = u.role
        WHERE u.deleted_at IS NULL
        ON CONFLICT DO NOTHING;
    END IF;
END;
$$;

-- 10. Remove the old single-role column
ALTER TABLE public.users DROP COLUMN IF EXISTS role;
