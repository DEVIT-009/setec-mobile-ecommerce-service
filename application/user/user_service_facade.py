from typing import Dict, Any, List, Optional
from django.utils import timezone
from domain.user.ports.user_repository import UserRepositoryInterface
from domain.user.service.user_service import UserServiceInterface
from domain.user.entity.user import User, UserProfile, UserSecuritySettings, UserSession
from domain.user.exception.user_exception import UserException
from domain.address.ports.address_repository import AddressRepositoryInterface
from interface.user.serializer.mapper.user_controller_mapper import UserControllerMapper
from interface.address.serializer.mapper.address_controller_mapper import AddressControllerMapper


class UserServiceFacade(UserServiceInterface):

    def __init__(self, user_repo: UserRepositoryInterface, address_repo: Optional[AddressRepositoryInterface] = None):
        self.user_repo = user_repo
        self.address_repo = address_repo

    def get_me(self, user_id: str) -> Dict[str, Any]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserException.not_found()
        profile = self.user_repo.get_profile(user_id)
        security = self.user_repo.get_security_settings(user_id)
        default_addr = None
        if self.address_repo:
            addresses = self.address_repo.list_by_user(user_id)
            default = next((a for a in addresses if a.is_default), None)
            if default:
                default_addr = AddressControllerMapper.to_response(default)
        return UserControllerMapper.to_user_response(user, profile, security, default_addr)

    def update_me(self, user_id: str, data: dict) -> Dict[str, Any]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserException.not_found()
        for field in ['first_name', 'last_name', 'avatar_url', 'phone_number']:
            if field in data:
                setattr(user, field, data[field])
        saved = self.user_repo.save(user)
        profile = self.user_repo.get_profile(user_id)
        security = self.user_repo.get_security_settings(user_id)
        return UserControllerMapper.to_user_response(saved, profile, security)

    def get_profile(self, user_id: str) -> Dict[str, Any]:
        profile = self.user_repo.get_profile(user_id)
        if not profile:
            profile = UserProfile(user_id=user_id)
            profile = self.user_repo.save_profile(profile)
        return UserControllerMapper.to_profile_response(profile)

    def update_profile(self, user_id: str, data: dict) -> Dict[str, Any]:
        profile = self.user_repo.get_profile(user_id) or UserProfile(user_id=user_id)
        for field in ['date_of_birth', 'gender', 'preferred_language', 'marketing_opt_in']:
            if field in data:
                setattr(profile, field, data[field])
        saved = self.user_repo.save_profile(profile)
        return UserControllerMapper.to_profile_response(saved)

    def get_security_settings(self, user_id: str) -> Dict[str, Any]:
        settings_obj = self.user_repo.get_security_settings(user_id)
        if not settings_obj:
            settings_obj = UserSecuritySettings(user_id=user_id)
            settings_obj = self.user_repo.save_security_settings(settings_obj)
        return UserControllerMapper.to_security_response(settings_obj)

    def update_security_settings(self, user_id: str, data: dict) -> Dict[str, Any]:
        settings_obj = self.user_repo.get_security_settings(user_id) or UserSecuritySettings(user_id=user_id)
        for field in ['two_factor_enabled', 'biometric_enabled']:
            if field in data:
                setattr(settings_obj, field, data[field])
        saved = self.user_repo.save_security_settings(settings_obj)
        return UserControllerMapper.to_security_response(saved)

    def list_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        sessions = self.user_repo.list_sessions(user_id)
        return [UserControllerMapper.to_session_response(s) for s in sessions]

    def revoke_session(self, user_id: str, session_id: str) -> None:
        session = self.user_repo.get_session(session_id, user_id)
        if not session:
            raise UserException.session_not_found()
        session.revoked_at = timezone.now()
        self.user_repo.save_session(session)

    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        from infrastructure.persistence.models.ecom_user_model import EcomUser
        qs = EcomUser.objects.filter(deleted_at__isnull=True).order_by('-created_at')
        if filters.get('role'):
            qs = qs.filter(role=filters['role'])
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('q'):
            qs = qs.filter(email__icontains=filters['q'])

        total = qs.count()
        offset = (page - 1) * page_size
        users = list(qs[offset:offset + page_size])
        return {
            "items": [
                {
                    "id": str(u.id), "email": u.email, "first_name": u.first_name,
                    "last_name": u.last_name, "role": u.role, "status": u.status,
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                }
                for u in users
            ],
            "total": total,
        }

    def get_admin_user(self, user_id: str) -> Dict[str, Any]:
        return self.get_me(user_id)

    def update_admin_user(self, user_id: str, data: dict) -> Dict[str, Any]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserException.not_found()
        for field in ['role', 'status', 'first_name', 'last_name']:
            if field in data:
                setattr(user, field, data[field])
        saved = self.user_repo.save(user)
        return UserControllerMapper.to_user_response(saved)

    def block_user(self, user_id: str) -> Dict[str, Any]:
        return self.update_admin_user(user_id, {'status': 'blocked'})

    def unblock_user(self, user_id: str) -> Dict[str, Any]:
        return self.update_admin_user(user_id, {'status': 'active'})
