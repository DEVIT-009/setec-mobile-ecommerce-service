from typing import Optional
from domain.user.entity.user import (
    User as DomainUser,
    UserProfile as DomainUserProfile,
    UserSecuritySettings as DomainUserSecuritySettings,
    UserSession as DomainUserSession,
)
from infrastructure.persistence.models.ecom_user_model import (
    EcomUser as EcomUserModel,
    UserProfile as UserProfileModel,
    UserSecuritySettings as UserSecuritySettingsModel,
    UserSession as UserSessionModel,
)


class UserPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[EcomUserModel]) -> Optional[DomainUser]:
        if entity is None:
            return None
        return DomainUser(
            id=str(entity.id),
            email=entity.email,
            phone_number=entity.phone_number,
            first_name=entity.first_name,
            last_name=entity.last_name,
            avatar_url=entity.avatar_url,
            role=entity.role,
            status=entity.status,
            email_verified_at=entity.email_verified_at,
            phone_verified_at=entity.phone_verified_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainUser, model_instance: Optional[EcomUserModel] = None) -> EcomUserModel:
        model = model_instance or EcomUserModel()
        model.email = domain.email
        model.phone_number = domain.phone_number
        model.first_name = domain.first_name
        model.last_name = domain.last_name
        model.avatar_url = domain.avatar_url
        model.role = domain.role
        model.status = domain.status
        model.email_verified_at = domain.email_verified_at
        model.phone_verified_at = domain.phone_verified_at
        model.deleted_at = domain.deleted_at
        return model

    @staticmethod
    def profile_from_entity(entity: Optional[UserProfileModel]) -> Optional[DomainUserProfile]:
        if entity is None:
            return None
        return DomainUserProfile(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            date_of_birth=entity.date_of_birth.isoformat() if entity.date_of_birth else None,
            gender=entity.gender,
            preferred_language=entity.preferred_language,
            marketing_opt_in=entity.marketing_opt_in,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def profile_to_model(domain: DomainUserProfile, model_instance: Optional[UserProfileModel] = None) -> UserProfileModel:
        model = model_instance or UserProfileModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.date_of_birth = domain.date_of_birth
        model.gender = domain.gender
        model.preferred_language = domain.preferred_language
        model.marketing_opt_in = domain.marketing_opt_in
        return model

    @staticmethod
    def security_from_entity(entity: Optional[UserSecuritySettingsModel]) -> Optional[DomainUserSecuritySettings]:
        if entity is None:
            return None
        return DomainUserSecuritySettings(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            two_factor_enabled=entity.two_factor_enabled,
            biometric_enabled=entity.biometric_enabled,
            last_password_changed_at=entity.last_password_changed_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def security_to_model(domain: DomainUserSecuritySettings, model_instance: Optional[UserSecuritySettingsModel] = None) -> UserSecuritySettingsModel:
        model = model_instance or UserSecuritySettingsModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.two_factor_enabled = domain.two_factor_enabled
        model.biometric_enabled = domain.biometric_enabled
        model.last_password_changed_at = domain.last_password_changed_at
        return model

    @staticmethod
    def session_from_entity(entity: Optional[UserSessionModel]) -> Optional[DomainUserSession]:
        if entity is None:
            return None
        return DomainUserSession(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            device_name=entity.device_name,
            ip_address=entity.ip_address,
            user_agent=entity.user_agent,
            last_seen_at=entity.last_seen_at,
            revoked_at=entity.revoked_at,
            created_at=entity.created_at,
        )

    @staticmethod
    def session_to_model(domain: DomainUserSession, model_instance: Optional[UserSessionModel] = None) -> UserSessionModel:
        model = model_instance or UserSessionModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.device_name = domain.device_name
        model.ip_address = domain.ip_address
        model.user_agent = domain.user_agent
        model.last_seen_at = domain.last_seen_at
        model.revoked_at = domain.revoked_at
        return model
