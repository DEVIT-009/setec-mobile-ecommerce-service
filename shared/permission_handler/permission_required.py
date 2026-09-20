from functools import wraps
from typing import List

from shared.security.auth_exception import AuthException
from shared.security.jwt_util import JwtUtil


def require_roles(*required_roles: str):
    """
    RBAC decorator that enforces role membership for a view method.

    Reads the 'role' JWT claim, which may be a comma-separated string to
    support users with multiple roles (e.g. "customer,admin").

    Must be applied AFTER @metadata_handler(required_user_id=True) so that
    the Authorization header and token are already validated.

    Usage:
        @metadata_handler(required_user_id=True)
        @require_roles("admin")
        def my_view(self, request, *, metadata):
            ...

    Returns 403 Forbidden when the authenticated user does not hold any of
    the required roles.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(view, request, *args, **kwargs):
            metadata = kwargs.get("metadata")
            if not metadata or metadata.user_id is None:
                raise AuthException.unauthorized()

            if not required_roles:
                raise AuthException.forbidden()

            user_roles: List[str] = metadata.roles
            if not user_roles:
                raise AuthException.forbidden()

            if any(role in required_roles for role in user_roles):
                return func(view, request, *args, **kwargs)

            raise AuthException.forbidden()

        return wrapper
    return decorator
