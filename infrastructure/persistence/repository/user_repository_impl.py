from typing import Optional, List
from django.utils import timezone
from domain.user.ports.user_repository import UserRepositoryInterface
from domain.user.entity.user import User, UserProfile, UserSecuritySettings, UserSession
from infrastructure.persistence.mapper.user_persistence_mapper import UserPersistenceMapper
from infrastructure.persistence.models.ecom_user_model import (
    EcomUser as EcomUserModel,
    UserProfile as UserProfileModel,
    UserSecuritySettings as UserSecuritySettingsModel,
    UserSession as UserSessionModel,
)


class UserRepositoryInterfaceImpl(UserRepositoryInterface):

    def get_by_id(self, user_id: str) -> Optional[User]:
        model = EcomUserModel.objects.filter(id=user_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return UserPersistenceMapper.from_entity(model)

    def get_by_email(self, email: str) -> Optional[User]:
        model = EcomUserModel.objects.filter(email=email, deleted_at__isnull=True).first()
        if not model:
            return None
        return UserPersistenceMapper.from_entity(model)

    def save(self, user: User) -> User:
        db_instance = EcomUserModel.objects.filter(pk=user.id).first() if user.id else None
        db_instance = UserPersistenceMapper.to_model(user, db_instance)
        db_instance.save()
        return UserPersistenceMapper.from_entity(db_instance)

    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        model = UserProfileModel.objects.filter(user_id=user_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return UserPersistenceMapper.profile_from_entity(model)

    def save_profile(self, profile: UserProfile) -> UserProfile:
        db_instance = UserProfileModel.objects.filter(user_id=profile.user_id, deleted_at__isnull=True).first() if profile.user_id else None
        db_instance = UserPersistenceMapper.profile_to_model(profile, db_instance)
        db_instance.save()
        return UserPersistenceMapper.profile_from_entity(db_instance)

    def get_security_settings(self, user_id: str) -> Optional[UserSecuritySettings]:
        model = UserSecuritySettingsModel.objects.filter(user_id=user_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return UserPersistenceMapper.security_from_entity(model)

    def save_security_settings(self, settings: UserSecuritySettings) -> UserSecuritySettings:
        db_instance = UserSecuritySettingsModel.objects.filter(user_id=settings.user_id, deleted_at__isnull=True).first() if settings.user_id else None
        db_instance = UserPersistenceMapper.security_to_model(settings, db_instance)
        db_instance.save()
        return UserPersistenceMapper.security_from_entity(db_instance)

    def list_sessions(self, user_id: str) -> List[UserSession]:
        sessions = UserSessionModel.objects.filter(user_id=user_id).order_by('-created_at')
        return [UserPersistenceMapper.session_from_entity(s) for s in sessions if s is not None]

    def get_session(self, session_id: str, user_id: str) -> Optional[UserSession]:
        session = UserSessionModel.objects.filter(id=session_id, user_id=user_id).first()
        if not session:
            return None
        return UserPersistenceMapper.session_from_entity(session)

    def save_session(self, session: UserSession) -> UserSession:
        db_instance = UserSessionModel.objects.filter(pk=session.id).first() if session.id else None
        db_instance = UserPersistenceMapper.session_to_model(session, db_instance)
        db_instance.save()
        return UserPersistenceMapper.session_from_entity(db_instance)
