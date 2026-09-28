import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone

from .auth_exception import AuthException


class JwtUtil:

    SECRET_KEY = settings.SECRET_KEY
    EXPIRATION_MS = getattr(settings, "JWT_EXPIRATION_MS", 604800000)

    @classmethod
    def generate_token_for_ecom(cls, user, session_id=None, roles=None):
        """
        Generate JWT for EcomUser.

        Args:
            user: EcomUser instance.
            session_id: Optional session identifier.
            roles: Optional list of role slugs (e.g. ["customer", "admin"]).
                   Stored as a comma-joined string in the 'role' claim for
                   backward compatibility with extract_roles().
                   When not provided the user's roles are fetched from the DB.
        """
        now = datetime.now(timezone.utc)
        exp = now + timedelta(milliseconds=cls.EXPIRATION_MS)

        if roles is None:
            # Fetch roles from DB when not explicitly provided.
            roles = user.get_role_slugs()

        role_claim = ",".join(r.strip() for r in roles if r.strip()) if roles else ""
        payload = {
            "sub": user.email,
            "user_id": str(user.id),
            "role": role_claim,
            "session_id": session_id,
            "token_type": "ecom",
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm="HS256")
        return token if isinstance(token, str) else token.decode('utf-8')

    @classmethod
    def extract_email(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"], options={"verify_signature": True})
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise AuthException.unauthorized()
        except jwt.InvalidTokenError:
            raise AuthException.unauthorized()

    @classmethod
    def is_token_expired(cls, token):
        try:
            jwt.decode(
                token, cls.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True}
            )
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True

    @classmethod
    def validate_token(cls, token, user):
        try:
            email = cls.extract_email(token)
            if email != user.email:
                return False
            if cls.is_token_expired(token):
                return False
            return True
        except:
            return False

    @classmethod
    def validate_and_get_user(cls, token):
        """
        Validate token and return corresponding EcomUser instance.
        Raises AuthException if invalid or user does not exist.
        """
        from infrastructure.persistence.models.ecom_user_model import EcomUser
        email = cls.extract_email(token)
        user = EcomUser.objects.filter(email=email, deleted_at__isnull=True).first()
        if user and cls.validate_token(token, user):
            return user
        raise AuthException.unauthorized()

    @classmethod
    def extract_user_id(cls, token):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            raise AuthException.unauthorized()
        except jwt.InvalidTokenError:
            raise AuthException.unauthorized()

    @classmethod
    def extract_role(cls, token):
        """
        Return the raw 'role' claim string from the JWT.
        May be a single role ("customer") or comma-separated ("customer,admin").
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=["HS256"])
            return payload.get("role", "")
        except jwt.ExpiredSignatureError:
            raise AuthException.unauthorized()
        except jwt.InvalidTokenError:
            raise AuthException.unauthorized()

    @classmethod
    def extract_roles(cls, token):
        """
        Return the JWT roles as a list of strings.
        Handles both single-role ("admin") and comma-separated ("customer,admin") claims.
        """
        raw = cls.extract_role(token)
        if not raw:
            return []
        return [r.strip() for r in raw.split(",") if r.strip()]
