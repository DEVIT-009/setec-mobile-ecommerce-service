import uuid
from typing import Dict, Any, Optional
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from domain.auth.service.auth_service import AuthServiceInterface
from domain.auth.exception.auth_domain_exception import AuthDomainException
from domain.user.ports.user_repository import UserRepositoryInterface
from infrastructure.persistence.models.ecom_user_model import EcomUser, UserProfile, UserSecuritySettings, UserSession
from shared.security.jwt_util import JwtUtil

_reset_tokens: dict = {}


class AuthServiceFacade(AuthServiceInterface):

    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    def register(self, email: str, password: str, first_name: Optional[str] = None, last_name: Optional[str] = None, phone_number: Optional[str] = None) -> Dict[str, Any]:
        if EcomUser.objects.filter(email=email.lower()).exists():
            raise AuthDomainException.email_already_exists()

        user = EcomUser.objects.create(
            email=email.lower(),
            password_hash=make_password(password),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role='customer',
            status='active',
        )
        UserProfile.objects.create(user=user)
        UserSecuritySettings.objects.create(user=user)

        token = self._generate_token(user)
        return {"user_id": str(user.id), "email": user.email, "access_token": token}

    def login(self, email: str, password: str, request: Any = None) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.get(email=email.lower(), deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_credentials()

        if not check_password(password, user.password_hash or ""):
            raise AuthDomainException.invalid_credentials()

        if user.status == 'blocked':
            raise AuthDomainException.account_blocked()
        if user.status == 'inactive':
            raise AuthDomainException.account_inactive()

        ip = self._get_client_ip(request) if request else None
        ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
        session = UserSession.objects.create(
            user=user,
            ip_address=ip,
            user_agent=ua,
            last_seen_at=timezone.now(),
        )

        token = self._generate_token(user, session_id=str(session.id))
        return {"access_token": token, "user_id": str(user.id), "role": user.role}

    def get_me(self, user_id: str) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.select_related('profile').get(id=user_id, deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_token()

        if user.status == 'blocked':
            raise AuthDomainException.account_blocked()

        return {
            "id": str(user.id),
            "email": user.email,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar_url": user.avatar_url,
            "role": user.role,
            "status": user.status,
            "email_verified_at": user.email_verified_at.isoformat() if user.email_verified_at else None,
            "phone_verified_at": user.phone_verified_at.isoformat() if user.phone_verified_at else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    def logout(self, user_id: str, session_id: Optional[str] = None) -> None:
        if session_id:
            # Reject if the session is already revoked — prevents silent re-logout.
            updated = UserSession.objects.filter(
                id=session_id,
                user_id=user_id,
                revoked_at__isnull=True,
            ).update(revoked_at=timezone.now())
            if updated == 0:
                raise AuthDomainException.invalid_token()
        else:
            UserSession.objects.filter(user_id=user_id, revoked_at__isnull=True).update(revoked_at=timezone.now())


    def refresh(self, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.get(id=user_id, deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_token()
        if user.status == 'blocked':
            raise AuthDomainException.account_blocked()
        token = self._generate_token(user, session_id=session_id)
        return {"access_token": token, "user_id": str(user.id), "role": user.role}

    def forgot_password(self, email: str) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.get(email=email.lower(), deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            return {"message": "If the email exists, a reset link has been sent."}
        reset_token = uuid.uuid4().hex
        _reset_tokens[reset_token] = str(user.id)
        return {"message": "If the email exists, a reset link has been sent.", "reset_token": reset_token}

    def reset_password(self, reset_token: str, new_password: str) -> Dict[str, Any]:
        user_id = _reset_tokens.pop(reset_token, None)
        if not user_id:
            raise AuthDomainException.invalid_token()
        try:
            user = EcomUser.objects.get(id=user_id, deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_token()
        user.password_hash = make_password(new_password)
        user.save()
        UserSecuritySettings.objects.filter(user_id=user_id).update(last_password_changed_at=timezone.now())
        return {"message": "Password updated successfully."}

    def verify_email(self, user_id: str) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.get(id=user_id, deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_token()
        if user.email_verified_at is None:
            user.email_verified_at = timezone.now()
            user.save()
        return {"email_verified_at": user.email_verified_at.isoformat()}

    def verify_phone(self, user_id: str, phone_number: Optional[str] = None) -> Dict[str, Any]:
        try:
            user = EcomUser.objects.get(id=user_id, deleted_at__isnull=True)
        except EcomUser.DoesNotExist:
            raise AuthDomainException.invalid_token()
        if phone_number:
            user.phone_number = phone_number
        if user.phone_verified_at is None:
            user.phone_verified_at = timezone.now()
        user.save()
        return {"phone_verified_at": user.phone_verified_at.isoformat()}

    @staticmethod
    def _generate_token(user: EcomUser, session_id: Optional[str] = None) -> str:
        return JwtUtil.generate_token_for_ecom(user, session_id)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
