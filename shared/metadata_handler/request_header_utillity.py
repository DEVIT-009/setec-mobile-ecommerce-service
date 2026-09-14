from functools import wraps
from typing import List

from django.conf import settings
from rest_framework.request import Request

from shared.security.auth_exception import AuthException
from shared.security.jwt_util import JwtUtil


class Metadata:
    def __init__(self, user_id=None, merchant_id=None, app_id=None, merchant_app_id=None, roles=None):
        self.user_id = user_id
        self.merchant_id = merchant_id
        self.app_id = app_id
        self.merchant_app_id = merchant_app_id
        # List of role strings for the authenticated user, e.g. ["customer", "admin"].
        # Populated from the JWT 'role' claim (comma-separated for multi-role support).
        # Empty list for unauthenticated requests.
        self.roles: List[str] = roles or []


def metadata_handler(required_user_id=True, optional_user_id=False):

    def decorator(func):
        @wraps(func)
        def wrapper(view, request: Request, *args, **kwargs):
            metadata = Metadata()

            auth_header = request.headers.get("Authorization")

            if required_user_id:
                if not auth_header or not auth_header.startswith("Bearer "):
                    raise AuthException.unauthorized()

                token = auth_header[7:]
                try:
                    username = JwtUtil.extract_user_id(token)
                    if not username:
                        raise AuthException.unauthorized()
                    metadata.user_id = username
                    # Populate roles from JWT for RBAC checks
                    raw_role = JwtUtil.extract_role(token)
                    metadata.roles = _parse_roles(raw_role)

                    # Validate that the session has not been revoked (i.e. user has not logged out).
                    # The session_id is embedded in the JWT payload.
                    _validate_session(token, username)
                except AuthException:
                    raise
                except Exception:
                    raise AuthException.unauthorized()

            elif optional_user_id and auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
                try:
                    username = JwtUtil.extract_user_id(token)
                    metadata.user_id = username
                    raw_role = JwtUtil.extract_role(token)
                    metadata.roles = _parse_roles(raw_role)
                    # Best-effort session validation for optional auth — stay unauthenticated on failure
                    _validate_session(token, username)
                except Exception:
                    pass  # optional — remain unauthenticated

            kwargs["metadata"] = metadata
            return func(view, request, *args, **kwargs)

        return wrapper
    return decorator


def _parse_roles(raw_role) -> List[str]:
    """
    Parse the JWT role claim into a list of role strings.

    Supports:
    - Single role string: "admin" → ["admin"]
    - Comma-separated multi-role: "customer,admin" → ["customer", "admin"]
    - None / empty: → []
    """
    if not raw_role:
        return []
    return [r.strip() for r in str(raw_role).split(",") if r.strip()]


def _validate_session(token: str, user_id: str) -> None:
    """
    Decode the JWT and verify its session_id has not been revoked in the DB.

    - Tokens issued without a session_id (e.g. legacy tokens) are allowed
      through so existing integrations are not broken.
    - Raises AuthException.unauthorized() when the session has been revoked
      (logged out) or does not exist.
    """
    import jwt as pyjwt
    from infrastructure.persistence.models.ecom_user_model import UserSession

    try:
        payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise AuthException.unauthorized()

    session_id = payload.get("session_id")
    if not session_id:
        # No session binding in this token — allow (backward-compatible).
        return

    # Reject if the session does not exist or has already been revoked.
    session_exists = UserSession.objects.filter(
        id=session_id,
        user_id=user_id,
        revoked_at__isnull=True,
    ).exists()

    if not session_exists:
        raise AuthException.unauthorized()
