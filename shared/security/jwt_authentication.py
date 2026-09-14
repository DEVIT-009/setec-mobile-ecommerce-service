from rest_framework.authentication import BaseAuthentication

from infrastructure.persistence.models.user_model import User
from infrastructure.persistence.models.ecom_user_model import EcomUser
from .jwt_util import JwtUtil
from .auth_exception import AuthException


class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthException.unauthorized()
        except ValueError:
            raise AuthException.unauthorized()

        email = JwtUtil.extract_email(token)

        user = EcomUser.objects.filter(email=email, deleted_at__isnull=True).first()
        if not user:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise AuthException.unauthorized()

        if not JwtUtil.validate_token(token, user):
            raise AuthException.unauthorized()

        return user, None
